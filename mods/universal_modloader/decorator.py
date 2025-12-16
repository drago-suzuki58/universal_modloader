from dataclasses import dataclass
from typing import Callable, Dict, List

from .enums import At


@dataclass
class Patch:
    target_module: str
    selector: str
    at: At
    hook_func: Callable


REGISTRY: Dict[str, List[Patch]] = {}


def Inject(target: str, selector: str | None = None, at: At | None = None):
    if at is None:
        raise ValueError("@Inject requires 'at' argument.")

    def wrapper(func):
        final_selector = selector if selector else "__body__"

        if target not in REGISTRY:
            REGISTRY[target] = []

        REGISTRY[target].append(
            Patch(target_module=target, selector=final_selector, at=at, hook_func=func)
        )
        return func

    return wrapper
