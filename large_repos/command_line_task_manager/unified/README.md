# Unified Command Line Task Manager

A unified library for command line task management supporting multiple persona-specific implementations.

## Overview

This project provides a unified framework for task management with support for different personas and use cases. It consists of a common library providing shared functionality and persona-specific implementations that extend the base functionality.

## Architecture

### Common Library (`common/`)

The common library provides the foundational components that are shared across all persona implementations:

#### Core Components (`common/core/`)

- **BaseEntity**: Base class for all entities with common fields (id, timestamps, tags, notes, metadata)
- **StatusManagedEntity**: Enhanced entity with status management and change history tracking
- **AnnotatedEntity**: Entity with rich annotation capabilities for detailed documentation
- **StatusManagedAnnotatedEntity**: Combined status management and annotation capabilities
- **BaseEnum**: Base enumeration class with validation helpers
- **BaseService**: Generic service class providing CRUD operations and business logic patterns
- **StatusManagedService**: Enhanced service with status transition validation and hooks
- **AnnotationService**: Service for managing entity annotations
- **AssociationService**: Service for managing complex entity relationships
- **BaseStorageInterface**: Abstract storage interface with multiple implementations:
  - **InMemoryStorage**: Fast in-memory storage for development and testing
  - **SecureStorage**: Encrypted storage with field-level encryption
  - **IndexedStorage**: High-performance storage with secondary indices
  - **HybridStorage**: Combined encryption and indexing capabilities
- **Exception Classes**: Comprehensive exception hierarchy for error handling

#### Utilities (`common/utils/`)

- **Validation**: Field validators, rules, and validation utilities
- **Serialization**: JSON serialization with support for complex types (datetime, UUID, etc.)
- **Filtering**: Advanced query builder and filtering utilities with domain-specific patterns:
  - **QueryBuilder**: Basic filtering, sorting, and pagination
  - **AdvancedQueryBuilder**: Status history, annotation, and association filtering
  - **StatusQueryBuilder**: Specialized queries for status-managed entities
  - **AnnotationQueryBuilder**: Content search and annotation-specific filters

### Persona Implementations

#### Research Track (`researchtrack/`)

Specialized for academic research task management:

- **Bibliography Management**: Citation formatting, reference import/export
- **Dataset Versioning**: Version control for research datasets with lineage tracking
- **Environment Tracking**: Computational environment snapshots and comparison
- **Experiment Tracking**: Scientific experiment management with parameters and metrics
- **Export Capabilities**: Research artifact export in various formats
- **Task Management**: Research-specific task management with academic workflow support

#### Security Task Manager (`securetask/`)

Specialized for security analysis workflows:

- **Findings Management**: Security vulnerability tracking with CVSS scoring
- **Evidence Vault**: Encrypted evidence storage with access controls
- **Compliance Tracking**: Framework compliance management (SOC 2, NIST, etc.)
- **Remediation Workflow**: Security issue remediation tracking
- **Reporting**: Automated report generation with redaction capabilities
- **Cryptographic Security**: End-to-end encryption and data integrity verification

## Features

### Common Features

- **Entity Management**: Create, read, update, delete operations for all entity types
- **Status Management**: Built-in status tracking with change history and validation
- **Annotation System**: Rich annotation capabilities with authorship and timestamps
- **Tag System**: Flexible tagging for categorization and organization
- **Custom Metadata**: Extensible metadata fields for domain-specific information
- **Association Management**: Link entities across different modules with metadata
- **Search and Filtering**: Powerful query capabilities with multiple filter options
- **Advanced Queries**: Status history, annotation content, and association filtering
- **Serialization**: JSON import/export with type safety
- **Validation**: Comprehensive input validation with detailed error reporting
- **Secure Storage**: Optional field-level encryption for sensitive data
- **Performance Optimization**: Indexing and caching for large-scale operations

### Research-Specific Features

- **Academic Citations**: APA, MLA, Harvard, and IEEE citation formatting
- **Reference Import**: BibTeX and JSON bibliography import
- **Dataset Lineage**: Track dataset transformations and versioning
- **Environment Snapshots**: Capture and compare computational environments
- **Experiment Tracking**: Parameter logging, metric collection, and result analysis
- **Multi-format Export**: Export research artifacts to various academic formats

### Security-Specific Features

- **CVSS Scoring**: Automated CVSS v3.1 vulnerability scoring
- **Encrypted Storage**: AES-256 encryption for sensitive security data
- **Access Controls**: Role-based access to security findings and evidence
- **Compliance Mapping**: Map findings to compliance framework controls
- **Report Generation**: Automated security report creation with customizable templates
- **Data Redaction**: Intelligent redaction of sensitive information in reports

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd unified-command-line-task-manager

# Install dependencies
pip install -e .
```

## Usage

### Basic Entity Operations

```python
from common.core.models import BaseEntity
from common.core.service import BaseService
from common.core.storage import InMemoryStorage

# Create storage and service
storage = InMemoryStorage()
service = BaseService(storage, "MyEntity")

# Create entity
entity_data = {
    "title": "Example Task",
    "description": "This is an example",
    "tags": {"important", "example"}
}
entity = service.create(entity_data, MyEntityClass)

# Update entity
service.update(entity.id, {"description": "Updated description"})

# Query entities
entities = service.list(filters={"tags": {"important"}})
```

### Research Track Usage

```python
from researchtrack.task_management.service import TaskManagementService
from researchtrack.task_management.storage import InMemoryTaskStorage

# Initialize service
storage = InMemoryTaskStorage()
service = TaskManagementService(storage)

# Create research task
task_id = service.create_task(
    title="Literature Review",
    description="Systematic review of machine learning papers",
    priority=TaskPriority.HIGH,
    tags={"ml", "literature-review"}
)

# Create research question
question_id = service.create_research_question(
    text="How effective is transfer learning in NLP?",
    task_id=task_id
)
```

### Security Track Usage

```python
from securetask.findings.repository import FindingRepository
from securetask.findings.models import Finding

# Initialize repository
repo = FindingRepository()

# Create security finding
finding = Finding(
    title="SQL Injection Vulnerability",
    description="User input not properly sanitized",
    severity="high",
    affected_systems=["web-app-prod"],
    discovered_by="security-team"
)

finding_id = repo.create(finding)
```

## Testing

Run the complete test suite:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=common --cov=researchtrack --cov=securetask

# Generate JSON report
pytest tests/ --json-report --json-report-file=report.json
```

### Test Coverage

The project maintains comprehensive test coverage across all components:

- **416 total tests** covering all functionality
- **100% pass rate** ensuring reliability
- **Unit tests** for individual components
- **Integration tests** for cross-module functionality
- **Performance tests** for scalability validation

## Project Structure

```
.
├── common/                        # Shared functionality
│   ├── core/                      # Core abstractions
│   │   ├── models.py             # Base entity classes
│   │   ├── service.py            # Base service classes
│   │   ├── storage.py            # Storage interfaces
│   │   └── exceptions.py         # Exception classes
│   └── utils/                     # Utilities
│       ├── validation.py         # Validation helpers
│       ├── serialization.py      # JSON serialization
│       └── filtering.py          # Query utilities
├── researchtrack/                 # Research persona
│   ├── task_management/          # Research task management
│   ├── bibliography/             # Citation management
│   ├── dataset_versioning/       # Dataset version control
│   ├── environment/              # Environment tracking
│   ├── experiment_tracking/      # Experiment management
│   └── export/                   # Export functionality
├── securetask/                   # Security persona
│   ├── findings/                 # Security findings
│   ├── evidence/                 # Evidence management
│   ├── compliance/               # Compliance tracking
│   ├── remediation/              # Remediation workflow
│   ├── reporting/                # Report generation
│   ├── cvss/                     # CVSS scoring
│   └── utils/                    # Security utilities
├── tests/                        # Test suite
│   ├── researcher/              # Research track tests
│   └── security_analyst/        # Security track tests
├── PLAN.md                       # Architecture documentation
├── pyproject.toml               # Project configuration
└── README.md                    # This file
```

## Development

### Adding New Personas

To add a new persona implementation:

1. Create a new package directory (e.g., `newpersona/`)
2. Inherit from common base classes in `common.core`
3. Implement persona-specific models extending `BaseEntity`
4. Create services extending `BaseService`
5. Add comprehensive tests following existing patterns

### Extending Common Functionality

To extend the common library:

1. Add new base classes to `common/core/models.py`
2. Extend utilities in `common/utils/`
3. Update `__init__.py` files to export new functionality
4. Add tests to verify compatibility with existing personas

## Security Considerations

- **Encryption**: All sensitive data is encrypted using AES-256
- **Access Control**: Role-based access controls for sensitive operations
- **Data Integrity**: HMAC verification for data integrity
- **Input Validation**: Comprehensive validation to prevent injection attacks
- **Audit Logging**: Security operations are logged for compliance

## Performance

The unified architecture provides:

- **Efficient Storage**: In-memory storage with optional persistence
- **Optimized Queries**: Indexed search capabilities for large datasets
- **Lazy Loading**: Optional lazy loading for resource-intensive operations
- **Batch Operations**: Bulk operations for performance-critical workflows

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 1.0.0 (Current)

- ✅ **Unified Architecture**: Complete common library with enhanced base classes and utilities
- ✅ **Status Management**: Built-in status tracking with history and transition validation
- ✅ **Annotation System**: Rich annotation capabilities with content search
- ✅ **Advanced Storage**: Multiple storage implementations including encryption and indexing
- ✅ **Enhanced Filtering**: Domain-specific query builders for complex searches
- ✅ **Research Track**: Full academic research workflow support with status management
- ✅ **Security Track**: Comprehensive security analysis with enhanced annotation capabilities
- ✅ **Test Coverage**: 416 tests with 100% pass rate
- ✅ **Documentation**: Complete architecture and usage documentation

### Future Enhancements

- **Additional Personas**: Project management, software development workflows
- **Advanced Analytics**: Built-in analytics and reporting across personas
- **API Layer**: REST API for web and mobile integration
- **Plugin System**: Extensible plugin architecture for custom functionality