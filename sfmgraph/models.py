import uuid
from pydantic import BaseModel
from typing import Optional, Dict

class SFMEntity(BaseModel):
    """
    Represents an entity (policy, regulation, program, etc.) within the Social Fabric Matrix.
    """
    def __init__(self, entity_id: uuid.UUID, name: str, type: str, properties: dict):
        self.id = entity_id
        self.name = name
        self.type = type
        self.properties = properties

    def __repr__(self):
        return f"{self.name} ({self.type})"

class SFMRelationship(BaseModel):
    """
    Represents a directed relationship between two SFEntity objects.
    """
    def __init__(self, rel_id: uuid.UUID, sourceEntityId: uuid.UUID, targetEntityId: uuid.UUID, description: str,
                 value: float, metadata: dict):
        self.id = rel_id
        self.sourceEntityId = sourceEntityId
        self.targetEntityId = targetEntityId
        self.description = description  # e.g., 'impacts', 'supports', etc.
        self.value = value  # A weight or strength indicator between 0 and 1.
        self.metadata = metadata

    def __repr__(self):
        return f"{self.sourceEntityId} --{self.description}:{self.value}--> {self.targetEntityId}"
