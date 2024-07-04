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
from edgeimpulse_api.models.portal_file import PortalFile

class ListPortalFilesInFolderResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    files: List[PortalFile] = ...
    continuation_token: Optional[StrictStr] = Field(None, alias="continuationToken")
    __properties = ["success", "error", "files", "continuationToken"]

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
    def from_json(cls, json_str: str) -> ListPortalFilesInFolderResponse:
        """Create an instance of ListPortalFilesInFolderResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in files (list)
        _items = []
        if self.files:
            for _item in self.files:
                if _item:
                    _items.append(_item.to_dict())
            _dict['files'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListPortalFilesInFolderResponse:
        """Create an instance of ListPortalFilesInFolderResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListPortalFilesInFolderResponse.construct(**obj)

        _obj = ListPortalFilesInFolderResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "files": [PortalFile.from_dict(_item) for _item in obj.get("files")] if obj.get("files") is not None else None,
            "continuation_token": obj.get("continuationToken")
        })
        return _obj

