import uuid
from pydantic import BaseModel
from typing import Optional, Dict

class SFMEntity(BaseModel):
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    entity_id: uuid.UUID
    name: str
    type: str
    properties: dict

    def __repr__(self):
        return f"{self.name} ({self.type})"

class SFMRelationship(BaseModel):
    """
    Represents a directed relationship between two SFEntity objects.
    """
    rel_id: uuid.UUID
    sourceEntityId: uuid.UUID
    targetEntityId: uuid.UUID
    description: str  # e.g., 'impacts', 'supports', etc.
    value: float  # A weight or strength indicator between 0 and 1.
    metadata: dict

    def __repr__(self):
        return f"{self.sourceEntityId} --{self.description}:{self.value}--> {self.targetEntityId}"
