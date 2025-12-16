import sys

from .core import UniversalFinder


def install():
    sys.meta_path.insert(0, UniversalFinder())
