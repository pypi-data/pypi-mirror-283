from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from typing import Optional

from pydantic import BaseModel, Field, StrictInt

from xingchen.models.user_profile import UserProfile


class KnowledgeBaseQueryDTO(BaseModel):
    page_num: Optional[StrictInt] = Field(None, alias="pageNum")
    page_size: Optional[StrictInt] = Field(None, alias="pageSize")
    user_profile: Optional[UserProfile] = Field(None, alias="userProfile")
    __properties = ["pageNum", "pageSize", "userProfile"]

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
    def from_json(cls, json_str: str) -> KnowledgeBaseQueryDTO:
        """Create an instance of KnowledgeBaseQueryDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> KnowledgeBaseQueryDTO:
        """Create an instance of KnowledgeBaseQueryDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return KnowledgeBaseQueryDTO.parse_obj(obj)

        _obj = KnowledgeBaseQueryDTO.parse_obj({
            "page_num": obj.get("pageNum"),
            "page_size": obj.get("pageSize"),
            "user_profile": UserProfile.from_dict(obj.get("userProfile")) if obj.get(
                "userProfile") is not None else None
        })
        return _obj
