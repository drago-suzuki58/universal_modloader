import ast
import importlib.abc
import sys
from typing import Any, Dict

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
        self.generic_visit(node)

        selector = self._get_current_selector(node.name)
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

            # TODO: OTHER at_types (INVOKE, ASSIGN, FIELD)

        return node

    def visit_Module(self, node):
        import_stmt = ast.Import(
            names=[ast.alias(name="universal_modloader.core", asname=None)]
        )
        node.body.insert(0, import_stmt)

        self.generic_visit(node)

        return node


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
