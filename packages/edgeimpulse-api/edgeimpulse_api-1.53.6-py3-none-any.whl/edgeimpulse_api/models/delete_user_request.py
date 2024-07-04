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
from pydantic import BaseModel, Field, StrictStr

class DeleteUserRequest(BaseModel):
    password: Optional[StrictStr] = Field(None, description="User's current password. Required if the user has a password set.")
    totp_token: Optional[StrictStr] = Field(None, alias="totpToken", description="TOTP Token. Required if a user has multi-factor authentication with a TOTP token enabled. If a user has MFA enabled, but no totpToken is submitted; then an error starting with \"ERR_TOTP_TOKEN IS REQUIRED\" is returned. Use this to then prompt for an MFA token and re-try this request.")
    __properties = ["password", "totpToken"]

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
    def from_json(cls, json_str: str) -> DeleteUserRequest:
        """Create an instance of DeleteUserRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DeleteUserRequest:
        """Create an instance of DeleteUserRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DeleteUserRequest.construct(**obj)

        _obj = DeleteUserRequest.construct(**{
            "password": obj.get("password"),
            "totp_token": obj.get("totpToken")
        })
        return _obj

