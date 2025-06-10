#!/usr/bin/env python3
"""
Test script for unified repositories in large_repos/*/unified directories.

This script:
1. Finds all unified directories in large_repos/
2. For each unified directory:
   - Creates a virtual environment with uv venv
   - Activates the virtual environment
   - Installs the package in editable mode with pip install -e .
   - Runs pytest to test the installation
3. Reports results for each unified repository

Usage:
  python test_unified_repos.py
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd, shell=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 5 minutes"
    except Exception as e:
        return -1, "", str(e)


def find_unified_directories():
    """Find all unified directories in large_repos/."""
    base_dir = Path("large_repos")
    unified_dirs = []

    if not base_dir.exists():
        print(f"Base directory {base_dir} does not exist")
        return unified_dirs

    for library_dir in base_dir.iterdir():
        if library_dir.is_dir():
            unified_dir = library_dir / "unified"
            if unified_dir.exists() and unified_dir.is_dir():
                unified_dirs.append(unified_dir)

    return unified_dirs


def test_unified_repository(unified_dir):
    """Test a single unified repository."""
    print(f"\n{'='*60}")
    print(f"Testing: {unified_dir}")
    print(f"{'='*60}")

    results = {
        "venv_creation": False,
        "package_install": False,
        "pytest_run": False,
        "errors": [],
    }

    # Step 1: Create virtual environment
    print("1. Creating virtual environment...")
    returncode, stdout, stderr = run_command("uv venv", unified_dir)
    if returncode == 0:
        print("   ✓ Virtual environment created successfully")
        results["venv_creation"] = True
    else:
        error_msg = f"Failed to create venv: {stderr}"
        print(f"   ✗ {error_msg}")
        results["errors"].append(error_msg)
        return results

    # Step 2: Install package in editable mode
    print("2. Installing package in editable mode...")
    # Use uv pip install which automatically uses the venv
    install_cmd = "uv pip install -e ."
    returncode, stdout, stderr = run_command(install_cmd, unified_dir)
    if returncode == 0:
        print("   ✓ Package installed successfully")
        results["package_install"] = True
    else:
        error_msg = f"Failed to install package: {stderr}"
        print(f"   ✗ {error_msg}")
        results["errors"].append(error_msg)
        return results

    # Step 3: Run pytest
    print("3. Running pytest...")
    pytest_cmd = f"uv run pytest -v --tb=short"
    returncode, stdout, stderr = run_command(pytest_cmd, unified_dir)

    # Check for any errors in output
    has_errors = (
        "ERRORS" in stdout
        or "ERROR" in stdout
        or "ImportError" in stdout
        or "ModuleNotFoundError" in stdout
        or "AttributeError" in stdout
        or "SyntaxError" in stdout
        or "INTERNALERROR" in stdout
    )

    # Check if pytest started properly
    pytest_started = "test session starts" in stdout or "collected" in stdout

    if returncode == 0:
        print("   ✓ All tests passed!")
        results["pytest_run"] = True
    elif pytest_started and not has_errors:
        # Tests ran but some failed (test assertions) - this is acceptable
        print("   ⚠ Tests ran but some test assertions failed (this is expected)")
        results["pytest_run"] = True
    else:
        # Any errors mean failure
        error_msg = "Pytest failed with errors"
        if not pytest_started:
            error_msg = "Pytest failed to start"
        elif has_errors:
            error_msg = "Pytest encountered errors during test collection or execution"
        if stderr:
            error_msg += f": {stderr}"
        print(f"   ✗ {error_msg}")
        results["errors"].append(error_msg)
        results["pytest_run"] = False

    # Show some test output for context
    if stdout:
        print("\nTest output summary:")
        lines = stdout.split("\n")
        # Show last 10 lines of output for summary
        for line in lines[-10:]:
            if line.strip():
                print(f"   {line}")

    return results


def main():
    """Main function to test all unified repositories."""
    print("Finding unified directories in large_repos/...")
    unified_dirs = find_unified_directories()

    if not unified_dirs:
        print("No unified directories found!")
        return

    print(f"Found {len(unified_dirs)} unified directories to test")

    # Test each unified repository
    all_results = {}
    for unified_dir in unified_dirs:
        library_name = unified_dir.parent.name
        results = test_unified_repository(unified_dir)
        all_results[library_name] = results

    # Print summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    successful_setups = 0
    successful_tests = 0

    for library_name, results in all_results.items():
        status_venv = "✓" if results["venv_creation"] else "✗"
        status_install = "✓" if results["package_install"] else "✗"
        status_pytest = "✓" if results["pytest_run"] else "✗"

        print(
            f"{library_name:40} | Venv: {status_venv} | Install: {status_install} | Tests: {status_pytest}"
        )

        if results["venv_creation"] and results["package_install"]:
            successful_setups += 1
        if results["pytest_run"]:
            successful_tests += 1

        # Show errors if any
        if results["errors"]:
            for error in results["errors"]:
                print(f"   Error: {error}")

    print(f"\nSetup success rate: {successful_setups}/{len(unified_dirs)}")
    print(f"Test success rate: {successful_tests}/{len(unified_dirs)}")


if __name__ == "__main__":
    main()
