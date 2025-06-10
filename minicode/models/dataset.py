"""
Pydantic models for working with the DeepMind Code Contests dataset.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, root_validator


class Solution(BaseModel):
    """Solution data from the Code Contests dataset."""

    language: List[int] = Field(default_factory=list, description="Language IDs")
    solution: List[str] = Field(default_factory=list, description="Solution code")


class TestSet(BaseModel):
    """Test case set (input/output pairs) from the Code Contests dataset."""

    input: List[str] = Field(default_factory=list, description="Input test cases")
    output: List[str] = Field(default_factory=list, description="Expected output for test cases")
    explanation: Optional[List[str]] = Field(default=None, description="Explanations for test cases")


class DatasetProblem(BaseModel):
    """
    A problem from the DeepMind Code Contests dataset.
    This model matches the structure of problems in the dataset.
    """

    name: str = Field(..., description="Problem name")
    description: str = Field("", description="Problem description")
    solutions: Solution = Field(default_factory=lambda: Solution(), description="Problem solutions")
    public_tests: TestSet = Field(default_factory=lambda: TestSet(), description="Public test cases")
    private_tests: TestSet = Field(default_factory=lambda: TestSet(), description="Private test cases")
    generated_tests: Optional[TestSet] = Field(None, description="Generated test cases")
    difficulty: Optional[int] = Field(None, description="Difficulty level (1-7)")
    source: Optional[int] = Field(None, description="Source platform ID")
    cf_contest_id: Optional[int] = Field(None, description="Codeforces contest ID")
    cf_index: Optional[str] = Field(None, description="Codeforces problem index")
    cf_points: Optional[int] = Field(None, description="Codeforces points")
    cf_rating: Optional[int] = Field(None, description="Codeforces rating")
    cf_tags: List[str] = Field(default_factory=list, description="Codeforces tags")
    url: Optional[str] = Field(None, description="Problem URL")

    @root_validator(pre=True)
    def ensure_solution_structure(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures the solutions field has the right structure."""
        if "solutions" in values and isinstance(values["solutions"], dict):
            values["solutions"] = Solution(**values["solutions"])
        return values

    @root_validator(pre=True)
    def ensure_test_set_structure(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures test sets have the right structure."""
        for field in ["public_tests", "private_tests", "generated_tests"]:
            if field in values and isinstance(values[field], dict):
                values[field] = TestSet(**values[field])
        return values

    def get_python3_solution(self) -> Optional[str]:
        """
        Extract a Python 3 solution from the problem's solutions.

        Returns:
            Python 3 solution code or None if not found
        """
        # Python 3 is language code 3
        python3_solutions = []
        for i, lang in enumerate(self.solutions.language):
            if lang == 3 and i < len(self.solutions.solution):
                python3_solutions.append(self.solutions.solution[i])

        return python3_solutions[0] if python3_solutions else None

    def get_all_test_cases(self, min_test_cases: int = 10) -> List[Dict[str, str]]:
        """
        Get all test cases from public, private, and generated tests.

        Args:
            min_test_cases: Minimum number of test cases to aim for

        Returns:
            List of test cases as dicts with 'input' and 'output' keys
        """
        all_inputs = []
        all_outputs = []

        # Add public tests
        all_inputs.extend(self.public_tests.input)
        all_outputs.extend(self.public_tests.output)

        # Add private tests if available
        all_inputs.extend(self.private_tests.input)
        all_outputs.extend(self.private_tests.output)

        # Add generated tests if available and if we need more tests
        if len(all_inputs) < min_test_cases and self.generated_tests:
            gen_inputs = self.generated_tests.input
            gen_outputs = self.generated_tests.output
            if len(gen_inputs) == len(gen_outputs):
                all_inputs.extend(gen_inputs)
                all_outputs.extend(gen_outputs)

        # Make sure we have the same number of inputs and outputs
        # but also truncate to 10
        min_count = min(len(all_inputs), len(all_outputs), min_test_cases)
        all_inputs = all_inputs[:min_count]
        all_outputs = all_outputs[:min_count]

        return [{"input": inp, "output": out} for inp, out in zip(all_inputs, all_outputs, strict=False)]

    def get_source_name(self) -> str:
        """
        Get the source platform name.

        Returns:
            Name of the source platform
        """
        return {
            1: "CodeChef",
            2: "Codeforces",
            3: "AtCoder",
            4: "HackerEarth",
            5: "Aizu",
        }.get(self.source or 0, "Unknown")

    def get_difficulty_name(self) -> str:
        """
        Get the difficulty level as a string.

        Returns:
            String representation of difficulty
        """
        if not self.difficulty:
            return "Unknown"

        return {
            1: "very easy",
            2: "easy",
            3: "easy-medium",
            4: "medium",
            5: "medium-hard",
            6: "hard",
            7: "very hard",
        }.get(self.difficulty, str(self.difficulty))
