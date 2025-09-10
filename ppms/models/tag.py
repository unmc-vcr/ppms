from pydantic import (
    BaseModel,
    Field,
    TypeAdapter,
    field_serializer,
    AliasChoices,
    ValidationInfo,
    AliasPath,
    model_validator
)
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum

class TagType(Enum):
    Person = True
    Facility = False

class Tag(BaseModel):
    id: int = Field(alias="tagId")
    name: str = Field(alias="tagString")
    facility_id: Optional[int] = Field(alias="plateformId", default=0)
    created_at: Optional[datetime] = Field(alias="madeDate", default=None)
    created_by: Optional[int] = Field(alias="madeByUserId", default=None)
    description: Optional[str] = ""
    type: TagType
    hidden: bool = False
    hiddenFromSearch: bool = False
    readOnly: int = 0