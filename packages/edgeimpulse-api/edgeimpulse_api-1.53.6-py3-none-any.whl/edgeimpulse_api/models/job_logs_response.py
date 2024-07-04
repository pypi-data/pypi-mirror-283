# coding: utf-8

"""
    Edge Impulse API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr
from edgeimpulse_api.models.log_stdout_response_all_of_stdout import LogStdoutResponseAllOfStdout

class JobLogsResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    logs: List[LogStdoutResponseAllOfStdout] = ...
    __properties = ["success", "error", "logs"]

    class Config:
        allow_population_by_field_name = True
        validate_assignment = False

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> JobLogsResponse:
        """Create an instance of JobLogsResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in logs (list)
        _items = []
        if self.logs:
            for _item in self.logs:
                if _item:
                    _items.append(_item.to_dict())
            _dict['logs'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> JobLogsResponse:
        """Create an instance of JobLogsResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return JobLogsResponse.construct(**obj)

        _obj = JobLogsResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "logs": [LogStdoutResponseAllOfStdout.from_dict(_item) for _item in obj.get("logs")] if obj.get("logs") is not None else None
        })
        return _obj

