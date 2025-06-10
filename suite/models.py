from pydantic import BaseModel
from typing import Optional, Dict

class SFMEntity(BaseModel):
    id: str
    name: str
    category: str
    properties: Optional[Dict] = {}

class SFMRelationship(BaseModel):
    id: str
    source_id: str
    target_id: str
    description: str
    weight: Optional[float] = None
