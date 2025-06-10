from fastapi import FastAPI
from .models import SFMEntity, SFMRelationship
from .graphservice import SFMGraph
from .db import SFMDatabase

app = FastAPI()
sfm_graph = SFMGraph()
db = SFMDatabase()

@app.post("/entity/")
def add_entity(entity: SFMEntity):
    db.create_entity(entity.id, entity.name, entity.type, entity.properties)
    return {"message": "Entity added to Neo4j"}

@app.post("/relationship/")
def add_relationship(rel: SFMRelationship):
    db.create_relationship(rel.sourceEntityId, rel.targetEntityId, rel.description, rel.value)
    return {"message": "Relationship added to Neo4j"}

@app.get("/visualize/")
def visualize():
    sfm_graph.visualize()
    return {"message": "Graph visualization rendered"}







