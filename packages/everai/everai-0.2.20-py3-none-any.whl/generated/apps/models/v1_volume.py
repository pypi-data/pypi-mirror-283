# coding: utf-8

"""
    everai/apps/v1/worker.proto

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: version not set
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, StrictStr
from pydantic import Field
from generated.apps.models.volume_config_map_item import VolumeConfigMapItem
from generated.apps.models.volume_secret_item import VolumeSecretItem
from generated.apps.models.volume_volume_item import VolumeVolumeItem
from typing import Dict, Any
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class V1Volume(BaseModel):
    """
    V1Volume
    """
    name: StrictStr
    volume: Optional[VolumeVolumeItem] = None
    secret: Optional[VolumeSecretItem] = None
    config_map: Optional[VolumeConfigMapItem] = Field(default=None, alias="configMap")
    __properties: ClassVar[List[str]] = ["name", "volume", "secret", "configMap"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of V1Volume from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of volume
        if self.volume:
            _dict['volume'] = self.volume.to_dict()
        # override the default output from pydantic by calling `to_dict()` of secret
        if self.secret:
            _dict['secret'] = self.secret.to_dict()
        # override the default output from pydantic by calling `to_dict()` of config_map
        if self.config_map:
            _dict['configMap'] = self.config_map.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """Create an instance of V1Volume from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "volume": VolumeVolumeItem.from_dict(obj.get("volume")) if obj.get("volume") is not None else None,
            "secret": VolumeSecretItem.from_dict(obj.get("secret")) if obj.get("secret") is not None else None,
            "configMap": VolumeConfigMapItem.from_dict(obj.get("configMap")) if obj.get("configMap") is not None else None
        })
        return _obj


