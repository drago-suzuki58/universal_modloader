import ast
import importlib.abc
import sys
from typing import Any, Callable, Dict

from .decorator import REGISTRY


class VariableCollector(ast.NodeVisitor):
    def __init__(self):
        self.vars = set()

    def visit_arg(self, node):
        self.vars.add(node.arg)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.vars.add(node.id)

    def collect(self, node):
        self.vars.clear()
        if hasattr(node, "args"):
            for arg in node.args.args:
                self.visit_arg(arg)
        self.generic_visit(node)
        return self.vars


class HookGenerator:
    @staticmethod
    def create_hook_block(target_module, selector, at_type, available_vars):
        template = f"""
_uml_ctx = locals()
universal_modloader.core.execute_hooks('{target_module}', '{selector}', '{at_type}', _uml_ctx)
"""
        for var_name in available_vars:
            if var_name == "__return__":
                continue

            template += (
                f"if '{var_name}' in _uml_ctx: {var_name} = _uml_ctx['{var_name}']\n"
            )

        return ast.parse(template).body

    @staticmethod
    def create_return_block(target_module, selector, original_return_node):
        ret_val_node = (
            original_return_node.value
            if original_return_node.value
            else ast.Constant(value=None)
        )

        template = f"""
_uml_ctx = locals()
_uml_ctx['__return__'] = None
universal_modloader.core.execute_hooks('{target_module}', '{selector}', 'RETURN', _uml_ctx)
return _uml_ctx['__return__']
"""
        nodes = ast.parse(template).body

        nodes[1].value = ret_val_node

        return nodes


class ReturnReplacer(ast.NodeTransformer):
    def __init__(self, target_module, selector):
        self.target_module = target_module
        self.selector = selector

    def visit_Return(self, node):
        new_nodes = HookGenerator.create_return_block(
            self.target_module, self.selector, node
        )

        for n in new_nodes:
            ast.copy_location(n, node)
        return new_nodes

    def visit_FunctionDef(self, node):
        return node

    def visit_AsyncFunctionDef(self, node):
        return node


def invoke_wrapper(
    original_func: Callable,
    target_module: str,
    selector: str,
    args: tuple,
    kwargs: dict,
    caller_ctx: dict,
):
    ctx = {
        "args": list(args),
        "kwargs": kwargs,
        "caller_locals": caller_ctx,
        "__return__": None,
    }

    if target_module in REGISTRY:
        for patch in REGISTRY[target_module]:
            if (
                patch.at.type.name == "INVOKE"
                and patch.at.target == selector
                and patch.at.shift.name == "BEFORE"
            ):
                patch.hook_func(ctx)

    try:
        result = original_func(*ctx["args"], **ctx["kwargs"])
    except Exception as e:
        raise e

    ctx["__return__"] = result

    if target_module in REGISTRY:
        for patch in REGISTRY[target_module]:
            if (
                patch.at.type.name == "INVOKE"
                and patch.at.target == selector
                and patch.at.shift.name == "AFTER"
            ):
                patch.hook_func(ctx)

    return ctx["__return__"]


class InjectionTransformer(ast.NodeTransformer):
    def __init__(self, target_module_name):
        self.target_module_name = target_module_name
        self.patches = REGISTRY.get(target_module_name, [])
        self.scope_stack = []
        self.var_collector = VariableCollector()

    def _get_current_selector(self, node_name):
        if self.scope_stack:
            return ".".join(self.scope_stack + [node_name])
        return node_name

    def visit_ClassDef(self, node):
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()
        return node

    def visit_FunctionDef(self, node):
        # 1. まずスタックに自分の名前を積む (これがないと中のINVOKEが迷子になる)
        self.scope_stack.append(node.name)

        try:
            self.generic_visit(node)

            selector = ".".join(self.scope_stack)
            active_patches = [p for p in self.patches if p.selector == selector]

            if not active_patches:
                return node

            used_vars = self.var_collector.collect(node)

            for patch in active_patches:
                at_type = patch.at.type.name

                if at_type in ["HEAD", "TAIL"]:
                    hook_block = HookGenerator.create_hook_block(
                        self.target_module_name, selector, at_type, used_vars
                    )

                    if at_type == "HEAD":
                        for stmt in reversed(hook_block):
                            node.body.insert(0, stmt)
                        print(f"[uml] Injected HEAD w/ WriteBack into {selector}")

                    elif at_type == "TAIL":
                        node.body.extend(hook_block)
                        print(f"[uml] Injected TAIL w/ WriteBack into {selector}")

                elif at_type == "RETURN":
                    print(f"[uml] Rewriting RETURN in {selector}")
                    replacer = ReturnReplacer(self.target_module_name, selector)

                    new_body = []
                    for stmt in node.body:
                        res = replacer.visit(stmt)
                        if isinstance(res, list):
                            new_body.extend(res)
                        elif res:
                            new_body.append(res)
                    node.body = new_body

        finally:
            self.scope_stack.pop()

        return node

    def visit_Module(self, node):
        import_stmt = ast.Import(
            names=[ast.alias(name="universal_modloader.core", asname=None)]
        )
        node.body.insert(0, import_stmt)

        self.generic_visit(node)

        return node

    def visit_Call(self, node):
        self.generic_visit(node)

        target_func_name = None
        if isinstance(node.func, ast.Name):
            target_func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            target_func_name = node.func.attr

        if not target_func_name:
            return node

        current_scope = ".".join(self.scope_stack)

        patches = REGISTRY.get(self.target_module_name, [])
        has_hook = False

        for patch in patches:
            if patch.at.type.name == "INVOKE" and patch.at.target == target_func_name:
                if patch.selector == "__body__" or patch.selector == current_scope:
                    has_hook = True
                    break

        if not has_hook:
            return node

        print(f"[uml] Wrapping INVOKE: {target_func_name} inside {current_scope}")

        new_args = [
            node.func,
            ast.Constant(value=self.target_module_name),
            ast.Constant(value=target_func_name),
            ast.Tuple(elts=node.args, ctx=ast.Load()),
            ast.Dict(
                keys=[ast.Constant(value=k.arg) for k in node.keywords],
                values=[k.value for k in node.keywords],
            ),
            ast.Call(func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]),
        ]

        wrapper_call = ast.Call(
            func=ast.Attribute(
                value=ast.Attribute(
                    value=ast.Name(id="universal_modloader", ctx=ast.Load()),
                    attr="core",
                    ctx=ast.Load(),
                ),
                attr="invoke_wrapper",
                ctx=ast.Load(),
            ),
            args=new_args,
            keywords=[],
        )

        ast.copy_location(wrapper_call, node)
        return wrapper_call


class UniversalLoader(importlib.abc.Loader):
    def __init__(self, original_loader, target_name):
        self.original_loader = original_loader
        self.target_name = target_name

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        try:
            source = self.original_loader.get_source(self.target_name)
        except AttributeError:
            return

        tree = ast.parse(source)
        transformer = InjectionTransformer(self.target_name)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        code = compile(tree, module.__file__, "exec")  # type: ignore
        exec(code, module.__dict__)


class UniversalFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in REGISTRY:
            for finder in sys.meta_path:
                if isinstance(finder, UniversalFinder):
                    continue
                spec = finder.find_spec(fullname, path, target)

                if spec and spec.loader:
                    print(f"[uml] Hooking module import: {fullname}")
                    spec.loader = UniversalLoader(spec.loader, fullname)
                    return spec
        return None


def execute_hooks(
    target_module: str, selector: str, at_type_name: str, context: Dict[str, Any]
):
    if target_module not in REGISTRY:
        return

    for patch in REGISTRY[target_module]:
        if patch.selector == selector and patch.at.type.name == at_type_name:
            patch.hook_func(context)
