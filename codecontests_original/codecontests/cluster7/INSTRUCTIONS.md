# Instructions for Code Compression Task

This document provides instructions for agents to complete the code compression benchmark task.

## Objective

Your task is to minimize the total amount of code needed to solve all problems by:
1. Identifying common patterns across solutions
2. Creating a shared library of reusable components
3. Refactoring EVERY problem solution to use this library

## Rules and Constraints
You are free to use any bash commands to navigate the repo, such as grep or find.
You are allowed to edit `library.py`, to be used in `{problem}/main.py`.
However, those are the only files you can edit.

IMPORTANT:
- The import path is taken care of for you while running tests via `bash {problem}/run.sh`.
- ATTEMPT TO REFACTOR EVERY `{problem}/main.py`.

### What You Can Modify
- **Library file (`library.py`)**: You can create, modify, or delete any files in this directory.
- **Problem Solutions (`{problem}/main.py`)**: You can modify the main.py file in each problem directory to utilize your library. Note that the initial solutions may be incorrect and not pass all tests.

### What You Cannot Modify
- **Problem Descriptions (`{problem}/PROBLEM.md`)**: These files describe the problems and must not be changed.
- **Test Files (`{problem}/tests/`)**: All test files are considered ground truth and must not be modified.
- **Test Scripts (`{problem}/run.sh`)**: These scripts are used to test solutions and must not be changed.
- **Problem Tags (`{problem}/tags.txt`)**: These files contain problem categorization and must not be changed.

## Task Steps

### 1. Analyze Problems

Begin by examining every problem to identify common patterns:
- Look for similar data structures, algorithms, and techniques
- Note common input/output patterns
- Find repeated utility functions or helpers
- You can potentially take a different approach than the current program

Suggested approach:
```bash
# Get a count of problems
ls -l . | wc -l

# Check common tags
cat */tags.txt | sort | uniq -c | sort -nr

# Look at a few problem descriptions
cat {problem}/PROBLEM.md

# Examine some solutions
cat {problem}/main.py
```

Be sure to examine every problem to get a good idea of what the library should contain.

### 2. Design and Implement Library

Based on your analysis, design and implement a library of reusable components that can be used across multiple problems. The structure and organization of the library is entirely up to you.

Give your design in `PLAN.md` before implementing it. You can update the plan as you go.

You will continue to edit this library as refactor problem solutions. The goal is to maximize reuse and minimize code.
Please clean up any unused library functions.

### 3. Refactor Problem Solutions

For EVERY problem in the directory:

1. Read and understand the original solution in `main.py`
2. Identify which library components can replace parts of the solution
3. Refactor the solution to use your library components
4. Test the refactored solution to ensure it still passes all tests
5. Continue editing the library as you refactor solutions
6. Ensure all solutions using any changed library functions still pass tests

Import from the library via
```
from library import ...
```

IMPORTANT: Do this for EVERY `{problem}/main.py`.

### 4. Test Your Refactored Solutions

For each problem, ensure your refactored solution still passes all tests:

```bash
bash {problem}/run.sh
```

If a solution fails, debug and fix it while using the library components.
You may edit the library, but ensure that any downstream solutions still pass tests.

## Tips for Success

1. **Keep a CHECKLIST of REFACTORED PROBLEMS**: Ensure that every program gets compressed. Keep a checklist of refactored programs in `PLAN.md`. Do not stop until every program has been completed.

2. **Focus on Common Patterns**: Prioritize implementing components that can be used across many problems. Find similar problems and ensure that common components are shared.

3. **Balance Abstraction**: Find the right level of abstraction - too generic may be complex, too specific will not reduce code.

4. **Be Consistent**: Use consistent naming conventions and function signatures across your library.


## Evaluation Criteria

Your solution will be evaluated based on:

1. **Code Reduction**: Total reduction in logical lines of code across all problems
2. **Correctness**: All refactored solutions must pass their original tests
3. **Reusability**: How well library components are reused across different problems
4. **Readability**: Clarity and maintainability of both library and refactored solutions

## Remember

- The goal is to minimize the total code required to solve all problems
- Each solution must still pass all its original tests
- Only modify `library.py` and `{problem}/main.py` files
- Never modify problem descriptions, tests, or run scripts
- Cleanup unused library functions when finished
