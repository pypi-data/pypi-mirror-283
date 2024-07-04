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

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr, validator
from edgeimpulse_api.models.organization_dataset_bucket import OrganizationDatasetBucket

class OrganizationDataset(BaseModel):
    dataset: StrictStr = ...
    last_file_created: datetime = Field(..., alias="lastFileCreated")
    total_file_size: StrictInt = Field(..., alias="totalFileSize")
    total_file_count: StrictInt = Field(..., alias="totalFileCount")
    total_item_count: StrictInt = Field(..., alias="totalItemCount")
    total_item_count_checklist_ok: StrictInt = Field(..., alias="totalItemCountChecklistOK")
    total_item_count_checklist_failed: StrictInt = Field(..., alias="totalItemCountChecklistFailed")
    tags: List[StrictStr] = ...
    category: Optional[StrictStr] = None
    bucket: Optional[OrganizationDatasetBucket] = None
    type: StrictStr = ...
    bucket_path: Optional[StrictStr] = Field(None, alias="bucketPath", description="Location of the dataset within the bucket")
    __properties = ["dataset", "lastFileCreated", "totalFileSize", "totalFileCount", "totalItemCount", "totalItemCountChecklistOK", "totalItemCountChecklistFailed", "tags", "category", "bucket", "type", "bucketPath"]

    @validator('type')
    def type_validate_enum(cls, v):
        if v not in ('files', 'clinical'):
            raise ValueError("must validate the enum values ('files', 'clinical')")
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
    def from_json(cls, json_str: str) -> OrganizationDataset:
        """Create an instance of OrganizationDataset from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of bucket
        if self.bucket:
            _dict['bucket'] = self.bucket.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrganizationDataset:
        """Create an instance of OrganizationDataset from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return OrganizationDataset.construct(**obj)

        _obj = OrganizationDataset.construct(**{
            "dataset": obj.get("dataset"),
            "last_file_created": obj.get("lastFileCreated"),
            "total_file_size": obj.get("totalFileSize"),
            "total_file_count": obj.get("totalFileCount"),
            "total_item_count": obj.get("totalItemCount"),
            "total_item_count_checklist_ok": obj.get("totalItemCountChecklistOK"),
            "total_item_count_checklist_failed": obj.get("totalItemCountChecklistFailed"),
            "tags": obj.get("tags"),
            "category": obj.get("category"),
            "bucket": OrganizationDatasetBucket.from_dict(obj.get("bucket")) if obj.get("bucket") is not None else None,
            "type": obj.get("type"),
            "bucket_path": obj.get("bucketPath")
        })
        return _obj

