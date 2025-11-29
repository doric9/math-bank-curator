"""Problem bank storage and management"""

from typing import List, Dict, Any
import json
import os
import logging
from datetime import datetime
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class MathProblem(BaseModel):
    """Represents a mathematical problem"""

    id: str = Field(description="Unique identifier for the problem")
    problem_text: str = Field(description="The problem statement")
    solution: str = Field(description="The solution to the problem")
    difficulty: str = Field(description="Difficulty level: easy, medium, hard")
    topic: str = Field(description="Mathematical topic (e.g., algebra, geometry)")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    validated: bool = Field(default=False, description="Whether the problem has been validated")
    validation_score: float = Field(default=0.0, description="Validation score 0-1")
    source_problem_id: str = Field(default="", description="ID of the problem this was generated from")
    diagram_code: str = Field(default="", description="Python code to generate diagram")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MathProblem':
        """Create from dictionary"""
        return cls(**data)


class ProblemBank:
    """Manages the storage and retrieval of math problems"""

    def __init__(self, storage_path: str = "src/problem_bank/problems.json"):
        self.storage_path = storage_path
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        """Ensure the storage file exists"""
        if not os.path.exists(self.storage_path):
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            with open(self.storage_path, 'w') as f:
                json.dump({"problems": []}, f, indent=2)

    def add_problem(self, problem: MathProblem) -> bool:
        """Add a validated problem to the bank"""
        try:
            problems = self.get_all_problems()

            # Check for duplicates
            if any(p.id == problem.id for p in problems):
                logger.warning(f"Problem with ID {problem.id} already exists")
                return False

            problems.append(problem)
            self._save_problems(problems)
            return True
        except Exception as e:
            logger.error(f"Error adding problem: {e}")
            return False

    def get_all_problems(self) -> List[MathProblem]:
        """Get all problems from the bank"""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [MathProblem.from_dict(p) for p in data.get("problems", [])]
        except Exception as e:
            logger.error(f"Error reading problems: {e}")
            return []

    def get_validated_problems(self) -> List[MathProblem]:
        """Get only validated problems"""
        return [p for p in self.get_all_problems() if p.validated]

    def _save_problems(self, problems: List[MathProblem]):
        """Save problems to storage"""
        with open(self.storage_path, 'w') as f:
            json.dump({
                "problems": [p.to_dict() for p in problems],
                "last_updated": datetime.now().isoformat()
            }, f, indent=2)

    def get_problem_count(self) -> int:
        """Get total number of problems"""
        return len(self.get_all_problems())

    def get_validated_count(self) -> int:
        """Get number of validated problems"""
        return len(self.get_validated_problems())
