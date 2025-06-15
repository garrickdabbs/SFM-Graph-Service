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
        """Establish connection to Neo4j database.
        
        Returns:
            bool: True if connection successful, False otherwise
            
        Raises:
            ServiceUnavailable: If Neo4j service cannot be reached
            AuthError: If authentication credentials are invalid
        """
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
        if self.driver:
            self.driver.close()
            self.driver = None

    def create_entity(self, entity_id, name, type, properties):
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MERGE (e:SFMEntity {id: $entity_id})
        SET e.name = $name, e.type = $type, e.properties = $properties
        RETURN e
        """
        with self.driver.session() as session:
            session.run(query, entity_id=entity_id, name=name, type=type, properties=properties)

    def create_relationship(self, source_id, target_id, description, weight=None):
        if not self.driver:
            raise RuntimeError("Database connection not established. Call connect() first.")
            
        query = """
        MATCH (a:SFMEntity {id: $source_id}), (b:SFMEntity {id: $target_id})
        MERGE (a)-[r:DELIVERS_TO {description: $description, weight: $weight}]->(b)
        RETURN r
        """
        with self.driver.session() as session:
            session.run(query, source_id=source_id, target_id=target_id, description=description, weight=weight)
