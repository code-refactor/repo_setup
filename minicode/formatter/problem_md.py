"""
Generate PROBLEM.md files for formatted problems.

This module creates Markdown files with problem descriptions,
formatted in a standardized way.
"""

from pathlib import Path

from ..models.problem import Problem, TestCase


def generate_problem_md(problem: Problem, output_dir: Path) -> Path:
    """
    Generate a PROBLEM.md file for a given problem.

    Args:
        problem: Problem model with problem details
        output_dir: Directory where PROBLEM.md will be written

    Returns:
        Path to the generated file
    """
    # Use the problem's to_markdown method to generate content
    markdown_content = problem.to_markdown()

    # Add example test cases if available
    if problem.test_cases:
        markdown_content += "\n\n## Examples\n\n"

        # Include up to 3 examples
        for i, test_case in enumerate(problem.test_cases[:3], 1):
            markdown_content += f"### Example {i}\n\n"
            markdown_content += "**Input**:\n```\n"
            markdown_content += test_case.input.strip()
            markdown_content += "\n```\n\n"
            markdown_content += "**Output**:\n```\n"
            markdown_content += test_case.output.strip()
            markdown_content += "\n```\n\n"

    # Add note about testing
    markdown_content += "\n## Testing\n\n"
    markdown_content += "Run the solution with:\n\n"
    markdown_content += "```bash\n./run.sh\n```\n\n"
    markdown_content += "Or test with a specific input file:\n\n"
    markdown_content += "```bash\nuv run main.py < tests/input_1.txt\n```\n"

    # Write the file
    output_file = output_dir / "PROBLEM.md"
    with open(output_file, "w") as f:
        f.write(markdown_content)

    return output_file


if __name__ == "__main__":
    # Example usage for testing
    import sys
    from pathlib import Path

    if len(sys.argv) != 3:
        print("Usage: python problem_md.py problem_id output_dir")
        sys.exit(1)

    problem_id = sys.argv[1]
    output_dir = Path(sys.argv[2])

    # Create a dummy problem for testing
    test_problem = Problem(
        id=problem_id,
        name="Example Problem",
        description="This is an example problem description.\n\nWrite a function that adds two numbers.",
        category=["math", "implementation"],
        difficulty="easy",
        test_cases=[
            TestCase(input="1 2", output="3", time_limit_ms=30000, memory_limit_mb=512),
            TestCase(input="5 7", output="12", time_limit_ms=30000, memory_limit_mb=512),
        ],
        source="Example Source",
    )

    output_file = generate_problem_md(test_problem, output_dir)
    print(f"Generated problem description at: {output_file}")
