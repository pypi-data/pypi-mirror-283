import datetime
from copy import copy
from pathlib import Path, PurePosixPath
from typing import Any

import fsspec

from sentineltoolbox._utils import _credential_required, fix_url, split_protocol
from sentineltoolbox.configuration import get_config
from sentineltoolbox.exceptions import MultipleResultsError
from sentineltoolbox.models.credentials import S3BucketCredentials
from sentineltoolbox.models.filename_generator import detect_filename_pattern
from sentineltoolbox.readers._utils import is_eopf_adf
from sentineltoolbox.typedefs import Credentials, PathOrPattern, fix_datetime


def get_fsspec_filesystem(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[Any, PurePosixPath]:
    """
    Function to instantiate fsspec.filesystem from url.
    Return path relative to filesystem. Can be absolute or not depending on fs.
    This function clean url and extract credentials (if necessary) for you.

    >>> fs, root = get_fsspec_filesystem("tests")
    >>> fs, root = get_fsspec_filesystem("s3://s3-input/Products/", secret_alias="s3-input") # doctest: +SKIP
    >>> fs.ls(root) # doctest: +SKIP

    See `fsspec documentation <https://filesystem-spec.readthedocs.io/en/latest/usage.html>`_

    :param path_or_pattern: path to use to build filesystem
    :param kwargs: see generic input parameters in :obj:`sentineltoolbox.typedefs` module
    :return: fsspec.AbstractFileSystem, path relative to filesystem
    """
    if "filesystem" in kwargs:
        return kwargs["filesystem"]
    else:
        url, credentials = get_url_and_credentials(path_or_pattern, **kwargs)
        protocols, relurl = split_protocol(url)
        if credentials:
            return fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem)), relurl
        else:
            return fsspec.filesystem("::".join(protocols)), relurl


def resolve_pattern(pattern: str | Path, credentials: Credentials | None = None, **kwargs: Any) -> str:
    match_criteria = kwargs.get("match_criteria", "last_creation_date")
    protocols, relurl = split_protocol(str(pattern))
    if "filesystem" in kwargs:
        fs = kwargs["filesystem"]
    else:
        if "zip" in protocols:
            # first check that path exists and is not a pattern
            resolve_protocols = copy(protocols)
            resolve_protocols.remove("zip")
            # resolve_protocols.add("file")
            fs = fsspec.filesystem("::".join(resolve_protocols))
        else:
            if credentials:
                fs = fsspec.filesystem(**credentials.to_kwargs(target=fsspec.filesystem))
            else:
                fs = fsspec.filesystem("::".join(protocols))
    paths = fs.expand_path(str(relurl))
    if not paths:
        raise ValueError(f"Invalid pattern {pattern!r}")
    elif len(paths) == 1:
        return fix_url("::".join(protocols) + "://" + str(paths[0]))
    elif len(paths) > 1:
        dates = {}
        for path in paths:
            ftype = detect_filename_pattern(path)
            if ftype.startswith("adf") and match_criteria == "last_creation_date":
                creation_date = fix_datetime(PurePosixPath(path).name.split(".")[0].split("_")[-1])
            else:
                creation_date = fs.modified(path)
            dates[path] = creation_date

        last, last_date = None, datetime.datetime(1, 1, 1, 1, tzinfo=datetime.timezone.utc)
        for path, creation_date in dates.items():
            if creation_date > last_date:
                last = path
                last_date = creation_date
            elif creation_date == last_date:
                raise MultipleResultsError(
                    f"cannot select file from pattern {pattern}.\n"  # nosec B608
                    f"files {last} and {path} have same creation date",  # nosec B608
                )
        if last:
            return fix_url("::".join(protocols) + "://" + str(last))
        else:
            raise ValueError(f"cannot select file from pattern {pattern}")  # nosec B608
    else:
        raise ValueError(f"Cannot expand pattern {pattern!r}: result: {paths}")  # nosec B608


def get_url_and_credentials(
    path_or_pattern: PathOrPattern,
    **kwargs: Any,
) -> tuple[str, Credentials | None]:
    """
    Function that cleans url and extract credentials (if necessary) for you.

    :param path_or_pattern:
    :param credentials:
    :param kwargs:
    :return:
    """
    credentials = kwargs.get("credentials")
    if isinstance(path_or_pattern, (str, Path)):
        url = fix_url(str(path_or_pattern))
        conf = get_config(**kwargs)
        secret_alias = conf.get_secret_alias(url)
        if secret_alias:
            kwargs["secret_alias"] = secret_alias
        if _credential_required(url, credentials):
            credentials = S3BucketCredentials.from_env(**kwargs)
        try:
            kwargs["credentials"] = credentials
            url = resolve_pattern(path_or_pattern, **kwargs)
        except NotImplementedError:
            url = str(path_or_pattern)

    elif is_eopf_adf(path_or_pattern):
        url = str(path_or_pattern.path.original_url)
        if _credential_required(url, credentials):
            storage_options = path_or_pattern.store_params["storage_options"]
            credentials = S3BucketCredentials.from_kwargs(**storage_options)
    else:
        raise NotImplementedError(f"path {path_or_pattern} of type {type(path_or_pattern)} is not supported yet")

    return url, credentials
