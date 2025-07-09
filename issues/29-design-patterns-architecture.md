# Design Pattern and Architecture Improvements

## Issue Summary
While the SFM framework has good foundational design patterns, several architectural improvements would enhance maintainability, extensibility, and robustness. This issue addresses missing design patterns and architectural refinements.

## Missing Design Patterns

### 1. Observer Pattern for Graph Changes
**Problem**: No notification mechanism for graph modifications
**Current State**: Direct mutations without change notifications
```python
# Current approach - no change tracking
def add_node(self, node: Node) -> Node:
    collection = getattr(self, collection_name)
    collection[node.id] = node
    # No notification of change
```

**Proposed Implementation**:
```python
class GraphChangeObserver(ABC):
    @abstractmethod
    def on_node_added(self, node: Node) -> None: pass
    
    @abstractmethod
    def on_node_removed(self, node_id: uuid.UUID) -> None: pass
    
    @abstractmethod
    def on_relationship_added(self, rel: Relationship) -> None: pass

class SFMGraph:
    def __init__(self):
        self._observers: List[GraphChangeObserver] = []
    
    def add_observer(self, observer: GraphChangeObserver) -> None:
        self._observers.append(observer)
    
    def _notify_node_added(self, node: Node) -> None:
        for observer in self._observers:
            observer.on_node_added(node)
```

### 2. Command Pattern for Undo/Redo Operations
**Problem**: No way to undo complex operations or track command history
**Impact**: Users cannot recover from mistakes, no operation history

**Proposed Implementation**:
```python
class Command(ABC):
    @abstractmethod
    def execute(self) -> Any: pass
    
    @abstractmethod
    def undo(self) -> Any: pass
    
    @abstractmethod
    def can_undo(self) -> bool: pass

class AddNodeCommand(Command):
    def __init__(self, graph: SFMGraph, node: Node):
        self.graph = graph
        self.node = node
        
    def execute(self) -> Node:
        return self.graph.add_node(self.node)
        
    def undo(self) -> bool:
        return self.graph.remove_node(self.node.id)

class CommandManager:
    def __init__(self, max_history: int = 100):
        self._history: List[Command] = []
        self._current_index = -1
        self._max_history = max_history
    
    def execute(self, command: Command) -> Any:
        result = command.execute()
        self._add_to_history(command)
        return result
    
    def undo(self) -> bool:
        if self.can_undo():
            command = self._history[self._current_index]
            success = command.undo()
            if success:
                self._current_index -= 1
            return success
        return False
```

### 3. Strategy Pattern for Query Algorithms
**Problem**: Query algorithms are hardcoded, difficult to extend or swap
**Current State**: Single implementation per query type

**Proposed Implementation**:
```python
class CentralityStrategy(ABC):
    @abstractmethod
    def calculate(self, graph: nx.Graph, node_id: uuid.UUID) -> float: pass

class BetweennessCentralityStrategy(CentralityStrategy):
    def calculate(self, graph: nx.Graph, node_id: uuid.UUID) -> float:
        centrality_scores = nx.betweenness_centrality(graph)
        return centrality_scores.get(node_id, 0.0)

class EigenvectorCentralityStrategy(CentralityStrategy):
    def calculate(self, graph: nx.Graph, node_id: uuid.UUID) -> float:
        try:
            centrality_scores = nx.eigenvector_centrality(graph)
            return centrality_scores.get(node_id, 0.0)
        except nx.NetworkXError:
            return 0.0

class CentralityAnalyzer:
    def __init__(self):
        self._strategies: Dict[str, CentralityStrategy] = {
            "betweenness": BetweennessCentralityStrategy(),
            "eigenvector": EigenvectorCentralityStrategy(),
        }
    
    def calculate_centrality(self, graph: nx.Graph, node_id: uuid.UUID, 
                           strategy_name: str) -> float:
        strategy = self._strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Unknown centrality strategy: {strategy_name}")
        return strategy.calculate(graph, node_id)
```

### 4. Decorator Pattern for Validation and Logging
**Problem**: Cross-cutting concerns (validation, logging, caching) scattered throughout code
**Current State**: Manual validation and logging in each method

**Proposed Implementation**:
```python
def validate_inputs(validator_func):
    """Decorator to validate method inputs."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not validator_func(*args, **kwargs):
                raise ValidationError(f"Input validation failed for {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

def audit_operation(operation_type: str):
    """Decorator to log operations for audit trail."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            try:
                result = func(self, *args, **kwargs)
                self._audit_logger.log_success(operation_type, func.__name__, 
                                             time.time() - start_time, args, kwargs)
                return result
            except Exception as e:
                self._audit_logger.log_failure(operation_type, func.__name__, 
                                             time.time() - start_time, str(e))
                raise
        return wrapper
    return decorator

def cache_result(ttl: int = 3600):
    """Decorator to cache method results."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{func.__name__}:{hash(args)}:{hash(frozenset(kwargs.items()))}"
            cached_result = self._cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            result = func(self, *args, **kwargs)
            self._cache.set(cache_key, result, ttl)
            return result
        return wrapper
    return decorator

# Usage example:
class SFMService:
    @validate_inputs(lambda self, request: isinstance(request, CreateActorRequest))
    @audit_operation("CREATE_ACTOR")
    @cache_result(ttl=1800)
    def create_actor(self, request: CreateActorRequest) -> NodeResponse:
        # Implementation
        pass
```

## Architectural Improvements

### 1. Plugin Architecture for Extensions
**Problem**: Framework is not easily extensible for domain-specific needs
**Proposed Solution**: Plugin system for custom entities, relationships, and analysis

```python
class SFMPlugin(ABC):
    @abstractmethod
    def get_name(self) -> str: pass
    
    @abstractmethod
    def get_version(self) -> str: pass
    
    @abstractmethod
    def register_entities(self) -> List[Type[Node]]: pass
    
    @abstractmethod
    def register_relationships(self) -> List[RelationshipKind]: pass
    
    @abstractmethod
    def register_analyzers(self) -> Dict[str, Any]: pass

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, SFMPlugin] = {}
        self._entity_registry: Dict[str, Type[Node]] = {}
    
    def register_plugin(self, plugin: SFMPlugin) -> None:
        self._plugins[plugin.get_name()] = plugin
        for entity_type in plugin.register_entities():
            self._entity_registry[entity_type.__name__] = entity_type
```

### 2. Event-Driven Architecture
**Problem**: Tight coupling between components, difficult to add new features
**Proposed Solution**: Event bus for loose coupling

```python
class Event:
    def __init__(self, event_type: str, data: Dict[str, Any], timestamp: datetime = None):
        self.event_type = event_type
        self.data = data
        self.timestamp = timestamp or datetime.now()

class EventHandler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None: pass

class EventBus:
    def __init__(self):
        self._handlers: Dict[str, List[EventHandler]] = defaultdict(list)
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)
    
    def publish(self, event: Event) -> None:
        for handler in self._handlers[event.event_type]:
            try:
                handler.handle(event)
            except Exception as e:
                logger.error(f"Error in event handler: {e}")

# Example usage:
class PolicyImpactAnalyzer(EventHandler):
    def handle(self, event: Event) -> None:
        if event.event_type == "POLICY_ADDED":
            self.analyze_impact(event.data["policy_id"])
```

### 3. Dependency Injection Container
**Problem**: Hard-coded dependencies, difficult testing and configuration
**Current State**: Manual dependency management

**Proposed Solution**:
```python
class DIContainer:
    def __init__(self):
        self._services: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
    
    def register_singleton(self, service_type: Type[T], instance: T) -> None:
        self._services[service_type] = instance
    
    def register_factory(self, service_type: Type[T], factory: Callable[[], T]) -> None:
        self._factories[service_type] = factory
    
    def get(self, service_type: Type[T]) -> T:
        if service_type in self._services:
            return self._services[service_type]
        
        if service_type in self._factories:
            instance = self._factories[service_type]()
            self._services[service_type] = instance
            return instance
        
        raise ValueError(f"Service {service_type} not registered")

# Configuration:
container = DIContainer()
container.register_singleton(SFMGraph, SFMGraph())
container.register_factory(SFMQueryEngine, lambda: NetworkXSFMQueryEngine(container.get(SFMGraph)))
```

### 4. Repository Pattern Enhancement
**Problem**: Data access logic mixed with business logic
**Current State**: Basic repository pattern, could be enhanced

**Proposed Enhancement**:
```python
class UnitOfWork:
    def __init__(self, repository_factory: RepositoryFactory):
        self._factory = repository_factory
        self._repositories: Dict[Type, Any] = {}
        self._transaction_active = False
    
    def __enter__(self):
        self._begin_transaction()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._commit_transaction()
        else:
            self._rollback_transaction()
    
    def get_repository(self, entity_type: Type[T]) -> Repository[T]:
        if entity_type not in self._repositories:
            self._repositories[entity_type] = self._factory.create(entity_type)
        return self._repositories[entity_type]
```

## Implementation Priority

### Phase 1 - Core Patterns (Week 1-2)
- Implement Observer pattern for graph changes
- Add Decorator pattern for cross-cutting concerns
- Create basic event bus architecture

### Phase 2 - Extensibility (Week 2-3)
- Implement Command pattern for undo/redo
- Add Strategy pattern for query algorithms
- Create plugin architecture foundation

### Phase 3 - Advanced Architecture (Week 3-4)
- Implement dependency injection container
- Enhance repository pattern with Unit of Work
- Add comprehensive event-driven features

## Benefits

### Maintainability
- Cleaner separation of concerns
- Easier to modify and extend functionality
- Better testability with dependency injection

### Extensibility
- Plugin system allows domain-specific extensions
- Strategy pattern enables algorithm swapping
- Event-driven architecture supports loose coupling

### Robustness
- Command pattern enables operation recovery
- Observer pattern provides change tracking
- Decorators add consistent cross-cutting functionality

## Testing Strategy

### Pattern Testing
- Unit tests for each design pattern implementation
- Integration tests for pattern interactions
- Performance tests to ensure patterns don't degrade performance

### Architecture Testing
- Plugin loading and registration tests
- Event bus reliability and performance tests
- Dependency injection container tests

## Acceptance Criteria
- [ ] Observer pattern implemented for all graph changes
- [ ] Command pattern supports undo/redo for major operations
- [ ] Strategy pattern allows pluggable algorithms
- [ ] Decorator pattern handles validation and logging consistently
- [ ] Plugin architecture supports custom extensions
- [ ] Event-driven architecture reduces coupling
- [ ] Dependency injection improves testability
- [ ] Performance impact <5% for pattern overhead

## Priority
🔶 **MEDIUM** - Important for long-term maintainability

## Dependencies
- Core functionality completion (Issues 24-27)
- Testing infrastructure improvements
- Documentation updates

## Related Issues
- Links to all core functionality issues
- Links to extensibility requirements
- Links to testing and documentation needs
