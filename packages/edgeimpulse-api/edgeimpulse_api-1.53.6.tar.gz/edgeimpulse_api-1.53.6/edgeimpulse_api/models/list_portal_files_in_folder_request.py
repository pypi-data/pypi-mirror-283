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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class ListPortalFilesInFolderRequest(BaseModel):
    prefix: StrictStr = Field(..., description="S3 prefix")
    continuation_token: Optional[StrictStr] = Field(None, alias="continuationToken", description="Only one S3 page (1000 items typically) is returned. Pass in the continuationToken on the next request to receive the next page.")
    only_fetch_folders: Optional[StrictBool] = Field(None, alias="onlyFetchFolders", description="If set, then no files will be returned")
    __properties = ["prefix", "continuationToken", "onlyFetchFolders"]

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
    def from_json(cls, json_str: str) -> ListPortalFilesInFolderRequest:
        """Create an instance of ListPortalFilesInFolderRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListPortalFilesInFolderRequest:
        """Create an instance of ListPortalFilesInFolderRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListPortalFilesInFolderRequest.construct(**obj)

        _obj = ListPortalFilesInFolderRequest.construct(**{
            "prefix": obj.get("prefix"),
            "continuation_token": obj.get("continuationToken"),
            "only_fetch_folders": obj.get("onlyFetchFolders")
        })
        return _obj

