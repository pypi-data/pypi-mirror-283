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
from edgeimpulse_api.models.classify_job_response_all_of_accuracy import ClassifyJobResponseAllOfAccuracy
from edgeimpulse_api.models.classify_job_response_all_of_additional_metrics_by_learn_block import ClassifyJobResponseAllOfAdditionalMetricsByLearnBlock
from edgeimpulse_api.models.keras_model_variant_enum import KerasModelVariantEnum
from edgeimpulse_api.models.model_prediction import ModelPrediction
from edgeimpulse_api.models.model_result import ModelResult

class ClassifyJobResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    result: List[ModelResult] = ...
    predictions: List[ModelPrediction] = ...
    accuracy: ClassifyJobResponseAllOfAccuracy = ...
    additional_metrics_by_learn_block: List[ClassifyJobResponseAllOfAdditionalMetricsByLearnBlock] = Field(..., alias="additionalMetricsByLearnBlock")
    available_variants: List[KerasModelVariantEnum] = Field(..., alias="availableVariants", description="List of all model variants for which classification results exist")
    __properties = ["success", "error", "result", "predictions", "accuracy", "additionalMetricsByLearnBlock", "availableVariants"]

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
    def from_json(cls, json_str: str) -> ClassifyJobResponse:
        """Create an instance of ClassifyJobResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in result (list)
        _items = []
        if self.result:
            for _item in self.result:
                if _item:
                    _items.append(_item.to_dict())
            _dict['result'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in predictions (list)
        _items = []
        if self.predictions:
            for _item in self.predictions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['predictions'] = _items
        # override the default output from pydantic by calling `to_dict()` of accuracy
        if self.accuracy:
            _dict['accuracy'] = self.accuracy.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in additional_metrics_by_learn_block (list)
        _items = []
        if self.additional_metrics_by_learn_block:
            for _item in self.additional_metrics_by_learn_block:
                if _item:
                    _items.append(_item.to_dict())
            _dict['additionalMetricsByLearnBlock'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClassifyJobResponse:
        """Create an instance of ClassifyJobResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ClassifyJobResponse.construct(**obj)

        _obj = ClassifyJobResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "result": [ModelResult.from_dict(_item) for _item in obj.get("result")] if obj.get("result") is not None else None,
            "predictions": [ModelPrediction.from_dict(_item) for _item in obj.get("predictions")] if obj.get("predictions") is not None else None,
            "accuracy": ClassifyJobResponseAllOfAccuracy.from_dict(obj.get("accuracy")) if obj.get("accuracy") is not None else None,
            "additional_metrics_by_learn_block": [ClassifyJobResponseAllOfAdditionalMetricsByLearnBlock.from_dict(_item) for _item in obj.get("additionalMetricsByLearnBlock")] if obj.get("additionalMetricsByLearnBlock") is not None else None,
            "available_variants": obj.get("availableVariants")
        })
        return _obj

