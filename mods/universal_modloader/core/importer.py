import ast
import importlib.abc
import sys

from ..decorator import REGISTRY
from .transformer import MainTransformer


class ModLoader(importlib.abc.Loader):
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
        transformer = MainTransformer(self.target_name)
        tree = transformer.visit(tree)
        ast.fix_missing_locations(tree)

        code = compile(tree, module.__file__, "exec")  # type: ignore
        exec(code, module.__dict__)


class ModFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname in REGISTRY:
            for finder in sys.meta_path:
                if isinstance(finder, ModFinder):
                    continue
                spec = finder.find_spec(fullname, path, target)

                if spec and spec.loader:
                    if isinstance(spec.loader, ModLoader):
                        return spec

                    print(f"[uml] Hooking module import: {fullname}")
                    spec.loader = ModLoader(spec.loader, fullname)
                    return spec
        return None
