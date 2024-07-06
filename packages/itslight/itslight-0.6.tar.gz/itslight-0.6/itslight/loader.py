from types import ModuleType, NoneType
from importlib import reload
from warnings import warn
from typing import Any, Optional, overload


@overload
def load(repo: str, attr: str) -> Any: ...

@overload
def load(repo: str, attr: NoneType = None) -> ModuleType: ...

def load(repo: str, attr: Optional[str] = None):
    """Load a module. (``--minimal`` installation is not supported)

    Args:
        repo (str): The repo to load.
        attr (str, optional): The attribute (item) to load. Use ``~`` to
            indicate "the same as package name." Defaults to None.
    """
    warn(
        "--minimal installation is not yet supported, defaulting to direct import"
    )
    
    mod = getattr(reload(__import__("its.%s" % repo)), repo)
    if attr:
        return getattr(mod, repo if attr == "~" else attr)

    return mod
