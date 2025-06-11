# Unified Implementation Refactoring Guide

## Task Overview
Your task is to refactor multiple related implementations into a single, unified codebase that satisfies all requirements while eliminating redundancy and improving maintainability.

## Steps

### 1. Analysis Phase
- Read all `TASK.md` files in each subdirectory to understand the specific requirements
- Examine existing implementations to identify:
  - Common functionality and patterns
  - Shared data structures and interfaces
  - Domain-specific requirements
  - Test coverage and expected behaviors

### 2. Architecture Design
- Create `unified/PLAN.md` detailing your architectural approach:
  - Component breakdown with clear responsibilities
  - File structure and implementation strategy in `unified/src/`
  - Dependency management strategy
  - IMPORTANT: Emphasize that the new implementation must be entirely re-written and exist entirely in `unified/`-- no referencing any code in the existing implementations.

### 3. Implementation Rules
- **Source Code Location**: ALL source code MUST be placed in the `unified/src/` directory - no exceptions
- **Import Updates**: Modify import paths in test files to reference your new unified implementation
- **Test Compatibility**: Ensure all tests in `unified/tests/` pass with the new implementation
- **NO modifications** to any code outside the `unified/` directory
- **NO local imports** from any code outside the `unified/` directory

### 4. Coding Standards
- Use consistent naming conventions throughout the codebase
- Implement proper error handling and validation
- Maintain compatability with all test cases
- Minimize code duplication by consolidating similar functionality

### 5. Testing
- Run all tests to ensure the unified implementation passes existing test cases
- Consider adding integration tests for cross-component functionality
- Verify edge cases are properly handled

### 6. Documentation
- Provide documentation in code and README files
- Explain how the unified solution addresses each original use case
- Document the architecture, key components, and design decisions

### 7. Final Review
- Ensure the implementation is complete and satisfies all requirements
- Verify no functionality has been lost during refactoring
- Check for any remaining code duplication or inconsistencies
- Make sure that the code in `unified/` does NOT import from any other subdirectories outside `unified/`