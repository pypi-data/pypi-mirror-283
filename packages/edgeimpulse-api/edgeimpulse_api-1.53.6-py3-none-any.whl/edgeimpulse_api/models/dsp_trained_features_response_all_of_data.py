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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr
from edgeimpulse_api.models.dsp_trained_features_response_all_of_sample import DspTrainedFeaturesResponseAllOfSample

class DspTrainedFeaturesResponseAllOfData(BaseModel):
    x: Dict[str, float] = Field(..., alias="X", description="Data by feature index for this window")
    y: StrictInt = Field(..., description="Training label index")
    y_label: StrictStr = Field(..., alias="yLabel", description="Training label string")
    sample: Optional[DspTrainedFeaturesResponseAllOfSample] = None
    __properties = ["X", "y", "yLabel", "sample"]

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
    def from_json(cls, json_str: str) -> DspTrainedFeaturesResponseAllOfData:
        """Create an instance of DspTrainedFeaturesResponseAllOfData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of sample
        if self.sample:
            _dict['sample'] = self.sample.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DspTrainedFeaturesResponseAllOfData:
        """Create an instance of DspTrainedFeaturesResponseAllOfData from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DspTrainedFeaturesResponseAllOfData.construct(**obj)

        _obj = DspTrainedFeaturesResponseAllOfData.construct(**{
            "x": obj.get("X"),
            "y": obj.get("y"),
            "y_label": obj.get("yLabel"),
            "sample": DspTrainedFeaturesResponseAllOfSample.from_dict(obj.get("sample")) if obj.get("sample") is not None else None
        })
        return _obj

