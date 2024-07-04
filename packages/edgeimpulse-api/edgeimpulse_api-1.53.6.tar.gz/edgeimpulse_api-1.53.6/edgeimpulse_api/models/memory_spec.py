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


from typing import Optional
from pydantic import BaseModel, Field
from edgeimpulse_api.models.resource_range import ResourceRange

class MemorySpec(BaseModel):
    fast_bytes: Optional[ResourceRange] = Field(None, alias="fastBytes")
    slow_bytes: Optional[ResourceRange] = Field(None, alias="slowBytes")
    __properties = ["fastBytes", "slowBytes"]

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
    def from_json(cls, json_str: str) -> MemorySpec:
        """Create an instance of MemorySpec from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of fast_bytes
        if self.fast_bytes:
            _dict['fastBytes'] = self.fast_bytes.to_dict()
        # override the default output from pydantic by calling `to_dict()` of slow_bytes
        if self.slow_bytes:
            _dict['slowBytes'] = self.slow_bytes.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> MemorySpec:
        """Create an instance of MemorySpec from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return MemorySpec.construct(**obj)

        _obj = MemorySpec.construct(**{
            "fast_bytes": ResourceRange.from_dict(obj.get("fastBytes")) if obj.get("fastBytes") is not None else None,
            "slow_bytes": ResourceRange.from_dict(obj.get("slowBytes")) if obj.get("slowBytes") is not None else None
        })
        return _obj

