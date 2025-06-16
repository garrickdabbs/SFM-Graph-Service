import networkx as nx
import uuid
from .models import SFMEntity, SFMRelationship
from typing import List, Optional, Dict, Any, Tuple, Union

class SFMGraph:
    def __init__(self, db=None):
        """Initialize SFM Graph with optional database connection.
        
        Args:
            db: Optional SFMDatabase instance for persistence
        """
        self.graph = nx.DiGraph()
        self.db = db
        
        # If database is provided, load initial data
        if db is not None and db.driver is not None:
            self.load_from_database()

    # ----- Entity Operations -----
    
    def add_entity(self, entity: SFMEntity) -> str:
        """Add entity to the graph and database.
        
        Args:
            entity: SFMEntity object to add
            
        Returns:
            str: ID of the added entity
            
        Raises:
            Exception: If database operation fails
        """
        # Add to in-memory graph
        self.graph.add_node(entity.entity_id, **entity.model_dump())
        
        # Sync with database if connected
        if self.db is not None:
            self.db.create_entity(
                entity.entity_id, 
                entity.name, 
                entity.type, 
                entity.properties
            )
        
        return str(entity.entity_id)

    def get_entity(self, entity_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get entity by ID.
        
        Args:
            entity_id: UUID of the entity to retrieve
            
        Returns:
            Dict: Entity data or None if not found
            
        Raises:
            Exception: If database operation fails
        """
        # Try from database first if connected
        if self.db is not None:
            entity = self.db.get_entity(entity_id)
            if entity:
                return entity
        
        # Fall back to in-memory graph
        if entity_id in self.graph.nodes:
            return dict(self.graph.nodes[entity_id])
        
        return None

    def get_all_entities(self) -> List[Dict[str, Any]]:
        """Get all entities.
        
        Returns:
            List[Dict]: List of all entities
            
        Raises:
            Exception: If database operation fails
        """
        # Get from database if connected
        if self.db is not None:
            return self.db.get_all_entities()
        
        # Fall back to in-memory graph
        return [dict(data) for _, data in self.graph.nodes(data=True)]

    def update_entity(self, entity_id: uuid.UUID, updates: Dict[str, Any]) -> bool:
        """Update entity properties.
        
        Args:
            entity_id: UUID of the entity to update
            updates: Dictionary of properties to update
            
        Returns:
            bool: True if entity was updated
            
        Raises:
            ValueError: If entity doesn't exist
            Exception: If database operation fails
        """
        # Check if entity exists
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")
        
        # Update in database if connected
        if self.db is not None:
            self.db.update_entity(
                entity_id=entity_id,
                name=updates.get('name'),
                type=updates.get('type'),
                properties=updates.get('properties')
            )
        
        # Update in-memory graph
        if entity_id in self.graph.nodes:
            for key, value in updates.items():
                if value is not None:  # Only update provided fields
                    self.graph.nodes[entity_id][key] = value
        
        return True

    def delete_entity(self, entity_id: uuid.UUID) -> bool:
        """Delete entity and its relationships.
        
        Args:
            entity_id: UUID of the entity to delete
            
        Returns:
            bool: True if entity was deleted
            
        Raises:
            ValueError: If entity doesn't exist
            Exception: If database operation fails
        """
        # Check if entity exists
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")
        
        # Delete from database if connected
        if self.db is not None:
            self.db.delete_entity(entity_id)
        
        # Delete from in-memory graph
        if entity_id in self.graph.nodes:
            self.graph.remove_node(entity_id)
        
        return True

    # ----- Relationship Operations -----
    
    def add_relationship(self, relationship: SFMRelationship) -> str:
        """Add relationship to the graph and database.
        
        Args:
            relationship: SFMRelationship object to add
            
        Returns:
            str: ID of the added relationship
            
        Raises:
            ValueError: If source or target entity doesn't exist
            Exception: If database operation fails
        """
        source_id = relationship.sourceEntityId
        target_id = relationship.targetEntityId
        
        # Check if entities exist
        source = self.get_entity(source_id)
        if not source:
            raise ValueError(f"Source entity {source_id} not found")
        
        target = self.get_entity(target_id)
        if not target:
            raise ValueError(f"Target entity {target_id} not found")
        
        # Add to in-memory graph
        if source_id in self.graph.nodes and target_id in self.graph.nodes:
            self.graph.add_edge(source_id, target_id, **relationship.model_dump())
        
        # Sync with database if connected
        if self.db is not None:
            self.db.create_relationship(
                source_id,
                target_id,
                relationship.description,
                relationship.value,
                relationship.rel_id  # Pass the ID to ensure consistency
            )
        
        return str(relationship.rel_id)

    def get_relationship(self, rel_id: uuid.UUID) -> Optional[Dict[str, Any]]:
        """Get relationship by ID.
        
        Args:
            rel_id: UUID of the relationship to retrieve
            
        Returns:
            Dict: Relationship data or None if not found
            
        Raises:
            Exception: If database operation fails
        """
        # Try from database first if connected
        if self.db is not None:
            relationship = self.db.get_relationship(rel_id)
            if relationship:
                return relationship
        
        # Fall back to in-memory graph
        for u, v, data in self.graph.edges(data=True):
            if data.get('rel_id') == rel_id:
                return {
                    'source_id': str(u),
                    'target_id': str(v),
                    **data
                }
        
        return None

    def get_all_relationships(self, source_id=None, target_id=None) -> List[Dict[str, Any]]:
        """Get all relationships, optionally filtered.
        
        Args:
            source_id: Optional source entity ID filter
            target_id: Optional target entity ID filter
            
        Returns:
            List[Dict]: List of relationships
            
        Raises:
            Exception: If database operation fails
        """
        # Get from database if connected
        if self.db is not None:
            relationships = self.db.get_all_relationships()
            
            # Apply filters if provided
            if source_id:
                relationships = [r for r in relationships if uuid.UUID(r['source_id']) == source_id]
            if target_id:
                relationships = [r for r in relationships if uuid.UUID(r['target_id']) == target_id]
                
            return relationships
        
        # Fall back to in-memory graph
        result = []
        for u, v, data in self.graph.edges(data=True):
            if source_id and u != source_id:
                continue
            if target_id and v != target_id:
                continue
                
            result.append({
                'source_id': str(u),
                'target_id': str(v),
                **data
            })
        
        return result

    def get_entity_relationships(self, entity_id: uuid.UUID) -> Dict[str, Any]:
        """Get all relationships for a specific entity.
        
        Args:
            entity_id: UUID of the entity
            
        Returns:
            Dict: Entity and its relationships
            
        Raises:
            ValueError: If entity doesn't exist
            Exception: If database operation fails
        """
        # Check if entity exists
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")
        
        # Get all relationships
        all_rels = self.get_all_relationships()
        
        # Filter relationships involving this entity
        outgoing = [r for r in all_rels if uuid.UUID(r['source_id']) == entity_id]
        incoming = [r for r in all_rels if uuid.UUID(r['target_id']) == entity_id]
        
        return {
            "entity": entity,
            "outgoing_relationships": outgoing,
            "incoming_relationships": incoming
        }

    def update_relationship(self, rel_id: uuid.UUID, updates: Dict[str, Any]) -> bool:
        """Update relationship properties.
        
        Args:
            rel_id: UUID of the relationship to update
            updates: Dictionary of properties to update
            
        Returns:
            bool: True if relationship was updated
            
        Raises:
            ValueError: If relationship doesn't exist
            Exception: If database operation fails
        """
        # Check if relationship exists
        relationship = self.get_relationship(rel_id)
        if not relationship:
            raise ValueError(f"Relationship with ID {rel_id} not found")
        
        # Update in database if connected
        if self.db is not None:
            self.db.update_relationship(
                rel_id=rel_id,
                description=updates.get('description'),
                weight=updates.get('value')
            )
        
        # Update in-memory graph
        source_id = uuid.UUID(relationship['source_id'])
        target_id = uuid.UUID(relationship['target_id'])
        
        if (source_id in self.graph.nodes and 
            target_id in self.graph.nodes and
            self.graph.has_edge(source_id, target_id)):
            
            for key, value in updates.items():
                if value is not None:  # Only update provided fields
                    self.graph[source_id][target_id][key] = value
        
        return True

    def delete_relationship(self, rel_id: uuid.UUID) -> bool:
        """Delete a relationship.
        
        Args:
            rel_id: UUID of the relationship to delete
            
        Returns:
            bool: True if relationship was deleted
            
        Raises:
            ValueError: If relationship doesn't exist
            Exception: If database operation fails
        """
        # Check if relationship exists
        relationship = self.get_relationship(rel_id)
        if not relationship:
            raise ValueError(f"Relationship with ID {rel_id} not found")
        
        # Delete from database if connected
        if self.db is not None:
            self.db.delete_relationship(rel_id)
        
        # Delete from in-memory graph
        source_id = uuid.UUID(relationship['source_id'])
        target_id = uuid.UUID(relationship['target_id'])
        
        if (source_id in self.graph.nodes and 
            target_id in self.graph.nodes and
            self.graph.has_edge(source_id, target_id)):
            self.graph.remove_edge(source_id, target_id)
        
        return True
    
    # ----- Data Synchronization -----
    
    def load_from_database(self, db=None) -> Tuple[int, int]:
        """Load all entities and relationships from the database.
        
        Args:
            db: SFMDatabase instance to load from (uses self.db if None)
            
        Returns:
            Tuple[int, int]: Count of entities and relationships loaded
            
        Raises:
            ValueError: If no database connection
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
                uuid.UUID(entity['id']), 
                name=entity['name'],
                type=entity['type'],
                properties=entity.get('properties', {})
            )
            
        # Load all relationships
        relationships = db.get_all_relationships()
        for rel in relationships:
            self.graph.add_edge(
                uuid.UUID(rel['source_id']),
                uuid.UUID(rel['target_id']),
                rel_id=rel.get('id', uuid.uuid4()),
                description=rel['description'],
                value=rel.get('weight', 0.0),
                metadata=rel.get('metadata', {})
            )
        
        return len(entities), len(relationships)
    
    def save_to_database(self, db=None, clear_existing=False) -> Tuple[int, int]:
        """Save the entire graph to the database.
        
        Args:
            db: SFMDatabase instance to save to (uses self.db if None)
            clear_existing: Whether to clear existing database data first
            
        Returns:
            Tuple[int, int]: Count of entities and relationships saved
            
        Raises:
            ValueError: If no database connection
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
            rel_id = edge_data.get('rel_id', uuid.uuid4())
            
            db.create_relationship(source, target, description, weight, rel_id)
            
        return len(self.graph.nodes), len(self.graph.edges)
    
    # ----- Visualization -----
    
    def visualize(self, node_size=2000, font_size=10, save_path=None) -> None:
        """Visualize the SFM graph.
        
        Args:
            node_size: Size of nodes in visualization
            font_size: Size of node labels
            save_path: Path to save image (if None, displays interactively)
        """
        import matplotlib.pyplot as plt
        pos = nx.spring_layout(self.graph)
        
        # Get node labels from node data
        labels = {n: data.get('name', str(n)) for n, data in self.graph.nodes(data=True)}
        
        # Draw nodes
        nx.draw(self.graph, pos, with_labels=True, labels=labels,
                node_size=node_size, font_size=font_size)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()


