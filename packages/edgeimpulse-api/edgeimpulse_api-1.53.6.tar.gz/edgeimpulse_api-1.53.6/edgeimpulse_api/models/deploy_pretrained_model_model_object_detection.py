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


from typing import List
from pydantic import BaseModel, Field, StrictStr, validator
from edgeimpulse_api.models.object_detection_last_layer import ObjectDetectionLastLayer

class DeployPretrainedModelModelObjectDetection(BaseModel):
    model_type: StrictStr = Field(..., alias="modelType")
    labels: List[StrictStr] = ...
    last_layer: ObjectDetectionLastLayer = Field(..., alias="lastLayer")
    minimum_confidence: float = Field(..., alias="minimumConfidence", description="Threshold for objects (f.e. 0.3)")
    __properties = ["modelType", "labels", "lastLayer", "minimumConfidence"]

    @validator('model_type')
    def model_type_validate_enum(cls, v):
        if v not in ('object-detection'):
            raise ValueError("must validate the enum values ('object-detection')")
        return v

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
    def from_json(cls, json_str: str) -> DeployPretrainedModelModelObjectDetection:
        """Create an instance of DeployPretrainedModelModelObjectDetection from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DeployPretrainedModelModelObjectDetection:
        """Create an instance of DeployPretrainedModelModelObjectDetection from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DeployPretrainedModelModelObjectDetection.construct(**obj)

        _obj = DeployPretrainedModelModelObjectDetection.construct(**{
            "model_type": obj.get("modelType"),
            "labels": obj.get("labels"),
            "last_layer": obj.get("lastLayer"),
            "minimum_confidence": obj.get("minimumConfidence")
        })
        return _obj

