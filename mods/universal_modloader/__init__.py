import sys

from .core.importer import ModFinder
from .decorator import REGISTRY, Inject
from .enums import At, AtType, Shift


def install():
    sys.meta_path.insert(0, ModFinder())


__all__ = ["Inject", "At", "Shift", "AtType", "REGISTRY", "install"]
