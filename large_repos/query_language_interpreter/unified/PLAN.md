# Unified Query Language Interpreter - Refactoring Plan

## Executive Summary

This document outlines the plan for refactoring two domain-specific query language interpreters (Legal Discovery and Privacy Query) into a unified architecture with a shared common library. The goal is to eliminate 60-70% of code duplication while maintaining specialized functionality for each domain.

## Current State Analysis

### Persona Implementations
1. **Legal Discovery Interpreter** (`legal_discovery_interpreter/`): Handles legal document discovery, privilege detection, and compliance with legal procedures
2. **Privacy Query Interpreter** (`privacy_query_interpreter/`): Manages personal data queries, PII detection, and privacy regulation compliance

### Identified Common Functionality (60-70% overlap)
**Already Unified in Common Library:**
- ✅ Query framework with BaseQueryExecutor and BaseQueryParser interfaces
- ✅ Shared data models (Document, AuditEvent, PolicyDecision, QueryExecutionContext)
- ✅ Audit system with unified logging and metrics collection
- ✅ Content processor with document analysis capabilities
- ✅ Policy engine with rule evaluation framework
- ✅ Comprehensive utility functions (text processing, crypto, datetime)

**Requires Migration:**
- Persona-specific query engines need to use common framework
- Document analysis modules should extend common content processor
- Policy enforcement should use unified policy engine
- Audit logging needs integration with common audit system

## Unified Architecture Design

### Core Components Structure

```
common/
├── core/
│   ├── __init__.py
│   ├── query_framework.py      # Universal query processing engine
│   ├── content_processor.py    # Document/data processing infrastructure
│   ├── audit_system.py         # Logging and audit infrastructure
│   ├── policy_engine.py        # Rule evaluation framework
│   └── models.py              # Shared data models and structures
├── utils/
│   ├── __init__.py
│   ├── text_processing.py     # Text analysis and pattern matching
│   ├── crypto.py              # Cryptographic functions (hashing, HMAC)
│   ├── datetime_utils.py      # Date/time handling utilities
│   └── config.py              # Configuration management
└── interfaces/
    ├── __init__.py
    ├── analyzer.py            # Content analyzer interface
    ├── detector.py            # Pattern detector interface
    ├── enforcer.py            # Policy enforcer interface
    └── logger.py              # Audit logger interface
```

## Component Specifications

### 1. Query Framework (`common/core/query_framework.py`)

**Responsibilities:**
- Parse SQL-like queries into AST structures
- Execute queries with pluggable business logic
- Manage query context and user sessions
- Handle query result standardization

**Key Classes:**
```python
class QueryParser:
    """Parse SQL-like queries into structured AST"""
    
class QueryExecutor:
    """Execute parsed queries with domain-specific logic"""
    
class QueryResult:
    """Standardized query result with metadata"""
    
class QueryContext:
    """User context, permissions, and session management"""
```

### 2. Content Processor (`common/core/content_processor.py`)

**Responsibilities:**
- Analyze text content and extract entities
- Process structured data fields with metadata
- Perform pattern matching and classification
- Handle document parsing and content extraction

**Key Classes:**
```python
class DocumentAnalyzer:
    """Base document analysis functionality"""
    
class FieldProcessor:
    """Structured data field processing"""
    
class PatternMatcher:
    """Regex and pattern matching utilities"""
    
class EntityExtractor:
    """Extract entities from content"""
```

### 3. Audit System (`common/core/audit_system.py`)

**Responsibilities:**
- Log data access events with context
- Maintain tamper-resistant audit trails
- Track performance metrics and usage
- Provide audit log search capabilities

**Key Classes:**
```python
class AccessLogger:
    """Standardized access logging"""
    
class AuditTrail:
    """Tamper-resistant audit chain management"""
    
class MetricsCollector:
    """Performance and usage metrics"""
    
class AuditSearcher:
    """Search and query audit logs"""
```

### 4. Policy Engine (`common/core/policy_engine.py`)

**Responsibilities:**
- Evaluate business rules and policies
- Make access control decisions
- Handle context-based policy evaluation
- Dispatch policy enforcement actions

**Key Classes:**
```python
class RuleEvaluator:
    """Base policy and rule evaluation"""
    
class ContextManager:
    """Manage user and request context"""
    
class DecisionEngine:
    """Make policy-based decisions"""
    
class ActionDispatcher:
    """Execute policy enforcement actions"""
```

### 5. Shared Models (`common/core/models.py`)

**Core Data Structures:**
```python
@dataclass
class BaseQuery:
    """Universal query representation"""
    
@dataclass  
class QueryResult:
    """Standardized result format"""
    
@dataclass
class UserContext:
    """Universal user context model"""
    
@dataclass
class AuditEvent:
    """Common audit event structure"""
    
@dataclass
class PolicyDecision:
    """Shared policy decision format"""
```

## Domain-Specific Extensions

### Legal Discovery Interpreter Extensions
- **Privilege Detection**: Attorney-client privilege, work product doctrine
- **Legal Ontology**: Legal term expansion and case law references
- **Discovery Procedures**: Court-specific discovery rules and workflows
- **Communication Analysis**: Email thread analysis for legal context
- **Document Production**: Legal document formatting and production

### Privacy Query Interpreter Extensions  
- **PII Detection**: Personal data identification patterns
- **Privacy Compliance**: GDPR, CCPA regulation compliance
- **Data Anonymization**: Hashing, masking, pseudonymization techniques
- **Privacy Policies**: Data usage policies and access restrictions
- **Data Minimization**: Purpose-based data access controls

## Migration Strategy

### Phase 1: Foundation Review (COMPLETED)
✅ Common library infrastructure already established
✅ Shared data models in `common/core/models.py`
✅ Utility functions in `common/utils/`
✅ Core framework components implemented

### Phase 2: Privacy Query Interpreter Migration 
1. **Query Engine Integration**:
   - Refactor `privacy_query_interpreter/query_engine/` to extend `BaseQueryExecutor`
   - Migrate query parsing to use common `BaseQueryParser`
   - Update result handling to use common `QueryResult` format

2. **PII Detection Integration**:
   - Extend common `ContentProcessor` for PII detection
   - Integrate with common audit system for PII access logging
   - Use common crypto utilities for anonymization

3. **Policy Enforcement Migration**:
   - Refactor policy enforcement to extend common `PolicyEngine`
   - Migrate access logging to common `AuditLogger`
   - Use common `PolicyDecision` models

### Phase 3: Legal Discovery Interpreter Migration
1. **Core Components Migration**:
   - Refactor `legal_discovery_interpreter/core/interpreter.py` to use common framework
   - Migrate query processing to extend `BaseQueryExecutor`
   - Update document models to extend common `Document` class

2. **Analysis Components Integration**:
   - Extend common `ContentProcessor` for legal document analysis
   - Integrate privilege detection with common policy engine
   - Unify temporal analysis with common datetime utilities

3. **Ontology and Communication Analysis**:
   - Maintain domain-specific ontology service
   - Integrate communication analysis with common audit system
   - Use common text processing utilities where applicable

### Phase 4: Testing and Validation
1. Run comprehensive test suite for both personas
2. Validate performance benchmarks
3. Ensure backward compatibility
4. Generate final test report

## Testing Strategy

### Test Requirements
- All existing tests must pass without modification
- Performance must meet or exceed original implementations
- Maintain exact behavioral compatibility
- Test common library components independently

### Test Execution
```bash
# Install in development mode
pip install -e .

# Run all tests with coverage
pytest tests/ --json-report --json-report-file=report.json --continue-on-collection-errors

# Run persona-specific tests
pytest tests/legal_discovery_specialist/
pytest tests/data_privacy_officer/
```

## Success Metrics

### Code Quality Metrics
- **Code Reduction**: Target 60-70% reduction in duplicate code
- **Test Coverage**: Maintain 100% test coverage
- **Performance**: Maintain or improve execution speed
- **Maintainability**: Clear separation of concerns and interfaces

### Functional Requirements  
- **Correctness**: All existing tests pass
- **Backward Compatibility**: No breaking changes to public APIs
- **Feature Completeness**: All persona-specific features preserved
- **Documentation**: Clear documentation for common library usage

## Risk Mitigation

### Technical Risks
- **Abstraction Complexity**: Keep interfaces simple and focused
- **Performance Regression**: Continuous benchmarking during refactoring
- **Integration Issues**: Incremental migration with frequent testing

### Delivery Risks
- **Scope Creep**: Focus strictly on refactoring, no new features
- **Test Failures**: Maintain test-first approach throughout migration
- **Compatibility**: Preserve existing APIs and behaviors exactly

## Implementation Timeline

1. **Phase 1-2** (Foundation & Query Framework): Establish core infrastructure
2. **Phase 3-4** (Content & Audit Systems): Unify processing components  
3. **Phase 5** (Policy Engine): Consolidate rule evaluation
4. **Phase 6** (Persona Migration): Refactor domain-specific implementations
5. **Testing & Validation**: Comprehensive test execution and validation

## Conclusion

This refactoring will create a robust, maintainable unified library that eliminates code duplication while preserving the specialized functionality required by each domain. The phased approach ensures minimal risk while maximizing code reuse and maintainability benefits.