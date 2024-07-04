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

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, StrictInt, StrictStr
from pydantic import Field
from generated.apps.models.v1_worker import V1Worker
from typing import Dict, Any
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class V1ListWorkersResponse(BaseModel):
    """
    V1ListWorkersResponse
    """
    workers: Optional[List[V1Worker]] = None
    queue_size: Optional[StrictInt] = Field(default=None, alias="queueSize")
    queue_name: Optional[StrictStr] = Field(default=None, alias="queueName")
    last_scale_up_time: Optional[datetime] = Field(default=None, alias="lastScaleUpTime")
    last_scale_down_delete_time: Optional[datetime] = Field(default=None, alias="lastScaleDownDeleteTime")
    max_workers: Optional[StrictInt] = Field(default=None, alias="maxWorkers")
    __properties: ClassVar[List[str]] = ["workers", "queueSize", "queueName", "lastScaleUpTime", "lastScaleDownDeleteTime", "maxWorkers"]

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
        """Create an instance of V1ListWorkersResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in workers (list)
        _items = []
        if self.workers:
            for _item in self.workers:
                if _item:
                    _items.append(_item.to_dict())
            _dict['workers'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """Create an instance of V1ListWorkersResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "workers": [V1Worker.from_dict(_item) for _item in obj.get("workers")] if obj.get("workers") is not None else None,
            "queueSize": obj.get("queueSize"),
            "queueName": obj.get("queueName"),
            "lastScaleUpTime": obj.get("lastScaleUpTime"),
            "lastScaleDownDeleteTime": obj.get("lastScaleDownDeleteTime"),
            "maxWorkers": obj.get("maxWorkers")
        })
        return _obj


