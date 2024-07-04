"""
This module provides type definition, interface and documentation about common arguments

Generic input arguments:

match_criteria: :obj:`sentineltoolbox.typedefs.PathMatchingCriteria`
    - ``"last_creation_date"`` the product creation date (last part of filename)
      is used to define the most recent data
    - ``"last_modified_time"`` the file/directory modified time (in sense of file system mtime)
      is used to define the most recent data

path_or_pattern: :obj:`sentineltoolbox.typedefs.PathOrPattern`
    example of path:
        - ``"s3://s2-input/Auxiliary/MSI/S2A_ADF_REOB2_xxxxxxx.json"``
        - ``"s3://s3-input/Auxiliary/OL1/S3A_ADF_OLINS_xxxxxxx.zarr"``
        - ``"/home/username/data/S3A_ADF_OLINS_xxxxxxx.zarr"``
        - ``"/d/data/S3A_ADF_OLINS_xxxxxxx.zarr"``
        - ``"D:\\data\\S3A_ADF_OLINS_xxxxxxx.zarr"`` <-- WARNING, don't forget to escape backslash
    example of patterns:
        - ``"s3://s2-input/Auxiliary/MSI/S2A_ADF_REOB2_*.json"``

    path_or_pattern also accept :obj:`eopf.computing.abstract.ADF`


All functions that accept path_or_pattern also accept this **kwargs**:
  - **secret_alias** a string defining secret_alias to use. secret aliases are defined in configuration files.
    If not set, tries to look in predefined secret_alias <-> paths mappings. See Software Configuration
  - **configuration** (FOR EXPERT ONLY): an instance of :obj:`sentineltoolbox.configuration.Configuration`
    Use default configuration if not set.
  - **credentials** (FOR EXPERT ONLY): an instance of :obj:`sentineltoolbox.typedefs.Credentials`
    If not set and required, extract credentials from environment and configuration


This module also provide convenience functions to convert Union of types to canonical type.
For example, for input paths:
  - user input can be Path, list of Path, str, list of str and Path. This is defined by type `T_Paths`
  - in code we want to manipulate only list[Path] (our canonical type) and do not write this boring code each time ...

=> this module provide a convenience function for that (:obj:`~sentineltoolbox.typedefs.fix_paths`)
return type of this function also propose the canonical type to use in your code

"""

__all__ = ["Credentials", "PathMatchingCriteria", "PathOrPattern"]

import os
from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal, Protocol, TypeAlias

import dask.array as da
import numpy as np
import xarray as xr

# -----------------------------------------------------------------------------
# SIMPLE ALIASES
# -----------------------------------------------------------------------------

PathMatchingCriteria: TypeAlias = Literal["last_creation_date", "last_modified_time"]  # can be extended
PathOrPattern: TypeAlias = Any  # Need to support at least str, Path, cpm Adf, cpm AnyPath. Data can be zipped or not!
AnyArray: TypeAlias = xr.DataArray | da.Array | np.ndarray[Any, Any]

T_DateTime: TypeAlias = datetime | str | int
T_TimeDelta: TypeAlias = timedelta | int

L_DataFileNamePattern = Literal[
    # S3A_OL_0_EFR____20221101T162118_20221101T162318_20221101T180111_0119_091_311______PS1_O_NR_002.SEN3
    "product/s3-legacy",
    "product/s2-legacy",  # S2A_MSIL1C_20231001T094031_N0509_R036_T33RUJ_20231002T065101
    "product/eopf-legacy",  # S3OLCEFR_20230506T015316_0180_B117_T931.zarr
    "product/eopf",  # S03OLCEFR_20230506T015316_0180_B117_T931.zarr
    "product/permissive",  # S03OLCEFR*
    # S3__AX___CLM_AX_20000101T000000_20991231T235959_20151214T120000___________________MPC_O_AL_001.SEN3
    "adf/s3-legacy",
    "adf/s2-legacy",  # S2__OPER_AUX_CAMSAN_ADG__20220330T000000_V20220330T000000_20220331T120000
    "adf/eopf-legacy",  # S3__ADF_SLBDF_20160216T000000_20991231T235959_20231102T155016.zarr
    "adf/eopf",  # S03__ADF_SLBDF_20160216T000000_20991231T235959_20231102T155016.zarr
    "adf/permissive",  # *ADF_SLBDF*,
    "unknown/unknown",
]

T_Paths: TypeAlias = Path | str | list[Path] | list[str] | list[Path | str]


# -----------------------------------------------------------------------------
# INTERFACES / ABSTRACT CLASSES
# -----------------------------------------------------------------------------
class Credentials(Protocol):
    """
    Class storing credential information
    """

    """List of targets available for :meth:`to_kwargs`. Each derived class must define this list."""
    available_targets: list[Any] = []

    def to_kwargs(self, *, url: str | None = None, target: Any = None, **kwargs: Any) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def from_env(cls) -> "Credentials":
        """
        Tries to generate credential instance from environment variables
        """
        raise NotImplementedError

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> "Credentials":
        """
        Tries to generate credential instance from given kwargs
        """
        raise NotImplementedError


class FileNameGenerator(Protocol):
    @staticmethod
    def from_string(filename: str, **kwargs: Any) -> "FileNameGenerator":
        """
        Generate a FileNameGenerator from filename string.
        If filename is a legacy filename, you must specify `semantic` to specify the new format semantic.
        """
        raise NotImplementedError

    def is_valid(self) -> bool:
        """
        return True if all required data are set, else retrun False
        """
        raise NotImplementedError

    def to_string(self, **kwargs: Any) -> str:
        """Generate a filename from data and arguments passed by user"""
        raise NotImplementedError


@dataclass(order=True)
class DataPath(Protocol):
    """
    Interface representing Path object.
    This interface is defined to be a subset of pathlib.Path.
    So you can consider pathlib.Path will be always compatible with this interface.

    Compared to pathlib.Path, DataPath is the minimal subset required by DataWalker to extract file information and do
    its work. It may evolve depending on DataWalker requirements but will remain compatible with pathlib.Path.
    """

    path: Path | str

    def __init__(self, path: Path | str) -> None:
        super().__init__()
        self.path = path

    def __str__(self) -> str:
        """return absolute and canonical str representation of itself."""
        return str(self.path)

    @abstractmethod
    def is_file(self) -> bool:
        """
        Whether this path is a regular file (also True for symlinks pointing
        to regular files).
        """
        raise NotImplementedError

    @abstractmethod
    def is_dir(self) -> bool:
        """
        Whether this path is a directory.
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """The final path component, if any."""
        return Path(self.path).name

    @property
    def parent(self) -> str:
        """The logical parent of the path."""
        raise NotImplementedError

    def stat(self, *, follow_symlinks: bool = True) -> os.stat_result:
        """
        Returns information about this path (similarly to boto3's ObjectSummary).
        For compatibility with pathlib, the returned object some similar attributes like os.stat_result.
        The result is looked up at each call to this method
        """
        raise NotImplementedError

    def open(
        self,
        mode: str = "r",
        buffering: int = -1,
        encoding: str | None = None,
        errors: str | None = None,
        newline: Any = None,
    ) -> Any:
        raise NotImplementedError

    @property
    def suffix(self) -> str:
        """
        The final component's last suffix, if any.

        This includes the leading period. For example: '.txt'
        """
        return Path(self.path).suffix

    @property
    def suffixes(self) -> list[Any] | list[str]:
        """
        A list of the final component's suffixes, if any.

        These include the leading periods. For example: ['.tar', '.gz']
        """
        return Path(self.path).suffixes

    @property
    def stem(self) -> str:
        """The final path component, minus its last suffix."""
        return Path(self.path).stem


T_DataPath: TypeAlias = Path | DataPath

# -----------------------------------------------------------------------------
# Convenience function to convert any type to canonical types
# -----------------------------------------------------------------------------


def fix_paths(paths: T_Paths) -> list[Path]:
    """Convenience function to convert user paths to canonical list[Path]"""
    if isinstance(paths, (str, Path)):
        path_list = [Path(paths)]
    else:
        path_list = [Path(path) for path in paths]
    return path_list


def fix_datetime(date: T_DateTime) -> datetime:
    """Convenience function to convert date to canonical :class:`datetime.datetime`

    Conversion depends on input type:
      - datetime: no change
      - int: consider it's a timestamp
      - str: consider it's a date str following ISO format YYYYMMDDTHHMMSS
    """
    if isinstance(date, datetime):
        return date
    elif isinstance(date, int):
        return datetime.fromtimestamp(date).replace(tzinfo=timezone.utc)
    else:
        return datetime.fromisoformat(date).replace(tzinfo=timezone.utc)


def fix_timedelta(delta: T_TimeDelta) -> timedelta:
    """Convenience function to convert time delta to canonical :class:`datetime.timedelta`

    Conversion depends on input type:
      - timedelta: no change
      - int: consider it a delta in seconds
    """
    if isinstance(delta, timedelta):
        return delta
    else:
        return timedelta(seconds=delta)


def as_dataarray(input: AnyArray) -> da.Array | np.ndarray[Any, Any]:
    """Conveniance function that converts xarray datatypes into dask arrays. Will return the original
    array if it is a numpy array or already a dask array.

    Parameters
    ----------
    input
        The array to be converted
    Returns
    -------
        Either a dask array or the original array
    """
    if isinstance(input, xr.DataArray):
        return input.data
    else:
        return input


MetadataType_L: TypeAlias = Literal["stac_properties", "stac_discovery", "metadata", "root"]
category_paths: dict[MetadataType_L, str] = {
    "stac_properties": "stac_discovery/properties/",
    "stac_discovery": "stac_discovery/",
    "metadata": "other_metadata/",
    "root": "",
}
