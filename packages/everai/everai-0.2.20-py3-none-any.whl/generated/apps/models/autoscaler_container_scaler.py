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


from typing import List, Optional
from pydantic import BaseModel, StrictInt, StrictStr
from pydantic import Field
from generated.apps.models.v1_entry_path import V1EntryPath
from generated.apps.models.v1_image_pull_secrets import V1ImagePullSecrets
from generated.apps.models.v1_volume import V1Volume
from typing import Dict, Any
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class AutoscalerContainerScaler(BaseModel):
    """
    AutoscalerContainerScaler
    """
    image: Optional[StrictStr] = None
    image_pull_secrets: Optional[V1ImagePullSecrets] = Field(default=None, alias="imagePullSecrets")
    command: Optional[List[StrictStr]] = None
    port: Optional[StrictInt] = None
    entry_path: Optional[V1EntryPath] = Field(default=None, alias="entryPath")
    volumes: Optional[List[V1Volume]] = None
    __properties: ClassVar[List[str]] = ["image", "imagePullSecrets", "command", "port", "entryPath", "volumes"]

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
        """Create an instance of AutoscalerContainerScaler from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of image_pull_secrets
        if self.image_pull_secrets:
            _dict['imagePullSecrets'] = self.image_pull_secrets.to_dict()
        # override the default output from pydantic by calling `to_dict()` of entry_path
        if self.entry_path:
            _dict['entryPath'] = self.entry_path.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in volumes (list)
        _items = []
        if self.volumes:
            for _item in self.volumes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['volumes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """Create an instance of AutoscalerContainerScaler from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "image": obj.get("image"),
            "imagePullSecrets": V1ImagePullSecrets.from_dict(obj.get("imagePullSecrets")) if obj.get("imagePullSecrets") is not None else None,
            "command": obj.get("command"),
            "port": obj.get("port"),
            "entryPath": V1EntryPath.from_dict(obj.get("entryPath")) if obj.get("entryPath") is not None else None,
            "volumes": [V1Volume.from_dict(_item) for _item in obj.get("volumes")] if obj.get("volumes") is not None else None
        })
        return _obj


