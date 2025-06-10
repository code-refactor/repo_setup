"""
Generate run.sh test scripts for problems.

This module creates executable test scripts for each problem that:
1. Set up the correct Python path for importing from the library
2. Run the solution against test cases
3. Validate outputs against expected results
"""

import os
import stat
from pathlib import Path

# Script template
SCRIPT_TEMPLATE = """#!/bin/bash
# Test script for {problem_id}

# Get the absolute path to the problem directory
PROBLEM_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
CLUSTER_DIR="$(cd "$PROBLEM_DIR/.." && pwd)"

# Import paths - include both repo root and cluster directory
# This allows importing from problems/cluster{{i}}/library.py with: from library import *
export PYTHONPATH="$CLUSTER_DIR:$PYTHONPATH"

# Default to main.py if no specific file is provided
SOLUTION_FILE=${{1:-"$PROBLEM_DIR/main.py"}}

# Function to run a test case
run_test() {{
    local test_num=$1
    local input_file="$PROBLEM_DIR/tests/input_${{test_num}}.txt"
    local expected_file="$PROBLEM_DIR/tests/output_${{test_num}}.txt"

    if [ ! -f "$input_file" ]; then
        echo "Test #$test_num: Input file not found!"
        return 1
    fi

    if [ ! -f "$expected_file" ]; then
        echo "Test #$test_num: Expected output file not found!"
        return 1
    fi

    echo "Running test #$test_num..."

    # Run the solution with the test input using python
    OUTPUT=$(python "$SOLUTION_FILE" < "$input_file")
    EXIT_CODE=$?

    if [ $EXIT_CODE -ne 0 ]; then
        echo "Test #$test_num: Error running solution! Exit code: $EXIT_CODE"
        return 1
    fi

    # Read expected output
    EXPECTED=$(cat "$expected_file")

    # Compare outputs (ignoring trailing whitespace)
    if [ "$(echo "$OUTPUT" | sed -e 's/[ \\t]*$//')" = "$(echo "$EXPECTED" | sed -e 's/[ \\t]*$//')" ]; then
        echo "Test #$test_num: PASSED ✅"
        return 0
    else
        echo "Test #$test_num: FAILED ❌"
        echo "Expected:"
        echo "$EXPECTED"
        echo "Got:"
        echo "$OUTPUT"
        return 1
    fi
}}

# Count test files
NUM_TESTS=$(ls "$PROBLEM_DIR/tests/input_"*.txt 2>/dev/null | wc -l)

if [ $NUM_TESTS -eq 0 ]; then
    echo "No test cases found!"
    exit 1
fi

# Run all tests
PASSED=0
TOTAL=$NUM_TESTS

for ((i=1; i<=$NUM_TESTS; i++)); do
    if run_test $i; then
        PASSED=$((PASSED+1))
    fi
done

echo "Results: $PASSED/$TOTAL tests passed"
echo "$PASSED/$TOTAL" > $PROBLEM_DIR/results.txt

if [ $PASSED -eq $TOTAL ]; then
    exit 0
else
    exit 1
fi
"""


def generate_run_script(problem_id: str, output_dir: Path) -> Path:
    """
    Generate a run.sh script for testing a specific problem.

    Args:
        problem_id: The ID of the problem
        output_dir: The problem directory where the script will be written

    Returns:
        Path to the generated script
    """
    # Customize for the problem
    script_content = SCRIPT_TEMPLATE.format(problem_id=problem_id)

    # Write the script
    script_path = output_dir / "run.sh"
    with open(script_path, "w") as f:
        f.write(script_content)

    # Make the script executable
    os.chmod(
        script_path,
        os.stat(script_path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
    )

    return script_path


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) != 3:
        print("Usage: python script_sh.py problem_id output_dir")
        sys.exit(1)

    problem_id = sys.argv[1]
    output_dir = Path(sys.argv[2])

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    script_path = generate_run_script(problem_id, output_dir)
    print(f"Generated test script at: {script_path}")
