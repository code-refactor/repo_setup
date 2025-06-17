#!/usr/bin/env python3
"""
Parser for large_repos results to extract metrics from LIBRARYBENCH_metrics.json files.
Extracts: total log prob, total tokens, total cyclomatic complexity

Uses:
- large_repos/*/LIBRARYBENCH_metrics.json for original repository metrics
- large_repos/text_editor/unified/LIBRARYBENCH_metrics.json for unified repository metrics
"""

import json
from pathlib import Path
from typing import Dict


def load_json_metrics(file_path: Path) -> Dict:
    """Load metrics from a LIBRARYBENCH_metrics.json file."""
    if not file_path.exists():
        return {}
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        # Extract totals
        metrics = {
            "log_prob": data.get("total_logprobs", 0.0),
            "total_tokens": data.get("total_tokens", 0),
            "cyclomatic_complexity": data.get("total_cyclomatic", 0),
            "total_lloc": data.get("total_lloc", 0)
        }
        
        return metrics
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing {file_path}: {e}")
        return {}


def load_test_results(file_path: Path) -> Dict:
    """Load test results from a report.json file."""
    if not file_path.exists():
        return {}
    
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        
        summary = data.get("summary", {})
        metrics = {
            "tests_passed": summary.get("passed", 0),
            "total_tests": summary.get("total", 0)
        }
        
        return metrics
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error parsing test results {file_path}: {e}")
        return {}


def parse_project_results(project_name: str, large_repos_dir: Path) -> Dict:
    """Parse JSON metrics for a single project."""
    results = {"original": {}, "unified": {}}
    
    # Parse original repo results
    original_json = large_repos_dir / project_name / "LIBRARYBENCH_metrics.json"
    if original_json.exists():
        results["original"] = load_json_metrics(original_json)
    
    # Parse unified repo results
    unified_json = large_repos_dir / project_name / "unified" / "LIBRARYBENCH_metrics.json"
    if unified_json.exists():
        results["unified"] = load_json_metrics(unified_json)
        
        # Add test results for unified (only available for unified)
        test_results_json = large_repos_dir / project_name / "unified" / "report.json"
        if test_results_json.exists():
            test_data = load_test_results(test_results_json)
            results["unified"].update(test_data)
    
    return results


def main():
    """Main function to parse all large_repos results."""
    large_repos_dir = Path("/home/justinchiu_cohere_com/minicode/large_repos")
    all_results = {}

    # Get all project directories that have LIBRARYBENCH_metrics.json
    project_dirs = [d for d in large_repos_dir.iterdir() if d.is_dir() and (d / "LIBRARYBENCH_metrics.json").exists()]

    for project_dir in sorted(project_dirs):
        project_name = project_dir.name
        print(f"Parsing {project_name}...")

        try:
            project_results = parse_project_results(project_name, large_repos_dir)
            all_results[project_name] = project_results
        except Exception as e:
            print(f"Error parsing {project_name}: {e}")

    # Print summary table
    print("\n" + "=" * 160)
    print(
        f"{'Project':<30} {'Type':<10} {'Tests P/T':<12} {'Pass %':<8} {'Log Prob':<15} {'Tokens':<10} {'LLOC':<8} {'Complexity':<10} {'LogP Ratio':<12}"
    )
    print("=" * 160)

    for project_name in sorted(all_results.keys()):
        project_data = all_results[project_name]

        for repo_type in ["original", "unified"]:
            data = project_data[repo_type]
            
            # Skip empty data
            if not data:
                continue

            # Test metrics
            tests_passed = data.get("tests_passed", "N/A")
            total_tests = data.get("total_tests", "N/A")
            if tests_passed != "N/A" and total_tests != "N/A" and total_tests > 0:
                test_display = f"{tests_passed}/{total_tests}"
                pass_rate = f"{100 * tests_passed / total_tests:.1f}%"
            else:
                test_display = "N/A"
                pass_rate = "N/A"
            
            log_prob = (
                f"{data.get('log_prob', 0.0):.2f}"
                if data.get("log_prob") is not None
                else "N/A"
            )
            tokens = data.get("total_tokens", "N/A")
            lloc = data.get("total_lloc", "N/A")
            complexity = data.get("cyclomatic_complexity", "N/A")

            # Calculate ratios for unified rows
            logp_ratio = ""
            token_ratio = ""
            if repo_type == "unified" and project_data["original"]:
                orig_data = project_data["original"]
                if (
                    data.get("log_prob") is not None
                    and orig_data.get("log_prob") is not None
                    and orig_data.get("log_prob") != 0
                ):
                    logp_ratio = f"{data['log_prob'] / orig_data['log_prob']:.3f}"
                if (
                    data.get("total_tokens") is not None
                    and orig_data.get("total_tokens") is not None
                    and orig_data.get("total_tokens") != 0
                ):
                    token_ratio = (
                        f"{data['total_tokens'] / orig_data['total_tokens']:.3f}"
                    )

            print(
                f"{project_name:<30} {repo_type:<10} {test_display:<12} {pass_rate:<8} {log_prob:<15} {tokens:<10} {lloc:<8} {complexity:<10} {logp_ratio:<12}"
            )

    # Calculate totals
    print("\n" + "=" * 160)
    print("TOTALS:")
    print("=" * 160)

    for repo_type in ["original", "unified"]:
        total_tests_passed = 0
        total_tests_all = 0
        total_log_prob = 0.0
        total_tokens_all = 0
        total_lloc_all = 0
        total_complexity_all = 0
        valid_projects = 0

        for project_data in all_results.values():
            data = project_data[repo_type]
            if data and data.get("tests_passed") is not None:
                total_tests_passed += data["tests_passed"]
            if data and data.get("total_tests") is not None:
                total_tests_all += data["total_tests"]
            if data and data.get("log_prob") is not None:
                total_log_prob += data["log_prob"]
            if data and data.get("total_tokens") is not None:
                total_tokens_all += data["total_tokens"]
            if data and data.get("total_lloc") is not None:
                total_lloc_all += data["total_lloc"]
            if data and data.get("cyclomatic_complexity") is not None:
                total_complexity_all += data["cyclomatic_complexity"]
                valid_projects += 1

        # Calculate overall ratios for totals
        total_logp_ratio = ""
        total_token_ratio = ""
        if repo_type == "unified":
            # Calculate totals for original to get ratios
            orig_total_log_prob = 0.0
            orig_total_tokens = 0
            for project_data in all_results.values():
                orig_data = project_data["original"]
                if orig_data and orig_data.get("log_prob") is not None:
                    orig_total_log_prob += orig_data["log_prob"]
                if orig_data and orig_data.get("total_tokens") is not None:
                    orig_total_tokens += orig_data["total_tokens"]

            if orig_total_log_prob != 0:
                total_logp_ratio = f"{total_log_prob / orig_total_log_prob:.3f}"
            if orig_total_tokens != 0:
                total_token_ratio = f"{total_tokens_all / orig_total_tokens:.3f}"

        # Only print if we have data
        if valid_projects > 0 or total_tokens_all > 0:
            total_test_display = f"{total_tests_passed}/{total_tests_all}" if total_tests_all > 0 else "N/A"
            total_pass_rate = f"{100 * total_tests_passed / total_tests_all:.1f}%" if total_tests_all > 0 else "N/A"
            
            print(
                f"{'TOTAL ' + repo_type.upper():<30} {'':<10} {total_test_display:<12} {total_pass_rate:<8} {total_log_prob:<15.2f} {total_tokens_all:<10} {total_lloc_all:<8} {total_complexity_all:<10} {total_logp_ratio:<12}"
            )

    # Generate LaTeX table
    print("\n" + "=" * 80)
    print("LATEX TABLE:")
    print("=" * 80)
    
    print("\\begin{tabular}{|l|l|r|r|r|r|}")
    print("\\hline")
    print("Collection & Model & LLoC & CC & LogP Ratio & Pass \\% \\\\")
    print("\\hline")
    
    for project_name in sorted(all_results.keys()):
        project_data = all_results[project_name]
        
        # Original row
        orig_data = project_data["original"]
        if orig_data:
            print(f"{project_name.replace('_', '\\_')} & Original & {orig_data.get('total_lloc', 0)} & {orig_data.get('cyclomatic_complexity', 0)} & - & - \\\\")
        
        # Unified row
        unified_data = project_data["unified"]
        if unified_data and orig_data:
            logp_ratio = ""
            if (unified_data.get("log_prob") is not None and 
                orig_data.get("log_prob") is not None and 
                orig_data.get("log_prob") != 0):
                logp_ratio = f"{unified_data['log_prob'] / orig_data['log_prob']:.3f}"
            
            pass_rate = ""
            if (unified_data.get("tests_passed") is not None and 
                unified_data.get("total_tests") is not None and 
                unified_data.get("total_tests") > 0):
                pass_rate = f"{100 * unified_data['tests_passed'] / unified_data['total_tests']:.1f}"
            
            print(f"{project_name.replace('_', '\\_')} & Unified & {unified_data.get('total_lloc', 0)} & {unified_data.get('cyclomatic_complexity', 0)} & {logp_ratio} & {pass_rate} \\\\")
    
    print("\\hline")
    print("\\end{tabular}")

    # Save detailed results to JSON
    output_file = "large_repos_parsed_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nDetailed results saved to {output_file}")


if __name__ == "__main__":
    main()
