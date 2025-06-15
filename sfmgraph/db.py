import os
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable, AuthError

class SFMDatabase:
    def __init__(self):
        self.uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = os.getenv("NEO4J_USER", "neo4j")
        self.password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = None

    def connect(self):
        """Establish connection to Neo4j database."""
        try:
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
            # Verify connection is working by running a simple query
            with self.driver.session() as session:
                session.run("RETURN 1")
            return True
        except (ServiceUnavailable, AuthError) as e:
            if self.driver:
                self.driver.close()
                self.driver = None
            raise e

    def close(self):
        """Close the database connection."""
        if self.driver:
            self.driver.close()
            self.driver = None

    def create_entity(self, entity_id, name, type, properties):
        """Create or update an entity in the database."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MERGE (e:SFMEntity {id: $entity_id})
        SET e.name = $name, e.type = $type, e.properties = $properties
        RETURN e
        """
        with self.driver.session() as session:
            session.run(query, entity_id=str(entity_id), name=name, type=type, properties=properties)

    def create_relationship(self, source_id, target_id, description, weight=None):
        """Create or update a relationship in the database."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (a:SFMEntity {id: $source_id}), (b:SFMEntity {id: $target_id})
        MERGE (a)-[r:DELIVERS_TO {description: $description}]->(b)
        SET r.weight = $weight
        RETURN r
        """
        with self.driver.session() as session:
            session.run(query, 
                       source_id=str(source_id), 
                       target_id=str(target_id), 
                       description=description, 
                       weight=weight)
    
    def get_all_entities(self):
        """Retrieve all entities from the database."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (e:SFMEntity)
        RETURN e.id AS id, e.name AS name, e.type AS type, e.properties AS properties
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]
    
    def get_all_relationships(self):
        """Retrieve all relationships from the database."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (a:SFMEntity)-[r:DELIVERS_TO]->(b:SFMEntity)
        RETURN a.id AS source_id, b.id AS target_id, 
               r.description AS description, r.weight AS weight
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]
    
    def get_entity(self, entity_id):
        """Retrieve a specific entity by ID."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (e:SFMEntity {id: $entity_id})
        RETURN e.id AS id, e.name AS name, e.type AS type, e.properties AS properties
        """
        with self.driver.session() as session:
            result = session.run(query, entity_id=str(entity_id))
            record = result.single()
            return dict(record) if record else None
    
    def delete_entity(self, entity_id):
        """Delete an entity and all its relationships."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (e:SFMEntity {id: $entity_id})
        DETACH DELETE e
        """
        with self.driver.session() as session:
            session.run(query, entity_id=str(entity_id))
    
    def clear_database(self):
        """Remove all entities and relationships from the database."""
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (n:SFMEntity)
        DETACH DELETE n
        """
        with self.driver.session() as session:
            session.run(query)
