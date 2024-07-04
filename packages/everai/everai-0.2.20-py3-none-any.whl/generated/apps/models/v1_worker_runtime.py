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
from typing import Optional
from pydantic import BaseModel, StrictInt, StrictStr
from pydantic import Field
from generated.apps.models.worker_worker_detail_status import WorkerWorkerDetailStatus
from generated.apps.models.worker_worker_status import WorkerWorkerStatus
from typing import Dict, Any
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class V1WorkerRuntime(BaseModel):
    """
    V1WorkerRuntime
    """
    worker_id: Optional[StrictStr] = Field(default=None, alias="workerId")
    device_id: Optional[StrictStr] = Field(default=None, alias="deviceId")
    revision: Optional[StrictStr] = None
    launch_time: Optional[datetime] = Field(default=None, alias="launchTime")
    last_serve_time: Optional[datetime] = Field(default=None, alias="lastServeTime")
    success_count: Optional[StrictStr] = Field(default=None, alias="successCount")
    failed_count: Optional[StrictStr] = Field(default=None, alias="failedCount")
    replace_worker_id: Optional[StrictStr] = Field(default=None, alias="replaceWorkerId")
    status: Optional[WorkerWorkerStatus] = None
    detail_status: Optional[WorkerWorkerDetailStatus] = Field(default=None, alias="detailStatus")
    number_of_sessions: Optional[StrictInt] = Field(default=None, alias="numberOfSessions")
    gpu_type: Optional[StrictStr] = Field(default=None, alias="gpuType")
    region: Optional[StrictStr] = None
    current_request: Optional[StrictInt] = Field(default=None, alias="currentRequest")
    __properties: ClassVar[List[str]] = ["workerId", "deviceId", "revision", "launchTime", "lastServeTime", "successCount", "failedCount", "replaceWorkerId", "status", "detailStatus", "numberOfSessions", "gpuType", "region", "currentRequest"]

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
        """Create an instance of V1WorkerRuntime from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        """Create an instance of V1WorkerRuntime from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "workerId": obj.get("workerId"),
            "deviceId": obj.get("deviceId"),
            "revision": obj.get("revision"),
            "launchTime": obj.get("launchTime"),
            "lastServeTime": obj.get("lastServeTime"),
            "successCount": obj.get("successCount"),
            "failedCount": obj.get("failedCount"),
            "replaceWorkerId": obj.get("replaceWorkerId"),
            "status": obj.get("status"),
            "detailStatus": obj.get("detailStatus"),
            "numberOfSessions": obj.get("numberOfSessions"),
            "gpuType": obj.get("gpuType"),
            "region": obj.get("region"),
            "currentRequest": obj.get("currentRequest")
        })
        return _obj


