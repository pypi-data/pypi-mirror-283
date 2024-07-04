"""
No public API here.
Use root package to import public function and classes
"""

__all__: list[str] = []

import copy
from pathlib import Path
from typing import Any, Hashable

import numpy as np
import xarray as xr
import zarr
import zarr.hierarchy
from datatree import DataTree, datatree
from xarray import Variable
from xarray.conventions import decode_cf_variable

from sentineltoolbox.attributes import AttributeHandler
from sentineltoolbox.converters import convert_to_datatree
from sentineltoolbox.filesystem_utils import get_url_and_credentials
from sentineltoolbox.readers._utils import (
    fix_kwargs_for_lazy_loading,
    is_eopf_adf_loaded,
)
from sentineltoolbox.readers.open_json import is_json, open_json
from sentineltoolbox.typedefs import Credentials, PathMatchingCriteria, PathOrPattern


def convert_zarrgroup_to_light_datatree(
    zgroup: zarr.hierarchy.Group,
    name: str = "product",
) -> DataTree[Any]:
    """
    Warning: arrays are not loaded but replaced with empty arrays!
    """

    class FillDataTree:

        def __init__(
            self,
            dt: DataTree[Any],
            zdata: zarr.hierarchy.Group,
            light: bool = True,
        ) -> None:
            """_summary_

            Parameters
            ----------
            dt
                _description_
            zdata
                _description_
            light, optional
                extract only metadata, ignore arrays, by default True
            """
            self.zdata = zdata
            self.dt = dt
            self.light = light

        def __call__(self, path: str) -> None:
            # TODO: replace manual cf conversion with xarray
            # See https://github.com/pydata/xarray/blob/main/xarray/backends/zarr.py#L625
            zgr = self.zdata[path]
            dt = self.dt
            name = Path(path).name
            zattrs = zgr.attrs.asdict()
            attrs = copy.copy(zattrs)
            dims = zattrs.get("_ARRAY_DIMENSIONS")
            if isinstance(zgr, zarr.core.Array):
                if "scale_factor" in zattrs:
                    dtype = np.dtype(type(zattrs["scale_factor"]))
                else:
                    dtype = zgr.dtype
                dtype = zgr.dtype
                storage_type = zgr.dtype
                try:
                    shape = [1 for n in zgr.shape]
                    attrs["_FillValue"] = zgr.fill_value
                    if self.light:
                        data = np.empty(shape, dtype)
                        array = xr.DataArray(dims=dims, data=data, attrs=attrs)
                    else:
                        data = zgr
                        array = xr.DataArray(dims=dims, data=data, attrs=attrs)

                    variable = Variable(array.dims, data=array, attrs=attrs)
                except ValueError as e:
                    raise e
                else:
                    # Fill io dict (encoded information)
                    io = {}
                    for field in {
                        "valid_min",
                        "valid_max",
                        "scale_factor",
                        "add_offset",
                    }:
                        if field in zattrs:
                            io[field] = zattrs[field]
                    if zgr.fill_value is not None:
                        io["fill_value"] = zgr.fill_value
                    io["dtype"] = storage_type

                    # Decode array if required
                    variable = decode_cf_variable(name, variable, decode_times=False)
                    dt[path] = variable

                    # Compute decode information
                    scale_factor = io.get("scale_factor", 1.0)
                    add_offset = io.get("add_offset", 0.0)
                    mini = io.get("valid_min")
                    maxi = io.get("valid_max")

                    try:
                        valid_max = (add_offset + maxi * scale_factor) if maxi is not None else None
                    except TypeError:
                        raise TypeError(
                            f"{path}: TypeError during operation {add_offset=} + {maxi=} * {scale_factor=}",
                        )

                    try:
                        valid_min = (add_offset + mini * scale_factor) if mini is not None else None
                    except TypeError:
                        raise TypeError(
                            f"{path}: TypeError during operation {add_offset=} + {mini=} * {scale_factor=}",
                        )

                    decoded: dict[Hashable, Any] = {}
                    decoded["valid_min"] = valid_min
                    decoded["valid_max"] = valid_max
                    decoded["fill_value"] = (
                        (add_offset + zgr.fill_value * scale_factor) if zgr.fill_value is not None else None
                    )
                    for field in {"valid_min", "valid_max", "fill_value"}:
                        if decoded[field] is not None:
                            attrs[field] = decoded[field]

                    if io:
                        dt[path].attrs["_io_config"] = io
                    dt[path].attrs.update(decoded)

            else:
                dt[path] = DataTree(name=name)
                dt[path].attrs = attrs

    dt: DataTree[Any] = DataTree(name=name)
    dt.attrs = zgroup.attrs.asdict()
    filler = FillDataTree(dt, zgroup)
    zgroup.visit(filler)

    for gr in dt.subtree:
        coordinates = set()
        for p_var in gr.variables:
            try:
                coords = gr[p_var].coordinates.split(" ")
            except AttributeError:
                pass
            else:
                coordinates.update(set(coords))
        if coordinates:
            gr.attrs["_coordinates"] = coordinates

    return dt


def load_metadata(
    path_or_pattern: PathOrPattern,
    *,
    credentials: Credentials | None = None,
    match_criteria: PathMatchingCriteria = "last_creation_date",
    **kwargs: Any,
) -> AttributeHandler:

    if isinstance(path_or_pattern, DataTree):
        return AttributeHandler(path_or_pattern)
    elif is_eopf_adf_loaded(path_or_pattern) and isinstance(path_or_pattern.data_ptr, datatree.DataTree):
        return AttributeHandler(path_or_pattern.data_ptr)
    url, credentials = get_url_and_credentials(
        path_or_pattern,
        credentials=credentials,
        match_criteria=match_criteria,
        **kwargs,
    )
    fix_kwargs_for_lazy_loading(kwargs)

    if is_json(url):
        dt = convert_to_datatree(open_json(url, credentials=credentials, **kwargs))
    else:
        if credentials is not None:
            kwargs = credentials.to_kwargs(url=url, target="zarr.open_consolidated")
        else:
            kwargs = dict(store=url)

        data = zarr.open_consolidated(**kwargs)
        dt = convert_zarrgroup_to_light_datatree(data)
    return AttributeHandler(dt)
