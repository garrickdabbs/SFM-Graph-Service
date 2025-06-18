from typing import Dict, Type, Optional, Any, List
import networkx as nx
from db.abstract_repository import (
    ActorRepository, InstitutionRepository, PolicyRepository, ResourceRepository,
    ProcessRepository, FlowRepository, BeliefSystemRepository, TechnologySystemRepository,
    IndicatorRepository, RelationshipRepository, FeedbackLoopRepository,
    AnalyticalContextRepository, SystemPropertyRepository, GraphRepository
)
import uuid
from core.sfm_models import SFMGraph

class RepositoryFactory:
    """Factory for creating repository instances with different storage backends."""
    
    # Registry for repository implementations
    _implementations: Dict[str, Dict[str, Type]] = {
        'actor': {},
        'institution': {},
        'policy': {},
        'resource': {},
        'process': {},
        'flow': {},
        'belief_system': {},
        'technology_system': {},
        'indicator': {},
        'relationship': {},
        'feedback_loop': {},
        'analytical_context': {},
        'system_property': {},
        'graph': {}
    }
    
    @classmethod
    def register_actor_repository(cls, provider: str, repository_class: Type[ActorRepository]) -> None:
        """Register an actor repository implementation."""
        cls._implementations['actor'][provider] = repository_class
    
    @classmethod
    def register_institution_repository(cls, provider: str, repository_class: Type[InstitutionRepository]) -> None:
        """Register an institution repository implementation."""
        cls._implementations['institution'][provider] = repository_class
    
    @classmethod
    def register_policy_repository(cls, provider: str, repository_class: Type[PolicyRepository]) -> None:
        """Register a policy repository implementation."""
        cls._implementations['policy'][provider] = repository_class
    
    @classmethod
    def register_resource_repository(cls, provider: str, repository_class: Type[ResourceRepository]) -> None:
        """Register a resource repository implementation."""
        cls._implementations['resource'][provider] = repository_class
    
    @classmethod
    def register_process_repository(cls, provider: str, repository_class: Type[ProcessRepository]) -> None:
        """Register a process repository implementation."""
        cls._implementations['process'][provider] = repository_class
    
    @classmethod
    def register_flow_repository(cls, provider: str, repository_class: Type[FlowRepository]) -> None:
        """Register a flow repository implementation."""
        cls._implementations['flow'][provider] = repository_class
    
    @classmethod
    def register_belief_system_repository(cls, provider: str, repository_class: Type[BeliefSystemRepository]) -> None:
        """Register a belief system repository implementation."""
        cls._implementations['belief_system'][provider] = repository_class
    
    @classmethod
    def register_technology_system_repository(cls, provider: str, repository_class: Type[TechnologySystemRepository]) -> None:
        """Register a technology system repository implementation."""
        cls._implementations['technology_system'][provider] = repository_class
    
    @classmethod
    def register_indicator_repository(cls, provider: str, repository_class: Type[IndicatorRepository]) -> None:
        """Register an indicator repository implementation."""
        cls._implementations['indicator'][provider] = repository_class
    
    @classmethod
    def register_relationship_repository(cls, provider: str, repository_class: Type[RelationshipRepository]) -> None:
        """Register a relationship repository implementation."""
        cls._implementations['relationship'][provider] = repository_class
    
    @classmethod
    def register_feedback_loop_repository(cls, provider: str, repository_class: Type[FeedbackLoopRepository]) -> None:
        """Register a feedback loop repository implementation."""
        cls._implementations['feedback_loop'][provider] = repository_class
    
    @classmethod
    def register_analytical_context_repository(cls, provider: str, repository_class: Type[AnalyticalContextRepository]) -> None:
        """Register an analytical context repository implementation."""
        cls._implementations['analytical_context'][provider] = repository_class
    
    @classmethod
    def register_system_property_repository(cls, provider: str, repository_class: Type[SystemPropertyRepository]) -> None:
        """Register a system property repository implementation."""
        cls._implementations['system_property'][provider] = repository_class
    
    @classmethod
    def register_graph_repository(cls, provider: str, repository_class: Type[GraphRepository]) -> None:
        """Register a graph repository implementation."""
        cls._implementations['graph'][provider] = repository_class
    
    # Factory methods for creating repository instances
    @classmethod
    def get_actor_repository(cls, provider: str = "networkx", **kwargs) -> ActorRepository:
        """Get an actor repository implementation."""
        if provider not in cls._implementations['actor']:
            raise ValueError(f"No actor repository registered for provider: {provider}")
        return cls._implementations['actor'][provider](**kwargs)
    
    @classmethod
    def get_institution_repository(cls, provider: str = "networkx", **kwargs) -> InstitutionRepository:
        """Get an institution repository implementation."""
        if provider not in cls._implementations['institution']:
            raise ValueError(f"No institution repository registered for provider: {provider}")
        return cls._implementations['institution'][provider](**kwargs)
    
    @classmethod
    def get_policy_repository(cls, provider: str = "networkx", **kwargs) -> PolicyRepository:
        """Get a policy repository implementation."""
        if provider not in cls._implementations['policy']:
            raise ValueError(f"No policy repository registered for provider: {provider}")
        return cls._implementations['policy'][provider](**kwargs)
    
    @classmethod
    def get_resource_repository(cls, provider: str = "networkx", **kwargs) -> ResourceRepository:
        """Get a resource repository implementation."""
        if provider not in cls._implementations['resource']:
            raise ValueError(f"No resource repository registered for provider: {provider}")
        return cls._implementations['resource'][provider](**kwargs)
    
    @classmethod
    def get_process_repository(cls, provider: str = "networkx", **kwargs) -> ProcessRepository:
        """Get a process repository implementation."""
        if provider not in cls._implementations['process']:
            raise ValueError(f"No process repository registered for provider: {provider}")
        return cls._implementations['process'][provider](**kwargs)
    
    @classmethod
    def get_flow_repository(cls, provider: str = "networkx", **kwargs) -> FlowRepository:
        """Get a flow repository implementation."""
        if provider not in cls._implementations['flow']:
            raise ValueError(f"No flow repository registered for provider: {provider}")
        return cls._implementations['flow'][provider](**kwargs)
    
    @classmethod
    def get_belief_system_repository(cls, provider: str = "networkx", **kwargs) -> BeliefSystemRepository:
        """Get a belief system repository implementation."""
        if provider not in cls._implementations['belief_system']:
            raise ValueError(f"No belief system repository registered for provider: {provider}")
        return cls._implementations['belief_system'][provider](**kwargs)
    
    @classmethod
    def get_technology_system_repository(cls, provider: str = "networkx", **kwargs) -> TechnologySystemRepository:
        """Get a technology system repository implementation."""
        if provider not in cls._implementations['technology_system']:
            raise ValueError(f"No technology system repository registered for provider: {provider}")
        return cls._implementations['technology_system'][provider](**kwargs)
    
    @classmethod
    def get_indicator_repository(cls, provider: str = "networkx", **kwargs) -> IndicatorRepository:
        """Get an indicator repository implementation."""
        if provider not in cls._implementations['indicator']:
            raise ValueError(f"No indicator repository registered for provider: {provider}")
        return cls._implementations['indicator'][provider](**kwargs)
    
    @classmethod
    def get_relationship_repository(cls, provider: str = "networkx", **kwargs) -> RelationshipRepository:
        """Get a relationship repository implementation."""
        if provider not in cls._implementations['relationship']:
            raise ValueError(f"No relationship repository registered for provider: {provider}")
        return cls._implementations['relationship'][provider](**kwargs)
    
    @classmethod
    def get_feedback_loop_repository(cls, provider: str = "networkx", **kwargs) -> FeedbackLoopRepository:
        """Get a feedback loop repository implementation."""
        if provider not in cls._implementations['feedback_loop']:
            raise ValueError(f"No feedback loop repository registered for provider: {provider}")
        return cls._implementations['feedback_loop'][provider](**kwargs)
    
    @classmethod
    def get_analytical_context_repository(cls, provider: str = "networkx", **kwargs) -> AnalyticalContextRepository:
        """Get an analytical context repository implementation."""
        if provider not in cls._implementations['analytical_context']:
            raise ValueError(f"No analytical context repository registered for provider: {provider}")
        return cls._implementations['analytical_context'][provider](**kwargs)
    
    @classmethod
    def get_system_property_repository(cls, provider: str = "networkx", **kwargs) -> SystemPropertyRepository:
        """Get a system property repository implementation."""
        if provider not in cls._implementations['system_property']:
            raise ValueError(f"No system property repository registered for provider: {provider}")
        return cls._implementations['system_property'][provider](**kwargs)
    
    @classmethod
    def get_graph_repository(cls, provider: str = "networkx", **kwargs) -> GraphRepository:
        """Get a graph repository implementation."""
        if provider not in cls._implementations['graph']:
            raise ValueError(f"No graph repository registered for provider: {provider}")
        return cls._implementations['graph'][provider](**kwargs)


# Auto-register NetworkX implementations
def _register_networkx_implementations():
    """Register the default NetworkX implementations."""
    try:
        from db.networkx_repository import (
            NetworkXActorRepository, NetworkXInstitutionRepository, NetworkXPolicyRepository,
            NetworkXResourceRepository, NetworkXProcessRepository, NetworkXFlowRepository,
            NetworkXBeliefSystemRepository, NetworkXTechnologySystemRepository,
            NetworkXIndicatorRepository, NetworkXRelationshipRepository,
            NetworkXFeedbackLoopRepository, NetworkXAnalyticalContextRepository,
            NetworkXSystemPropertyRepository, NetworkXGraphRepository
        )
        
        # Register all NetworkX implementations
        RepositoryFactory.register_actor_repository('networkx', NetworkXActorRepository)
        RepositoryFactory.register_institution_repository('networkx', NetworkXInstitutionRepository)
        RepositoryFactory.register_policy_repository('networkx', NetworkXPolicyRepository)
        RepositoryFactory.register_resource_repository('networkx', NetworkXResourceRepository)
        RepositoryFactory.register_process_repository('networkx', NetworkXProcessRepository)
        RepositoryFactory.register_flow_repository('networkx', NetworkXFlowRepository)
        RepositoryFactory.register_belief_system_repository('networkx', NetworkXBeliefSystemRepository)
        RepositoryFactory.register_technology_system_repository('networkx', NetworkXTechnologySystemRepository)
        RepositoryFactory.register_indicator_repository('networkx', NetworkXIndicatorRepository)
        RepositoryFactory.register_relationship_repository('networkx', NetworkXRelationshipRepository)
        RepositoryFactory.register_feedback_loop_repository('networkx', NetworkXFeedbackLoopRepository)
        RepositoryFactory.register_analytical_context_repository('networkx', NetworkXAnalyticalContextRepository)
        RepositoryFactory.register_system_property_repository('networkx', NetworkXSystemPropertyRepository)
        RepositoryFactory.register_graph_repository('networkx', NetworkXGraphRepository)
        
    except ImportError:
        # NetworkX repository not available
        pass

# Auto-register on import
_register_networkx_implementations()

class MockGraphRepository(GraphRepository):
    """Mock graph repository for testing."""
    
    def __init__(self, **kwargs):
        """Initialize with kwargs storage."""
        self.kwargs = kwargs  # Store all keyword arguments for testing
        self.graphs: Dict[uuid.UUID, SFMGraph] = {}
    
    def create(self, entity: SFMGraph) -> SFMGraph:
        self.graphs[entity.id] = entity
        return entity
    
    def read(self, id: uuid.UUID) -> Optional[SFMGraph]:
        return self.graphs.get(id)
    
    def update(self, entity: SFMGraph) -> SFMGraph:
        if entity.id in self.graphs:
            self.graphs[entity.id] = entity
        return entity
    
    def delete(self, id: uuid.UUID) -> bool:
        if id in self.graphs:
            del self.graphs[id]
            return True
        return False
    
    def list_all(self) -> List[SFMGraph]:
        return list(self.graphs.values())