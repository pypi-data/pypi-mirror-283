import logging
import warnings
from typing import Any, Generator, MutableMapping, TypeAlias

from datatree import DataTree
from xarray import Dataset

from sentineltoolbox._utils import string_to_slice
from sentineltoolbox.attributes_hotfix import (
    attribute_short_names,
    convert_functions,
    legacy_aliases,
    valid_aliases,
)
from sentineltoolbox.typedefs import MetadataType_L, category_paths

logger = logging.getLogger("sentineltoolbox")

__all__ = ["AttributeHandler"]

ContainerWithAttributes: TypeAlias = DataTree[Any] | Dataset | MutableMapping[str, Any]


def path_relative_to_category(path: str, category: MetadataType_L | None) -> str:
    if category in ("stac_properties", "stac_discovery", "metadata"):
        return path.replace(category_paths[category], "")
    else:
        return path


def fix_attribute_value(path: str, value: Any, category: MetadataType_L | None) -> Any:
    if category is None:
        category = guess_category(path)
    if category is None:
        return value
    else:
        new_value = value
        relpath = path_relative_to_category(path, category)

        conversions = convert_functions.get(category, {})
        if relpath in conversions:
            f = conversions[relpath]
            new_value = f(value, path=path)

        return new_value


def guess_category(path: str, **kwargs: Any) -> MetadataType_L | None:
    if path.startswith("properties") or path.startswith("stac_discovery/properties"):
        return "stac_properties"
    elif path.startswith("stac_discovery"):
        return "stac_discovery"
    elif path.startswith("other_metadata") or path.startswith("metadata"):
        return "metadata"
    elif path in attribute_short_names:
        # search in prop lookuptable / short names
        return attribute_short_names[path][0]
    else:
        # else: no category in path, not find in lookup table => None
        return None


def get_valid_alias(path: str, **kwargs: Any) -> str:
    warn = kwargs.get("warn_deprecated", True)

    if path in valid_aliases:
        newpath = valid_aliases[path]
    else:
        newpath = path
    if path != newpath and warn:
        logger.warning(f"{path!r} is deprecated, use {newpath!r} instead")
    return newpath


def get_legacy_alias(part: str, **kwargs: Any) -> str:
    if part in legacy_aliases:
        return legacy_aliases[part]
    else:
        return part


def _get_attr_dict(data: ContainerWithAttributes) -> MutableMapping[Any, Any]:
    if isinstance(data, (DataTree, Dataset)):
        return data.attrs
    else:
        return data


def fix_attribute_path(path: str, category: MetadataType_L | None = None, **kwargs: Any) -> str:
    if category is None:
        category = guess_category(path)
    if category is None:
        return path

    recognized_properties = ["stac_discovery/properties/", "properties/"]
    recognized_stac = ["stac_discovery/"]
    recognized_metadata = ["other_metadata/", "metadata/"]
    recognized_prefixes = recognized_properties + recognized_stac + recognized_metadata

    if category == "stac_properties":
        prefix = "stac_discovery/properties/"
    elif category == "stac_discovery":
        prefix = "stac_discovery/"
    elif category == "metadata":
        prefix = "other_metadata/"
    else:
        prefix = ""

    for possible_prefix in recognized_prefixes:
        prefix_parts = possible_prefix.split("/")

        for prefix_part in prefix_parts:
            if prefix_part and path.startswith(prefix_part):
                path = path[len(prefix_part) + 1 :]  # noqa: E203

    category_fixed_path = prefix + path
    fixed_parts = []
    for part in category_fixed_path.split("/"):
        fixed_parts.append(get_valid_alias(part))
    return "/".join(fixed_parts)


def find_and_fix_attribute(
    attrs: MutableMapping[str, Any],
    path: str,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> tuple[str, str, Any]:
    convert_value_type = kwargs.get("convert_value_type", True)

    if category is None and path is not None:
        category = guess_category(path)

    # Define all possible place, depending on category
    places_properties = [
        ("stac_discovery/properties/", attrs.get("stac_discovery", {}).get("properties")),
        ("properties/", attrs.get("properties")),
        # ("stac_discovery/", attrs.get("stac_discovery")),
    ]
    places_metadata = [
        ("other_metadata/", attrs.get("other_metadata")),
        ("metadata/", attrs.get("metadata")),
    ]
    places_stac = [
        ("stac_discovery/", attrs.get("stac_discovery")),
    ]
    places_root: list[tuple[str, Any]] = [("", attrs)]
    if category == "stac_properties":
        # search order: stac_discovery/properties -> properties -> root
        places = places_properties + places_root
    elif category == "metadata":
        # search order: other_metadata -> root
        places = places_metadata + places_root
    elif category == "stac_discovery":
        # search order: stac_discovery -> root
        places = places_stac + places_root
    elif category == "root":
        places = places_root
    else:
        category = None
        places = places_root + places_properties + places_stac + places_metadata

    # remove trailing space
    path = path.strip().rstrip("/")

    value = None

    real_path_parts = []

    value_found = False

    for place_path, place in places:
        if place is None:
            continue

        if place_path:
            real_path_parts = [place_path.rstrip("/")]
        else:
            real_path_parts = []

        group = place
        parts: list[str] = path.split("/")
        for part in parts:
            try:
                valid_part: int | slice | str = int(part)
            except ValueError:
                try:
                    valid_part = string_to_slice(part)
                except ValueError:
                    valid_part = part

            if isinstance(valid_part, (int, slice)):
                real_path_parts.append(part)
                if isinstance(group, list):
                    group = group[valid_part]
                    value_found = True
                else:
                    raise KeyError(
                        f"Invalid path {path!r}. Part {valid_part!r} is not correct because {group} is not a list",
                    )
            else:
                valid_name = get_valid_alias(part, warn_deprecated=False)
                legacy_name = get_legacy_alias(part, **kwargs)

                if valid_name in group:
                    value_found = True
                    group = group[valid_name]
                    real_path_parts.append(valid_name)
                elif legacy_name in group:
                    value_found = True
                    group = group[legacy_name]
                    real_path_parts.append(legacy_name)
                else:
                    # key not found on this place, try another place
                    # useless to continue the end of the path => break
                    break
        if value_found:
            break
    if value_found:
        value = group
        real_path = "/".join(real_path_parts)
        fixed_path = fix_attribute_path(real_path, category, warn_deprecated=kwargs.get("warn_deprecated", True))
        if convert_value_type:
            value = fix_attribute_value(fixed_path, value, category=category)
        return value, fixed_path, real_path
    else:
        raise KeyError(path)


def recurse_json_dict(
    d: MutableMapping[Any, Any] | list[Any],
    root: str = "",
) -> Generator[tuple[str, Any], None, None]:
    if isinstance(d, dict):
        items = list(d.items())
    elif isinstance(d, list):
        items = [(str(i), v) for i, v in enumerate(d)]
    else:
        items = []

    for k, v in items:
        path = root + k + "/"
        yield path, v
        if isinstance(v, (dict, list)):
            yield from recurse_json_dict(v, path)


def search_attributes(
    attrs: ContainerWithAttributes,
    path: str,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> list[str]:
    kwargs["warn_deprecated"] = kwargs.get("warn_deprecated", False)
    kwargs["convert_value_type"] = kwargs.get("convert_value_type", False)
    recursive = kwargs.get("recursive", True)
    limit = kwargs.get("limit")

    dict_attrs = _get_attr_dict(attrs)
    results = set()

    try:
        value, fixed, real = find_and_fix_attribute(dict_attrs, path, category=category, **kwargs)
        results.add(real)
    except KeyError:
        pass

    if recursive:
        for p, v in recurse_json_dict(dict_attrs):
            if isinstance(limit, int) and len(results) > limit:
                break
            if not isinstance(v, dict):
                continue
            current_category = guess_category(p)
            if category is not None and current_category != category:
                continue
            try:
                value, fixed, real = find_and_fix_attribute(v, path, category=category, **kwargs)
            except KeyError:
                pass
            else:
                results.add(p + real)
    return list(sorted(results))


def extract_attr(
    data: ContainerWithAttributes,
    path: str | None = None,
    *,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> Any:
    attrs = _get_attr_dict(data)
    if path is None:
        if category is None:
            return attrs
        else:
            category_path = category_paths[category]
            return extract_attr(attrs, category_path)
    else:
        value, fixed_path, real_path = find_and_fix_attribute(attrs, path, category=category, **kwargs)
        return value


def set_attr(
    data: ContainerWithAttributes,
    path: str,
    value: Any,
    category: MetadataType_L | None = None,
    **kwargs: Any,
) -> MutableMapping[Any, Any]:
    root_attrs = _get_attr_dict(data)
    path = fix_attribute_path(path, category=category)
    attrs = root_attrs
    parts = path.split("/")
    for part in parts[:-1]:
        attrs = attrs.setdefault(part, {})
    attrs[parts[-1]] = fix_attribute_value(path, value, category=category)
    return root_attrs


class AttributeHandler:

    def __init__(self, container: ContainerWithAttributes, **kwargs: Any):
        """

        :param container:
        :param kwargs:
          - template: template name to use
          - context: template context
        """
        self._container = container

    def to_dict(self) -> MutableMapping[Any, Any]:
        return _get_attr_dict(self._container)

    def container(self) -> Any:
        return self._container

    def set_property(self, path: str, value: Any, **kwargs: Any) -> None:
        warnings.warn("use set_stac_property instead", DeprecationWarning)
        self.set_stac_property(path, value, **kwargs)

    def set_stac_property(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="stac_properties", **kwargs)

    def set_metadata(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="metadata", **kwargs)

    def set_stac(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="stac_discovery", **kwargs)

    def set_root_attr(self, path: str, value: Any, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category="root", **kwargs)

    def set_attr(self, path: str, value: Any, category: MetadataType_L | None = None, **kwargs: Any) -> None:
        set_attr(self._container, path, value, category=category, **kwargs)

    def get_attr(self, path: str | None = None, category: MetadataType_L | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category=category, **kwargs)

    def get_stac_property(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="stac_properties", **kwargs)

    def get_metadata(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="metadata", **kwargs)

    def get_stac(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="stac_discovery", **kwargs)

    def get_root_attr(self, path: str | None = None, **kwargs: Any) -> Any:
        return extract_attr(self._container, path, category="root", **kwargs)

    def search(
        self,
        path: str,
        *,
        category: MetadataType_L | None = None,
        **kwargs: Any,
    ) -> list[str]:
        return search_attributes(self._container, path, category=category, **kwargs)

    def fix_path(self, path: str, **kwargs: Any) -> str:
        return fix_attribute_path(path, **kwargs)
