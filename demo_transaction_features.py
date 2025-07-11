#!/usr/bin/env python3
"""
Demonstration of Transaction Management and Data Integrity Features

This script demonstrates the enhanced transaction management, data integrity
validation, and concurrency control features added to the SFM service.
"""

import time
import uuid
from core.sfm_service import SFMService, SFMServiceConfig, CreateActorRequest, CreatePolicyRequest, CreateRelationshipRequest
from core.lock_manager import LockType

def demo_transaction_management():
    """Demonstrate transaction management features."""
    print("=" * 60)
    print("TRANSACTION MANAGEMENT DEMONSTRATION")
    print("=" * 60)
    
    # Create service with minimal validation to avoid rate limiting
    config = SFMServiceConfig(validation_enabled=False)
    service = SFMService(config)
    
    print("1. Basic Transaction Context Manager")
    print("-" * 40)
    
    # Demonstrate basic transaction
    with service.transaction(metadata={"demo": "basic_transaction"}) as tx:
        print(f"In transaction: {service._transaction_manager.is_in_transaction()}")
        actor = service.create_actor(CreateActorRequest(name="DemoActor", sector="demo"))
        print(f"Created actor: {actor.id}")
    
    print(f"Outside transaction: {service._transaction_manager.is_in_transaction()}")
    
    print("\n2. Transaction Rollback on Error")
    print("-" * 40)
    
    initial_stats = service.get_statistics()
    print(f"Initial node count: {initial_stats.total_nodes}")
    
    try:
        with service.transaction(metadata={"demo": "rollback_test"}) as tx:
            actor = service.create_actor(CreateActorRequest(name="RollbackActor", sector="demo"))
            print(f"Created actor: {actor.id}")
            # Simulate an error
            raise ValueError("Simulated error for rollback demo")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    final_stats = service.get_statistics()
    print(f"Final node count: {final_stats.total_nodes}")
    
    # Check transaction statistics
    tx_stats = service.get_transaction_metrics()
    print(f"Total transactions: {tx_stats['total_transactions']}")
    print(f"Committed: {tx_stats['committed_transactions']}")
    print(f"Rolled back: {tx_stats['rolled_back_transactions']}")
    
    print("\n3. Bulk Operations with Transactions")
    print("-" * 40)
    
    # Create multiple actors in a single transaction
    actor_requests = [
        CreateActorRequest(name=f"BulkActor{i}", sector="bulk_demo") 
        for i in range(3)
    ]
    
    try:
        results = service.bulk_create_actors(actor_requests)
        print(f"Successfully created {len(results)} actors in bulk")
        for result in results:
            print(f"  - {result.label}: {result.id}")
    except Exception as e:
        print(f"Bulk operation failed: {e}")
    
    return service

def demo_data_integrity(service):
    """Demonstrate data integrity features."""
    print("\n" + "=" * 60)
    print("DATA INTEGRITY DEMONSTRATION")
    print("=" * 60)
    
    print("1. Referential Integrity Validation")
    print("-" * 40)
    
    # Create two actors for a valid relationship
    actor1 = service.create_actor(CreateActorRequest(name="Actor1", sector="integrity_demo"))
    actor2 = service.create_actor(CreateActorRequest(name="Actor2", sector="integrity_demo"))
    
    # Create a valid relationship
    relationship = service.create_relationship(CreateRelationshipRequest(
        source_id=actor1.id,
        target_id=actor2.id,
        kind="AFFECTS"
    ))
    print(f"Created valid relationship: {relationship.id}")
    
    # Try to create an invalid relationship (non-existent entities)
    try:
        invalid_relationship = service.create_relationship(CreateRelationshipRequest(
            source_id=str(uuid.uuid4()),  # Non-existent
            target_id=str(uuid.uuid4()),  # Non-existent
            kind="AFFECTS"
        ))
    except Exception as e:
        print(f"Caught expected integrity violation: {e}")
    
    print("\n2. Graph Integrity Validation")
    print("-" * 40)
    
    violations = service.validate_graph_integrity()
    print(f"Found {len(violations)} integrity violations")
    for violation in violations:
        print(f"  - {violation.get('type', 'unknown')}: {violation.get('message', 'No message')}")
    
    return service

def demo_concurrency_control(service):
    """Demonstrate concurrency control features."""
    print("\n" + "=" * 60)
    print("CONCURRENCY CONTROL DEMONSTRATION")
    print("=" * 60)
    
    print("1. Entity Locking")
    print("-" * 40)
    
    entity_id = uuid.uuid4()
    
    # Acquire a read lock
    with service._lock_manager.lock_entity(entity_id, LockType.READ) as lock_info:
        print(f"Acquired read lock: {lock_info.lock_id}")
        
        # Check lock status
        lock_status = service._lock_manager.get_lock_info(entity_id)
        print(f"Active locks: {lock_status['active_locks']}")
        print(f"Read locks: {lock_status['read_locks']}")
        print(f"Write locks: {lock_status['write_locks']}")
    
    print("Lock released")
    
    print("\n2. Lock Statistics")
    print("-" * 40)
    
    lock_stats = service._lock_manager.get_lock_stats()
    print(f"Total locks acquired: {lock_stats['total_locks_acquired']}")
    print(f"Total locks released: {lock_stats['total_locks_released']}")
    print(f"Active entity locks: {lock_stats['active_entity_locks']}")
    
    return service

def demo_enhanced_monitoring(service):
    """Demonstrate enhanced monitoring features."""
    print("\n" + "=" * 60)
    print("ENHANCED MONITORING DEMONSTRATION")
    print("=" * 60)
    
    print("1. Comprehensive Status")
    print("-" * 40)
    
    status = service.get_comprehensive_status()
    print(f"Service status: {status['health']['status']}")
    print(f"Node count: {status['health']['node_count']}")
    print(f"Relationship count: {status['health']['relationship_count']}")
    
    print("\n2. Transaction Metrics")
    print("-" * 40)
    
    tx_metrics = status['transaction_metrics']
    print(f"Total transactions: {tx_metrics['total_transactions']}")
    print(f"Committed: {tx_metrics['committed_transactions']}")
    print(f"Rolled back: {tx_metrics['rolled_back_transactions']}")
    print(f"Average duration: {tx_metrics['average_duration']:.4f}s")
    
    print("\n3. Lock Metrics")
    print("-" * 40)
    
    lock_metrics = status['lock_metrics']
    print(f"Locks acquired: {lock_metrics['total_locks_acquired']}")
    print(f"Locks released: {lock_metrics['total_locks_released']}")
    print(f"Active locks: {lock_metrics['total_active_locks']}")
    
    print("\n4. Performance Metrics")
    print("-" * 40)
    
    perf_metrics = status['performance_metrics']
    print(f"Total operations: {perf_metrics.get('total_operations', 0)}")
    print(f"Operations per second: {perf_metrics.get('operations_per_second', 0):.2f}")
    print(f"Error rate: {perf_metrics.get('error_rate', 0):.2f}%")

def main():
    """Main demonstration function."""
    print("SFM Transaction Management and Data Integrity Demo")
    print("=" * 60)
    
    # Run demonstrations
    service = demo_transaction_management()
    service = demo_data_integrity(service)
    service = demo_concurrency_control(service)
    demo_enhanced_monitoring(service)
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    
    # Final statistics
    final_stats = service.get_statistics()
    print(f"\nFinal Statistics:")
    print(f"  Total nodes: {final_stats.total_nodes}")
    print(f"  Total relationships: {final_stats.total_relationships}")
    print(f"  Node types: {final_stats.node_types}")
    print(f"  Relationship kinds: {final_stats.relationship_kinds}")

if __name__ == "__main__":
    main()