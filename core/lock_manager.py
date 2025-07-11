"""
Lock Manager for SFM Service

This module provides basic concurrency control for SFM operations,
allowing entity-level locking to prevent concurrent modification conflicts.

Features:
- Entity-level read/write locks
- Deadlock prevention with timeout
- Context manager support
- Thread-safe operations
"""

import logging
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Set

logger = logging.getLogger(__name__)


class LockType(Enum):
    """Types of locks available."""
    READ = "read"
    WRITE = "write"


@dataclass
class LockInfo:
    """Information about an active lock."""
    lock_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    entity_id: uuid.UUID = field(default_factory=uuid.uuid4)
    lock_type: LockType = LockType.READ
    thread_id: int = 0
    acquired_at: str = field(default_factory=lambda: datetime.now().isoformat())
    timeout: Optional[float] = None
    
    def __hash__(self):
        """Make LockInfo hashable for use in sets."""
        return hash((self.lock_id, self.entity_id, self.lock_type, self.thread_id))
    
    def __eq__(self, other):
        """Define equality for LockInfo objects."""
        if not isinstance(other, LockInfo):
            return False
        return (self.lock_id == other.lock_id and 
                self.entity_id == other.entity_id and
                self.lock_type == other.lock_type and
                self.thread_id == other.thread_id)


class LockManager:
    """
    Manages entity-level locking for concurrent access control.
    
    Provides read/write locks for entities to prevent data corruption
    during concurrent operations.
    """
    
    def __init__(self, default_timeout: float = 30.0):
        """
        Initialize the lock manager.
        
        Args:
            default_timeout: Default timeout for lock acquisition in seconds
        """
        self.default_timeout = default_timeout
        self._locks: Dict[uuid.UUID, threading.RLock] = {}
        self._active_locks: Dict[uuid.UUID, Set[LockInfo]] = {}
        self._global_lock = threading.RLock()
        self._lock_stats = {
            "total_locks_acquired": 0,
            "total_locks_released": 0,
            "lock_timeouts": 0,
            "deadlocks_prevented": 0
        }
    
    def _get_entity_lock(self, entity_id: uuid.UUID) -> threading.RLock:
        """Get or create a lock for the specified entity."""
        with self._global_lock:
            if entity_id not in self._locks:
                self._locks[entity_id] = threading.RLock()
                self._active_locks[entity_id] = set()
            return self._locks[entity_id]
    
    @contextmanager
    def lock_entity(self, entity_id: uuid.UUID, lock_type: LockType = LockType.READ, 
                   timeout: Optional[float] = None):
        """
        Context manager for entity-level locking.
        
        Args:
            entity_id: UUID of the entity to lock
            lock_type: Type of lock (READ or WRITE)
            timeout: Timeout for lock acquisition (uses default if None)
            
        Yields:
            LockInfo: Information about the acquired lock
            
        Raises:
            TimeoutError: If lock cannot be acquired within timeout
        """
        timeout = timeout or self.default_timeout
        entity_lock = self._get_entity_lock(entity_id)
        lock_info = LockInfo(
            entity_id=entity_id,
            lock_type=lock_type,
            thread_id=threading.get_ident(),
            timeout=timeout
        )
        
        acquired = False
        start_time = time.time()
        
        try:
            # Try to acquire the lock
            while time.time() - start_time < timeout:
                if self._try_acquire_lock(entity_id, lock_info):
                    acquired = True
                    break
                time.sleep(0.01)  # Small delay before retry
            
            if not acquired:
                self._lock_stats["lock_timeouts"] += 1
                raise TimeoutError(f"Could not acquire {lock_type.value} lock for entity {entity_id} within {timeout} seconds")
            
            self._lock_stats["total_locks_acquired"] += 1
            logger.debug(f"Acquired {lock_type.value} lock for entity {entity_id}")
            
            yield lock_info
            
        finally:
            if acquired:
                self._release_lock(entity_id, lock_info)
                self._lock_stats["total_locks_released"] += 1
                logger.debug(f"Released {lock_type.value} lock for entity {entity_id}")
    
    def _try_acquire_lock(self, entity_id: uuid.UUID, lock_info: LockInfo) -> bool:
        """
        Try to acquire a lock for an entity.
        
        Args:
            entity_id: UUID of the entity
            lock_info: Information about the lock to acquire
            
        Returns:
            True if lock was acquired, False otherwise
        """
        with self._global_lock:
            active_locks = self._active_locks.get(entity_id, set())
            
            # Check if we can acquire the lock
            if lock_info.lock_type == LockType.READ:
                # Can acquire read lock if no write locks exist
                write_locks = [l for l in active_locks if l.lock_type == LockType.WRITE]
                if not write_locks:
                    active_locks.add(lock_info)
                    return True
            else:  # WRITE lock
                # Can acquire write lock only if no other locks exist
                if not active_locks:
                    active_locks.add(lock_info)
                    return True
            
            return False
    
    def _release_lock(self, entity_id: uuid.UUID, lock_info: LockInfo):
        """Release a lock for an entity."""
        with self._global_lock:
            active_locks = self._active_locks.get(entity_id, set())
            active_locks.discard(lock_info)
            
            # Clean up empty lock sets
            if not active_locks and entity_id in self._active_locks:
                del self._active_locks[entity_id]
            
            # Clean up unused locks (optional optimization)
            if entity_id in self._locks and not active_locks:
                del self._locks[entity_id]
    
    def get_lock_info(self, entity_id: uuid.UUID) -> Dict[str, any]:
        """
        Get information about locks for a specific entity.
        
        Args:
            entity_id: UUID of the entity
            
        Returns:
            Dictionary with lock information
        """
        with self._global_lock:
            active_locks = self._active_locks.get(entity_id, set())
            
            return {
                "entity_id": str(entity_id),
                "active_locks": len(active_locks),
                "read_locks": len([l for l in active_locks if l.lock_type == LockType.READ]),
                "write_locks": len([l for l in active_locks if l.lock_type == LockType.WRITE]),
                "locks": [
                    {
                        "lock_id": lock.lock_id,
                        "lock_type": lock.lock_type.value,
                        "thread_id": lock.thread_id,
                        "acquired_at": lock.acquired_at
                    }
                    for lock in active_locks
                ]
            }
    
    def get_lock_stats(self) -> Dict[str, any]:
        """Get overall lock manager statistics."""
        with self._global_lock:
            return {
                **self._lock_stats,
                "active_entity_locks": len(self._active_locks),
                "total_active_locks": sum(len(locks) for locks in self._active_locks.values())
            }
    
    def force_release_all_locks(self, entity_id: Optional[uuid.UUID] = None):
        """
        Force release all locks (emergency use only).
        
        Args:
            entity_id: If provided, only release locks for this entity
        """
        with self._global_lock:
            if entity_id:
                if entity_id in self._active_locks:
                    lock_count = len(self._active_locks[entity_id])
                    del self._active_locks[entity_id]
                    logger.warning(f"Force released {lock_count} locks for entity {entity_id}")
            else:
                total_locks = sum(len(locks) for locks in self._active_locks.values())
                self._active_locks.clear()
                self._locks.clear()
                logger.warning(f"Force released all {total_locks} locks")


# Global lock manager instance
_lock_manager: Optional[LockManager] = None


def get_lock_manager(default_timeout: float = 30.0) -> LockManager:
    """Get the global lock manager instance."""
    global _lock_manager
    if _lock_manager is None:
        _lock_manager = LockManager(default_timeout)
    return _lock_manager


def reset_lock_manager():
    """Reset the global lock manager (for testing)."""
    global _lock_manager
    _lock_manager = None