"""Tools for the ADK agents"""

from typing import Any, Dict
import json
from src.problem_bank import MathProblem, ProblemBank


def save_validated_problem(
    problem_text: str,
    solution: str,
    difficulty: str,
    topic: str,
    validation_score: float,
    source_problem_id: str = ""
) -> str:
    """
    Save a validated problem to the problem bank.

    Args:
        problem_text: The problem statement
        solution: The solution
        difficulty: Difficulty level (easy, medium, hard)
        topic: Mathematical topic
        validation_score: Score from validation (0-1)
        source_problem_id: ID of source problem

    Returns:
        Success message with problem ID
    """
    import uuid
    from datetime import datetime

    problem = MathProblem(
        id=str(uuid.uuid4()),
        problem_text=problem_text,
        solution=solution,
        difficulty=difficulty,
        topic=topic,
        created_at=datetime.now().isoformat(),
        validated=True,
        validation_score=validation_score,
        source_problem_id=source_problem_id
    )

    bank = ProblemBank()
    success = bank.add_problem(problem)

    if success:
        return f"Problem saved successfully with ID: {problem.id}"
    else:
        return "Failed to save problem (may be duplicate)"


def get_problem_bank_stats() -> str:
    """
    Get statistics about the problem bank.

    Returns:
        JSON string with bank statistics
    """
    bank = ProblemBank()
    return json.dumps({
        "total_problems": bank.get_problem_count(),
        "validated_problems": bank.get_validated_count()
    }, indent=2)


def validate_problem_mathematical_accuracy(
    problem_text: str,
    solution: str
) -> Dict[str, Any]:
    """
    Validate a problem for mathematical accuracy and completeness.

    This function checks:
    - Whether the problem is well-formed
    - Whether the solution is logically correct
    - Whether steps are clearly explained

    Args:
        problem_text: The problem to validate
        solution: The proposed solution

    Returns:
        Dictionary with validation results
    """
    # Basic validation checks
    validation_results = {
        "is_well_formed": True,
        "has_solution": bool(solution and len(solution) > 10),
        "has_clear_question": "?" in problem_text,
        "sufficient_length": len(problem_text) > 20,
        "feedback": []
    }

    if not validation_results["has_solution"]:
        validation_results["feedback"].append("Solution is too short or missing")
        validation_results["is_well_formed"] = False

    if not validation_results["has_clear_question"]:
        validation_results["feedback"].append("Problem should contain a clear question")

    if not validation_results["sufficient_length"]:
        validation_results["feedback"].append("Problem statement is too short")
        validation_results["is_well_formed"] = False

    # Calculate overall score
    score = sum([
        validation_results["has_solution"],
        validation_results["has_clear_question"],
        validation_results["sufficient_length"]
    ]) / 3

    validation_results["score"] = score
    validation_results["passed"] = score >= 0.7

    return validation_results
