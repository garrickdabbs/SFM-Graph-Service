from pydantic import BaseModel
from typing import Optional, Dict

class SFEntity(BaseModel):
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, entity_id: uuid.UUID, name: str, entity_type: str, properties: dict):
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
    def __init__(self, id: uuid.UUID, sourceEntityId: uuid.UUID, targetEntityId: uuid.UUID, delivery: str,
                 weight: Optional[float], metadata: dict):
        self.id = id
        self.sourceEntityId = sourceEntityId
        self.targetEntityId = targetEntityId
        self.action = action  # e.g., 'impacts', 'supports', etc.
        self.weight = weight  # A weight or strength indicator between 0 and 1.
        self.metadata = metadata

    def __repr__(self):
        return f"{self.source.name} --{self.property_name}:{self.value}--> {self.target.name}"
