import networkx as nx
import uuid
from sfmgraph.models import SFMEntity, SFMRelationship

class SFMGraph:
    def __init__(self, db=None):
        """Initialize SFM Graph with optional database connection.
        
        Args:
            db: Optional SFMDatabase instance for persistence
        """
        self.graph = nx.DiGraph()
        self.db = db
        
        # If database is provided, load initial data
        if db is not None:
            self.load_from_database(db)

    def add_entity(self, entity):
        """Add entity to the graph and optionally to database."""
        self.graph.add_node(entity.entity_id, **entity.model_dump())
        
        # Sync with database if connected
        if self.db is not None:
            self.db.create_entity(
                entity.entity_id, 
                entity.name, 
                entity.type, 
                entity.properties
            )

    def add_relationship(self, relationship):
        """Add relationship to the graph and optionally to database."""
        source_id = relationship.sourceEntityId
        target_id = relationship.targetEntityId
        
        if source_id not in self.graph.nodes:
            raise ValueError(f"Source entity {source_id} does not exist")
        if target_id not in self.graph.nodes:
            raise ValueError(f"Target entity {target_id} does not exist")
            
        self.graph.add_edge(source_id, target_id, **relationship.model_dump())
        
        # Sync with database if connected
        if self.db is not None:
            self.db.create_relationship(
                source_id,
                target_id,
                relationship.description,
                relationship.value
            )
    
    def remove_entity(self, entity_id):
        """Remove entity from graph and optionally from database."""
        self.graph.remove_node(entity_id)
        
        # Sync with database if connected
        if self.db is not None:
            self.db.delete_entity(entity_id)
        
    def get_entity(self, entity_id):
        """Get entity by ID from the graph."""
        if entity_id in self.graph.nodes:
            return self.graph.nodes[entity_id]
        return None
    
    def load_from_database(self, db=None):
        """Load all entities and relationships from the database.
        
        Args:
            db: SFMDatabase instance to load from (uses self.db if None)
        """
        db = db or self.db
        if db is None:
            raise ValueError("No database connection provided")
            
        # Clear existing graph
        self.graph.clear()
        
        # Load all entities
        entities = db.get_all_entities()
        for entity in entities:
            self.graph.add_node(
                entity['id'], 
                name=entity['name'],
                type=entity['type'],
                properties=entity.get('properties', {})
            )
            
        # Load all relationships
        relationships = db.get_all_relationships()
        for rel in relationships:
            self.graph.add_edge(
                rel['source_id'],
                rel['target_id'],
                rel_id=rel.get('id', uuid.uuid4()),
                description=rel['description'],
                value=rel.get('weight', 0.0),
                metadata=rel.get('metadata', {})
            )
        
        return len(entities), len(relationships)
    
    def save_to_database(self, db=None, clear_existing=False):
        """Save the entire graph to the database.
        
        Args:
            db: SFMDatabase instance to save to (uses self.db if None)
            clear_existing: Whether to clear existing database data first
        """
        db = db or self.db
        if db is None:
            raise ValueError("No database connection provided")
            
        if clear_existing:
            db.clear_database()
        
        # Save all entities
        for node_id, node_data in self.graph.nodes(data=True):
            entity_id = node_id
            name = node_data.get('name', f"Entity {node_id}")
            entity_type = node_data.get('type', 'Unknown')
            properties = {k: v for k, v in node_data.items() 
                          if k not in ['name', 'type', 'id']}
                          
            db.create_entity(entity_id, name, entity_type, properties)
            
        # Save all relationships
        for source, target, edge_data in self.graph.edges(data=True):
            description = edge_data.get('description', 'connects to')
            weight = edge_data.get('value', 0.0)
            
            db.create_relationship(source, target, description, weight)
            
        return len(self.graph.nodes), len(self.graph.edges)
    
    # TODO: move to a separate service
    def visualize(self, node_size=2000, font_size=10, save_path=None):
        """Visualize the SFM graph."""
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=node_size, font_size=font_size)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


