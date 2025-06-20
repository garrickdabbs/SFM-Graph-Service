"""
SFM Service - Unified Facade for Social Fabric Matrix Framework

This module provides a simplified, unified interface to the SFM framework's core functionality.
It acts as a facade that abstracts away the complexity of directly working with repositories,
query engines, and data models, providing an intuitive API for common SFM operations.

The service is designed to work both as a direct Python library and as a backend service
for FastAPI REST endpoints.

Key Features:
- Unified interface for creating, managing, and analyzing SFM graphs
- Built-in repository management with pluggable storage backends
- Integrated query engine for advanced network analysis
- High-level operations for common SFM use cases
- Type-safe operations with runtime validation
- Automatic graph synchronization and consistency management
- FastAPI-compatible data models and response formats
- Comprehensive error handling and logging

Usage Examples:

Direct Python Usage:
```python
from core.sfm_service import SFMService

service = SFMService()
actor = service.create_actor(name="USDA", sector="government")
policy = service.create_policy(name="Farm Bill 2023")
service.connect(actor.id, policy.id, "IMPLEMENTS")
analysis = service.analyze_centrality()
```

FastAPI Integration:
```python
from fastapi import FastAPI
from core.sfm_service import SFMService, get_sfm_service

app = FastAPI()
service = get_sfm_service()

@app.post("/actors")
async def create_actor(request: CreateActorRequest):
    return service.create_actor(**request.dict())
```
"""

from typing import Dict, List, Optional, Any, Union, Tuple, Type, TypeVar
import uuid

from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from contextlib import contextmanager

# Core imports
from core.sfm_models import (
    Node,
    Actor,
    Institution,
    Resource,
    Process,
    Flow,
    Relationship,
    Policy,
    Indicator,
    SFMGraph,
    AnalyticalContext,
    RelationshipKind,
)
from core.sfm_enums import ResourceType, FlowNature
from core.sfm_query import (
    SFMQueryEngine,
    NetworkXSFMQueryEngine,
    NodeMetrics,
    FlowAnalysis,
    QueryResult,
)

# Repository imports
from db.sfm_dao import (
    SFMRepository,
    SFMRepositoryFactory,
    ActorRepository,
    InstitutionRepository,
    PolicyRepository,
    ResourceRepository,
    RelationshipRepository,
    ProcessRepository,
    FlowRepository,
)

# Setup logging
logger = logging.getLogger(__name__)

T = TypeVar("T", bound=Node)  # Generic type for Node entities


# ═══ DATA TRANSFER OBJECTS (DTOs) FOR API ═══

@dataclass
class CreateActorRequest:
    """Request model for creating an actor."""

    name: str
    description: str = ""
    sector: str = ""
    legal_form: str = ""
    meta: Optional[Dict[str, str]] = None


@dataclass
class CreateInstitutionRequest:
    """Request model for creating an institution."""

    name: str
    description: str = ""
    meta: Optional[Dict[str, str]] = None


@dataclass
class CreatePolicyRequest:
    """Request model for creating a policy."""

    name: str
    description: str = ""
    authority: str = ""
    target_sectors: Optional[List[str]] = None
    enforcement: float = 0.0
    meta: Optional[Dict[str, str]] = None


@dataclass
class CreateResourceRequest:
    """Request model for creating a resource."""

    name: str
    description: str = ""
    rtype: str = "NATURAL"  # String representation for API
    unit: str = ""
    meta: Optional[Dict[str, str]] = None


@dataclass
class CreateRelationshipRequest:
    """Request model for creating a relationship."""

    source_id: str  # String UUID for API
    target_id: str  # String UUID for API
    kind: str
    weight: float = 1.0
    meta: Optional[Dict[str, str]] = None


@dataclass
class NodeResponse:
    """Response model for node entities."""

    id: str
    label: str
    description: str
    node_type: str
    meta: Dict[str, Any]
    created_at: Optional[str] = None


@dataclass
class RelationshipResponse:
    """Response model for relationships."""

    id: str
    source_id: str
    target_id: str
    kind: str
    weight: float
    meta: Optional[Dict[str, Any]] = None


@dataclass
class GraphStatistics:
    """Response model for graph statistics."""

    total_nodes: int
    total_relationships: int
    node_types: Dict[str, int]
    relationship_kinds: Dict[str, int]
    timestamp: str


@dataclass
class CentralityAnalysis:
    """Response model for centrality analysis."""

    node_centrality: Dict[str, float]
    most_central_nodes: List[Tuple[str, float]]
    analysis_type: str
    timestamp: str


@dataclass
class PolicyImpactAnalysis:
    """Response model for policy impact analysis."""

    policy_id: str
    total_affected_nodes: int
    affected_actors: List[str]
    affected_institutions: List[str]
    affected_resources: List[str]
    network_metrics: Dict[str, float]
    impact_radius: int


class ServiceStatus(Enum):
    """Service operational status."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass
class ServiceHealth:
    """Service health check response."""

    status: ServiceStatus
    timestamp: str
    version: str = "1.0.0"
    backend: str = "networkx"
    node_count: int = 0
    relationship_count: int = 0
    last_operation: Optional[str] = None


# ═══ SERVICE CONFIGURATION ═══


@dataclass
class SFMServiceConfig:
    """Configuration for SFM Service."""

    storage_backend: str = "networkx"
    auto_sync: bool = True
    validation_enabled: bool = True
    cache_queries: bool = True
    enable_logging: bool = True
    log_level: str = "INFO"
    max_graph_size: int = 10000
    query_timeout: int = 30


class SFMServiceError(Exception):
    """Base exception for SFM Service operations."""

    def __init__(
        self,
        message: str,
        error_code: str = "SFM_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class ValidationError(SFMServiceError):
    """Validation-related service error."""

    def __init__(self, message: str, field: Optional[str] = None, value: Any = None):
        super().__init__(message, "VALIDATION_ERROR", {"field": field, "value": value})


class NotFoundError(SFMServiceError):
    """Entity not found error."""

    def __init__(self, entity_type: str, entity_id: str):
        super().__init__(
            f"{entity_type} with ID {entity_id} not found",
            "NOT_FOUND",
            {"entity_type": entity_type, "entity_id": entity_id},
        )


# ═══ MAIN SERVICE CLASS ═══


class SFMService:
    """
    Unified facade for Social Fabric Matrix framework operations.

    This service provides a simplified interface for creating, managing, and analyzing
    SFM graphs without requiring direct interaction with repositories or query engines.
    It's designed to work both as a direct Python library and as a backend for REST APIs.
    """

    def __init__(self, config: Optional[SFMServiceConfig] = None):
        """
        Initialize the SFM Service.

        Args:
            config: Service configuration options
        """
        self.config = config or SFMServiceConfig()

        # Setup logging
        if self.config.enable_logging:
            logging.basicConfig(level=getattr(logging, self.config.log_level.upper()))

        # Initialize repositories
        self._base_repo = SFMRepositoryFactory.create_repository(
            self.config.storage_backend
        )
        self._actor_repo = ActorRepository(self._base_repo)
        self._institution_repo = InstitutionRepository(self._base_repo)
        self._policy_repo = PolicyRepository(self._base_repo)
        self._resource_repo = ResourceRepository(self._base_repo)
        self._relationship_repo = RelationshipRepository(self._base_repo)
        self._process_repo = ProcessRepository(self._base_repo)
        self._flow_repo = FlowRepository(self._base_repo)

        # Initialize query engine (lazy-loaded)
        self._query_engine: Optional[SFMQueryEngine] = None
        self._graph_cache: Optional[SFMGraph] = None
        self._cache_dirty = True
        self._last_operation: Optional[str] = None

        logger.info(
            f"SFM Service initialized with backend: {self.config.storage_backend}"
        )

    # ═══ PROPERTY ACCESS & INTERNAL METHODS ═══

    @property
    def query_engine(self) -> SFMQueryEngine:
        """Get the query engine, creating it if necessary."""
        if self._query_engine is None or self._cache_dirty:
            graph = self.get_graph()
            self._query_engine = NetworkXSFMQueryEngine(graph)
            self._cache_dirty = False
        return self._query_engine

    def get_graph(self) -> SFMGraph:
        """Get the current SFM graph."""
        if self._graph_cache is None or self._cache_dirty:
            self._graph_cache = self._base_repo.load_graph()
            self._cache_dirty = False
        return self._graph_cache

    def _mark_dirty(self, operation: Optional[str] = None):
        """Mark the cache as dirty after modifications."""
        if self.config.auto_sync:
            self._cache_dirty = True
        self._last_operation = operation or "unknown"
        logger.debug(f"Cache marked dirty after operation: {self._last_operation}")

    def _validate_graph_size(self):
        """Validate that the graph hasn't exceeded size limits."""
        if self.config.max_graph_size > 0:
            stats = self.get_statistics()
            if stats.total_nodes > self.config.max_graph_size:
                raise SFMServiceError(
                    f"Graph size ({stats.total_nodes}) exceeds maximum ({self.config.max_graph_size})",
                    "GRAPH_SIZE_EXCEEDED",
                )

    def _convert_to_resource_type(self, rtype_str: str) -> ResourceType:
        """Convert string to ResourceType enum."""
        try:
            return ResourceType[rtype_str.upper()]
        except KeyError:
            raise ValidationError(
                f"Invalid resource type: {rtype_str}", "rtype", rtype_str
            )

    def _convert_to_relationship_kind(self, kind_str: str) -> RelationshipKind:
        """Convert string to RelationshipKind enum."""
        try:
            return RelationshipKind[kind_str.upper()]
        except KeyError:
            # Default to AFFECTS if not found
            logger.warning(f"Unknown relationship kind '{kind_str}', using AFFECTS")
            return RelationshipKind.AFFECTS

    def _node_to_response(self, node: Node) -> NodeResponse:
        """Convert a Node to a NodeResponse."""
        return NodeResponse(
            id=str(node.id),
            label=node.label,
            description=node.description or "",
            node_type=type(node).__name__,
            meta=node.meta or {},
            created_at=datetime.now().isoformat(),
        )

    def _relationship_to_response(self, rel: Relationship) -> RelationshipResponse:
        """Convert a Relationship to a RelationshipResponse."""
        return RelationshipResponse(
            id=str(rel.id),
            source_id=str(rel.source_id),
            target_id=str(rel.target_id),
            kind=rel.kind.name,
            weight=rel.weight or 1.0,
            meta=rel.meta if hasattr(rel, "meta") else {},
        )

    # ═══ HEALTH & STATUS ═══

    def get_health(self) -> ServiceHealth:
        """Get service health status."""
        try:
            stats = self.get_statistics()
            return ServiceHealth(
                status=ServiceStatus.HEALTHY,
                timestamp=datetime.now().isoformat(),
                backend=self.config.storage_backend,
                node_count=stats.total_nodes,
                relationship_count=stats.total_relationships,
                last_operation=self._last_operation,
            )
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return ServiceHealth(
                status=ServiceStatus.ERROR,
                timestamp=datetime.now().isoformat(),
                backend=self.config.storage_backend,
                last_operation=self._last_operation,
            )

    # ═══ ENTITY CREATION (API-COMPATIBLE) ═══

    def create_actor(
        self, request: Union[CreateActorRequest, dict], **kwargs
    ) -> NodeResponse:
        """
        Create a new Actor entity.

        Args:
            request: CreateActorRequest object or dict with actor data
            **kwargs: Additional arguments for direct Python usage

        Returns:
            NodeResponse with the created actor data
        """
        try:
            # Handle both API request objects and direct calls
            if isinstance(request, dict):
                data = request
            elif isinstance(request, CreateActorRequest):
                data = asdict(request)
            else:
                # Direct call with named parameters
                data = {"name": request, **kwargs}

            if self.config.validation_enabled:
                if not data.get("name"):
                    raise ValidationError("Actor name is required", "name")

            actor = Actor(
                label=data["name"],
                description=data.get("description", ""),
                sector=data.get("sector", ""),
                legal_form=data.get("legal_form", ""),
                meta=data.get("meta", {}),
            )

            result = self._actor_repo.create(actor)
            self._mark_dirty("create_actor")
            self._validate_graph_size()

            logger.info(f"Created actor: {result.label} ({result.id})")
            return self._node_to_response(result)

        except Exception as e:
            logger.error(f"Failed to create actor: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to create actor: {str(e)}", "CREATE_ACTOR_FAILED"
            )

    def create_institution(
        self, request: Union[CreateInstitutionRequest, dict], **kwargs
    ) -> NodeResponse:
        """Create a new Institution entity."""
        try:
            if isinstance(request, dict):
                data = request
            elif isinstance(request, CreateInstitutionRequest):
                data = asdict(request)
            else:
                data = {"name": request, **kwargs}

            if self.config.validation_enabled:
                if not data.get("name"):
                    raise ValidationError("Institution name is required", "name")

            institution = Institution(
                label=data["name"],
                description=data.get("description", ""),
                meta=data.get("meta", {}),
            )

            result = self._institution_repo.create(institution)
            self._mark_dirty("create_institution")

            logger.info(f"Created institution: {result.label} ({result.id})")
            return self._node_to_response(result)

        except Exception as e:
            logger.error(f"Failed to create institution: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to create institution: {str(e)}", "CREATE_INSTITUTION_FAILED"
            )

    def create_policy(
        self, request: Union[CreatePolicyRequest, dict], **kwargs
    ) -> NodeResponse:
        """Create a new Policy entity."""
        try:
            if isinstance(request, dict):
                data = request
            elif isinstance(request, CreatePolicyRequest):
                data = asdict(request)
            else:
                data = {"name": request, **kwargs}

            if self.config.validation_enabled:
                if not data.get("name"):
                    raise ValidationError("Policy name is required", "name")

            policy = Policy(
                label=data["name"],
                description=data.get("description", ""),
                authority=data.get("authority", ""),
                target_sectors=data.get("target_sectors", []),
                enforcement=data.get("enforcement", 0.0),
                meta=data.get("meta", {}),
            )

            result = self._policy_repo.create(policy)
            self._mark_dirty("create_policy")

            logger.info(f"Created policy: {result.label} ({result.id})")
            return self._node_to_response(result)

        except Exception as e:
            logger.error(f"Failed to create policy: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to create policy: {str(e)}", "CREATE_POLICY_FAILED"
            )

    def create_resource(
        self, request: Union[CreateResourceRequest, dict], **kwargs
    ) -> NodeResponse:
        """Create a new Resource entity."""
        try:
            if isinstance(request, dict):
                data = request
            elif isinstance(request, CreateResourceRequest):
                data = asdict(request)
            else:
                data = {"name": request, **kwargs}

            if self.config.validation_enabled:
                if not data.get("name"):
                    raise ValidationError("Resource name is required", "name")

            rtype = self._convert_to_resource_type(data.get("rtype", "NATURAL"))

            resource = Resource(
                label=data["name"],
                description=data.get("description", ""),
                rtype=rtype,
                unit=data.get("unit", ""),
                meta=data.get("meta", {}),
            )

            result = self._resource_repo.create(resource)
            self._mark_dirty("create_resource")

            logger.info(f"Created resource: {result.label} ({result.id})")
            return self._node_to_response(result)

        except Exception as e:
            logger.error(f"Failed to create resource: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to create resource: {str(e)}", "CREATE_RESOURCE_FAILED"
            )

    # ═══ RELATIONSHIP MANAGEMENT ═══

    def create_relationship(
        self, request: Union[CreateRelationshipRequest, dict], **kwargs
    ) -> RelationshipResponse:
        """Create a relationship between two entities."""
        try:
            if isinstance(request, dict):
                data = request
            elif isinstance(request, CreateRelationshipRequest):
                data = asdict(request)
            else:
                # Direct call with positional args
                data = {
                    "source_id": str(request),
                    "target_id": str(kwargs.get("target_id")),
                    "kind": kwargs.get(
                        "kind", kwargs.get("relationship_kind", "AFFECTS")
                    ),
                    "weight": kwargs.get("weight", 1.0),
                    "meta": kwargs.get("meta", {}),
                }

            if self.config.validation_enabled:
                if not data.get("source_id") or not data.get("target_id"):
                    raise ValidationError("Source and target IDs are required")
                if not data.get("kind"):
                    raise ValidationError("Relationship kind is required")

            source_id = uuid.UUID(data["source_id"])
            target_id = uuid.UUID(data["target_id"])
            kind = self._convert_to_relationship_kind(data["kind"])

            relationship = Relationship(
                source_id=source_id,
                target_id=target_id,
                kind=kind,
                weight=data.get("weight", 1.0),
                meta=data.get("meta", {}),
            )

            result = self._relationship_repo.create(relationship)
            self._mark_dirty("create_relationship")

            logger.info(
                f"Created relationship: {source_id} --{kind.name}--> {target_id}"
            )
            return self._relationship_to_response(result)

        except ValueError as e:
            raise ValidationError(f"Invalid UUID format: {e}")
        except Exception as e:
            logger.error(f"Failed to create relationship: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to create relationship: {str(e)}", "CREATE_RELATIONSHIP_FAILED"
            )

    def connect(
        self,
        source_id: Union[str, uuid.UUID],
        target_id: Union[str, uuid.UUID],
        kind: str,
        weight: float = 1.0,
        **kwargs,
    ) -> RelationshipResponse:
        """Convenience method for creating relationships (backward compatibility)."""
        return self.create_relationship(
            {
                "source_id": str(source_id),
                "target_id": str(target_id),
                "kind": kind,
                "weight": weight,
                "meta": kwargs.get("meta", {}),
            }
        )

    # ═══ ENTITY RETRIEVAL ═══

    def get_entity(self, entity_type: Type[T], entity_id: uuid.UUID) -> Optional[T]:
        """Generic method to retrieve any entity by type and ID."""
        try:
            repo_mapping = {
                Actor: self._actor_repo,
                Policy: self._policy_repo,
                Institution: self._institution_repo,
                Resource: self._resource_repo,
                Process: self._process_repo,
                Flow: self._flow_repo,
                Relationship: self._relationship_repo,
                # Add other entity types as needed
            }

            repo = repo_mapping.get(entity_type)
            if repo is None:
                raise ValueError(f"No repository found for entity type: {entity_type}")

            return repo.read(entity_id)
        except Exception as e:
            logger.error(f"Failed to retrieve {entity_type.__name__} {entity_id}: {e}")
            return None

    def get_actor(self, actor_id: uuid.UUID) -> Optional[Actor]:
        """Retrieve an actor by ID."""
        return self.get_entity(Actor, actor_id)

    def get_policy(self, policy_id: uuid.UUID) -> Optional[Policy]:
        """Retrieve a policy by ID."""
        return self.get_entity(Policy, policy_id)

    def get_institution(self, institution_id: uuid.UUID) -> Optional[Institution]:
        """Retrieve an institution by ID."""
        return self.get_entity(Institution, institution_id)

    def get_resource(self, resource_id: uuid.UUID) -> Optional[Resource]:
        """Retrieve a resource by ID."""
        return self.get_entity(Resource, resource_id)

    def get_process(self, process_id: uuid.UUID) -> Optional[Process]:
        """Retrieve a process by ID."""
        return self.get_entity(Process, process_id)

    def get_flow(self, flow_id: uuid.UUID) -> Optional[Flow]:
        """Retrieve a flow by ID."""
        return self.get_entity(Flow, flow_id)

    def get_relationship(
        self, rel_id: Union[str, uuid.UUID]
    ) -> Optional[RelationshipResponse]:
        """Get a relationship by ID."""
        try:
            if isinstance(rel_id, str):
                rel_id = uuid.UUID(rel_id)

            rel = self._relationship_repo.read(rel_id)
            if not rel:
                return None

            return self._relationship_to_response(rel)

        except ValueError:
            raise ValidationError(f"Invalid UUID format: {rel_id}")
        except Exception as e:
            logger.error(f"Failed to get relationship {rel_id}: {e}")
            raise SFMServiceError(
                f"Failed to retrieve relationship: {str(e)}", "GET_RELATIONSHIP_FAILED"
            )

    def get_node_neighbors(
        self,
        node_id: Union[str, uuid.UUID],
        relationship_kinds: Optional[List[str]] = None,
        distance: int = 1,
    ) -> List[str]:
        """
        Get neighboring nodes within specified distance.

        Args:
            node_id: ID of the node to find neighbors for
            relationship_kinds: Optional list of relationship kind names to filter by
            distance: Distance/hops to search (default: 1 for direct neighbors)

        Returns:
            List of node IDs as strings
        """
        try:
            if isinstance(node_id, str):
                node_uuid = uuid.UUID(node_id)
            else:
                node_uuid = node_id

            # Convert string relationship kinds to enum values if provided
            relationship_kind_enums = None
            if relationship_kinds:
                relationship_kind_enums = []
                for kind_str in relationship_kinds:
                    try:
                        kind_enum = self._convert_to_relationship_kind(kind_str)
                        relationship_kind_enums.append(kind_enum)
                    except ValidationError:
                        logger.warning(f"Unknown relationship kind: {kind_str}")

            # Use the query engine to find neighbors
            engine = self.query_engine
            neighbor_ids = engine.get_node_neighbors(
                node_uuid, relationship_kind_enums, distance
            )

            # Convert UUIDs back to strings for API compatibility
            return [str(neighbor_id) for neighbor_id in neighbor_ids]

        except ValueError:
            raise ValidationError(f"Invalid UUID format: {node_id}")
        except Exception as e:
            logger.error(f"Failed to get neighbors for node {node_id}: {e}")
            raise SFMServiceError(
                f"Failed to get node neighbors: {str(e)}", "GET_NODE_NEIGHBORS_FAILED"
            )

    # ═══ ENTITY LISTING ═══

    def list_nodes(
        self, node_type: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[NodeResponse]:
        """List nodes with optional filtering and pagination."""
        try:
            # Map string types to classes
            type_mapping = {
                "Actor": Actor,
                "Institution": Institution,
                "Policy": Policy,
                "Resource": Resource,
                "Flow": Flow,
            }

            filter_type = type_mapping.get(node_type) if node_type else None
            nodes = self._base_repo.list_nodes(filter_type)

            # Apply pagination
            paginated_nodes = nodes[offset : offset + limit]

            return [self._node_to_response(node) for node in paginated_nodes]

        except Exception as e:
            logger.error(f"Failed to list nodes: {e}")
            raise SFMServiceError(
                f"Failed to list nodes: {str(e)}", "LIST_NODES_FAILED"
            )

    def list_relationships(
        self, kind: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[RelationshipResponse]:
        """List relationships with optional filtering and pagination."""
        try:
            filter_kind = self._convert_to_relationship_kind(kind) if kind else None
            relationships = (
                self._relationship_repo.list_all()
                if not filter_kind
                else self._relationship_repo.find_by_kind(filter_kind)
            )

            # Apply pagination
            paginated_rels = relationships[offset : offset + limit]

            return [self._relationship_to_response(rel) for rel in paginated_rels]

        except Exception as e:
            logger.error(f"Failed to list relationships: {e}")
            raise SFMServiceError(
                f"Failed to list relationships: {str(e)}", "LIST_RELATIONSHIPS_FAILED"
            )

    # ═══ ANALYSIS OPERATIONS ═══

    def get_statistics(self) -> GraphStatistics:
        """Get basic statistics about the current graph."""
        try:
            graph = self.get_graph()

            # Count entities by type
            type_counts = {}
            for node in graph:
                node_type = type(node).__name__
                type_counts[node_type] = type_counts.get(node_type, 0) + 1

            # Count relationships by kind
            rel_counts = {}
            for rel in graph.relationships.values():
                kind = rel.kind.name
                rel_counts[kind] = rel_counts.get(kind, 0) + 1

            return GraphStatistics(
                total_nodes=len(graph),
                total_relationships=len(graph.relationships),
                node_types=type_counts,
                relationship_kinds=rel_counts,
                timestamp=datetime.now().isoformat(),
            )

        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            raise SFMServiceError(
                f"Failed to get statistics: {str(e)}", "GET_STATISTICS_FAILED"
            )

    def analyze_centrality(
        self, centrality_type: str = "betweenness", limit: int = 10
    ) -> CentralityAnalysis:
        """Perform centrality analysis on the network."""
        try:
            engine = self.query_engine
            graph = self.get_graph()

            # Calculate centrality for all nodes
            centrality_scores = {}
            most_central = []

            if len(graph) > 0:
                for node in graph:
                    score = engine.get_node_centrality(node.id, centrality_type)
                    centrality_scores[str(node.id)] = score

                # Get most central nodes
                central_nodes = engine.get_most_central_nodes(
                    None, centrality_type, limit
                )
                most_central = [
                    (str(node_id), score) for node_id, score in central_nodes
                ]

            return CentralityAnalysis(
                node_centrality=centrality_scores,
                most_central_nodes=most_central,
                analysis_type=centrality_type,
                timestamp=datetime.now().isoformat(),
            )

        except Exception as e:
            logger.error(f"Failed to analyze centrality: {e}")
            raise SFMServiceError(
                f"Failed to analyze centrality: {str(e)}", "CENTRALITY_ANALYSIS_FAILED"
            )

    def analyze_policy_impact(
        self, policy_id: Union[str, uuid.UUID], impact_radius: int = 3
    ) -> PolicyImpactAnalysis:
        """Analyze the potential impact of a policy."""
        try:
            if isinstance(policy_id, str):
                policy_id = uuid.UUID(policy_id)

            engine = self.query_engine
            impact_data = engine.analyze_policy_impact(policy_id, impact_radius)

            if "error" in impact_data:
                raise NotFoundError("Policy", str(policy_id))

            return PolicyImpactAnalysis(
                policy_id=str(policy_id),
                total_affected_nodes=impact_data.get("total_affected_nodes", 0),
                affected_actors=[
                    str(node_id) for node_id in impact_data.get("affected_actors", [])
                ],
                affected_institutions=[
                    str(node_id)
                    for node_id in impact_data.get("affected_institutions", [])
                ],
                affected_resources=[
                    str(node_id)
                    for node_id in impact_data.get("affected_resources", [])
                ],
                network_metrics=impact_data.get("network_metrics", {}),
                impact_radius=impact_radius,
            )

        except ValueError:
            raise ValidationError(f"Invalid UUID format: {policy_id}")
        except Exception as e:
            logger.error(f"Failed to analyze policy impact: {e}")
            if isinstance(e, SFMServiceError):
                raise
            raise SFMServiceError(
                f"Failed to analyze policy impact: {str(e)}",
                "POLICY_IMPACT_ANALYSIS_FAILED",
            )

    def find_shortest_path(
        self,
        source_id: Union[str, uuid.UUID],
        target_id: Union[str, uuid.UUID],
        relationship_kinds: Optional[List[str]] = None,
    ) -> Optional[List[str]]:
        """
        Find the shortest path between two nodes.

        Args:
            source_id: ID of the source node
            target_id: ID of the target node
            relationship_kinds: Optional list of relationship kind names to filter by

        Returns:
            List of node IDs representing the path (including source and target),
            or None if no path exists
        """
        try:
            if isinstance(source_id, str):
                source_uuid = uuid.UUID(source_id)
            else:
                source_uuid = source_id

            if isinstance(target_id, str):
                target_uuid = uuid.UUID(target_id)
            else:
                target_uuid = target_id

            # Convert string relationship kinds to enum values if provided
            relationship_kind_enums = None
            if relationship_kinds:
                relationship_kind_enums = []
                for kind_str in relationship_kinds:
                    try:
                        kind_enum = self._convert_to_relationship_kind(kind_str)
                        relationship_kind_enums.append(kind_enum)
                    except ValidationError:
                        logger.warning(f"Unknown relationship kind: {kind_str}")

            # Use the query engine to find the path
            engine = self.query_engine
            path_ids = engine.find_shortest_path(
                source_uuid, target_uuid, relationship_kind_enums
            )

            if path_ids is None:
                return None

            # Convert UUIDs back to strings for API compatibility
            return [str(node_id) for node_id in path_ids]

        except ValueError:
            raise ValidationError(f"Invalid UUID format in path finding")
        except Exception as e:
            logger.error(
                f"Failed to find path between {source_id} and {target_id}: {e}"
            )
            raise SFMServiceError(
                f"Failed to find shortest path: {str(e)}", "FIND_PATH_FAILED"
            )

    def find_shortest_path_legacy(self, source_id: str, target_id: str) -> list:
        """
        Find the shortest path between two nodes by their IDs.
        Returns a list of node IDs representing the path, or None if no path exists.
        """
        # Assuming the base repo has a graph attribute with networkx
        graph = getattr(self._base_repo, "graph", None)
        if graph is None:
            return []
        try:
            import networkx as nx

            path = nx.shortest_path(graph, source=source_id, target=target_id)
            if isinstance(path, list):
                return path
            else:
                return []
        except Exception:
            return []

    # ═══ SYSTEM MANAGEMENT ═══

    def clear_all_data(self) -> Dict[str, Any]:
        """Clear all data from the repository."""
        try:
            stats_before = self.get_statistics()
            self._base_repo.clear()
            self._graph_cache = None
            self._query_engine = None
            self._cache_dirty = True
            self._mark_dirty("clear_all_data")

            logger.warning("All data cleared from repository")
            return {
                "status": "success",
                "nodes_removed": stats_before.total_nodes,
                "relationships_removed": stats_before.total_relationships,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Failed to clear data: {e}")
            raise SFMServiceError(
                f"Failed to clear data: {str(e)}", "CLEAR_DATA_FAILED"
            )

    # ═══ BULK OPERATIONS ═══

    def bulk_create_actors(
        self, requests: List[CreateActorRequest]
    ) -> List[NodeResponse]:
        """Create multiple actors in batch."""
        results = []
        for request in requests:
            try:
                result = self.create_actor(request)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to create actor in bulk operation: {e}")
                # Continue with other actors, collect errors separately

        return results

    @contextmanager
    def transaction(self):
        """Context manager for transactional operations (placeholder for future implementation)."""
        try:
            yield self
        except Exception:
            # In a real implementation, this would rollback changes
            logger.error("Transaction failed, would rollback if supported")
            raise


# ═══ SERVICE FACTORY & DEPENDENCY INJECTION ═══

_service_instance: Optional[SFMService] = None


def create_sfm_service(config: Optional[SFMServiceConfig] = None) -> SFMService:
    """Factory function to create SFM service instances."""
    return SFMService(config)


def get_sfm_service() -> SFMService:
    """Get singleton SFM service instance (for FastAPI dependency injection)."""
    global _service_instance
    if _service_instance is None:
        _service_instance = create_sfm_service()
    return _service_instance


def reset_sfm_service():
    """Reset the singleton service instance (useful for testing)."""
    global _service_instance
    _service_instance = None


# ═══ CONVENIENCE FUNCTIONS ═══


def quick_analysis(service: SFMService) -> Dict[str, Any]:
    """
    Perform a quick analysis of an SFM graph.

    Args:
        service: SFM service instance

    Returns:
        Dictionary containing analysis results
    """
    try:
        stats = service.get_statistics()
        centrality = service.analyze_centrality(limit=5)
        health = service.get_health()

        return {
            "health": asdict(health),
            "statistics": asdict(stats),
            "top_central_nodes": centrality.most_central_nodes,
            "analysis_timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Quick analysis failed: {e}")
        return {"error": str(e), "analysis_timestamp": datetime.now().isoformat()}
