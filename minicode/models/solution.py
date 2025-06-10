"""
Pydantic models for representing solutions and execution results.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class Solution(BaseModel):
    """
    A solution to a competitive programming problem.
    """

    problem_id: str = Field(..., description="ID of the problem this solution is for")
    code: str = Field(..., description="Source code of the solution")
    language: str = Field("python", description="Programming language of the solution")
    uses_shared_lib: bool = Field(False, description="Whether the solution uses the shared library")
    original_code: Optional[str] = Field(None, description="Original code before refactoring")
    metrics: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Performance metrics")


class ExecutionResult(BaseModel):
    """
    Results from executing a solution against test cases.
    """

    passed: List[bool] = Field(..., description="Whether each test case passed")
    test_inputs: List[str] = Field(..., description="Test inputs used")
    test_outputs: List[str] = Field(..., description="Expected test outputs")
    predicted_outputs: List[str] = Field(..., description="Actual outputs from the solution")
    stderrs: List[str] = Field(..., description="Standard error output for each test")
    execution_times_ms: Optional[List[float]] = Field(None, description="Execution time for each test in ms")
    memory_usage_mb: Optional[List[float]] = Field(None, description="Memory usage for each test in MB")

    @property
    def all_passed(self) -> bool:
        """Check if all test cases passed."""
        return all(self.passed)

    @property
    def total_tests(self) -> int:
        """Total number of tests run."""
        return len(self.passed)

    @property
    def num_passed(self) -> int:
        """Number of tests passed."""
        return sum(1 for p in self.passed if p)

    def summary(self) -> str:
        """Generate a human-readable summary of the execution results."""
        result = f"Tests: {self.num_passed}/{self.total_tests} passed\n"

        if self.execution_times_ms:
            avg_time = sum(self.execution_times_ms) / len(self.execution_times_ms)
            result += f"Average execution time: {avg_time:.2f} ms\n"

        if self.memory_usage_mb:
            avg_mem = sum(self.memory_usage_mb) / len(self.memory_usage_mb)
            result += f"Average memory usage: {avg_mem:.2f} MB\n"

        for i, (passed, stderr) in enumerate(zip(self.passed, self.stderrs, strict=False)):
            if not passed:
                result += f"\nTest #{i+1} failed:\n"
                result += f"Expected: {self.test_outputs[i]}\n"
                result += f"Got: {self.predicted_outputs[i]}\n"
                if stderr:
                    result += f"Error: {stderr}\n"

        return result
