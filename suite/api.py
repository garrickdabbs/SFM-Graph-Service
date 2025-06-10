from fastapi import FastAPI
from .models import SFMEntity, SFMRelationship
from .graphservice import SFMGraph

app = FastAPI()
sfm_graph = SFMGraph()

@app.post("/entity/")
def add_entity(entity: SFMEntity):
    sfm_graph.add_entity(entity)
    return {"message": "Entity added"}

@app.post("/relationship/")
def add_relationship(rel: SFMRelationship):
    sfm_graph.add_relationship(rel)
    return {"message": "Relationship added"}

@app.get("/visualize/")
def visualize():
    sfm_graph.visualize()
    return {"message": "Graph visualization rendered"}
