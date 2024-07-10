from __future__ import annotations

import json
import pprint
import re  # noqa: F401
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, StrictStr, StrictInt


class KnowledgeBaseDetailDTO(BaseModel):
    id: Optional[StrictInt] = Field(None, alias="id")
    gmt_create: Optional[datetime] = Field(None, alias="gmtCreate", description="创建时间")
    gmt_modified: Optional[datetime] = Field(None, alias="gmtModified", description="修改时间")
    knowledge_base_id: Optional[StrictStr] = Field(None, alias="knowledgeBaseId", description="知识库id")
    name: Optional[StrictStr] = Field(None, alias="name")
    type: Optional[StrictStr] = Field(None, alias="type")
    status: Optional[StrictStr] = Field(None, alias="status")
    __properties = ["id", "gmtCreate", "gmtModified", "knowledgeBaseId", "name", "type", "status"]

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
    def from_json(cls, json_str: str) -> KnowledgeBaseDetailDTO:
        """Create an instance of KnowledgeBaseDetailDTO from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> KnowledgeBaseDetailDTO:
        """Create an instance of KnowledgeBaseDetailDTO from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return KnowledgeBaseDetailDTO.parse_obj(obj)

        _obj = KnowledgeBaseDetailDTO.parse_obj({
            "id": obj.get("id"),
            "gmt_create": obj.get("gmtCreate"),
            "gmt_modified": obj.get("gmtModified"),
            "knowledge_base_id": obj.get("knowledgeBaseId"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "status": obj.get("status"),
        })
        return _obj
