# coding: utf-8

"""
    Edge Impulse API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from inspect import getfullargspec
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class ModelEngineShortEnum(str, Enum):
    """
    allowed enum values
    """

    TFLITE_EON = 'tflite-eon'
    TFLITE_EON_RAM_OPTIMIZED = 'tflite-eon-ram-optimized'
    TFLITE = 'tflite'

