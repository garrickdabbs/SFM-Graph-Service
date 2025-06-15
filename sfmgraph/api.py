from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from sfmgraph.models import SFMEntity, SFMRelationship
from sfmgraph.graphservice import SFMGraph
from sfmgraph.db import SFMDatabase

app = FastAPI()
sfm_graph = SFMGraph()

def get_db():
    db = SFMDatabase()
    try:
        db.connect()  # Assuming there's a connect method
        yield db
    finally:
        db.close()  # Assuming there's a close method

@app.post("/entities/", status_code=201, response_model=dict)
def add_entity(entity: SFMEntity, db: SFMDatabase = Depends(get_db)):
    try:
        db.create_entity(entity.entity_id, entity.name, entity.type, entity.properties)
        sfm_graph.add_entity(entity)  # Also add to in-memory graph
        return {"message": "Entity added", "id": str(entity.entity_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/relationship/")
def add_relationship(rel: SFMRelationship, db: SFMDatabase = Depends(get_db)):
    db.create_relationship(rel.sourceEntityId, rel.targetEntityId, rel.description, rel.value)
    return {"message": "Relationship added to Neo4j"}

@app.get("/visualize/")
def get_visualization():
    """Generate and return graph visualization as image file"""
    import tempfile
    import os
    
    temp_dir = tempfile.gettempdir()
    image_path = os.path.join(temp_dir, "sfm_graph.png")
    sfm_graph.visualize(save_path=image_path)
    
    return FileResponse(image_path, media_type="image/png")







