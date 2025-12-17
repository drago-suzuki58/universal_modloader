from typing import Any, Callable, Dict

from ..decorator import REGISTRY


def trigger_hooks(
    target_module: str, selector: str, at_type_name: str, context: Dict[str, Any]
):
    if target_module not in REGISTRY:
        return

    for patch in REGISTRY[target_module]:
        if patch.selector == selector and patch.at.type.name == at_type_name:
            patch.hook_func(context)


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

    # BEFORE
    if target_module in REGISTRY:
        for patch in REGISTRY[target_module]:
            if (
                patch.at.type.name == "INVOKE"
                and patch.at.target == selector
                and patch.at.shift.name == "BEFORE"
            ):
                patch.hook_func(ctx)

    # CHECK CANCEL
    if ctx.get("__cancel__", False):
        return ctx["__return__"]

    # EXECUTE
    try:
        result = original_func(*ctx["args"], **ctx["kwargs"])
    except Exception as e:
        raise e

    ctx["__return__"] = result

    # AFTER
    if target_module in REGISTRY:
        for patch in REGISTRY[target_module]:
            if (
                patch.at.type.name == "INVOKE"
                and patch.at.target == selector
                and patch.at.shift.name == "AFTER"
            ):
                patch.hook_func(ctx)

    return ctx["__return__"]
