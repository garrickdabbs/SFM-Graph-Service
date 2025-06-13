import os
from neo4j import GraphDatabase

class SFMDatabase:
    def __init__(self):
        uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        user = os.getenv("NEO4J_USER", "neo4j")
        password = os.getenv("NEO4J_PASSWORD", "password")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_entity(self, entity_id, name, type, properties):
        query = """
        MERGE (e:SFMEntity {id: $entity_id})
        SET e.name = $name, e.type = $type, e.properties = $properties
        RETURN e
        """
        with self.driver.session() as session:
            session.run(query, entity_id=entity_id, name=name, type=type, properties=properties)

    def create_relationship(self, source_id, target_id, description, weight=None):
        query = """
        MATCH (a:SFMEntity {id: $source_id}), (b:SFMEntity {id: $target_id})
        MERGE (a)-[r:DELIVERS_TO {description: $description, weight: $weight}]->(b)
        RETURN r
        """
        with self.driver.session() as session:
            session.run(query, source_id=source_id, target_id=target_id, description=description, weight=weight)
