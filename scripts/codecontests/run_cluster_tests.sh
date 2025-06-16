#!/bin/bash
# Script to run all tests for a specific cluster with condensed output

# Check if cluster number is provided
if [ $# -lt 1 ] || [ $# -gt 2 ]; then
    echo "Usage: $0 <cluster_number> [problem_name]"
    echo "Example: $0 0          # Run all problems in cluster0"
    echo "Example: $0 0 1041_e   # Run only problems matching 1041_e in cluster0"
    exit 1
fi

CLUSTER_NUM=$1
CLUSTER_DIR="codecontests/cluster$CLUSTER_NUM"
FILTER_PATTERN=${2:-""}

# Get the base directory
BASE_DIR=$(pwd)

# Check if this cluster directory exists
if [ ! -d "$CLUSTER_DIR" ]; then
    echo "Error: Cluster directory $CLUSTER_DIR does not exist"
    exit 1
fi

echo "Running tests for $CLUSTER_DIR..."
if [ ! -z "$FILTER_PATTERN" ]; then
    echo "Filtering problems matching: $FILTER_PATTERN"
fi

# Find all problem directories and run tests
TOTAL_PROBLEMS=0
PASSED_PROBLEMS=0
FAILED_PROBLEMS=()

for PROBLEM_DIR in "$CLUSTER_DIR"/*; do
    # Skip if it's not a directory or if it's the library.py file
    if [ ! -d "$PROBLEM_DIR" ] || [ "$(basename "$PROBLEM_DIR")" = "library.py" ]; then
        continue
    fi

    PROBLEM_NAME=$(basename "$PROBLEM_DIR")

    # Skip if filter pattern is provided and doesn't match
    if [ ! -z "$FILTER_PATTERN" ] && [[ ! "$PROBLEM_NAME" =~ $FILTER_PATTERN ]]; then
        continue
    fi

    echo -e "\n===================================="
    echo "Testing problem: $PROBLEM_NAME"
    echo "===================================="

    # Check if run.sh exists
    if [ ! -f "$PROBLEM_DIR/run.sh" ]; then
        echo "Error: run.sh script not found for problem $PROBLEM_NAME"
        continue
    fi

    # Run the test script with output redirection to capture only summary
    pushd "$PROBLEM_DIR" > /dev/null
    TEST_OUTPUT=$(./run.sh 2>&1)
    TEST_RESULT=$?
    popd > /dev/null

    # Extract summary lines from test output
    RESULTS_LINE=$(echo "$TEST_OUTPUT" | grep -E "Results: [0-9]+/[0-9]+ tests passed" || echo "No results found")

    TOTAL_PROBLEMS=$((TOTAL_PROBLEMS+1))
    if [ $TEST_RESULT -eq 0 ]; then
        PASSED_PROBLEMS=$((PASSED_PROBLEMS+1))
        echo "✅ Problem $PROBLEM_NAME: $RESULTS_LINE"
    else
        FAILED_PROBLEMS+=("$PROBLEM_NAME")
        echo "❌ Problem $PROBLEM_NAME: $RESULTS_LINE"

        # Show first few error messages for debugging
        ERROR_SAMPLE=$(echo "$TEST_OUTPUT" | grep -E "Error|FAILED|Traceback" | head -5)
        if [ ! -z "$ERROR_SAMPLE" ]; then
            echo "Sample errors:"
            echo "$ERROR_SAMPLE"
            echo "..."
        fi
    fi
done

echo -e "\n===================================="
echo "Final Results: $PASSED_PROBLEMS/$TOTAL_PROBLEMS problems passed all tests"
echo "===================================="

if [ ${#FAILED_PROBLEMS[@]} -gt 0 ]; then
    echo "Problems with failing tests:"
    for problem in "${FAILED_PROBLEMS[@]}"; do
        echo "- $problem"
    done
fi

if [ $PASSED_PROBLEMS -eq $TOTAL_PROBLEMS ]; then
    echo "🎉 All problems in cluster$CLUSTER_NUM passed all tests!"
    exit 0
else
    echo "⚠️ Some problems in cluster$CLUSTER_NUM failed tests."
    exit 1
fi
