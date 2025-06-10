from pydantic import BaseModel
from typing import Optional, Dict

class SFEntity(BaseModel):
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, entity_id: str, name: str, entity_type: str, properties: dict):
        self.id = entity_id
        self.name = name
        self.type = entity_type
        self.properties = properties

    def __repr__(self):
        return f"{self.name} ({self.type})"
class SFMRelationship(BaseModel):
    id: str
    source_id: str
    target_id: str
    description: str
    weight: Optional[float] = None
