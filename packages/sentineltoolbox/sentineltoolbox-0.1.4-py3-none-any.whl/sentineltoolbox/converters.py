import copy
from pathlib import PurePosixPath
from typing import Any, MutableMapping, Tuple, TypeAlias

import numpy as np
from dask.array.core import Array
from datatree import DataTree
from xarray import DataArray, Dataset

try:
    from eopf import EOProduct
except ImportError:
    EOProduct: TypeAlias = Any  # type: ignore


GROUP_ATTRIBUTES_KEY = "group_attrs"


def _dataset_path(dataset: Dataset, key: str) -> str:
    if dataset.name:
        return f"{dataset.name}/{key}"
    else:
        return key


def fix_json_xarray(dic: dict[str, Any]) -> dict[str, Any]:
    """

    :param dic:
    :return:
    """
    dic = copy.copy(dic)
    # group
    if ("attrs" in dic or "data_vars" in dic) and "data" not in dic:
        for field in ("attrs", "data_vars", "coords", "dims"):
            dic[field] = dic.get(field, {})
        for path, variable in dic["data_vars"].items():
            dic["data_vars"][path] = fix_json_xarray(variable)
    # variable
    elif "data" in dic:
        dic["dims"] = dic.get("dims", ())
    else:
        raise TypeError(dic)

    return dic


def _fix_dtype_and_value_formatting(dtype: Any, value: Any) -> Tuple[Any, Any]:
    """Function to fix problems encountered when converting type and value, for example
    with Sentinel 3 SLSTR L1 ADF SL1PP"""
    if dtype in ("STRING", "string"):
        dtype = str

    elif dtype in ("DOUBLE", "double"):
        dtype = np.float64
        if value == "":  # ex: value == ""
            value = np.empty(0)

    elif dtype in ("INTEGER", "integer"):
        if isinstance(value, str) and " " in value:  # ex: value == "0 0 0 0 0 0 0 0"
            value = [int(v) for v in list(value) if v != " "]

        elif value == "":  # ex: value == ""
            value = np.empty(0)

        dtype = np.int64
    elif isinstance(dtype, str) and "array" in dtype:
        dtype = dtype.replace("array", "").lstrip("[").rstrip("]")
    return dtype, value


def convert_json_to_datatree(json_dict: dict[Any, Any], path: str = "/") -> DataTree[Any]:
    datasets: MutableMapping[str, Dataset | DataArray | DataTree[Any] | None] = {}
    variables = {}
    attrs = {}
    for k, v in json_dict.items():
        if isinstance(v, dict):
            if "value" in v and "type" in v:
                value = v.pop("value")
                dtype = v.pop("type")
                dtype, value = _fix_dtype_and_value_formatting(dtype, value)
                a = np.array(value, dtype=dtype)
                if isinstance(value, list):
                    dims = [f"{k}_{i}" for i, _ in enumerate(a.shape)]
                else:
                    dims = None
                variables[k] = DataArray(a, attrs=v, dims=dims)
            elif k == "attrs" and isinstance(v, dict):
                attrs.update(v)
            else:
                datasets[k] = convert_json_to_datatree(v, path + k + "/")
        else:
            attrs[k] = v
    if variables:
        datasets["/"] = Dataset(data_vars=variables, attrs=attrs)

    dt = DataTree.from_dict(datasets)
    dt.attrs.update(attrs)
    return dt


def convert_datatree_to_dataset(dt: DataTree[Any]) -> Dataset:
    flat_ds = Dataset(attrs=dt.attrs)
    for ds in dt.subtree:
        if ds.name and ds.attrs:
            flat_ds.attrs.setdefault(GROUP_ATTRIBUTES_KEY, {})[ds.name] = ds.attrs
        for k, v in ds.variables.items():
            flat_ds[_dataset_path(ds, k)] = v
        for k, c in ds.coords.items():
            flat_ds[_dataset_path(ds, k)] = c
    return flat_ds


def convert_dataset_to_datatree(dataset: Dataset) -> DataTree[Any]:
    datatree: DataTree[Any] = DataTree()
    attribs = copy.copy(dataset.attrs)
    if GROUP_ATTRIBUTES_KEY in attribs:
        group_attribs = attribs.pop(GROUP_ATTRIBUTES_KEY)
    else:
        group_attribs = {}
    datatree.attrs.update(attribs)
    for path, variable in dataset.items():
        pathstr = str(path)
        if isinstance(variable, (DataArray, Array, np.ndarray)):
            datatree[pathstr] = variable
        else:
            try:
                datatree[pathstr]
            except KeyError:
                datatree[pathstr] = DataTree(name=PurePosixPath(pathstr).name)
            datatree[pathstr].attrs.update(variable.attrs)
    for path, attrs in group_attribs.items():
        pathstr = str(path)
        # DO NOT USE path in datatree. Doesn't behave as expected
        # DO NOT USE
        #   group = DataTree(...)
        #   datatree[path] = group
        #   use(group) # 'group' and 'datatree[path]' are differents
        if isinstance(attrs, str):
            # consider it is a global attribute, not a group
            datatree.attrs[pathstr] = attrs
        else:
            try:
                datatree[pathstr]
            except KeyError:
                datatree[pathstr] = DataTree(name=PurePosixPath(pathstr).name)
            datatree[pathstr].attrs.update(attrs)

    return datatree


def convert_eoproduct20_to_datatree(eoproduct: EOProduct) -> DataTree[Any]:
    dt: DataTree[Any] = DataTree(name=eoproduct.name)
    dt.attrs.update(eoproduct.attrs)
    for obj in eoproduct.walk():
        if isinstance(obj.data, DataArray):
            dt[str(obj.path)] = obj.data
        else:
            dt[str(obj.path)] = DataTree(name=obj.name)
        dt[str(obj.path)].attrs.update(obj.attrs)
    return dt


def convert_to_datatree(data: Any) -> DataTree[Any]:
    """

    :param data:
    :return:
    """
    input_type = data.__class__.__module__ + "." + data.__class__.__name__

    if isinstance(data, DataTree):
        return data

    original_data = data
    if isinstance(data, Dataset):
        data = convert_dataset_to_datatree(data)
    elif isinstance(data, dict):
        if "data_vars" in data:
            json = fix_json_xarray(data)
            ds = Dataset.from_dict(json)
            data = convert_dataset_to_datatree(ds)
        else:
            data = convert_json_to_datatree(data)
    elif input_type == "eopf.product.eo_product.EOProduct":
        return convert_eoproduct20_to_datatree(data)
    else:
        data = input_type

    if isinstance(data, str):
        raise NotImplementedError(f"{type(original_data)} {data}")
    else:
        return data
