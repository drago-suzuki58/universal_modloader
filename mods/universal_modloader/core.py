import ast
import importlib.abc
import sys
from typing import Any, Dict

from .decorator import REGISTRY


class InjectionTransformer(ast.NodeTransformer):
    def __init__(self, target_module_name):
        self.target_module_name = target_module_name
        self.patches = REGISTRY.get(target_module_name, [])
        self.scope_stack = []

    def _get_current_selector(self, node_name):
        if self.scope_stack:
            return ".".join(self.scope_stack + [node_name])
        return node_name

    def _create_hook_call(self, selector, at_type_name):
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Attribute(
                        value=ast.Name(id="universal_modloader", ctx=ast.Load()),
                        attr="core",
                        ctx=ast.Load(),
                    ),
                    attr="execute_hooks",
                    ctx=ast.Load(),
                ),
                args=[
                    ast.Constant(value=self.target_module_name),
                    ast.Constant(value=selector),
                    ast.Constant(value=at_type_name),
                    ast.Call(
                        func=ast.Name(id="locals", ctx=ast.Load()), args=[], keywords=[]
                    ),
                ],
                keywords=[],
            )
        )

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

        for patch in active_patches:
            if patch.at.type.name == "HEAD":
                hook_code = self._create_hook_call(selector, "HEAD")
                node.body.insert(0, hook_code)
                print(f"[uml] Injected HEAD into {selector}")

            elif patch.at.type.name == "TAIL":
                hook_code = self._create_hook_call(selector, "TAIL")
                node.body.append(hook_code)
                print(f"[uml] Injected TAIL into {selector}")

            # TODO: And more injection points can be added here.

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
