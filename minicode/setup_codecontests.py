"""
Process the code_contests dataset and format problems.

This script:
1. Loads problems from the code_contests dataset
2. Loads cluster information from data/clusters.json
3. Creates standardized problem directories in codecontests/cluster{i}/problem_name/
4. Generates PROBLEM.md, main.py, and test files
5. Creates run.sh script for each problem
"""

from datasets import load_dataset
import json
import logging
import os
from pathlib import Path
import shutil

from minicode.formatter.problem_md import generate_problem_md
from minicode.formatter.script_sh import generate_run_script
from minicode.models.dataset import DatasetProblem
from minicode.models.problem import Problem, TestCase

os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants
DATASET_NAME = "deepmind/code_contests"
PROBLEMS_DIR = Path("../codecontests")
CLUSTERS_PATH = REPO_ROOT / "data" / "clusters.json"
INSTRUCTIONS_PATH = REPO_ROOT / "prompts" / "INSTRUCTIONS_CODECONTESTS.md"


def load_clusters() -> dict[str, list[str]]:
    """
    Load cluster information from the clusters.json file.

    Returns:
        Dictionary mapping cluster IDs to lists of problem names
    """
    with open(CLUSTERS_PATH, "r") as f:
        clusters = json.load(f)
    logger.info(f"Loaded {len(clusters)} clusters from {CLUSTERS_PATH}")
    return clusters


def get_problem_id(name: str, index: int) -> str:
    """
    Generate a unique problem ID based on name and index.

    Args:
        name: Problem name
        index: Problem index in dataset

    Returns:
        Sanitized problem ID
    """
    # Sanitize name to create a valid directory name
    sanitized = name.lower().replace(" ", "_")
    sanitized = "".join(c for c in sanitized if c.isalnum() or c == "_")

    # Add index to ensure uniqueness
    return f"{sanitized}_{index}"


def extract_python_solution(problem: DatasetProblem) -> str | None:
    """
    Extract a Python 3 solution from the problem's solutions.
    Only returns Python 3 solutions, skipping Python 2 solutions.

    Args:
        problem: Problem from the dataset as a Pydantic model

    Returns:
        Python 3 solution code or None if not found
    """
    # Get Python 3 solution from the model
    python3_solution = problem.get_python3_solution()

    if python3_solution:
        logger.info(f"Found Python 3 solution for problem: {problem.name}")
        return python3_solution

    # If no Python 3 solution, skip this problem
    logger.warning(f"No Python 3 solution found for problem: {problem.name}, skipping")
    return None


def create_test_files(problem_dir: Path, test_inputs: list[str], test_outputs: list[str]) -> int:
    """
    Create test input and output files in the problem directory.

    Args:
        problem_dir: Path to the problem directory
        test_inputs: List of test input strings
        test_outputs: List of test output strings

    Returns:
        Number of test cases created
    """
    tests_dir = problem_dir / "tests"
    tests_dir.mkdir(exist_ok=True)

    # Create input and output files
    for i, (input_text, output_text) in enumerate(zip(test_inputs, test_outputs, strict=False), 1):
        input_path = tests_dir / f"input_{i}.txt"
        output_path = tests_dir / f"output_{i}.txt"

        with open(input_path, "w") as f:
            f.write(input_text.strip())

        with open(output_path, "w") as f:
            f.write(output_text.strip())

    return min(len(test_inputs), len(test_outputs))


def process_problem(dataset_problem: DatasetProblem, index: int, cluster_id: str):
    """
    Process a single problem and create its directory structure inside a cluster.

    Args:
        dataset_problem: Problem from the dataset as a Pydantic model
        index: Problem index for unique ID generation
        cluster_id: The cluster ID this problem belongs to

    Returns:
        True if processing succeeded, False otherwise
    """
    name = dataset_problem.name
    problem_id = get_problem_id(name, index)

    # Extract Python solution first
    solution_code = extract_python_solution(dataset_problem)
    if not solution_code:
        # Skip problems without Python solutions
        logger.warning(f"Skipping problem {name} due to missing Python solution")
        return False

    # Create cluster directory and problem directory
    cluster_dir = PROBLEMS_DIR / f"cluster{cluster_id}"
    problem_dir = cluster_dir / problem_id
    problem_dir.mkdir(parents=True, exist_ok=True)

    # Write main.py with solution code
    with open(problem_dir / "main.py", "w") as f:
        # Add shebang line
        f.write("#!/usr/bin/env python3\n\n")
        # Write the Python 3 solution directly
        f.write(solution_code)

    # Get all test cases
    test_case_dicts = dataset_problem.get_all_test_cases(min_test_cases=10)

    # Skip if no test cases
    if not test_case_dicts:
        logger.warning(f"Skipping problem {name} due to missing test cases")
        return False

    # Prepare input and output lists for test file creation
    all_inputs = [tc["input"] for tc in test_case_dicts]
    all_outputs = [tc["output"] for tc in test_case_dicts]

    # Create test cases for the problem model
    test_cases = [
        TestCase(input=inp, output=out, time_limit_ms=30000, memory_limit_mb=512)
        for inp, out in zip(all_inputs, all_outputs, strict=False)
    ]

    # Get difficulty and source as strings
    difficulty_str = dataset_problem.get_difficulty_name()
    source_name = dataset_problem.get_source_name()

    # Get tags/categories
    tags = dataset_problem.cf_tags

    # Create Problem model for our system
    problem_model = Problem(
        id=problem_id,
        name=name,
        description=dataset_problem.description,
        category=tags,
        difficulty=difficulty_str,
        test_cases=test_cases,
        source=source_name,
    )

    # Generate PROBLEM.md
    generate_problem_md(problem_model, problem_dir)

    # Create test files
    num_tests = create_test_files(problem_dir, all_inputs, all_outputs)

    # Generate run.sh script
    generate_run_script(problem_id, problem_dir)

    # Save CF tags to tags.txt
    if tags:
        with open(problem_dir / "tags.txt", "w") as f:
            f.write("\n".join(tags))
        logger.info(f"Saved {len(tags)} CF tags to tags.txt")

    logger.info(f"Processed problem: cluster{cluster_id}/{problem_id} with {num_tests} test cases")


def copy_instructions_to_cluster(cluster_dir: Path) -> bool:
    """
    Copy INSTRUCTIONS.md to the cluster directory.

    Args:
        cluster_dir: Path to the cluster directory

    Returns:
        True if successful, False otherwise
    """
    if not INSTRUCTIONS_PATH.exists():
        logger.warning(f"INSTRUCTIONS.md not found at {INSTRUCTIONS_PATH}")
        return False

    try:
        shutil.copy(INSTRUCTIONS_PATH, cluster_dir / "INSTRUCTIONS.md")
        logger.info(f"Copied INSTRUCTIONS.md to {cluster_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to copy INSTRUCTIONS.md to {cluster_dir}: {e}")
        return False


def main():
    """
    Main entry point for processing problems based on clusters.
    """
    # Ensure problems directory exists
    PROBLEMS_DIR.mkdir(parents=True, exist_ok=True)

    # Load clusters
    clusters = load_clusters()
    if not clusters:
        logger.error("Failed to load clusters, aborting")
        return

    # Load dataset
    logger.info(f"Loading dataset: {DATASET_NAME}")
    dataset = load_dataset(DATASET_NAME)

    # Get problems from training set
    # We need to type-ignore this because the Dataset class doesn't have proper type annotations
    train_dataset = dataset["train"]  # type: ignore

    # Create a mapping from problem names to dataset problems
    logger.info("Building problem name to object mapping from dataset...")
    name_to_problem = {}
    name_to_index = {}  # To keep track of indices for problem_id generation

    for i, raw_problem in enumerate(train_dataset):
        dataset_problem = DatasetProblem.model_validate(raw_problem)

        # We use this exact format to match against the clusters.json format
        problem_key = dataset_problem.name
        name_to_problem[problem_key] = dataset_problem
        name_to_index[problem_key] = i

    logger.info(f"Found {len(name_to_problem)} valid problems in the dataset")

    successful = 0
    attempted = 0
    processed_problems = set()  # Track processed problems to avoid duplicates

    # Process problems by cluster
    for cluster_id, problem_names in clusters.items():
        logger.info(f"Processing cluster {cluster_id} with {len(problem_names)} problems")

        # Create cluster directory
        cluster_dir = PROBLEMS_DIR / f"cluster{cluster_id}"
        cluster_dir.mkdir(parents=True, exist_ok=True)

        # Create a minimal library.py file in the cluster directory
        library_path = cluster_dir / "library.py"
        if not library_path.exists():
            with open(library_path, "w") as f:
                f.write(
                    f'"""\nLibrary file for cluster{cluster_id}.\nThis contains shared code that can be imported by problems in this cluster.\n"""\n'  # noqa: E501
                )

        # Copy INSTRUCTIONS.md to cluster directory
        copy_instructions_to_cluster(cluster_dir)

        # Process problems in this cluster
        for problem_name in problem_names:
            # Skip if we've already processed this problem
            if problem_name in processed_problems:
                logger.warning(f"Skipping duplicate problem: {problem_name}")
                continue

            # Get the problem from our mapping
            if problem_name not in name_to_problem:
                logger.warning(f"Problem not found in dataset: {problem_name}")
                continue

            dataset_problem = name_to_problem[problem_name]
            index = name_to_index[problem_name]
            _ = process_problem(dataset_problem, index, cluster_id)

            attempted += 1
            logger.info(
                f"Processing problem {attempted} (successful so far: {successful}): "
                f"{problem_name} in cluster{cluster_id}"
            )

            successful += 1
            processed_problems.add(problem_name)

    logger.info(f"Finished processing. {successful}/{attempted} problems formatted successfully.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process problems from the code_contests dataset based on clusters")

    args = parser.parse_args()
    main()
