# coding: utf-8

from __future__ import annotations

import json
import pprint
import re
from typing import Optional

from pydantic import BaseModel, Field, StrictBool, StrictStr

from xingchen.models.input import Input
from xingchen.models.model_parameters import ModelParameters


class BaseChatRequest(BaseModel):
    """
    BaseChatRequestAcaChatExtParam
    """
    model: Optional[StrictStr] = None
    parameters: Optional[ModelParameters] = None
    input: Input = Field(...)
    servicename: Optional[StrictStr] = None
    debug: Optional[StrictBool] = None
    __properties = ["model", "parameters", "input", "servicename", "debug"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> BaseChatRequest:
        """Create an instance of BaseChatRequestAcaChatExtParam from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of parameters
        if self.parameters:
            _dict['parameters'] = self.parameters.to_dict()
        # override the default output from pydantic by calling `to_dict()` of input
        if self.input:
            _dict['input'] = self.input.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> BaseChatRequest:
        """Create an instance of BaseChatRequestAcaChatExtParam from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return BaseChatRequest.parse_obj(obj)

        _obj = BaseChatRequest.parse_obj({
            "model": obj.get("model"),
            "parameters": ModelParameters.from_dict(obj.get("parameters")) if obj.get("parameters") is not None else None,
            "input": Input.from_dict(obj.get("input")) if obj.get("input") is not None else None,
            "servicename": obj.get("servicename"),
            "debug": obj.get("debug")
        })
        return _obj


