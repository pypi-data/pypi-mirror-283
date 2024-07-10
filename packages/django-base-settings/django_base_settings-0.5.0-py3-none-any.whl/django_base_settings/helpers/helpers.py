from typing import Any


def qualname(object: Any) -> Any:
    return object
    module = object.__class__.__module__
    if module == "builtins":
        return object.__class__.__qualname__
    return module + "." + object.__class__.__qualname__
