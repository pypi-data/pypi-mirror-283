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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, validator

class ImpulseBlockVersion(BaseModel):
    id: Optional[StrictInt] = Field(None, description="Identifier for the new block version. Make sure to up this number when creating a new block, and don't re-use identifiers.")
    primary_version: Optional[StrictBool] = Field(None, alias="primaryVersion", description="Whether this block is the primary version of its base block.")
    name: Optional[StrictStr] = Field(None, description="Block name, will be used in menus. If a block has a baseBlockId, this field is ignored and the base block's name is used instead.")
    description: Optional[StrictStr] = Field(None, description="A short description of the block version, displayed in the block versioning UI")
    dsp: Optional[List[StrictInt]] = Field(None, description="(Learn only) DSP dependencies, identified by DSP block ID")
    axes: Optional[List[StrictStr]] = Field(None, description="(DSP only) Input axes, identified by the name in the name of the axis")
    input: Optional[StrictInt] = Field(None, description="(DSP only) The ID of the Input block a DSP block is connected to")
    window_size_ms: Optional[StrictInt] = Field(None, alias="windowSizeMs", description="(Input only) Size of the sliding window in milliseconds")
    window_increase_ms: Optional[StrictInt] = Field(None, alias="windowIncreaseMs", description="(Input only) We use a sliding window to go over the raw data. How many milliseconds to increase the sliding window with for each step.")
    frequency_hz: Optional[float] = Field(None, alias="frequencyHz", description="(Input only) Frequency of the input data in Hz")
    classification_window_increase_ms: Optional[StrictInt] = Field(None, alias="classificationWindowIncreaseMs", description="(Input only) We use a sliding window to go over the raw data. How many milliseconds to increase the sliding window with for each step in classification mode.")
    pad_zeros: Optional[StrictBool] = Field(None, alias="padZeros", description="(Input only) Whether to zero pad data when there is not enough data.")
    image_width: Optional[StrictInt] = Field(None, alias="imageWidth", description="(Input only) Width all images are resized to before training")
    image_height: Optional[StrictInt] = Field(None, alias="imageHeight", description="(Input only) Width all images are resized to before training")
    resize_mode: Optional[StrictStr] = Field(None, alias="resizeMode", description="(Input only) How to resize images before training")
    resize_method: Optional[StrictStr] = Field(None, alias="resizeMethod", description="(Input only) Resize method to use when resizing images")
    crop_anchor: Optional[StrictStr] = Field(None, alias="cropAnchor", description="(Input only) If images are resized using a crop, choose where to anchor the crop")
    __properties = ["id", "primaryVersion", "name", "description", "dsp", "axes", "input", "windowSizeMs", "windowIncreaseMs", "frequencyHz", "classificationWindowIncreaseMs", "padZeros", "imageWidth", "imageHeight", "resizeMode", "resizeMethod", "cropAnchor"]

    @validator('resize_mode')
    def resize_mode_validate_enum(cls, v):
        if v is None:
            return v

        if v not in ('squash', 'fit-short', 'fit-long', 'crop'):
            raise ValueError("must validate the enum values ('squash', 'fit-short', 'fit-long', 'crop')")
        return v

    @validator('resize_method')
    def resize_method_validate_enum(cls, v):
        if v is None:
            return v

        if v not in ('lanczos3', 'nearest'):
            raise ValueError("must validate the enum values ('lanczos3', 'nearest')")
        return v

    @validator('crop_anchor')
    def crop_anchor_validate_enum(cls, v):
        if v is None:
            return v

        if v not in ('top-left', 'top-center', 'top-right', 'middle-left', 'middle-center', 'middle-right', 'bottom-left', 'bottom-center', 'bottom-right'):
            raise ValueError("must validate the enum values ('top-left', 'top-center', 'top-right', 'middle-left', 'middle-center', 'middle-right', 'bottom-left', 'bottom-center', 'bottom-right')")
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
    def from_json(cls, json_str: str) -> ImpulseBlockVersion:
        """Create an instance of ImpulseBlockVersion from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ImpulseBlockVersion:
        """Create an instance of ImpulseBlockVersion from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ImpulseBlockVersion.construct(**obj)

        _obj = ImpulseBlockVersion.construct(**{
            "id": obj.get("id"),
            "primary_version": obj.get("primaryVersion"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "dsp": obj.get("dsp"),
            "axes": obj.get("axes"),
            "input": obj.get("input"),
            "window_size_ms": obj.get("windowSizeMs"),
            "window_increase_ms": obj.get("windowIncreaseMs"),
            "frequency_hz": obj.get("frequencyHz"),
            "classification_window_increase_ms": obj.get("classificationWindowIncreaseMs"),
            "pad_zeros": obj.get("padZeros"),
            "image_width": obj.get("imageWidth"),
            "image_height": obj.get("imageHeight"),
            "resize_mode": obj.get("resizeMode"),
            "resize_method": obj.get("resizeMethod"),
            "crop_anchor": obj.get("cropAnchor")
        })
        return _obj

