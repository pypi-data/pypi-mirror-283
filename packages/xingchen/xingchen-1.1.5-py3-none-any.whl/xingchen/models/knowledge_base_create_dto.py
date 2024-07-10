from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictStr

from xingchen.models.user_profile import UserProfile


class KnowledgeBaseCreateDTO(BaseModel):
    name: Optional[StrictStr] = Field(None, alias="name")
    description: Optional[StrictStr] = Field(None, alias="description")
    user_profile: Optional[UserProfile] = Field(None, alias="userProfile")
    __properties = ["name", "description", "userProfile"]

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
    def from_json(cls, json_str: str) -> KnowledgeBaseCreateDTO:
        """Create an instance of KnowledgeBaseCreateDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> KnowledgeBaseCreateDTO:
        """Create an instance of KnowledgeBaseCreateDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return KnowledgeBaseCreateDTO.parse_obj(obj)

        _obj = KnowledgeBaseCreateDTO.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "user_profile": UserProfile.from_dict(obj.get("userProfile")) if obj.get(
                "userProfile") is not None else None
        })
        return _obj
