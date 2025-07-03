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
"""

# Standard library imports
import gzip
import hashlib
import json
import logging
import pickle
import shutil
import threading
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Sequence, Mapping

# Local imports
from core.sfm_enums import FlowNature, RelationshipKind, ResourceType, InstitutionLayer
from core.sfm_models import (
    Actor, AnalyticalContext, BeliefSystem, FeedbackLoop, Flow, Indicator,
    Institution, Node, Policy, Process, Relationship, Resource, SFMGraph,
    SystemProperty, TechnologySystem,
)

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
    NONE = "none"
    INCREMENTAL = "incremental"
    ROLLING = "rolling"
    SNAPSHOT = "snapshot"


@dataclass
class GraphMetadata:
    """Metadata associated with stored graphs."""
    graph_id: str
    name: str
    description: str = ""
    version: int = 1
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    author: str = ""
    tags: Optional[List[str]] = None
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


class SFMPersistenceError(Exception):
    """General persistence-related errors."""


class NodeSerializer:
    """Handles serialization of individual nodes."""

    @staticmethod
    def node_to_dict(node: Node) -> Dict[str, Any]:
        """Convert a Node to dictionary representation."""
        result: Dict[str, Any] = {
            'type': type(node).__name__,
            'id': str(node.id),
            'label': node.label,
            'description': node.description,
            'meta': node.meta,
            'version': getattr(node, 'version', 1),
            'created_at': getattr(node, 'created_at', datetime.now()).isoformat(),
            'modified_at': NodeSerializer._serialize_datetime(
                getattr(node, 'modified_at', None)
            ),
            'certainty': getattr(node, 'certainty', 1.0)
        }

        # Add type-specific fields using strategy pattern
        NodeSerializer._add_type_specific_fields(node, result)
        return result

    @staticmethod
    def _serialize_datetime(dt: Optional[datetime]) -> Optional[str]:
        """Safely serialize datetime objects."""
        return dt.isoformat() if dt else None

    @staticmethod
    def _add_type_specific_fields(node: Node, result: Dict[str, Any]) -> None:
        """Add type-specific fields to node dictionary."""
        type_handlers: Dict[type, Any] = {
            Actor: NodeSerializer._handle_actor,
            Institution: NodeSerializer._handle_institution,
            Resource: NodeSerializer._handle_resource,
            Policy: NodeSerializer._handle_policy,
            Flow: NodeSerializer._handle_flow,
        }

        handler = type_handlers.get(type(node))
        if handler:
            handler(node, result)

    @staticmethod
    def _handle_actor(actor: Actor, result: Dict[str, Any]) -> None:
        """Handle Actor-specific fields."""
        result.update({
            'legal_form': actor.legal_form,
            'sector': actor.sector,
            'power_resources': getattr(actor, 'power_resources', {}),
            'decision_making_capacity': getattr(actor, 'decision_making_capacity', None)
        })

    @staticmethod
    def _handle_institution(institution: Institution, result: Dict[str, Any]) -> None:
        """Handle Institution-specific fields."""
        result.update({
            'layer': institution.layer.name if institution.layer else None,
            'formal_rules': getattr(institution, 'formal_rules', []),
            'informal_norms': getattr(institution, 'informal_norms', [])
        })

    @staticmethod
    def _handle_resource(resource: Resource, result: Dict[str, Any]) -> None:
        """Handle Resource-specific fields."""
        result.update({
            'rtype': resource.rtype.name if resource.rtype else None,
            'unit': resource.unit
        })

    @staticmethod
    def _handle_policy(policy: Policy, result: Dict[str, Any]) -> None:
        """Handle Policy-specific fields."""
        result.update({
            'authority': policy.authority,
            'enforcement': policy.enforcement,
            'target_sectors': getattr(policy, 'target_sectors', [])
        })

    @staticmethod
    def _handle_flow(flow: Flow, result: Dict[str, Any]) -> None:
        """Handle Flow-specific fields."""
        result.update({
            'nature': flow.nature.name if flow.nature else None,
            'quantity': flow.quantity,
            'unit': flow.unit,
            'flow_type': getattr(flow, 'flow_type', ''),
            'source_process_id': str(flow.source_process_id) if getattr(
                flow, 'source_process_id', None) else None,
            'target_process_id': str(flow.target_process_id) if getattr(
                flow, 'target_process_id', None) else None
        })

    @staticmethod
    def dict_to_node(data: Dict[str, Any], node_class: type) -> Node:
        """Convert dictionary representation back to Node."""
        try:
            # Create basic node with common fields
            node_kwargs: Dict[str, Any] = {
                'id': uuid.UUID(data['id']),
                'label': data['label'],
                'description': data.get('description'),
                'meta': data.get('meta', {}),
            }

            # Add type-specific fields using strategy pattern
            NodeSerializer._add_type_specific_kwargs(data, node_class, node_kwargs)
            return node_class(**node_kwargs)
        except Exception as e:
            logger.error("Failed to deserialize node: %s", str(e))
            raise SFMSerializationError(f"Failed to deserialize node: {str(e)}") from e

    @staticmethod
    def _add_type_specific_kwargs(data: Dict[str, Any], node_class: type,
                                  node_kwargs: Dict[str, Any]) -> None:
        """Add type-specific constructor arguments."""
        type_handlers: Dict[type, Any] = {
            Actor: NodeSerializer._add_actor_kwargs,
            Institution: NodeSerializer._add_institution_kwargs,
            Resource: NodeSerializer._add_resource_kwargs,
            Policy: NodeSerializer._add_policy_kwargs,
            Flow: NodeSerializer._add_flow_kwargs,
        }

        handler = type_handlers.get(node_class)
        if handler:
            handler(data, node_kwargs)

    @staticmethod
    def _add_actor_kwargs(data: Dict[str, Any], node_kwargs: Dict[str, Any]) -> None:
        """Add Actor-specific constructor arguments."""
        node_kwargs.update({
            'legal_form': data.get('legal_form'),
            'sector': data.get('sector')
        })

    @staticmethod
    def _add_institution_kwargs(data: Dict[str, Any], node_kwargs: Dict[str, Any]) -> None:
        """Add Institution-specific constructor arguments."""
        layer_name = data.get('layer')
        node_kwargs['layer'] = InstitutionLayer[layer_name] if layer_name else None

    @staticmethod
    def _add_resource_kwargs(data: Dict[str, Any], node_kwargs: Dict[str, Any]) -> None:
        """Add Resource-specific constructor arguments."""
        rtype_name = data.get('rtype')
        node_kwargs.update({
            'rtype': ResourceType[rtype_name] if rtype_name else ResourceType.NATURAL,
            'unit': data.get('unit')
        })

    @staticmethod
    def _add_policy_kwargs(data: Dict[str, Any], node_kwargs: Dict[str, Any]) -> None:
        """Add Policy-specific constructor arguments."""
        node_kwargs.update({
            'authority': data.get('authority'),
            'enforcement': data.get('enforcement', 0.0),
        })

    @staticmethod
    def _add_flow_kwargs(data: Dict[str, Any], node_kwargs: Dict[str, Any]) -> None:
        """Add Flow-specific constructor arguments."""
        nature_name = data.get('nature')
        node_kwargs.update({
            'nature': FlowNature[nature_name] if nature_name else FlowNature.TRANSFER,
            'quantity': data.get('quantity'),
            'unit': data.get('unit')
        })


class SFMGraphSerializer:
    """Handles serialization and deserialization of SFM graphs."""

    @staticmethod
    def serialize_graph(graph: SFMGraph,
                        format_type: StorageFormat = StorageFormat.JSON) -> bytes:
        """Serialize an SFM graph to bytes."""
        try:
            if format_type in [StorageFormat.JSON, StorageFormat.COMPRESSED_JSON]:
                return SFMGraphSerializer._serialize_json(graph, format_type)
            if format_type in [StorageFormat.PICKLE, StorageFormat.COMPRESSED_PICKLE]:
                return SFMGraphSerializer._serialize_pickle(graph, format_type)

            raise SFMSerializationError(f"Unsupported format: {format_type}")

        except Exception as e:
            raise SFMSerializationError(f"Failed to serialize graph: {str(e)}") from e

    @staticmethod
    def _serialize_json(graph: SFMGraph, format_type: StorageFormat) -> bytes:
        """Serialize graph to JSON format."""
        data = SFMGraphSerializer._graph_to_dict(graph)
        json_str = json.dumps(data, indent=2,
                              default=SFMGraphSerializer._json_serializer)
        json_bytes = json_str.encode('utf-8')

        if format_type == StorageFormat.COMPRESSED_JSON:
            return gzip.compress(json_bytes)
        return json_bytes

    @staticmethod
    def _serialize_pickle(graph: SFMGraph, format_type: StorageFormat) -> bytes:
        """Serialize graph to Pickle format."""
        if format_type == StorageFormat.COMPRESSED_PICKLE:
            return gzip.compress(pickle.dumps(graph, protocol=pickle.HIGHEST_PROTOCOL))
        return pickle.dumps(graph, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def deserialize_graph(data: bytes, format_type: StorageFormat = StorageFormat.JSON) -> SFMGraph:
        """Deserialize bytes to an SFM graph."""
        try:
            logger.debug("Deserializing graph with format '%s'. Data size: %d bytes",
                        format_type, len(data))

            if format_type in [StorageFormat.COMPRESSED_JSON, StorageFormat.COMPRESSED_PICKLE]:
                data = gzip.decompress(data)

            if format_type in [StorageFormat.JSON, StorageFormat.COMPRESSED_JSON]:
                dict_data = json.loads(data.decode('utf-8'))
                logger.debug("Deserialized JSON data: %s", dict_data)
                required_keys = ['id', 'name', 'description', 'relationships']
                missing_keys = [key for key in required_keys if key not in dict_data]
                if missing_keys:
                    logger.error("Missing required keys in graph data: %s", missing_keys)
                    raise ValueError(f"Missing required keys: {missing_keys}")
                return SFMGraphSerializer._dict_to_graph(dict_data)

            if format_type in [StorageFormat.PICKLE, StorageFormat.COMPRESSED_PICKLE]:
                deserialized_data = pickle.loads(data)
                logger.debug("Deserialized PICKLE data: %s", deserialized_data)
                return deserialized_data

            raise SFMSerializationError(f"Unsupported format: {format_type}")

        except Exception as e:
            logger.error("Failed to deserialize graph. Format: '%s', Error: %s",
                        format_type, str(e))
            raise SFMSerializationError(f"Failed to deserialize graph: {str(e)}") from e

    @staticmethod
    def _dict_to_graph(data: Dict[str, Any]) -> SFMGraph:
        """Convert dictionary representation back to SFMGraph."""
        try:
            logger.debug("Deserializing graph from dictionary: %s", data)

            # Validate dictionary keys
            required_keys = ['id', 'name', 'description']
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing required key '{key}' in graph data: {data}")

            logger.debug("Dictionary keys: %s", list(data.keys()))
            logger.debug("Dictionary content: %s", data)

            logger.debug("Graph ID: %s, Name: %s, Description: %s",
                        data['id'], data['name'], data.get('description', ''))

            graph = SFMGraph(
                id=uuid.UUID(data['id']),
                name=data['name'],
                description=data.get('description', '')
            )

            logger.debug("Graph initialized: %s", graph)

            # Deserialize node collections
            node_type_mapping: List[tuple[str, type, Mapping[Any, Node]]] = [
                ('actors', Actor, graph.actors),
                ('institutions', Institution, graph.institutions),
                ('resources', Resource, graph.resources),
                ('processes', Process, graph.processes),
                ('flows', Flow, graph.flows),
                ('policies', Policy, graph.policies),
                ('belief_systems', BeliefSystem, graph.belief_systems),
                ('technology_systems', TechnologySystem, graph.technology_systems),
                ('indicators', Indicator, graph.indicators),
                ('feedback_loops', FeedbackLoop, graph.feedback_loops),
                ('system_properties', SystemProperty, graph.system_properties),
                ('analytical_contexts', AnalyticalContext, graph.analytical_contexts),
            ]

            logger.debug("Node collections during deserialization: %s", node_type_mapping)

            for collection_name, node_class, target_collection in node_type_mapping:
                collection_data = data.get(collection_name, {})
                if not isinstance(collection_data, dict):
                    raise ValueError(f"Invalid data for collection '{collection_name}': "
                                   f"{collection_data}")
                for node_data in collection_data.values():
                    node: Node = NodeSerializer.dict_to_node(node_data, node_class)
                    target_collection[node.id] = node

            logger.debug("Node collections deserialized successfully.")

            # Deserialize relationships
            relationships_data = data.get('relationships', {})
            if not isinstance(relationships_data, dict):
                raise ValueError(f"Invalid data for relationships: {relationships_data}")

            logger.debug("Relationships during deserialization: %s", relationships_data)

            for rel_data in relationships_data.values():
                relationship = SFMGraphSerializer._dict_to_relationship(rel_data)
                graph.relationships[relationship.id] = relationship

            logger.debug("Relationships deserialized successfully.")

            return graph

        except Exception as e:
            logger.error("Failed to deserialize graph: %s", str(e))
            raise SFMSerializationError(f"Failed to deserialize graph: {str(e)}") from e

    @staticmethod
    def _dict_to_relationship(data: Dict[str, Any]) -> Relationship:
        """Convert dictionary representation back to Relationship."""
        try:
            logger.debug("Deserializing relationship data: %s", data)
            return Relationship(
                id=uuid.UUID(data['id']),
                source_id=uuid.UUID(data['source_id']),
                target_id=uuid.UUID(data['target_id']),
                kind=RelationshipKind[data['kind']],
                weight=data.get('weight', 1.0),
                meta=data.get('meta', {}),
                certainty=data.get('certainty', 1.0),
                modified_at=data.get('modified_at', None)  # Handle missing modified_at
            )
        except Exception as e:
            logger.error("Failed to deserialize relationship: %s", str(e))
            raise SFMSerializationError(f"Failed to deserialize relationship: {str(e)}") from e

    @staticmethod
    def _json_serializer(obj: Any) -> str:
        """Custom JSON serializer for complex types."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    @staticmethod
    def _graph_to_dict(graph: SFMGraph) -> Dict[str, Any]:
        """Convert SFMGraph to dictionary representation."""
        node_collections: List[tuple[str, Mapping[Any, Node]]] = [
            ('actors', graph.actors),
            ('institutions', graph.institutions),
            ('resources', graph.resources),
            ('processes', graph.processes),
            ('flows', graph.flows),
            ('policies', graph.policies),
            ('belief_systems', graph.belief_systems),
            ('technology_systems', graph.technology_systems),
            ('indicators', graph.indicators),
            ('feedback_loops', graph.feedback_loops),
            ('system_properties', graph.system_properties),
            ('analytical_contexts', graph.analytical_contexts),
        ]

        result: Dict[str, Any] = {
            'id': str(graph.id),
            'name': graph.name,
            'description': graph.description,
            'relationships': {
                str(k): SFMGraphSerializer._relationship_to_dict(v)
                for k, v in graph.relationships.items()
            },
            'metadata': {
                'serialization_timestamp': datetime.now().isoformat(),
                'serialization_version': '1.0'
            }
        }

        # Add node collections
        for collection_name, collection in node_collections:
            result[collection_name] = {
                str(k): NodeSerializer.node_to_dict(v)
                for k, v in collection.items()
            }

        logger.debug("Serialized graph dictionary: %s", result)
        return result

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
            'modified_at': rel.modified_at.isoformat() if rel.modified_at else None,
        }


class FileManager:
    """Handles file operations for persistence."""

    def __init__(self, config: PersistenceConfig):
        self.config = config
        self.base_path = Path(config.base_path)
        self.graphs_path = self.base_path / "graphs"
        self.metadata_path = self.base_path / "metadata"
        self.backups_path = self.base_path / "backups"
        self.versions_path = self.base_path / "versions"

    def initialize_directories(self):
        """Create necessary directory structure."""
        for path in [self.base_path, self.graphs_path, self.metadata_path,
                     self.backups_path, self.versions_path]:
            path.mkdir(parents=True, exist_ok=True)

    def get_graph_file_path(self, graph_id: str, format_type: StorageFormat) -> Path:
        """Get file path for graph data."""
        extension_mapping = {
            StorageFormat.JSON: ".json",
            StorageFormat.PICKLE: ".pkl",
            StorageFormat.COMPRESSED_JSON: ".json.gz",
            StorageFormat.COMPRESSED_PICKLE: ".pkl.gz"
        }
        extension = extension_mapping[format_type]
        return self.graphs_path / f"{graph_id}{extension}"

    def get_version_file_path(self, graph_id: str, version: int,
                              format_type: StorageFormat) -> Path:
        """Get file path for versioned graph data."""
        extension_mapping = {
            StorageFormat.JSON: ".json",
            StorageFormat.PICKLE: ".pkl",
            StorageFormat.COMPRESSED_JSON: ".json.gz",
            StorageFormat.COMPRESSED_PICKLE: ".pkl.gz"
        }
        extension = extension_mapping[format_type]
        return self.versions_path / graph_id / f"v{version}_data{extension}"

    def get_metadata_file_path(self, graph_id: str) -> Path:
        """Get file path for metadata."""
        return self.metadata_path / f"{graph_id}.json"


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
        self.config = self._initialize_config(config)
        self.file_manager = FileManager(self.config)
        self._lock = threading.RLock() if self.config.thread_safe else None
        self._metadata_cache: Dict[str, GraphMetadata] = {}
        self._cache_dirty = True

        if self.config.auto_create_directories:
            self.file_manager.initialize_directories()

        logger.info("SFM Persistence Manager initialized at: %s",
                    self.file_manager.base_path)

    def _initialize_config(self, config: Union[PersistenceConfig, str, None]
                           ) -> PersistenceConfig:
        """Initialize configuration from various input types."""
        if isinstance(config, str):
            return PersistenceConfig(base_path=config)
        if config is None:
            return PersistenceConfig()

        return config

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
                   format_type: Optional[StorageFormat] = None) -> GraphMetadata:
        """
        Save an SFM graph to persistent storage.

        Args:
            graph_id: Unique identifier for the graph
            graph: SFMGraph instance to save
            metadata: Optional metadata dictionary
            format_type: Storage format (defaults to config default)

        Returns:
            GraphMetadata for the saved graph
        """
        with self._thread_safe():
            try:
                format_type = format_type or self.config.default_format

                if self.config.validate_on_save:
                    self._validate_graph(graph)

                current_metadata = self._get_metadata(graph_id)
                version = (current_metadata.version + 1) if current_metadata else 1

                if self.config.enable_versioning and current_metadata:
                    self._archive_version(graph_id, current_metadata)

                serialized_data = SFMGraphSerializer.serialize_graph(graph, format_type)
                checksum = hashlib.sha256(serialized_data).hexdigest()

                new_metadata = self._create_metadata(
                    graph_id, graph, version, current_metadata,
                    metadata, serialized_data, checksum, format_type
                )

                self._save_graph_data(graph_id, serialized_data, format_type)
                self._save_metadata(graph_id, new_metadata)
                self._metadata_cache[graph_id] = new_metadata

                logger.info("Graph '%s' saved successfully (version %d)",
                            graph_id, version)
                return new_metadata

            except Exception as e:
                logger.error("Failed to save graph '%s': %s", graph_id, str(e))
                raise SFMPersistenceError(f"Failed to save graph: {str(e)}") from e

    def _create_metadata(self, graph_id: str, graph: SFMGraph, version: int,
                         current_metadata: Optional[GraphMetadata],
                         metadata: Optional[Dict[str, Any]], serialized_data: bytes,
                         checksum: str, format_type: StorageFormat) -> GraphMetadata:
        """Create metadata object for saved graph."""
        return GraphMetadata(
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
            format=format_type
        )

    def _save_graph_data(self, graph_id: str, serialized_data: bytes,
                         format_type: StorageFormat) -> None:
        """Save serialized graph data to file."""
        graph_file = self.file_manager.get_graph_file_path(graph_id, format_type)
        graph_file.write_bytes(serialized_data)

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
                latest_metadata = self._get_metadata(graph_id)
                if not latest_metadata:
                    logger.warning("Graph '%s' not found", graph_id)
                    return None

                metadata_to_load: Optional[GraphMetadata]
                graph_file: Path

                if version is None or version == latest_metadata.version:
                    # Loading the latest version
                    metadata_to_load = latest_metadata
                    graph_file = self.file_manager.get_graph_file_path(
                        graph_id, metadata_to_load.format)
                else:
                    # Loading a specific archived version
                    metadata_to_load = self._get_metadata(graph_id, version)
                    if not metadata_to_load:
                        logger.warning("Graph '%s' version %s not found", graph_id, version)
                        return None
                    graph_file = self.file_manager.get_version_file_path(
                        graph_id, version, metadata_to_load.format)

                if not graph_file.exists():
                    logger.error("Graph file not found: %s", graph_file)
                    return None

                serialized_data = graph_file.read_bytes()
                self._verify_checksum(serialized_data, metadata_to_load, graph_id)

                graph = SFMGraphSerializer.deserialize_graph(serialized_data,
                                                             metadata_to_load.format)

                if self.config.validate_on_load:
                    self._validate_graph(graph)

                logger.info("Graph '%s' loaded successfully (version %d)",
                            graph_id, metadata_to_load.version)
                return graph

            except Exception as e:
                logger.error("Failed to load graph '%s': %s", graph_id, str(e))
                raise SFMPersistenceError(f"Failed to load graph: {str(e)}") from e

    def _verify_checksum(self, serialized_data: bytes, metadata: GraphMetadata,
                         graph_id: str) -> None:
        """Verify data integrity using checksum."""
        if metadata.checksum:
            actual_checksum = hashlib.sha256(serialized_data).hexdigest()
            if actual_checksum != metadata.checksum:
                logger.warning("Checksum mismatch for graph '%s'. Data may be corrupted.",
                               graph_id)

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
                graph_file = self.file_manager.get_graph_file_path(graph_id,
                                                                   metadata.format)
                if graph_file.exists():
                    graph_file.unlink()

                # Delete metadata
                metadata_file = self.file_manager.get_metadata_file_path(graph_id)
                if metadata_file.exists():
                    metadata_file.unlink()

                # Delete versions if requested
                if include_versions:
                    version_dir = self.file_manager.versions_path / graph_id
                    if version_dir.exists():
                        shutil.rmtree(version_dir)

                # Remove from cache
                self._metadata_cache.pop(graph_id, None)

                logger.info("Graph '%s' deleted successfully", graph_id)
                return True

            except Exception as e:
                logger.error("Failed to delete graph '%s': %s", graph_id, str(e))
                return False

    def list_graphs(self, include_metadata: bool = True) -> Sequence[Union[str, GraphMetadata]]:
        """
        List all stored graphs.

        Args:
            include_metadata: Whether to return metadata objects or just IDs

        Returns:
            List of graph IDs or GraphMetadata objects
        """
        with self._thread_safe():
            try:
                if not self.file_manager.metadata_path.exists():
                    return []

                graph_ids = [
                    metadata_file.stem
                    for metadata_file in self.file_manager.metadata_path.glob("*.json")
                ]

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
                logger.error("Failed to list graphs: %s", str(e))
                return []

    def get_graph_metadata(self, graph_id: str) -> Optional[GraphMetadata]:
        """Get metadata for a specific graph."""
        return self._get_metadata(graph_id)

    def get_storage_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        with self._thread_safe():
            try:
                stats = self._initialize_stats()
                graphs = self.list_graphs(include_metadata=True)
                stats['total_graphs'] = len(graphs)

                self._calculate_graph_stats(
                    [g for g in graphs if isinstance(g, GraphMetadata)], stats
                )
                self._count_backups(stats)

                return stats

            except Exception as e:
                logger.error("Failed to get storage statistics: %s", str(e))
                return {}

    def _initialize_stats(self) -> Dict[str, Any]:
        """Initialize statistics dictionary."""
        return {
            'total_graphs': 0,
            'total_size_bytes': 0,
            'total_versions': 0,
            'total_backups': 0,
            'format_distribution': {},
            'largest_graph': None,
            'oldest_graph': None,
            'newest_graph': None
        }

    def _calculate_graph_stats(self, graphs: List[GraphMetadata],
                               stats: Dict[str, Any]) -> None:
        """Calculate statistics for graphs."""
        largest_size = 0
        oldest_date = None
        newest_date = None

        for metadata in graphs:
            if isinstance(metadata, GraphMetadata):
                stats['total_size_bytes'] += metadata.size_bytes

                # Format distribution
                format_name = metadata.format.value
                stats['format_distribution'][format_name] = (
                    stats['format_distribution'].get(format_name, 0) + 1
                )

                # Largest graph
                if metadata.size_bytes > largest_size:
                    largest_size = metadata.size_bytes
                    stats['largest_graph'] = metadata.graph_id

                # Date tracking
                if (metadata.created_at is not None and
                        (oldest_date is None or
                         (oldest_date is not None and metadata.created_at < oldest_date))):
                    oldest_date = metadata.created_at
                    stats['oldest_graph'] = metadata.graph_id

                if (metadata.created_at is not None and
                        (newest_date is None or
                         (newest_date is not None and metadata.created_at > newest_date))):
                    newest_date = metadata.created_at
                    stats['newest_graph'] = metadata.graph_id

                # Count versions
                version_history = self.get_version_history(metadata.graph_id)
                stats['total_versions'] += len(version_history)

    def _count_backups(self, stats: Dict[str, Any]) -> None:
        """Count backup files."""
        if self.file_manager.backups_path.exists():
            stats['total_backups'] = len(
                list(self.file_manager.backups_path.glob("*.backup"))
            )

    # Additional methods would be implemented here following the same pattern
    # ... (continuing with remaining methods like get_version_history,
    # create_backup, etc.)

    def _get_metadata(self, graph_id: str,
                      version: Optional[int] = None) -> Optional[GraphMetadata]:
        """Load metadata for a graph."""
        try:
            # Check cache first
            if version is None and graph_id in self._metadata_cache:
                return self._metadata_cache[graph_id]

            metadata_data = self._load_metadata_data(graph_id, version)
            if not metadata_data:
                return None

            metadata = self._parse_metadata(metadata_data)

            # Cache current version
            if version is None:
                self._metadata_cache[graph_id] = metadata

            return metadata

        except Exception as e:
            logger.error("Failed to load metadata for '%s': %s", graph_id, str(e))
            return None

    def _load_metadata_data(self, graph_id: str,
                            version: Optional[int]) -> Optional[Dict[str, Any]]:
        """Load raw metadata data from file."""
        if version:
            # Load version-specific metadata
            version_file = (self.file_manager.versions_path / graph_id /
                            f"v{version}.json")
            if not version_file.exists():
                return None
            return json.loads(version_file.read_text())

        # Load current metadata
        metadata_file = self.file_manager.get_metadata_file_path(graph_id)
        if not metadata_file.exists():
            return None
        return json.loads(metadata_file.read_text())

    def _parse_metadata(self, metadata_data: Dict[str, Any]) -> GraphMetadata:
        """Parse metadata dictionary into GraphMetadata object."""
        # Convert datetime strings back to datetime objects
        metadata_data['created_at'] = datetime.fromisoformat(metadata_data['created_at'])
        if metadata_data.get('modified_at'):
            metadata_data['modified_at'] = datetime.fromisoformat(
                metadata_data['modified_at']
            )
        metadata_data['format'] = StorageFormat(metadata_data['format'])

        return GraphMetadata(**metadata_data)

    def _save_metadata(self, graph_id: str, metadata: GraphMetadata) -> None:
        """Save metadata for a graph."""
        try:
            metadata_file = self.file_manager.get_metadata_file_path(graph_id)
            metadata_dict = asdict(metadata)
            metadata_dict['format'] = metadata.format.value

            metadata_file.write_text(
                json.dumps(metadata_dict, indent=2,
                           default=SFMGraphSerializer._json_serializer)
            )

        except Exception as e:
            logger.error("Failed to save metadata for '%s': %s", graph_id, str(e))
            raise

    def _archive_version(self, graph_id: str, metadata: GraphMetadata) -> None:
        """Archive current version before updating."""
        try:
            version_dir = self.file_manager.versions_path / graph_id
            version_dir.mkdir(exist_ok=True)

            # Save version metadata
            version_metadata_file = version_dir / f"v{metadata.version}.json"
            metadata_dict = asdict(metadata)
            metadata_dict['format'] = metadata.format.value
            version_metadata_file.write_text(
                json.dumps(metadata_dict, indent=2,
                           default=SFMGraphSerializer._json_serializer)
            )

            # Copy current graph data to versioned file
            current_graph_file = self.file_manager.get_graph_file_path(
                graph_id, metadata.format
            )
            if current_graph_file.exists():
                version_data_file = self.file_manager.get_version_file_path(
                    graph_id, metadata.version, metadata.format)
                # Ensure directory exists
                version_data_file.parent.mkdir(exist_ok=True, parents=True)
                shutil.copy2(current_graph_file, version_data_file)

        except Exception as e:
            logger.error("Failed to archive version for '%s': %s", graph_id, str(e))
            raise

    def _validate_graph(self, graph: SFMGraph) -> None:
        """Validate graph integrity."""
        if not graph.id:
            raise SFMSerializationError("Graph must have an ID")

        # Validate relationship references
        all_node_ids = set()
        node_collections = [
            graph.actors, graph.institutions, graph.resources,
            graph.processes, graph.flows, graph.policies
        ]

        for collection in node_collections:
            all_node_ids.update(collection.keys())

        for rel in graph.relationships.values():
            if rel.source_id not in all_node_ids:
                raise SFMSerializationError(
                    f"Relationship {rel.id} references non-existent "
                    f"source node {rel.source_id}"
                )
            if rel.target_id not in all_node_ids:
                raise SFMSerializationError(
                    f"Relationship {rel.id} references non-existent "
                    f"target node {rel.target_id}"
                )

    def _count_nodes(self, graph: SFMGraph) -> int:
        """Count total nodes in graph."""
        return (len(graph.actors) + len(graph.institutions) + len(graph.resources) +
                len(graph.processes) + len(graph.flows) + len(graph.policies) +
                len(graph.belief_systems) + len(graph.technology_systems) +
                len(graph.indicators) + len(graph.feedback_loops) +
                len(graph.system_properties) + len(graph.analytical_contexts))

    # Implement remaining methods following the same pattern...
    def get_version_history(self, graph_id: str) -> List[Dict[str, Any]]:
        """Get version history for a graph."""
        version_dir = self.file_manager.versions_path / graph_id
        if not version_dir.exists() or not version_dir.is_dir():
            return []
        history: List[Dict[str, Any]] = []
        # Iterate over version metadata files v{version}.json (but not v{version}_data.json)
        for metadata_file in sorted(version_dir.glob("v[0-9]*.json")):
            # Skip data files which have '_data' in the name
            if '_data' in metadata_file.name:
                continue
            try:
                data = json.loads(metadata_file.read_text())
                history.append(data)
            except Exception as e:
                logger.error("Failed to load version metadata from %s: %s", metadata_file, e)
        return history

    def create_backup(self, graph_id: str, backup_name: Optional[str] = None) -> str:
        """Create a backup of a specific graph."""
        with self._thread_safe():
            try:
                metadata = self._get_metadata(graph_id)
                if not metadata:
                    raise SFMPersistenceError(f"Graph '{graph_id}' not found for backup.")

                graph_file = self.file_manager.get_graph_file_path(graph_id, metadata.format)
                if not graph_file.exists():
                    raise SFMPersistenceError(f"Graph file '{graph_file}' not found for backup.")

                backup_name = backup_name or f"{graph_id}_backup"
                backup_path = self.file_manager.backups_path / f"{backup_name}.backup"

                logger.debug("Creating backup for graph ID '%s'", graph_id)
                logger.debug("Graph file path: %s", graph_file)
                logger.debug("Metadata content: %s", metadata)
                logger.debug("Backup file path: %s", backup_path)

                # Log serialized data for debugging
                serialized_data = graph_file.read_bytes()
                logger.debug("Serialized data in graph file: %s", serialized_data[:100])

                shutil.copy2(graph_file, backup_path)
                logger.info("Backup created for graph '%s' at '%s'", graph_id, backup_path)
                return str(backup_path)

            except Exception as e:
                logger.error("Failed to create backup for graph '%s': %s", graph_id, str(e))
                raise SFMPersistenceError(f"Failed to create backup: {str(e)}") from e

    def restore_from_backup(self, backup_path: str, new_graph_id: Optional[str] = None) -> str:
        """Restore a graph from backup."""
        with self._thread_safe():
            try:
                backup_file = Path(backup_path)
                if not backup_file.exists():
                    raise SFMPersistenceError(f"Backup file '{backup_path}' not found.")

                # Extract original graph ID from backup filename
                original_graph_id = backup_file.stem.rsplit("_backup", 1)[0]
                new_graph_id = new_graph_id or original_graph_id

                # Restore graph data
                graph_file_path = self.file_manager.get_graph_file_path(
                    new_graph_id, self.config.default_format)
                shutil.copy2(backup_file, graph_file_path)

                # Restore metadata
                # This is a simplified restore; a real implementation might store
                # metadata in the backup
                # or reconstruct it. Here, we'll try to load the graph to create basic metadata.
                serialized_data = graph_file_path.read_bytes()
                if not serialized_data:
                    raise SFMPersistenceError("Restored graph file is empty.")

                restored_graph = SFMGraphSerializer.deserialize_graph(
                    serialized_data, self.config.default_format)
                if restored_graph is None:
                    raise SFMPersistenceError("Failed to deserialize restored graph.")

                # Create and save new metadata for the restored graph
                metadata = self._create_metadata(
                    graph_id=new_graph_id,
                    graph=restored_graph,
                    version=1,  # Start with version 1
                    current_metadata=None,
                    metadata={},
                    serialized_data=serialized_data,
                    checksum=hashlib.sha256(serialized_data).hexdigest(),
                    format_type=self.config.default_format
                )
                self._save_metadata(new_graph_id, metadata)
                self._metadata_cache[new_graph_id] = metadata

                logger.info("Graph '%s' restored successfully from backup '%s'",
                           new_graph_id, backup_path)
                return new_graph_id

            except Exception as e:
                logger.error("Failed to restore from backup: %s", str(e))
                raise SFMPersistenceError(f"Failed to restore from backup: {str(e)}") from e


# Convenience functions for quick operations

def save_sfm_graph(graph_id: str, graph: SFMGraph,
                   storage_path: str = "./sfm_data") -> GraphMetadata:
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
    # Ensure the result is a list of strings
    return [str(gid) for gid in manager.list_graphs(include_metadata=False)]
