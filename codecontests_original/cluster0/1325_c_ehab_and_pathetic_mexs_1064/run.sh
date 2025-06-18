#!/bin/bash
# Test script for 1325_c_ehab_and_pathetic_mexs_1064

# Get the absolute path to the problem directory
PROBLEM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLUSTER_DIR="$(cd "$PROBLEM_DIR/.." && pwd)"

# Import paths - include both repo root and cluster directory
# This allows importing from problems/cluster{i}/library.py with: from library import *
export PYTHONPATH="$CLUSTER_DIR:$PYTHONPATH"

# Default to main.py if no specific file is provided
SOLUTION_FILE=${1:-"$PROBLEM_DIR/main.py"}

# Function to run a test case
run_test() {
    local test_num=$1
    local input_file="$PROBLEM_DIR/tests/input_${test_num}.txt"
    local expected_file="$PROBLEM_DIR/tests/output_${test_num}.txt"

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
    if [ "$(echo "$OUTPUT" | sed -e 's/[ \t]*$//')" = "$(echo "$EXPECTED" | sed -e 's/[ \t]*$//')" ]; then
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
}

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
