from pydantic import BaseModel
from typing import Optional, Dict

class SFEntity(BaseModel):
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, entity_id: guid, name: str, entity_type: str, properties: dict):
        self.id = entity_id
        self.name = name
        self.type = entity_type
        self.properties = properties

    def __repr__(self):
        return f"{self.name} ({self.type})"

class SFMRelationship(BaseModel):
    """
    Represents a directed relationship between two SFEntity objects.
    """
    def __init__(self, rel_id: guid, source: SFEntity, target: SFEntity, delivery: str,
                 weight: Optional[float], metadata: dict):
        self.id = rel_id
        self.source = source
        self.target = target
        self.delivery = delivery  # e.g., 'impacts', 'supports', etc.
        self.weight = weight  # A weight or strength indicator between 0 and 1.
        self.metadata = metadata

    def __repr__(self):
        return f"{self.source.name} --{self.property_name}:{self.value}--> {self.target.name}"
