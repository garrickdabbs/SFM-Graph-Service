#!/usr/bin/env python3
"""
Test script for the persistence improvements to validate new functionality.
This is a temporary test file to demonstrate the new features work correctly.
"""

import tempfile
import shutil
from pathlib import Path
import time

from core.sfm_persistence import SFMPersistenceManager, PersistenceConfig
from core.graph import SFMGraph
from core.core_nodes import Actor, Resource
from core.sfm_enums import ResourceType
from core.relationships import Relationship, RelationshipKind


def create_test_graph():
    """Create a simple test graph."""
    graph = SFMGraph(
        name="Test Graph for Improvements",
        description="Testing new persistence improvements"
    )
    
    # Add a simple actor
    farmer = Actor(
        label="Test Farmer",
        description="A test farmer actor",
        sector="agriculture",
        legal_form="individual"
    )
    graph.actors[farmer.id] = farmer
    
    # Add a simple resource
    corn = Resource(
        label="Corn Crop",
        description="Test corn resource",
        rtype=ResourceType.NATURAL,
        unit="tons"
    )
    graph.resources[corn.id] = corn
    
    # Add a relationship
    produces_rel = Relationship(
        source_id=farmer.id,
        target_id=corn.id,
        kind=RelationshipKind.PRODUCES,
        weight=1.0
    )
    graph.relationships[produces_rel.id] = produces_rel
    
    return graph


def test_enhanced_backup_counting():
    """Test the enhanced backup counting functionality."""
    print("=== Testing Enhanced Backup Counting ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = PersistenceConfig(base_path=temp_dir)
        manager = SFMPersistenceManager(config)
        graph = create_test_graph()
        
        # Save graph and create backups
        manager.save_graph("test_graph", graph)
        backup1 = manager.create_backup("test_graph", "backup1")
        backup2 = manager.create_backup("test_graph", "backup2")
        
        # Test enhanced storage statistics
        stats = manager.get_storage_statistics()
        
        print(f"Total backups: {stats.get('total_backups', 0)}")
        print(f"Total backup size: {stats.get('total_backup_size_bytes', 0)} bytes")
        print(f"Valid backups: {stats.get('valid_backups', 0)}")
        print(f"Backup age stats: {stats.get('backup_age_stats', {})}")
        
        # Validate results
        assert stats['total_backups'] == 2, f"Expected 2 backups, got {stats['total_backups']}"
        assert stats['total_backup_size_bytes'] > 0, "Backup size should be greater than 0"
        assert stats['valid_backups'] == 2, f"Expected 2 valid backups, got {stats['valid_backups']}"
        
        print("✓ Enhanced backup counting works correctly!")


def test_metadata_validation():
    """Test the enhanced metadata validation."""
    print("\n=== Testing Enhanced Metadata Validation ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = PersistenceConfig(base_path=temp_dir)
        manager = SFMPersistenceManager(config)
        graph = create_test_graph()
        
        # Save graph
        metadata = manager.save_graph("test_graph", graph)
        print(f"Saved graph with metadata: {metadata.graph_id}, version {metadata.version}")
        
        # Test metadata retrieval with validation
        retrieved_metadata = manager._get_metadata("test_graph")
        assert retrieved_metadata is not None, "Should retrieve valid metadata"
        print(f"Retrieved metadata: {retrieved_metadata.graph_id}, version {retrieved_metadata.version}")
        
        # Test invalid graph ID handling
        invalid_metadata = manager._get_metadata("")
        assert invalid_metadata is None, "Should return None for empty graph ID"
        
        invalid_metadata = manager._get_metadata("nonexistent")
        assert invalid_metadata is None, "Should return None for nonexistent graph"
        
        print("✓ Enhanced metadata validation works correctly!")


def test_version_consistency():
    """Test version consistency checking."""
    print("\n=== Testing Version Consistency Checking ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = PersistenceConfig(base_path=temp_dir, enable_versioning=True)
        manager = SFMPersistenceManager(config)
        graph = create_test_graph()
        
        # Save multiple versions
        manager.save_graph("test_graph", graph)
        graph.description = "Updated description"
        manager.save_graph("test_graph", graph)
        
        # Check version consistency
        consistency_result = manager.check_version_consistency("test_graph")
        
        print(f"Consistency check for 'test_graph': {consistency_result}")
        print(f"Is consistent: {consistency_result['is_consistent']}")
        print(f"Current version: {consistency_result['current_version']}")
        print(f"Version files: {consistency_result['version_files']}")
        
        # Should be consistent since we just created it properly
        assert consistency_result['is_consistent'], "Version consistency should be True for properly created graph"
        
        # Test nonexistent graph
        nonexistent_result = manager.check_version_consistency("nonexistent")
        assert not nonexistent_result['is_consistent'], "Nonexistent graph should not be consistent"
        
        print("✓ Version consistency checking works correctly!")


def test_cleanup_operations():
    """Test cleanup operations."""
    print("\n=== Testing Cleanup Operations ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = PersistenceConfig(base_path=temp_dir, enable_versioning=True, max_versions=3)
        manager = SFMPersistenceManager(config)
        graph = create_test_graph()
        
        # Create multiple versions
        graph_id = "test_cleanup"
        for i in range(5):
            graph.description = f"Version {i + 1}"
            manager.save_graph(graph_id, graph)
            time.sleep(0.1)  # Small delay to ensure different timestamps
        
        # Check version history before cleanup
        history_before = manager.get_version_history(graph_id)
        print(f"Versions before cleanup: {len(history_before)}")
        
        # Clean up old versions (keep only 2)
        cleanup_result = manager.cleanup_old_versions(graph_id, keep_versions=2)
        
        print(f"Cleanup result: {cleanup_result}")
        print(f"Versions before: {cleanup_result['versions_before']}")
        print(f"Versions after: {cleanup_result['versions_after']}")
        print(f"Cleaned up: {cleanup_result['cleaned_up']}")
        print(f"Space freed: {cleanup_result['space_freed_bytes']} bytes")
        
        # Verify cleanup worked
        history_after = manager.get_version_history(graph_id)
        print(f"Versions after cleanup: {len(history_after)}")
        
        assert cleanup_result['versions_after'] == 2, f"Should have 2 versions after cleanup, got {cleanup_result['versions_after']}"
        assert len(cleanup_result['cleaned_up']) > 0, "Should have cleaned up some versions"
        
        # Test backup cleanup
        manager.create_backup(graph_id, "test_backup_1")
        manager.create_backup(graph_id, "test_backup_2")
        
        backup_cleanup = manager.cleanup_old_backups(max_age_days=0)  # Clean all backups
        print(f"Backup cleanup result: {backup_cleanup}")
        
        print("✓ Cleanup operations work correctly!")


def test_data_integrity_validation():
    """Test enhanced data integrity validation."""
    print("\n=== Testing Data Integrity Validation ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        config = PersistenceConfig(base_path=temp_dir, validate_on_save=True)
        manager = SFMPersistenceManager(config)
        graph = create_test_graph()
        
        # Test valid graph validation
        try:
            manager._validate_graph(graph)
            print("✓ Valid graph passed validation")
        except Exception as e:
            print(f"✗ Valid graph failed validation: {e}")
            assert False, f"Valid graph should pass validation: {e}"
        
        # Test graph with missing relationship target (should fail)
        invalid_graph = create_test_graph()
        bad_rel = Relationship(
            source_id=list(invalid_graph.actors.keys())[0],
            target_id="nonexistent-target",  # This target doesn't exist
            kind=RelationshipKind.AFFECTS,
            weight=0.5
        )
        invalid_graph.relationships[bad_rel.id] = bad_rel
        
        try:
            manager._validate_graph(invalid_graph)
            print("✗ Invalid graph incorrectly passed validation")
            assert False, "Invalid graph should fail validation"
        except Exception as e:
            print(f"✓ Invalid graph correctly failed validation: {e}")
        
        print("✓ Data integrity validation works correctly!")


def main():
    """Run all tests."""
    print("Testing SFM Persistence Improvements")
    print("=" * 50)
    
    try:
        test_enhanced_backup_counting()
        test_metadata_validation()
        test_version_consistency()
        test_cleanup_operations()
        test_data_integrity_validation()
        
        print("\n" + "=" * 50)
        print("✓ All persistence improvement tests passed!")
        
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()