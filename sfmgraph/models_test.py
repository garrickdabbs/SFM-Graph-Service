import unittest
import uuid
from .models import SFMEntity, SFMRelationship


class TestSFMEntity(unittest.TestCase):
    def test_entity_creation(self):
        """Test that an SFMEntity can be properly created with valid parameters."""
        entity_id = uuid.uuid4()
        entity = SFMEntity(
            entity_id=entity_id,
            name="Education Funding",
            type="Policy",
            properties={"jurisdiction": "State", "year_enacted": 2023}
        )
        
        self.assertEqual(entity.entity_id, entity_id)
        self.assertEqual(entity.name, "Education Funding")
        self.assertEqual(entity.type, "Policy")
        self.assertEqual(entity.properties["jurisdiction"], "State")
        self.assertEqual(entity.properties["year_enacted"], 2023)

    def test_entity_repr(self):
        """Test the string representation of SFMEntity objects."""
        entity = SFMEntity(
            entity_id=uuid.uuid4(),
            name="Environmental Protection",
            type="Regulation",
            properties={}
        )
        
        expected_repr = "Environmental Protection (Regulation)"
        self.assertEqual(repr(entity), expected_repr)

    def test_empty_properties(self):
        """Test that an entity can be created with empty properties."""
        entity = SFMEntity(
            entity_id=uuid.uuid4(),
            name="Test Entity",
            type="Test Type",
            properties={}
        )
        self.assertEqual(entity.properties, {})
    
    def test_entity_validation(self):
        """Test that invalid inputs raise validation errors."""
        with self.assertRaises(ValueError):
            # Missing required fields should fail validation
            SFMEntity(name="Test", type="Policy") # type: ignore for testing purposes

    def test_serialization(self):
        """Test model serialization to dict/JSON."""
        entity = SFMEntity(entity_id=uuid.uuid4(), name="Test", type="Policy", properties={})
        entity_dict = entity.model_dump()  # For Pydantic v2
        self.assertIsInstance(entity_dict, dict)
        self.assertEqual(entity_dict["name"], "Test")
    

class TestSFMRelationship(unittest.TestCase):
    def test_relationship_creation(self):
        """Test that an SFMRelationship can be properly created with valid parameters."""
        rel_id = uuid.uuid4()
        source_id = uuid.uuid4()
        target_id = uuid.uuid4()
        
        relationship = SFMRelationship(
            rel_id=rel_id,
            sourceEntityId=source_id,
            targetEntityId=target_id,
            description="impacts",
            value=0.75,
            metadata={"confidence": "high", "source": "research paper"}
        )
        
        self.assertEqual(relationship.rel_id, rel_id)
        self.assertEqual(relationship.sourceEntityId, source_id)
        self.assertEqual(relationship.targetEntityId, target_id)
        self.assertEqual(relationship.description, "impacts")
        self.assertEqual(relationship.value, 0.75)
        self.assertEqual(relationship.metadata["confidence"], "high")
        self.assertEqual(relationship.metadata["source"], "research paper")

    def test_relationship_repr(self):
        """Test the string representation of SFMRelationship objects."""
        source_id = uuid.uuid4()
        target_id = uuid.uuid4()
        
        relationship = SFMRelationship(
            rel_id=uuid.uuid4(),
            sourceEntityId=source_id,
            targetEntityId=target_id,
            description="supports",
            value=0.5,
            metadata={}
        )
        
        expected_repr = f"{source_id} --supports:0.5--> {target_id}"
        self.assertEqual(repr(relationship), expected_repr)

    def test_empty_metadata(self):
        """Test that a relationship can be created with empty metadata."""
        relationship = SFMRelationship(
            rel_id=uuid.uuid4(),
            sourceEntityId=uuid.uuid4(),
            targetEntityId=uuid.uuid4(),
            description="test",
            value=0.0,
            metadata={}
        )
        
        self.assertEqual(relationship.metadata, {})

    def test_value_extremes(self):
        """Test relationships with minimum and maximum values."""
        # Test with minimum value (0.0)
        rel_min = SFMRelationship(
            rel_id=uuid.uuid4(),
            sourceEntityId=uuid.uuid4(),
            targetEntityId=uuid.uuid4(),
            description="weak impact",
            value=0.0,
            metadata={}
        )
        self.assertEqual(rel_min.value, 0.0)
        
        # Test with maximum value (1.0)
        rel_max = SFMRelationship(
            rel_id=uuid.uuid4(),
            sourceEntityId=uuid.uuid4(),
            targetEntityId=uuid.uuid4(),
            description="strong impact",
            value=1.0,
            metadata={}
        )
        self.assertEqual(rel_max.value, 1.0)


if __name__ == "__main__":
    unittest.main()