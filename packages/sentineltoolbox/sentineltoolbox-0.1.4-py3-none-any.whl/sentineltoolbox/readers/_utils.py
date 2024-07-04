import logging
from pathlib import Path
from typing import Any, BinaryIO, Literal

import tomli

logger = logging.getLogger("sentineltoolbox")


L_SUPPORTED_FORMATS = Literal[".json", ".toml", ".txt", None]


def load_toml_fp(fp: BinaryIO) -> dict[str, Any]:
    with fp:
        return tomli.load(fp)


def load_toml(path: Path) -> dict[str, Any]:
    with open(str(path), mode="rb") as fp:
        return load_toml_fp(fp)


def is_eopf_adf(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    adf = path_or_pattern
    # do not check full module and class name case because it doesn't match convention, it is not logical
    # so ... it may change soon (eopf.computing.abstract.ADF)
    match = adf.__class__.__module__.startswith("eopf") and adf.__class__.__name__.lower() == "adf"
    match = match and hasattr(adf, "name")
    match = match and hasattr(adf, "path")
    match = match and hasattr(adf, "store_params")
    match = match and hasattr(adf, "data_ptr")
    return match


def is_eopf_adf_loaded(path_or_pattern: Any) -> bool:
    """

    :param path_or_pattern:
    :return:
    """
    return is_eopf_adf(path_or_pattern) and path_or_pattern.data_ptr


def _cleaned_kwargs(kwargs: Any) -> dict[str, Any]:
    cleaned = {}
    for kwarg in kwargs:
        if kwarg not in ("secret_alias",):
            cleaned[kwarg] = kwargs[kwarg]
    return cleaned


def fix_kwargs_for_lazy_loading(kwargs: Any) -> None:
    if "chunks" not in kwargs:
        kwargs["chunks"] = {}
    else:
        if kwargs["chunks"] is None:
            raise ValueError(
                "open_datatree(chunks=None) is not allowed. Use load_datatree instead to avoid lazy loading data",
            )
