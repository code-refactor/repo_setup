# Unified Command Line Task Manager - Refactoring Plan

## Overview

This document outlines the architecture and migration plan for creating a unified library from two persona-specific implementations: Research Track (`researchtrack`) and Security Task Manager (`securetask`). The goal is to extract common functionality into a shared `common` library while preserving persona-specific features.

## Current State Analysis

### Existing Implementations

1. **Research Track (`researchtrack/`)**: Academic research-focused task management with bibliography, experiment tracking, dataset versioning, and export capabilities.

2. **Security Task Manager (`securetask/`)**: Security analyst-focused task management with findings, evidence management, compliance tracking, and reporting with redaction.

### Common Patterns Identified

Both implementations share significant patterns that can be abstracted:

- **Base Entity Pattern**: Pydantic BaseModel with common fields (id, timestamps, tags, notes, metadata)
- **CRUD Service Pattern**: Create, Read, Update, Delete operations with consistent interfaces
- **Storage Interface Pattern**: Abstract storage with in-memory implementations
- **Association Management**: Entity linking through UUID references
- **Filtering and Search**: Complex query capabilities
- **Validation Patterns**: Pydantic validators and custom validation logic

## Unified Library Architecture

### Core Components

#### `common/core/`

**1. `models.py` - Base Entity Framework**
```python
# Base classes for entities
- BaseEntity: Common fields and methods for all entities
- BaseLink: Pattern for entity associations
- BaseEnum: String-based enumeration pattern
- BaseVersion: Versioning support for entities
```

**2. `storage.py` - Storage Interface Framework**
```python
# Storage abstractions
- BaseStorageInterface: Generic CRUD interface
- InMemoryStorage: Base in-memory implementation
- StorageException: Storage-specific exceptions
- FilterQuery: Query builder for filtering
```

**3. `service.py` - Service Layer Framework**
```python
# Service patterns
- BaseService: Generic service with CRUD operations
- ServiceRegistry: Dependency injection container
- ValidationMixin: Common validation patterns
- AssociationMixin: Entity relationship management
```

**4. `exceptions.py` - Common Exception Hierarchy**
```python
# Exception classes
- EntityNotFoundError
- ValidationError
- StorageError
- ServiceError
```

#### `common/utils/`

**1. `validation.py` - Validation Utilities**
```python
# Validation helpers
- field_validators: Common field validation functions
- custom_validators: Reusable validator decorators
- error_formatting: Consistent error message formatting
```

**2. `serialization.py` - Serialization Utilities**
```python
# Serialization support
- json_serializer: Enhanced JSON encoding/decoding
- datetime_utils: DateTime handling utilities
- uuid_utils: UUID generation and validation
```

**3. `filtering.py` - Query and Filter Utilities**
```python
# Query building
- FilterBuilder: Dynamic query construction
- SortOptions: Sorting configuration
- PaginationOptions: Pagination support
```

#### `common/patterns/`

**1. `associations.py` - Entity Association Patterns**
```python
# Association management
- LinkEntity: Base class for entity links
- AssociationManager: Bidirectional relationship management
- ReferenceValidator: Reference integrity validation
```

**2. `metadata.py` - Metadata Management**
```python
# Metadata handling
- MetadataManager: Custom metadata operations
- MetadataValidator: Metadata validation
- MetadataSerializer: Metadata serialization
```

**3. `versioning.py` - Entity Versioning**
```python
# Version control
- VersionManager: Entity version tracking
- VersionComparator: Version comparison utilities
- ChangeTracker: Change detection and logging
```

## Migration Strategy

### Phase 1: Common Library Implementation

1. **Create Base Models**
   - Implement `BaseEntity` with common fields and methods
   - Create base enumeration and link patterns
   - Implement version tracking support

2. **Implement Storage Framework**
   - Create `BaseStorageInterface` with generic CRUD operations
   - Implement `InMemoryStorage` base class
   - Add filtering and query support

3. **Build Service Framework**
   - Create `BaseService` with common operations
   - Implement validation and association mixins
   - Add service registry for dependency injection

4. **Add Utilities**
   - Implement validation helpers
   - Create serialization utilities
   - Build filtering and query utilities

### Phase 2: Research Track Migration

1. **Model Migration**
   - Migrate `Task`, `Reference`, `Dataset`, `Environment`, `Experiment` to inherit from `BaseEntity`
   - Update link entities to use `BaseLink` pattern
   - Preserve research-specific fields and methods

2. **Service Migration**
   - Refactor services to inherit from `BaseService`
   - Move common CRUD operations to base class
   - Preserve research-specific business logic

3. **Storage Migration**
   - Update storage classes to implement `BaseStorageInterface`
   - Utilize common filtering and query capabilities
   - Maintain backward compatibility

### Phase 3: Security Task Migration

1. **Model Migration**
   - Migrate `Finding`, `Evidence`, `ComplianceItem` to inherit from `BaseEntity`
   - Adapt security-specific models to use common patterns
   - Preserve encryption and security features

2. **Service Migration**
   - Refactor services to inherit from `BaseService`
   - Integrate security-specific validation with common patterns
   - Maintain access control and security features

3. **Storage Migration**
   - Adapt encrypted storage to implement `BaseStorageInterface`
   - Integrate security features with common storage patterns
   - Preserve data integrity and encryption

### Phase 4: Integration and Testing

1. **Integration Testing**
   - Verify all existing tests pass
   - Test cross-persona compatibility
   - Validate performance benchmarks

2. **Performance Optimization**
   - Profile common operations
   - Optimize storage and query performance
   - Ensure memory efficiency

3. **Documentation Updates**
   - Update API documentation
   - Create migration guides
   - Document new common interfaces

## Interface Definitions

### Core Interfaces

```python
# BaseEntity Interface
class BaseEntity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    tags: Set[str]
    notes: List[str]
    custom_metadata: Dict[str, Any]
    
    def update(self, **kwargs) -> None
    def add_tag(self, tag: str) -> None
    def remove_tag(self, tag: str) -> None
    def add_note(self, note: str) -> None

# BaseStorage Interface
class BaseStorageInterface(ABC, Generic[T]):
    def create(self, entity: T) -> UUID
    def get(self, entity_id: UUID) -> Optional[T]
    def update(self, entity: T) -> bool
    def delete(self, entity_id: UUID) -> bool
    def list(self, filters: Optional[FilterQuery] = None) -> List[T]
    def count(self, filters: Optional[FilterQuery] = None) -> int

# BaseService Interface
class BaseService(Generic[T]):
    def __init__(self, storage: BaseStorageInterface[T])
    def create(self, **kwargs) -> T
    def get(self, entity_id: UUID) -> Optional[T]
    def update(self, entity_id: UUID, **kwargs) -> bool
    def delete(self, entity_id: UUID) -> bool
    def list(self, **filters) -> List[T]
```

## Extension Points

### Persona-Specific Customization

1. **Custom Fields**: Each persona can extend base entities with domain-specific fields
2. **Custom Validation**: Persona-specific validation rules through mixins
3. **Custom Storage**: Specialized storage implementations (e.g., encrypted storage)
4. **Custom Services**: Business logic extensions through service inheritance
5. **Custom Formatters**: Domain-specific serialization and formatting

### Configuration Points

1. **Storage Backend**: Configurable storage implementations
2. **Validation Rules**: Pluggable validation frameworks
3. **Serialization**: Customizable serialization strategies
4. **Security**: Configurable security policies

## Benefits of Unified Architecture

1. **Code Reduction**: ~40-50% reduction in duplicated code
2. **Consistency**: Standardized interfaces across personas
3. **Maintainability**: Single source of truth for common functionality
4. **Extensibility**: Clear extension points for new personas
5. **Testing**: Centralized testing of common functionality
6. **Performance**: Optimized common operations

## Risks and Mitigation

### Identified Risks

1. **Breaking Changes**: Migration might break existing functionality
   - *Mitigation*: Comprehensive test coverage and incremental migration

2. **Performance Regression**: Common abstraction might reduce performance
   - *Mitigation*: Performance benchmarking and optimization

3. **Over-Abstraction**: Too generic interfaces might limit persona-specific features
   - *Mitigation*: Careful interface design with clear extension points

4. **Complex Dependencies**: Circular dependencies between common and persona code
   - *Mitigation*: Clear dependency hierarchy and interface contracts

## Success Criteria

1. **All Tests Pass**: 100% test coverage maintained
2. **Performance Maintained**: No performance regression
3. **Code Reduction**: Significant reduction in duplicated code
4. **Backward Compatibility**: Existing API contracts preserved
5. **Documentation**: Complete documentation of new architecture

## Timeline

1. **Phase 1** (Common Library): ~40% of effort
2. **Phase 2** (Research Track): ~25% of effort  
3. **Phase 3** (Security Task): ~25% of effort
4. **Phase 4** (Integration): ~10% of effort

## Conclusion

This unified architecture will create a solid foundation for both existing personas while providing clear extension points for future personas. The migration strategy ensures minimal disruption while maximizing code reuse and maintainability.