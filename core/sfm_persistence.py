"""
SFM Graph Persistence Manager

This module provides comprehensive persistence capabilities for Social Fabric Matrix (SFM) graphs,
enabling offline storage, loading, and state management of in-memory graph data.

Key Features:
- Multiple storage formats (JSON, Pickle, NetworkX formats)
- Incremental updates and change tracking
- Version management and rollback capabilities
- Data validation and integrity checking
- Compression and optimization for large graphs
- Backup and recovery mechanisms
- Thread-safe operations for concurrent access
- Automatic serialization of complex data types

Usage Examples:

Basic Usage:
```python
from core.sfm_persistence import SFMPersistenceManager
from core.sfm_models import SFMGraph

manager = SFMPersistenceManager("./data/sfm_graphs")
graph = manager.load_graph("my_graph")
# ... modify graph ...
manager.save_graph("my_graph", graph)
```

Advanced Usage:
```python
# Enable versioning and compression
manager = SFMPersistenceManager(
    base_path="./data", 
    enable_versioning=True, 
    compression=True
)

# Save with metadata
manager.save_graph("policy_analysis", graph, 
                  metadata={"author": "analyst", "purpose": "scenario_modeling"})

# Load specific version
graph_v2 = manager.load_graph("policy_analysis", version=2)

# Get change history
history = manager.get_version_history("policy_analysis")
```
"""

import os
import json
import pickle
import gzip
import shutil
import threading
import uuid
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from contextlib import contextmanager

# Core SFM imports
from core.sfm_models import (
    SFMGraph, Node, Relationship, Actor, Institution, Resource, 
    Process, Flow, Policy, BeliefSystem, TechnologySystem, 
    Indicator, FeedbackLoop, AnalyticalContext, SystemProperty
)
from core.sfm_enums import RelationshipKind, ResourceType, FlowNature
from db.sfm_dao import SFMRepository, NetworkXSFMRepository

# Setup logging
logger = logging.getLogger(__name__)


class StorageFormat(Enum):
    """Supported storage formats for SFM graphs."""
    JSON = "json"
    PICKLE = "pickle" 
    COMPRESSED_JSON = "json.gz"
    COMPRESSED_PICKLE = "pickle.gz"


class VersioningStrategy(Enum):
    """Versioning strategies for graph storage."""
    NONE = "none"          # No versioning
    INCREMENTAL = "incremental"  # Keep all versions
    ROLLING = "rolling"    # Keep only N recent versions
    SNAPSHOT = "snapshot"  # Periodic snapshots only


@dataclass
class GraphMetadata:
    """Metadata associated with stored graphs."""
    graph_id: str
    name: str
    description: str = ""
    version: int = 1
    created_at: datetime = None
    modified_at: datetime = None
    author: str = ""
    tags: List[str] = None
    size_bytes: int = 0
    node_count: int = 0
    relationship_count: int = 0
    checksum: str = ""
    format: StorageFormat = StorageFormat.JSON
    compression_ratio: Optional[float] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.tags is None:
            self.tags = []


@dataclass
class PersistenceConfig:
    """Configuration for persistence manager."""
    base_path: str = "./sfm_data"
    default_format: StorageFormat = StorageFormat.JSON
    enable_compression: bool = False
    enable_versioning: bool = True
    versioning_strategy: VersioningStrategy = VersioningStrategy.INCREMENTAL
    max_versions: int = 10
    enable_backup: bool = True
    backup_interval_hours: int = 24
    validate_on_load: bool = True
    validate_on_save: bool = True
    thread_safe: bool = True
    auto_create_directories: bool = True


class SFMSerializationError(Exception):
    """Errors related to graph serialization/deserialization."""
    pass


class SFMPersistenceError(Exception):
    """General persistence-related errors."""
    pass


class SFMGraphSerializer:
    """Handles serialization and deserialization of SFM graphs."""
    
    @staticmethod
    def serialize_graph(graph: SFMGraph, format: StorageFormat = StorageFormat.JSON) -> bytes:
        """Serialize an SFM graph to bytes."""
        try:
            if format in [StorageFormat.JSON, StorageFormat.COMPRESSED_JSON]:
                data = SFMGraphSerializer._graph_to_dict(graph)
                json_str = json.dumps(data, indent=2, default=SFMGraphSerializer._json_serializer)
                json_bytes = json_str.encode('utf-8')
                
                if format == StorageFormat.COMPRESSED_JSON:
                    return gzip.compress(json_bytes)
                return json_bytes
                
            elif format in [StorageFormat.PICKLE, StorageFormat.COMPRESSED_PICKLE]:
                pickle_bytes = pickle.dumps(graph)
                
                if format == StorageFormat.COMPRESSED_PICKLE:
                    return gzip.compress(pickle_bytes)
                return pickle_bytes
                
            else:
                raise SFMSerializationError(f"Unsupported format: {format}")
                
        except Exception as e:
            raise SFMSerializationError(f"Failed to serialize graph: {str(e)}")
    
    @staticmethod
    def deserialize_graph(data: bytes, format: StorageFormat = StorageFormat.JSON) -> SFMGraph:
        """Deserialize bytes to an SFM graph."""
        try:
            if format in [StorageFormat.COMPRESSED_JSON, StorageFormat.COMPRESSED_PICKLE]:
                data = gzip.decompress(data)
            
            if format in [StorageFormat.JSON, StorageFormat.COMPRESSED_JSON]:
                json_str = data.decode('utf-8')
                dict_data = json.loads(json_str)
                return SFMGraphSerializer._dict_to_graph(dict_data)
                
            elif format in [StorageFormat.PICKLE, StorageFormat.COMPRESSED_PICKLE]:
                return pickle.loads(data)
                
            else:
                raise SFMSerializationError(f"Unsupported format: {format}")
                
        except Exception as e:
            raise SFMSerializationError(f"Failed to deserialize graph: {str(e)}")
    
    @staticmethod
    def _graph_to_dict(graph: SFMGraph) -> Dict[str, Any]:
        """Convert SFMGraph to dictionary representation."""
        return {
            'id': str(graph.id),
            'name': graph.name,
            'description': graph.description,
            'actors': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.actors.items()},
            'institutions': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.institutions.items()},
            'resources': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.resources.items()},
            'processes': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.processes.items()},
            'flows': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.flows.items()},
            'policies': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.policies.items()},
            'belief_systems': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.belief_systems.items()},
            'technology_systems': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.technology_systems.items()},
            'indicators': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.indicators.items()},
            'feedback_loops': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.feedback_loops.items()},
            'system_properties': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.system_properties.items()},
            'analytical_contexts': {str(k): SFMGraphSerializer._node_to_dict(v) for k, v in graph.analytical_contexts.items()},
            'relationships': {str(k): SFMGraphSerializer._relationship_to_dict(v) for k, v in graph.relationships.items()},
            'metadata': {
                'serialization_timestamp': datetime.now().isoformat(),
                'serialization_version': '1.0'
            }
        }
    
    @staticmethod
    def _dict_to_graph(data: Dict[str, Any]) -> SFMGraph:
        """Convert dictionary representation back to SFMGraph."""
        graph = SFMGraph(
            id=uuid.UUID(data['id']),
            name=data['name'],
            description=data.get('description', '')
        )
        
        # Deserialize nodes
        for actor_data in data.get('actors', {}).values():
            actor = SFMGraphSerializer._dict_to_node(actor_data, Actor)
            graph.actors[actor.id] = actor
            
        for inst_data in data.get('institutions', {}).values():
            institution = SFMGraphSerializer._dict_to_node(inst_data, Institution)
            graph.institutions[institution.id] = institution
            
        for res_data in data.get('resources', {}).values():
            resource = SFMGraphSerializer._dict_to_node(res_data, Resource)
            graph.resources[resource.id] = resource
            
        for proc_data in data.get('processes', {}).values():
            process = SFMGraphSerializer._dict_to_node(proc_data, Process)
            graph.processes[process.id] = process
        
        for flow_data in data.get('flows', {}).values():
            flow = SFMGraphSerializer._dict_to_node(flow_data, Flow)
            graph.flows[flow.id] = flow
            
        for policy_data in data.get('policies', {}).values():
            policy = SFMGraphSerializer._dict_to_node(policy_data, Policy)
            graph.policies[policy.id] = policy
        
        # Handle other node types...
        for bs_data in data.get('belief_systems', {}).values():
            belief_system = SFMGraphSerializer._dict_to_node(bs_data, BeliefSystem)
            graph.belief_systems[belief_system.id] = belief_system
            
        for ts_data in data.get('technology_systems', {}).values():
            tech_system = SFMGraphSerializer._dict_to_node(ts_data, TechnologySystem)
            graph.technology_systems[tech_system.id] = tech_system
            
        for ind_data in data.get('indicators', {}).values():
            indicator = SFMGraphSerializer._dict_to_node(ind_data, Indicator)
            graph.indicators[indicator.id] = indicator
            
        for fl_data in data.get('feedback_loops', {}).values():
            feedback_loop = SFMGraphSerializer._dict_to_node(fl_data, FeedbackLoop)
            graph.feedback_loops[feedback_loop.id] = feedback_loop
            
        for sp_data in data.get('system_properties', {}).values():
            system_prop = SFMGraphSerializer._dict_to_node(sp_data, SystemProperty)
            graph.system_properties[system_prop.id] = system_prop
            
        for ac_data in data.get('analytical_contexts', {}).values():
            analytical_context = SFMGraphSerializer._dict_to_node(ac_data, AnalyticalContext)
            graph.analytical_contexts[analytical_context.id] = analytical_context
        
        # Deserialize relationships
        for rel_data in data.get('relationships', {}).values():
            relationship = SFMGraphSerializer._dict_to_relationship(rel_data)
            graph.relationships[relationship.id] = relationship
            
        return graph
    
    @staticmethod
    def _node_to_dict(node: Node) -> Dict[str, Any]:
        """Convert a Node to dictionary representation."""
        result = {
            'type': type(node).__name__,
            'id': str(node.id),
            'label': node.label,
            'description': node.description,
            'meta': node.meta,
            'version': getattr(node, 'version', 1),
            'created_at': getattr(node, 'created_at', datetime.now()).isoformat(),
            'modified_at': getattr(node, 'modified_at', None).isoformat() if getattr(node, 'modified_at', None) else None,
            'certainty': getattr(node, 'certainty', 1.0)
        }
        
        # Add type-specific fields
        if isinstance(node, Actor):
            result.update({
                'legal_form': node.legal_form,
                'sector': node.sector,
                'power_resources': getattr(node, 'power_resources', {}),
                'decision_making_capacity': getattr(node, 'decision_making_capacity', None)
            })
        elif isinstance(node, Institution):
            result.update({
                'layer': node.layer.name if node.layer else None,
                'formal_rules': getattr(node, 'formal_rules', []),
                'informal_norms': getattr(node, 'informal_norms', [])
            })
        elif isinstance(node, Resource):
            result.update({
                'rtype': node.rtype.name if node.rtype else None,
                'unit': node.unit
            })
        elif isinstance(node, Policy):
            result.update({
                'authority': node.authority,
                'enforcement': node.enforcement,
                'target_sectors': getattr(node, 'target_sectors', [])
            })
        elif isinstance(node, Flow):
            result.update({
                'nature': node.nature.name if node.nature else None,
                'quantity': node.quantity,
                'unit': node.unit,
                'flow_type': getattr(node, 'flow_type', ''),
                'source_process_id': str(node.source_process_id) if getattr(node, 'source_process_id', None) else None,
                'target_process_id': str(node.target_process_id) if getattr(node, 'target_process_id', None) else None
            })
        # Add other node types as needed...
        
        return result
    
    @staticmethod
    def _dict_to_node(data: Dict[str, Any], node_class: type) -> Node:
        """Convert dictionary representation back to Node."""
        # Create basic node with common fields
        node_kwargs = {
            'id': uuid.UUID(data['id']),
            'label': data['label'],
            'description': data.get('description'),
            'meta': data.get('meta', {}),
        }
        
        # Add type-specific fields
        if node_class == Actor:
            node_kwargs.update({
                'legal_form': data.get('legal_form'),
                'sector': data.get('sector')
            })
        elif node_class == Institution:
            from core.sfm_enums import InstitutionLayer
            layer_name = data.get('layer')
            node_kwargs['layer'] = InstitutionLayer[layer_name] if layer_name else None
            
        elif node_class == Resource:
            rtype_name = data.get('rtype')
            node_kwargs.update({
                'rtype': ResourceType[rtype_name] if rtype_name else ResourceType.NATURAL,
                'unit': data.get('unit')
            })
        elif node_class == Policy:
            node_kwargs.update({
                'authority': data.get('authority'),
                'enforcement': data.get('enforcement', 0.0),
            })
        elif node_class == Flow:
            nature_name = data.get('nature')
            node_kwargs.update({
                'nature': FlowNature[nature_name] if nature_name else FlowNature.TRANSFER,
                'quantity': data.get('quantity'),
                'unit': data.get('unit')
            })
        # Add other node types as needed...
        
        return node_class(**node_kwargs)
    
    @staticmethod
    def _relationship_to_dict(rel: Relationship) -> Dict[str, Any]:
        """Convert Relationship to dictionary representation."""
        return {
            'id': str(rel.id),
            'source_id': str(rel.source_id),
            'target_id': str(rel.target_id),
            'kind': rel.kind.name,
            'weight': rel.weight,
            'meta': getattr(rel, 'meta', {}),
            'certainty': getattr(rel, 'certainty', 1.0),
            'created_at': getattr(rel, 'created_at', datetime.now()).isoformat(),
            'modified_at': getattr(rel, 'modified_at', None).isoformat() if getattr(rel, 'modified_at', None) else None,
        }
    
    @staticmethod
    def _dict_to_relationship(data: Dict[str, Any]) -> Relationship:
        """Convert dictionary representation back to Relationship."""
        return Relationship(
            id=uuid.UUID(data['id']),
            source_id=uuid.UUID(data['source_id']),
            target_id=uuid.UUID(data['target_id']),
            kind=RelationshipKind[data['kind']],
            weight=data.get('weight', 1.0),
            meta=data.get('meta', {}),
            certainty=data.get('certainty', 1.0)
        )
    
    @staticmethod
    def _json_serializer(obj):
        """Custom JSON serializer for complex types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class SFMPersistenceManager:
    """
    Comprehensive persistence manager for SFM graphs.
    
    Provides offline storage, loading, versioning, and state management
    capabilities for in-memory SFM graph data.
    """
    
    def __init__(self, config: Union[PersistenceConfig, str, None] = None):
        """
        Initialize the persistence manager.
        
        Args:
            config: Configuration object, path string, or None for defaults
        """
        if isinstance(config, str):
            self.config = PersistenceConfig(base_path=config)
        elif config is None:
            self.config = PersistenceConfig()
        else:
            self.config = config
            
        self.base_path = Path(self.config.base_path)
        self.graphs_path = self.base_path / "graphs"
        self.metadata_path = self.base_path / "metadata"
        self.backups_path = self.base_path / "backups"
        self.versions_path = self.base_path / "versions"
        
        # Thread safety
        self._lock = threading.RLock() if self.config.thread_safe else None
        
        # Initialize storage directories
        if self.config.auto_create_directories:
            self._initialize_directories()
        
        # Cache for loaded metadata
        self._metadata_cache: Dict[str, GraphMetadata] = {}
        self._cache_dirty = True
        
        logger.info(f"SFM Persistence Manager initialized at: {self.base_path}")
    
    def _initialize_directories(self):
        """Create necessary directory structure."""
        for path in [self.base_path, self.graphs_path, self.metadata_path, 
                     self.backups_path, self.versions_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _thread_safe(self):
        """Context manager for thread-safe operations."""
        if self._lock:
            with self._lock:
                yield
        else:
            yield
    
    def save_graph(self, 
                   graph_id: str, 
                   graph: SFMGraph, 
                   metadata: Optional[Dict[str, Any]] = None,
                   format: Optional[StorageFormat] = None) -> GraphMetadata:
        """
        Save an SFM graph to persistent storage.
        
        Args:
            graph_id: Unique identifier for the graph
            graph: SFMGraph instance to save
            metadata: Optional metadata dictionary
            format: Storage format (defaults to config default)
            
        Returns:
            GraphMetadata for the saved graph
        """
        with self._thread_safe():
            try:
                format = format or self.config.default_format
                
                # Validate graph if enabled
                if self.config.validate_on_save:
                    self._validate_graph(graph)
                
                # Handle versioning
                current_metadata = self._get_metadata(graph_id)
                version = (current_metadata.version + 1) if current_metadata else 1
                
                if self.config.enable_versioning and current_metadata:
                    self._archive_version(graph_id, current_metadata)
                
                # Serialize graph
                serialized_data = SFMGraphSerializer.serialize_graph(graph, format)
                
                # Calculate checksum
                checksum = hashlib.sha256(serialized_data).hexdigest()
                
                # Prepare metadata
                new_metadata = GraphMetadata(
                    graph_id=graph_id,
                    name=graph.name or graph_id,
                    description=graph.description or "",
                    version=version,
                    created_at=current_metadata.created_at if current_metadata else datetime.now(),
                    modified_at=datetime.now(),
                    author=metadata.get('author', '') if metadata else '',
                    tags=metadata.get('tags', []) if metadata else [],
                    size_bytes=len(serialized_data),
                    node_count=self._count_nodes(graph),
                    relationship_count=len(graph.relationships),
                    checksum=checksum,
                    format=format
                )
                
                # Add custom metadata fields
                if metadata:
                    for key, value in metadata.items():
                        if not hasattr(new_metadata, key):
                            setattr(new_metadata, key, value)
                
                # Save graph data
                graph_file = self._get_graph_file_path(graph_id, format)
                graph_file.write_bytes(serialized_data)
                
                # Save metadata
                self._save_metadata(graph_id, new_metadata)
                
                # Update cache
                self._metadata_cache[graph_id] = new_metadata
                
                logger.info(f"Graph '{graph_id}' saved successfully (version {version})")
                return new_metadata
                
            except Exception as e:
                logger.error(f"Failed to save graph '{graph_id}': {str(e)}")
                raise SFMPersistenceError(f"Failed to save graph: {str(e)}")
    
    def load_graph(self, 
                   graph_id: str, 
                   version: Optional[int] = None) -> Optional[SFMGraph]:
        """
        Load an SFM graph from persistent storage.
        
        Args:
            graph_id: Unique identifier for the graph
            version: Specific version to load (latest if None)
            
        Returns:
            SFMGraph instance or None if not found
        """
        with self._thread_safe():
            try:
                # Get metadata
                metadata = self._get_metadata(graph_id, version)
                if not metadata:
                    logger.warning(f"Graph '{graph_id}' not found")
                    return None
                
                # Determine file path
                if version and version != metadata.version:
                    graph_file = self._get_version_file_path(graph_id, version, metadata.format)
                else:
                    graph_file = self._get_graph_file_path(graph_id, metadata.format)
                
                if not graph_file.exists():
                    logger.error(f"Graph file not found: {graph_file}")
                    return None
                
                # Load and deserialize
                serialized_data = graph_file.read_bytes()
                
                # Verify checksum if available
                if metadata.checksum:
                    actual_checksum = hashlib.sha256(serialized_data).hexdigest()
                    if actual_checksum != metadata.checksum:
                        logger.warning(f"Checksum mismatch for graph '{graph_id}'. Data may be corrupted.")
                
                graph = SFMGraphSerializer.deserialize_graph(serialized_data, metadata.format)
                
                # Validate graph if enabled
                if self.config.validate_on_load:
                    self._validate_graph(graph)
                
                logger.info(f"Graph '{graph_id}' loaded successfully (version {metadata.version})")
                return graph
                
            except Exception as e:
                logger.error(f"Failed to load graph '{graph_id}': {str(e)}")
                raise SFMPersistenceError(f"Failed to load graph: {str(e)}")
    
    def update_graph(self, 
                     graph_id: str, 
                     graph: SFMGraph, 
                     update_metadata: Optional[Dict[str, Any]] = None) -> GraphMetadata:
        """
        Update an existing graph.
        
        Args:
            graph_id: Unique identifier for the graph
            graph: Updated SFMGraph instance
            update_metadata: Optional metadata updates
            
        Returns:
            Updated GraphMetadata
        """
        return self.save_graph(graph_id, graph, update_metadata)
    
    def delete_graph(self, graph_id: str, include_versions: bool = True) -> bool:
        """
        Delete a graph and optionally its versions.
        
        Args:
            graph_id: Unique identifier for the graph  
            include_versions: Whether to delete all versions
            
        Returns:
            True if successful, False otherwise
        """
        with self._thread_safe():
            try:
                metadata = self._get_metadata(graph_id)
                if not metadata:
                    return False
                
                # Delete main graph file
                graph_file = self._get_graph_file_path(graph_id, metadata.format)
                if graph_file.exists():
                    graph_file.unlink()
                
                # Delete metadata
                metadata_file = self.metadata_path / f"{graph_id}.json"
                if metadata_file.exists():
                    metadata_file.unlink()
                
                # Delete versions if requested
                if include_versions:
                    version_dir = self.versions_path / graph_id
                    if version_dir.exists():
                        shutil.rmtree(version_dir)
                
                # Remove from cache
                self._metadata_cache.pop(graph_id, None)
                
                logger.info(f"Graph '{graph_id}' deleted successfully")
                return True
                
            except Exception as e:
                logger.error(f"Failed to delete graph '{graph_id}': {str(e)}")
                return False
    
    def list_graphs(self, include_metadata: bool = True) -> List[Union[str, GraphMetadata]]:
        """
        List all stored graphs.
        
        Args:
            include_metadata: Whether to return metadata objects or just IDs
            
        Returns:
            List of graph IDs or GraphMetadata objects
        """
        with self._thread_safe():
            try:
                if not self.metadata_path.exists():
                    return []
                
                graph_ids = []
                for metadata_file in self.metadata_path.glob("*.json"):
                    graph_id = metadata_file.stem
                    graph_ids.append(graph_id)
                
                if not include_metadata:
                    return graph_ids
                
                # Load metadata for each graph
                result = []
                for graph_id in graph_ids:
                    metadata = self._get_metadata(graph_id)
                    if metadata:
                        result.append(metadata)
                
                return result
                
            except Exception as e:
                logger.error(f"Failed to list graphs: {str(e)}")
                return []
    
    def get_graph_metadata(self, graph_id: str) -> Optional[GraphMetadata]:
        """Get metadata for a specific graph."""
        return self._get_metadata(graph_id)
    
    def get_version_history(self, graph_id: str) -> List[Dict[str, Any]]:
        """
        Get version history for a graph.
        
        Args:
            graph_id: Unique identifier for the graph
            
        Returns:
            List of version information dictionaries
        """
        with self._thread_safe():
            try:
                version_dir = self.versions_path / graph_id
                if not version_dir.exists():
                    return []
                
                versions = []
                for version_file in version_dir.glob("v*.json"):
                    try:
                        version_data = json.loads(version_file.read_text())
                        versions.append(version_data)
                    except Exception as e:
                        logger.warning(f"Failed to read version file {version_file}: {str(e)}")
                
                # Sort by version number
                versions.sort(key=lambda x: x.get('version', 0))
                return versions
                
            except Exception as e:
                logger.error(f"Failed to get version history for '{graph_id}': {str(e)}")
                return []
    
    def create_backup(self, graph_id: str, backup_name: Optional[str] = None) -> str:
        """
        Create a backup of a specific graph.
        
        Args:
            graph_id: Unique identifier for the graph
            backup_name: Optional custom backup name
            
        Returns:
            Backup file path
        """
        with self._thread_safe():
            try:
                metadata = self._get_metadata(graph_id)
                if not metadata:
                    raise SFMPersistenceError(f"Graph '{graph_id}' not found")
                
                # Create backup name
                if not backup_name:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{graph_id}_{timestamp}"
                
                # Load graph
                graph = self.load_graph(graph_id)
                if not graph:
                    raise SFMPersistenceError(f"Failed to load graph for backup")
                
                # Save backup
                backup_path = self.backups_path / f"{backup_name}.backup"
                backup_data = {
                    'graph': SFMGraphSerializer._graph_to_dict(graph),
                    'metadata': asdict(metadata),
                    'backup_timestamp': datetime.now().isoformat(),
                    'original_graph_id': graph_id
                }
                
                backup_path.write_text(json.dumps(backup_data, indent=2, default=SFMGraphSerializer._json_serializer))
                
                logger.info(f"Backup created: {backup_path}")
                return str(backup_path)
                
            except Exception as e:
                logger.error(f"Failed to create backup for '{graph_id}': {str(e)}")
                raise SFMPersistenceError(f"Failed to create backup: {str(e)}")
    
    def restore_from_backup(self, backup_path: str, new_graph_id: Optional[str] = None) -> str:
        """
        Restore a graph from backup.
        
        Args:
            backup_path: Path to backup file
            new_graph_id: Optional new graph ID (uses original if None)
            
        Returns:
            Restored graph ID
        """
        with self._thread_safe():
            try:
                backup_file = Path(backup_path)
                if not backup_file.exists():
                    raise SFMPersistenceError(f"Backup file not found: {backup_path}")
                
                # Load backup data
                backup_data = json.loads(backup_file.read_text())
                graph = SFMGraphSerializer._dict_to_graph(backup_data['graph'])
                
                # Determine graph ID
                graph_id = new_graph_id or backup_data['original_graph_id']
                
                # Save restored graph
                metadata = self.save_graph(graph_id, graph)
                
                logger.info(f"Graph restored from backup: {graph_id}")
                return graph_id
                
            except Exception as e:
                logger.error(f"Failed to restore from backup '{backup_path}': {str(e)}")
                raise SFMPersistenceError(f"Failed to restore from backup: {str(e)}")
    
    def cleanup_old_versions(self, graph_id: str, keep_versions: Optional[int] = None) -> int:
        """
        Clean up old versions of a graph.
        
        Args:
            graph_id: Unique identifier for the graph
            keep_versions: Number of versions to keep (uses config if None)
            
        Returns:
            Number of versions removed
        """
        with self._thread_safe():
            try:
                keep_versions = keep_versions or self.config.max_versions
                version_dir = self.versions_path / graph_id
                
                if not version_dir.exists():
                    return 0
                
                # Get all version files
                version_files = list(version_dir.glob("v*.json"))
                if len(version_files) <= keep_versions:
                    return 0
                
                # Sort by version number and remove oldest
                version_files.sort(key=lambda x: int(x.stem[1:]))  # Remove 'v' prefix
                files_to_remove = version_files[:-keep_versions]
                
                removed_count = 0
                for file_path in files_to_remove:
                    try:
                        file_path.unlink()
                        # Also remove corresponding data file
                        data_file = version_dir / f"{file_path.stem}.data"
                        if data_file.exists():
                            data_file.unlink()
                        removed_count += 1
                    except Exception as e:
                        logger.warning(f"Failed to remove version file {file_path}: {str(e)}")
                
                logger.info(f"Cleaned up {removed_count} old versions for graph '{graph_id}'")
                return removed_count
                
            except Exception as e:
                logger.error(f"Failed to cleanup versions for '{graph_id}': {str(e)}")
                return 0
    
    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        with self._thread_safe():
            try:
                stats = {
                    'total_graphs': 0,
                    'total_size_bytes': 0,
                    'total_versions': 0,
                    'total_backups': 0,
                    'format_distribution': {},
                    'largest_graph': None,
                    'oldest_graph': None,
                    'newest_graph': None
                }
                
                graphs = self.list_graphs(include_metadata=True)
                stats['total_graphs'] = len(graphs)
                
                largest_size = 0
                oldest_date = None
                newest_date = None
                
                for metadata in graphs:
                    if isinstance(metadata, GraphMetadata):
                        stats['total_size_bytes'] += metadata.size_bytes
                        
                        # Format distribution
                        format_name = metadata.format.value
                        stats['format_distribution'][format_name] = stats['format_distribution'].get(format_name, 0) + 1
                        
                        # Largest graph
                        if metadata.size_bytes > largest_size:
                            largest_size = metadata.size_bytes
                            stats['largest_graph'] = metadata.graph_id
                        
                        # Date tracking
                        if oldest_date is None or metadata.created_at < oldest_date:
                            oldest_date = metadata.created_at
                            stats['oldest_graph'] = metadata.graph_id
                        
                        if newest_date is None or metadata.created_at > newest_date:
                            newest_date = metadata.created_at
                            stats['newest_graph'] = metadata.graph_id
                        
                        # Count versions
                        version_history = self.get_version_history(metadata.graph_id)
                        stats['total_versions'] += len(version_history)
                
                # Count backups
                if self.backups_path.exists():
                    stats['total_backups'] = len(list(self.backups_path.glob("*.backup")))
                
                return stats
                
            except Exception as e:
                logger.error(f"Failed to get storage statistics: {str(e)}")
                return {}
    
    # Private helper methods
    
    def _get_metadata(self, graph_id: str, version: Optional[int] = None) -> Optional[GraphMetadata]:
        """Load metadata for a graph."""
        try:
            # Check cache first
            if version is None and graph_id in self._metadata_cache:
                return self._metadata_cache[graph_id]
            
            if version:
                # Load version-specific metadata
                version_file = self.versions_path / graph_id / f"v{version}.json"
                if not version_file.exists():
                    return None
                metadata_data = json.loads(version_file.read_text())
            else:
                # Load current metadata
                metadata_file = self.metadata_path / f"{graph_id}.json"
                if not metadata_file.exists():
                    return None
                metadata_data = json.loads(metadata_file.read_text())
            
            # Convert back to GraphMetadata object
            metadata_data['created_at'] = datetime.fromisoformat(metadata_data['created_at'])
            if metadata_data.get('modified_at'):
                metadata_data['modified_at'] = datetime.fromisoformat(metadata_data['modified_at'])
            metadata_data['format'] = StorageFormat(metadata_data['format'])
            
            metadata = GraphMetadata(**metadata_data)
            
            # Cache current version
            if version is None:
                self._metadata_cache[graph_id] = metadata
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to load metadata for '{graph_id}': {str(e)}")
            return None
    
    def _save_metadata(self, graph_id: str, metadata: GraphMetadata):
        """Save metadata for a graph."""
        try:
            metadata_file = self.metadata_path / f"{graph_id}.json"
            metadata_dict = asdict(metadata)
            metadata_dict['format'] = metadata.format.value
            
            metadata_file.write_text(json.dumps(metadata_dict, indent=2, default=SFMGraphSerializer._json_serializer))
            
        except Exception as e:
            logger.error(f"Failed to save metadata for '{graph_id}': {str(e)}")
            raise
    
    def _archive_version(self, graph_id: str, metadata: GraphMetadata):
        """Archive current version before updating."""
        try:
            version_dir = self.versions_path / graph_id
            version_dir.mkdir(exist_ok=True)
            
            # Save version metadata
            version_file = version_dir / f"v{metadata.version}.json"
            metadata_dict = asdict(metadata)
            metadata_dict['format'] = metadata.format.value
            version_file.write_text(json.dumps(metadata_dict, indent=2, default=SFMGraphSerializer._json_serializer))
            
            # Copy current graph data
            current_graph_file = self._get_graph_file_path(graph_id, metadata.format)
            if current_graph_file.exists():
                version_data_file = version_dir / f"v{metadata.version}.data"
                shutil.copy2(current_graph_file, version_data_file)
            
        except Exception as e:
            logger.error(f"Failed to archive version for '{graph_id}': {str(e)}")
            raise
    
    def _get_graph_file_path(self, graph_id: str, format: StorageFormat) -> Path:
        """Get file path for graph data."""
        extension = {
            StorageFormat.JSON: ".json",
            StorageFormat.PICKLE: ".pkl",
            StorageFormat.COMPRESSED_JSON: ".json.gz",
            StorageFormat.COMPRESSED_PICKLE: ".pkl.gz"
        }[format]
        
        return self.graphs_path / f"{graph_id}{extension}"
    
    def _get_version_file_path(self, graph_id: str, version: int, format: StorageFormat) -> Path:
        """Get file path for versioned graph data."""
        return self.versions_path / graph_id / f"v{version}.data"
    
    def _validate_graph(self, graph: SFMGraph):
        """Validate graph integrity."""
        # Basic validation - can be extended
        if not graph.id:
            raise SFMSerializationError("Graph must have an ID")
        
        # Validate relationship references
        all_node_ids = set()
        for collection in [graph.actors, graph.institutions, graph.resources, 
                          graph.processes, graph.flows, graph.policies]:
            all_node_ids.update(collection.keys())
        
        for rel in graph.relationships.values():
            if rel.source_id not in all_node_ids:
                raise SFMSerializationError(f"Relationship {rel.id} references non-existent source node {rel.source_id}")
            if rel.target_id not in all_node_ids:
                raise SFMSerializationError(f"Relationship {rel.id} references non-existent target node {rel.target_id}")
    
    def _count_nodes(self, graph: SFMGraph) -> int:
        """Count total nodes in graph."""
        return (len(graph.actors) + len(graph.institutions) + len(graph.resources) + 
                len(graph.processes) + len(graph.flows) + len(graph.policies) +
                len(graph.belief_systems) + len(graph.technology_systems) + 
                len(graph.indicators) + len(graph.feedback_loops) + 
                len(graph.system_properties) + len(graph.analytical_contexts))


# Convenience functions for quick operations

def save_sfm_graph(graph_id: str, graph: SFMGraph, storage_path: str = "./sfm_data") -> GraphMetadata:
    """Quick save function for SFM graphs."""
    manager = SFMPersistenceManager(storage_path)
    return manager.save_graph(graph_id, graph)


def load_sfm_graph(graph_id: str, storage_path: str = "./sfm_data") -> Optional[SFMGraph]:
    """Quick load function for SFM graphs."""
    manager = SFMPersistenceManager(storage_path)
    return manager.load_graph(graph_id)


def list_sfm_graphs(storage_path: str = "./sfm_data") -> List[str]:
    """Quick list function for SFM graphs."""
    manager = SFMPersistenceManager(storage_path)
    return manager.list_graphs(include_metadata=False)
