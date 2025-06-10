"""
Pydantic models for representing problems and test cases.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TestCase(BaseModel):
    """
    A single test case for a problem.
    """

    input: str = Field(..., description="Input text to provide via stdin")
    output: str = Field(..., description="Expected output text from stdout")
    time_limit_ms: Optional[int] = Field(30000, description="Time limit in milliseconds")
    memory_limit_mb: Optional[int] = Field(512, description="Memory limit in MB")


class Problem(BaseModel):
    """
    A competitive programming problem from the code_contests dataset.
    """

    id: str = Field(..., description="Unique identifier for the problem")
    name: str = Field(..., description="Problem title")
    description: str = Field(..., description="Problem description text")
    category: List[str] = Field(default_factory=list, description="Problem categories/tags")
    difficulty: Optional[str] = Field(None, description="Problem difficulty")
    test_cases: List[TestCase] = Field(..., description="Test cases for the problem")
    source: Optional[str] = Field(None, description="Source platform (e.g., Codeforces)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    def to_markdown(self) -> str:
        """
        Convert the problem to a Markdown format for PROBLEM.md files.
        """
        sections = [
            f"# {self.name}\n",
            f"**ID:** {self.id}",
            f"**Difficulty:** {self.difficulty or 'Unknown'}\n",
            "## Description\n",
            f"{self.description}\n",
        ]

        if self.category:
            sections.append("## Categories\n")
            sections.append("\n".join(f"- {cat}" for cat in self.category))

        if self.source:
            sections.append(f"\n## Source\n\n{self.source}")

        return "\n".join(sections)
