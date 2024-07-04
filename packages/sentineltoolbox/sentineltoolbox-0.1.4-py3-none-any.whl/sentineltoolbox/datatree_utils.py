from typing import Any

from sentineltoolbox._utils import patch
from sentineltoolbox.attributes import AttributeHandler

__all__ = ["DataTreeHandler", "patch_datatree"]


class DataTreeHandler(AttributeHandler):
    pass


def patch_datatree(datatree: Any, **kwargs: Any) -> None:
    patch(datatree, DataTreeHandler, **kwargs)
