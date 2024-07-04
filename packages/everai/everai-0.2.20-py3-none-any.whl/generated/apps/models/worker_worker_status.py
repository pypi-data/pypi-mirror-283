# coding: utf-8

"""
    everai/apps/v1/worker.proto

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: version not set
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
import re  # noqa: F401
from enum import Enum



try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class WorkerWorkerStatus(str, Enum):
    """
    WorkerWorkerStatus
    """

    """
    allowed enum values
    """
    STATUS_UNSPECIFIED = 'STATUS_UNSPECIFIED'
    STATUS_INITIALIZED = 'STATUS_INITIALIZED'
    STATUS_PENDING = 'STATUS_PENDING'
    STATUS_RUNNING = 'STATUS_RUNNING'
    STATUS_TERMINATING = 'STATUS_TERMINATING'
    STATUS_ERROR = 'STATUS_ERROR'
    STATUS_UNAVAILABLE = 'STATUS_UNAVAILABLE'
    STATUS_TERMINATED = 'STATUS_TERMINATED'
    STATUS_CREATED = 'STATUS_CREATED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of WorkerWorkerStatus from a JSON string"""
        return cls(json.loads(json_str))


