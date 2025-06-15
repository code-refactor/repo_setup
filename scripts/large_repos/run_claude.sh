#!/bin/bash
# must be run from the unified project directory

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory_name>"
    echo "Example: $0 large_repos/text_editor/unified"
    exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' does not exist"
    exit 1
fi

echo "Starting refactoring for $directory..."

# Push into the directory
pushd "$directory"

uv venv
source .venv/bin/activate

pip install -e .

echo "Following the instructions in REFACTOR.md..."
# Run Claude Code and tell it to follow instructions
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md"
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md. Be sure to complete the migrations."
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md. Be sure to complete the migrations."

# Ensure pytest results are collected
pytest tests/ --json-report --json-report-file=report.json --continue-on-collection-errors > test_output.txt 2>&1

deactivate

# Pop back to the original directory
popd

# Run scoring script
echo "Running scoring script on refactored repository..."
uv run python -m minicode.score_small_repos --directory "$directory" --enable_logprobs

echo "Done!"
