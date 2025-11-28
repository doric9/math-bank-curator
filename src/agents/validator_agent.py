"""Validator Agent - Validates mathematical problems for accuracy and quality"""

from google.genai.adk import Agent, Runner
from google.genai import types
from typing import Dict, Any, Optional
import re
import logging

from src.constants import (
    DEFAULT_MODEL,
    VALIDATOR_TEMPERATURE,
    VALIDATOR_TOP_P,
    VALIDATOR_TOP_K,
    VALIDATOR_MAX_TOKENS,
    MIN_PASSING_SCORE,
    VALIDATION_RESULT_PATTERN,
    SCORE_PATTERN,
    MATHEMATICAL_ACCURACY_PATTERN,
    SOLUTION_CORRECTNESS_PATTERN,
    CLARITY_COMPLETENESS_PATTERN,
    EDUCATIONAL_VALUE_PATTERN,
    FEEDBACK_PATTERN,
    ISSUES_PATTERN,
    RECOMMENDATION_PATTERN,
    MATHEMATICAL_ACCURACY_WEIGHT,
    SOLUTION_CORRECTNESS_WEIGHT,
    CLARITY_COMPLETENESS_WEIGHT,
    EDUCATIONAL_VALUE_WEIGHT,
    MAX_SCORE
)
from src.utils import retry_on_exception, safe_int_extraction, safe_regex_search, sanitize_text

logger = logging.getLogger(__name__)


def create_validator_agent(model_name: str = DEFAULT_MODEL) -> Agent:
    """
    Create the math problem validator agent.

    This agent validates generated problems for:
    - Mathematical accuracy
    - Solution correctness
    - Clarity and completeness
    - Educational value

    Args:
        model_name: The Gemini model to use

    Returns:
        Configured ADK Agent
    """

    instructions = f"""You are a mathematical problem validation agent.

Your role is to rigorously validate mathematical problems for accuracy, completeness, and quality.

For each problem, evaluate:

1. MATHEMATICAL ACCURACY ({MATHEMATICAL_ACCURACY_WEIGHT} points)
   - Is the problem mathematically sound?
   - Are there any logical errors or contradictions?
   - Is the solution method correct?

2. SOLUTION CORRECTNESS ({SOLUTION_CORRECTNESS_WEIGHT} points)
   - Is the final answer correct?
   - Are all steps in the solution valid?
   - Is the reasoning clear and logical?

3. CLARITY & COMPLETENESS ({CLARITY_COMPLETENESS_WEIGHT} points)
   - Is the problem statement clear and unambiguous?
   - Does it contain all necessary information?
   - Is the solution well-explained?

4. EDUCATIONAL VALUE ({EDUCATIONAL_VALUE_WEIGHT} points)
   - Is the problem engaging and instructive?
   - Does it promote mathematical thinking?
   - Is it appropriate for the stated difficulty level?

Provide your validation in this EXACT format:
---
VALIDATION RESULT: [PASS/FAIL]
SCORE: [0-{MAX_SCORE}]

MATHEMATICAL_ACCURACY: [0-{MATHEMATICAL_ACCURACY_WEIGHT}]
SOLUTION_CORRECTNESS: [0-{SOLUTION_CORRECTNESS_WEIGHT}]
CLARITY_COMPLETENESS: [0-{CLARITY_COMPLETENESS_WEIGHT}]
EDUCATIONAL_VALUE: [0-{EDUCATIONAL_VALUE_WEIGHT}]

FEEDBACK:
[Detailed feedback on the problem and solution]

ISSUES:
[List any mathematical errors, unclear points, or missing information. Write "None" if no issues]

RECOMMENDATION: [ACCEPT/REVISE/REJECT]
---

A problem PASSES if score >= {MIN_PASSING_SCORE} and has no critical mathematical errors.
"""

    agent = Agent(
        model=model_name,
        system_instruction=instructions,
        generation_config=types.GenerationConfig(
            temperature=VALIDATOR_TEMPERATURE,
            top_p=VALIDATOR_TOP_P,
            top_k=VALIDATOR_TOP_K,
            max_output_tokens=VALIDATOR_MAX_TOKENS,
        )
    )

    return agent


@retry_on_exception(max_retries=3, delay=2.0)
def validate_problem(
    problem_text: str,
    solution: str,
    model_name: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """
    Validate a mathematical problem.

    Args:
        problem_text: The problem statement
        solution: The proposed solution
        model_name: The model to use

    Returns:
        Dictionary with validation results

    Raises:
        ValueError: If inputs are invalid
        RuntimeError: If validation fails after retries
    """
    # Input validation
    if not problem_text or not problem_text.strip():
        raise ValueError("Problem text cannot be empty")
    if not solution or not solution.strip():
        raise ValueError("Solution cannot be empty")

    # Sanitize inputs
    problem_text = sanitize_text(problem_text)
    solution = sanitize_text(solution)

    try:
        agent = create_validator_agent(model_name)
        runner = Runner(agent=agent)

        prompt = f"""Validate this mathematical problem:

PROBLEM:
{problem_text}

SOLUTION:
{solution}

Provide a complete validation report following the exact format specified in your instructions.
"""

        result = runner.run(prompt)
        validation_text = result.messages[-1].content[0].text if result.messages else ""

        if not validation_text:
            logger.error("Validator returned empty response")
            raise RuntimeError("Validator returned empty response")

        # Parse the validation result
        parsed = parse_validation_result(validation_text)
        return parsed

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise


def parse_validation_result(validation_text: str) -> Dict[str, Any]:
    """
    Parse the validation result text into structured data.

    Args:
        validation_text: Raw validation text from agent

    Returns:
        Structured validation dictionary
    """
    result = {
        "passed": False,
        "score": 0,
        "mathematical_accuracy": 0,
        "solution_correctness": 0,
        "clarity_completeness": 0,
        "educational_value": 0,
        "feedback": "",
        "issues": "",
        "recommendation": "REJECT",
        "raw_response": validation_text
    }

    # Extract PASS/FAIL
    pass_result = safe_regex_search(
        VALIDATION_RESULT_PATTERN,
        validation_text,
        group=1,
        flags=re.IGNORECASE
    )
    if pass_result:
        result["passed"] = pass_result.upper() == "PASS"

    # Extract scores with bounds checking
    result["score"] = safe_int_extraction(
        SCORE_PATTERN,
        validation_text,
        default=0,
        min_value=0,
        max_value=MAX_SCORE
    )

    result["mathematical_accuracy"] = safe_int_extraction(
        MATHEMATICAL_ACCURACY_PATTERN,
        validation_text,
        default=0,
        min_value=0,
        max_value=MATHEMATICAL_ACCURACY_WEIGHT
    )

    result["solution_correctness"] = safe_int_extraction(
        SOLUTION_CORRECTNESS_PATTERN,
        validation_text,
        default=0,
        min_value=0,
        max_value=SOLUTION_CORRECTNESS_WEIGHT
    )

    result["clarity_completeness"] = safe_int_extraction(
        CLARITY_COMPLETENESS_PATTERN,
        validation_text,
        default=0,
        min_value=0,
        max_value=CLARITY_COMPLETENESS_WEIGHT
    )

    result["educational_value"] = safe_int_extraction(
        EDUCATIONAL_VALUE_PATTERN,
        validation_text,
        default=0,
        min_value=0,
        max_value=EDUCATIONAL_VALUE_WEIGHT
    )

    # Extract feedback
    feedback = safe_regex_search(
        FEEDBACK_PATTERN,
        validation_text,
        group=1,
        default="",
        flags=re.DOTALL
    )
    if feedback:
        result["feedback"] = feedback.strip()

    # Extract issues
    issues = safe_regex_search(
        ISSUES_PATTERN,
        validation_text,
        group=1,
        default="",
        flags=re.DOTALL
    )
    if issues:
        result["issues"] = issues.strip()

    # Extract recommendation
    recommendation = safe_regex_search(
        RECOMMENDATION_PATTERN,
        validation_text,
        group=1,
        flags=re.IGNORECASE
    )
    if recommendation:
        result["recommendation"] = recommendation.upper()

    # Verify score consistency
    component_sum = (
        result["mathematical_accuracy"] +
        result["solution_correctness"] +
        result["clarity_completeness"] +
        result["educational_value"]
    )

    if abs(component_sum - result["score"]) > 5:  # Allow small discrepancy
        logger.warning(
            f"Score mismatch: total={result['score']}, "
            f"components={component_sum}"
        )

    return result
