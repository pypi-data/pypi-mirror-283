import datetime
import logging
from typing import Any

from sentineltoolbox.typedefs import MetadataType_L, fix_datetime

logger = logging.getLogger("sentineltoolbox")

valid_aliases: dict[str, str] = {"eo:bands": "bands", "eopf:type": "product:type", "eopf:timeline": "product:timeline"}
short_names_stac_properties: dict[str, str] = {"bands": "bands", "platform": "platform"}
short_names_stac: dict[str, str] = {}
short_names_metadata: dict[str, str] = {}

legacy_aliases = {v: k for k, v in valid_aliases.items()}
attribute_short_names: dict[str, tuple[MetadataType_L, str]] = {}

for key, path in short_names_stac_properties.items():
    attribute_short_names[key] = ("stac_properties", path)
for key, path in short_names_stac.items():
    attribute_short_names[key] = ("stac_discovery", path)
for key, path in short_names_metadata.items():
    attribute_short_names[key] = ("metadata", path)


for legacy, valid in valid_aliases.items():
    if valid in attribute_short_names:
        attribute_short_names[legacy] = attribute_short_names[valid]


def to_lower(value: str, **kwargs: Any) -> str:
    path = kwargs.get("path", "value")
    new_value = value.lower()
    if value != new_value:
        logger.warning(f"{path}: value {value!r} has been fixed to {new_value!r}")
    return new_value


def to_datetime(value: str, **kwargs: Any) -> datetime.datetime:
    return fix_datetime(value)


convert_functions = {
    "stac_properties": {
        "platform": to_lower,
        "created": to_datetime,
        "end_datetime": to_datetime,
        "start_datetime": to_datetime,
    },
}
