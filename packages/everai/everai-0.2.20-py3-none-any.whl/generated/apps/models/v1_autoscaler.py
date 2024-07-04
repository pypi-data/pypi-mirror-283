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
from generated.apps.models.autoscaler_builtin_scaler import AutoscalerBuiltinScaler
from generated.apps.models.autoscaler_container_scaler import AutoscalerContainerScaler
from generated.apps.models.autoscaler_third_party_scaler import AutoscalerThirdPartyScaler
from typing import Dict, Any
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class V1Autoscaler(BaseModel):
    """
    V1Autoscaler
    """
    scheduler: Optional[StrictStr] = None
    builtin: Optional[AutoscalerBuiltinScaler] = None
    third_party: Optional[AutoscalerThirdPartyScaler] = Field(default=None, alias="thirdParty")
    container: Optional[AutoscalerContainerScaler] = None
    __properties: ClassVar[List[str]] = ["scheduler", "builtin", "thirdParty", "container"]

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
        """Create an instance of V1Autoscaler from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of builtin
        if self.builtin:
            _dict['builtin'] = self.builtin.to_dict()
        # override the default output from pydantic by calling `to_dict()` of third_party
        if self.third_party:
            _dict['thirdParty'] = self.third_party.to_dict()
        # override the default output from pydantic by calling `to_dict()` of container
        if self.container:
            _dict['container'] = self.container.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """Create an instance of V1Autoscaler from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "scheduler": obj.get("scheduler"),
            "builtin": AutoscalerBuiltinScaler.from_dict(obj.get("builtin")) if obj.get("builtin") is not None else None,
            "thirdParty": AutoscalerThirdPartyScaler.from_dict(obj.get("thirdParty")) if obj.get("thirdParty") is not None else None,
            "container": AutoscalerContainerScaler.from_dict(obj.get("container")) if obj.get("container") is not None else None
        })
        return _obj


