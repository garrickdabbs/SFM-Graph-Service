from fastapi import FastAPI, HTTPException, Depends, Query, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from uuid import UUID
from .models import SFMEntity, SFMRelationship
from .graphservice import SFMGraph
from .db import SFMDatabase

app = FastAPI()

# Create a database connection
db = SFMDatabase()

# Create a graph service with the database
sfm_graph = SFMGraph(db)

def get_graph_service():
    """Dependency to get graph service with connected database."""
    if not db.driver:
        try:
            db.connect()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")
    return sfm_graph

# Mount static files directory
static_directory = Path(__file__).parent / "static"
os.makedirs(static_directory, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_directory), name="static")

@app.get("/", response_class=HTMLResponse)
def get_index():
    """Serve the API testing UI."""
    with open(static_directory / "index.html") as f:
        return f.read()

# --- ENTITY ENDPOINTS ---

@app.post("/entities/", status_code=201, response_model=dict)
def add_entity(entity: SFMEntity, graph: SFMGraph = Depends(get_graph_service)):
    """Add a new entity to the SFM."""
    try:
        entity_id = graph.add_entity(entity)
        return {"message": "Entity added", "id": entity_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/entities/", response_model=List[dict])
def get_entities(graph: SFMGraph = Depends(get_graph_service)):
    """Get all entities from the SFM."""
    try:
        return graph.get_all_entities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/entities/{entity_id}", response_model=dict)
def get_entity(entity_id: UUID, graph: SFMGraph = Depends(get_graph_service)):
    """Get a specific entity by ID."""
    try:
        entity = graph.get_entity(entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail=f"Entity with ID {entity_id} not found")
        return entity
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/entities/{entity_id}", response_model=dict)
def update_entity(entity_id: UUID, updates: Dict[str, Any], graph: SFMGraph = Depends(get_graph_service)):
    """Update a specific entity by ID."""
    try:
        graph.update_entity(entity_id, updates)
        return {"message": f"Entity {entity_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/entities/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity(entity_id: UUID, graph: SFMGraph = Depends(get_graph_service)):
    """Delete an entity and its relationships."""
    try:
        graph.delete_entity(entity_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- RELATIONSHIP ENDPOINTS ---
    
@app.post("/relationships/", status_code=201, response_model=dict)
def add_relationship(rel: SFMRelationship, graph: SFMGraph = Depends(get_graph_service)):
    """Add a new relationship to the SFM."""
    try:
        rel_id = graph.add_relationship(rel)
        return {"message": "Relationship added", "id": rel_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/relationships/", response_model=List[dict])
def get_relationships(
    source_id: Optional[UUID] = Query(None, description="Filter by source entity ID"),
    target_id: Optional[UUID] = Query(None, description="Filter by target entity ID"),
    graph: SFMGraph = Depends(get_graph_service)
):
    """Get all relationships, optionally filtered by source or target entity."""
    try:
        return graph.get_all_relationships(source_id, target_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/entities/{entity_id}/relationships", response_model=dict)
def get_entity_relationships(entity_id: UUID, graph: SFMGraph = Depends(get_graph_service)):
    """Get all relationships for a specific entity (both incoming and outgoing)."""
    try:
        return graph.get_entity_relationships(entity_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/relationships/{rel_id}", response_model=dict)
def update_relationship(rel_id: UUID, updates: Dict[str, Any], graph: SFMGraph = Depends(get_graph_service)):
    """Update a relationship by ID."""
    try:
        graph.update_relationship(rel_id, updates)
        return {"message": f"Relationship {rel_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/relationships/{rel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relationship(rel_id: UUID, graph: SFMGraph = Depends(get_graph_service)):
    """Delete a relationship by ID."""
    try:
        graph.delete_relationship(rel_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- VISUALIZATION ENDPOINT ---

@app.get("/visualize/")
def get_visualization(graph: SFMGraph = Depends(get_graph_service)):
    """Generate and return graph visualization as image file."""
    try:
        import tempfile
        import os
        
        temp_dir = tempfile.gettempdir()
        image_path = os.path.join(temp_dir, "sfm_graph.png")
        graph.visualize(save_path=image_path)
        
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ADVANCED ENDPOINTS ---

@app.post("/graph/load/")
def load_graph_from_database(graph: SFMGraph = Depends(get_graph_service)):
    """Load the graph from database."""
    try:
        entities, relationships = graph.load_from_database()
        return {"message": f"Graph loaded with {entities} entities and {relationships} relationships"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/graph/save/")
def save_graph_to_database(
    clear_existing: bool = Query(False, description="Clear existing database data before saving"),
    graph: SFMGraph = Depends(get_graph_service)
):
    """Save the in-memory graph to database."""
    try:
        entities, relationships = graph.save_to_database(clear_existing=clear_existing)
        return {"message": f"Graph saved with {entities} entities and {relationships} relationships"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
