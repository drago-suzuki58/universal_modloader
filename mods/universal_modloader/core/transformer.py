import ast

from ..decorator import REGISTRY
from .analysis import ScopeAnalyzer
from .generation import HookCodeGenerator


class ReturnTransformer(ast.NodeTransformer):
    def __init__(self, target_module, selector):
        self.target_module = target_module
        self.selector = selector

    def visit_Return(self, node):
        new_nodes = HookCodeGenerator.create_return_block(
            self.target_module, self.selector, node
        )
        for n in new_nodes:
            ast.copy_location(n, node)
        return new_nodes

    def visit_FunctionDef(self, node):
        return node

    def visit_AsyncFunctionDef(self, node):
        return node


class MainTransformer(ast.NodeTransformer):
    def __init__(self, target_module_name):
        self.target_module_name = target_module_name
        self.patches = REGISTRY.get(target_module_name, [])
        self.scope_stack = []
        self.scope_analyzer = ScopeAnalyzer()

    def _get_current_selector(self, node_name):
        if self.scope_stack:
            return ".".join(self.scope_stack + [node_name])
        return node_name

    def visit_ClassDef(self, node):
        self.scope_stack.append(node.name)
        self.generic_visit(node)
        self.scope_stack.pop()
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

        has_hook = False
        for patch in self.patches:
            if patch.at.type.name == "INVOKE" and patch.at.target == target_func_name:
                if patch.selector == "__body__" or patch.selector == current_scope:
                    has_hook = True
                    break

        if not has_hook:
            return node

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
                    value=ast.Attribute(
                        value=ast.Name(id="universal_modloader", ctx=ast.Load()),
                        attr="core",
                        ctx=ast.Load(),
                    ),
                    attr="runtime",
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

    def visit_FunctionDef(self, node):
        self.scope_stack.append(node.name)
        try:
            self.generic_visit(node)

            selector = ".".join(self.scope_stack)
            active_patches = [p for p in self.patches if p.selector == selector]

            if not active_patches:
                return node

            used_vars = self.scope_analyzer.collect(node)

            for patch in active_patches:
                at_type = patch.at.type.name

                if at_type in ["HEAD", "TAIL"]:
                    hook_block = HookCodeGenerator.create_hook_block(
                        self.target_module_name, selector, at_type, used_vars
                    )

                    if at_type == "HEAD":
                        for stmt in reversed(hook_block):
                            node.body.insert(0, stmt)
                    elif at_type == "TAIL":
                        node.body.extend(hook_block)

                elif at_type == "RETURN":
                    replacer = ReturnTransformer(self.target_module_name, selector)
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
            names=[ast.alias(name="universal_modloader.core.runtime", asname=None)]
        )
        node.body.insert(0, import_stmt)
        self.generic_visit(node)
        return node
