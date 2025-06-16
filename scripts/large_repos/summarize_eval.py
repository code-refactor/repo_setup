#!/usr/bin/env python3
"""
Parser for large_repos results to extract metrics for original and unified repositories.
Extracts: total tests passed, total tests, total log prob, total tokens, total cyclomatic complexity

TODO: Use results.json and results_original.json for test output.
Unfortunately most recent run did overwrote original test results.
"""

import re
import json
from pathlib import Path
from typing import Dict


def parse_score_file(file_path: str) -> Dict:
    """Parse a score_*.txt file to extract metrics."""
    metrics = {}

    with open(file_path, "r") as f:
        content = f.read()

    # Extract summary section
    summary_match = re.search(
        r"=== Summary ===\s*\n(.*?)(?=\n\n|\nWritten|\Z)", content, re.DOTALL
    )
    if summary_match:
        summary_text = summary_match.group(1)

        # Extract log probability
        logprob_match = re.search(r"Full Repo Log Probability: ([-\d.]+)", summary_text)
        if logprob_match:
            metrics["log_prob"] = float(logprob_match.group(1))

        # Extract total tokens
        tokens_match = re.search(r"Total Tokens: (\d+)", summary_text)
        if tokens_match:
            metrics["total_tokens"] = int(tokens_match.group(1))

        # Extract cyclomatic complexity
        complexity_match = re.search(
            r"Total Cyclomatic Complexity: (\d+)", summary_text
        )
        if complexity_match:
            metrics["cyclomatic_complexity"] = int(complexity_match.group(1))

    return metrics


def parse_test_output_file(file_path: str) -> Dict:
    """Parse a test_output*.txt file to extract test metrics."""
    metrics = {}

    with open(file_path, "r") as f:
        lines = f.readlines()

    # Use the last line to extract test results
    if lines:
        last_line = lines[-1].strip()
        # Look for pytest summary format with various outcomes
        # Format: "=== X failed, Y passed, Z xfailed, W xpassed, N warnings in M.Ms ==="
        pytest_match = re.search(r"=+.*?(\d+) passed.*?in [\d.]+s =+", last_line)
        if pytest_match:
            metrics["tests_passed"] = int(pytest_match.group(1))

            # Look for "collected N items" in the content to get total tests
            content = "".join(lines)
            collected_match = re.search(r"collected (\d+) items", content)
            if collected_match:
                metrics["total_tests"] = int(collected_match.group(1))
            else:
                # If no collected items found, assume passed = total
                metrics["total_tests"] = metrics["tests_passed"]

    return metrics


def parse_project_results(project_dir: Path) -> Dict:
    """Parse all result files for a single project."""
    results = {"original": {}, "unified": {}}

    # Parse original repo results
    score_original = project_dir / "score_original.txt"
    test_original = project_dir / "test_output_original.txt"

    if score_original.exists():
        results["original"].update(parse_score_file(str(score_original)))

    if test_original.exists():
        results["original"].update(parse_test_output_file(str(test_original)))

    # Parse unified repo results
    score_unified = project_dir / "score_unified.txt"
    test_unified = project_dir / "test_output.txt"

    if score_unified.exists():
        results["unified"].update(parse_score_file(str(score_unified)))

    if test_unified.exists():
        results["unified"].update(parse_test_output_file(str(test_unified)))

    return results


def main():
    """Main function to parse all large_repos results."""
    results_dir = Path("/home/justinchiu_cohere_com/minicode/results/large_repos")
    all_results = {}

    # Get all project directories
    project_dirs = [d for d in results_dir.iterdir() if d.is_dir()]

    for project_dir in sorted(project_dirs):
        project_name = project_dir.name
        print(f"Parsing {project_name}...")

        try:
            project_results = parse_project_results(project_dir)
            all_results[project_name] = project_results
        except Exception as e:
            print(f"Error parsing {project_name}: {e}")

    # Print summary table
    print("\n" + "=" * 120)
    print(
        f"{'Project':<30} {'Type':<10} {'Tests Passed':<12} {'Total Tests':<12} {'Log Prob':<15} {'Tokens':<10} {'Complexity':<10}"
    )
    print("=" * 120)

    for project_name in sorted(all_results.keys()):
        project_data = all_results[project_name]

        for repo_type in ["original", "unified"]:
            data = project_data[repo_type]

            tests_passed = data.get("tests_passed", "N/A")
            total_tests = data.get("total_tests", "N/A")
            log_prob = (
                f"{data.get('log_prob', 'N/A'):.2f}"
                if data.get("log_prob") is not None
                else "N/A"
            )
            tokens = data.get("total_tokens", "N/A")
            complexity = data.get("cyclomatic_complexity", "N/A")

            print(
                f"{project_name:<30} {repo_type:<10} {tests_passed:<12} {total_tests:<12} {log_prob:<15} {tokens:<10} {complexity:<10}"
            )

    # Calculate totals
    print("\n" + "=" * 120)
    print("TOTALS:")
    print("=" * 120)

    for repo_type in ["original", "unified"]:
        total_tests_passed = 0
        total_tests_all = 0
        total_log_prob = 0.0
        total_tokens_all = 0
        total_complexity_all = 0
        valid_projects = 0

        for project_data in all_results.values():
            data = project_data[repo_type]
            if data.get("tests_passed") is not None:
                total_tests_passed += data["tests_passed"]
            if data.get("total_tests") is not None:
                total_tests_all += data["total_tests"]
            if data.get("log_prob") is not None:
                total_log_prob += data["log_prob"]
            if data.get("total_tokens") is not None:
                total_tokens_all += data["total_tokens"]
            if data.get("cyclomatic_complexity") is not None:
                total_complexity_all += data["cyclomatic_complexity"]
                valid_projects += 1

        print(
            f"{'TOTAL ' + repo_type.upper():<30} {'':<10} {total_tests_passed:<12} {total_tests_all:<12} {total_log_prob:<15.2f} {total_tokens_all:<10} {total_complexity_all:<10}"
        )

    # Save detailed results to JSON
    output_file = "large_repos_parsed_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nDetailed results saved to {output_file}")


if __name__ == "__main__":
    main()
