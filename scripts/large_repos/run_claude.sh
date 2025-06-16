#!/bin/bash
source .env

# must be run from the unified project's parent directory

if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory_name>"
    echo "Example: $0 text_editor"
    exit 1
fi

directory="$1"

if [ ! -d "$directory" ]; then
    echo "Error: Directory '$directory' does not exist"
    exit 1
fi

echo "Starting refactoring for $directory..."

# Push into the directory
pushd "large_repos/$directory/unified"

uv venv
source .venv/bin/activate

pip install -e .

# collect initial repo status
pytest tests/ --json-report --json-report-file=report.json --continue-on-collection-errors > test_output_original.txt 2>&1

echo "Following the instructions in REFACTOR.md..."
# Run Claude Code and tell it to follow instructions
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md"
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md. Be sure to complete the migrations."
time claude --dangerously-skip-permissions -p "Follow the instructions in REFACTOR.md. Be sure to complete the migrations."

# Ensure pytest results are collected post-refactor
pytest tests/ --json-report --json-report-file=report.json --continue-on-collection-errors > test_output.txt 2>&1

deactivate

# Pop back to the original directory
popd

# Run scoring script
echo "Running scoring script on refactored repository..."
uv run python -m minicode.score_large_repos --directory "large_repos/$directory/unified" --enable_logprobs > $directory/score_unified.txt
uv run python -m minicode.score_large_repos --directory "large_repos/$directory" --enable_logprobs  --skip_unified > $directory/score_original.txt

# Collect all results
mkdir -p results/large_repos/$directory

cp large_repos/$directory/unified/test_output_original.txt results/large_repos/$directory/test_output_original.txt
cp large_repos/$directory/unified/test_output.txt results/large_repos/$directory/test_output.txt

cp large_repos/$directory/score_original.txt results/large_repos/$directory/score_original.txt
cp large_repos/$directory/unified/score_unified.txt results/large_repos/$directory/score_unified.txt

echo "Done!"
