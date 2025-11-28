"""Validator Agent - Validates mathematical problems for accuracy and quality"""

from google.genai.adk import Agent, Runner
from google.genai import types
from typing import Dict, Any
import json
import re


def create_validator_agent(model_name: str = "gemini-3-pro-preview") -> Agent:
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

    instructions = """You are a mathematical problem validation agent.

Your role is to rigorously validate mathematical problems for accuracy, completeness, and quality.

For each problem, evaluate:

1. MATHEMATICAL ACCURACY (40 points)
   - Is the problem mathematically sound?
   - Are there any logical errors or contradictions?
   - Is the solution method correct?

2. SOLUTION CORRECTNESS (30 points)
   - Is the final answer correct?
   - Are all steps in the solution valid?
   - Is the reasoning clear and logical?

3. CLARITY & COMPLETENESS (20 points)
   - Is the problem statement clear and unambiguous?
   - Does it contain all necessary information?
   - Is the solution well-explained?

4. EDUCATIONAL VALUE (10 points)
   - Is the problem engaging and instructive?
   - Does it promote mathematical thinking?
   - Is it appropriate for the stated difficulty level?

Provide your validation in this EXACT format:
---
VALIDATION RESULT: [PASS/FAIL]
SCORE: [0-100]

MATHEMATICAL_ACCURACY: [0-40]
SOLUTION_CORRECTNESS: [0-30]
CLARITY_COMPLETENESS: [0-20]
EDUCATIONAL_VALUE: [0-10]

FEEDBACK:
[Detailed feedback on the problem and solution]

ISSUES:
[List any mathematical errors, unclear points, or missing information. Write "None" if no issues]

RECOMMENDATION: [ACCEPT/REVISE/REJECT]
---

A problem PASSES if score >= 70 and has no critical mathematical errors.
"""

    agent = Agent(
        model=model_name,
        system_instruction=instructions,
        generation_config=types.GenerationConfig(
            temperature=0.3,  # Lower temperature for consistency
            top_p=0.9,
            top_k=20,
            max_output_tokens=2048,
        )
    )

    return agent


def validate_problem(problem_text: str, solution: str, model_name: str = "gemini-3-pro-preview") -> Dict[str, Any]:
    """
    Validate a mathematical problem.

    Args:
        problem_text: The problem statement
        solution: The proposed solution
        model_name: The model to use

    Returns:
        Dictionary with validation results
    """
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

    # Parse the validation result
    parsed = parse_validation_result(validation_text)
    return parsed


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
    pass_match = re.search(r'VALIDATION RESULT:\s*(PASS|FAIL)', validation_text, re.IGNORECASE)
    if pass_match:
        result["passed"] = pass_match.group(1).upper() == "PASS"

    # Extract overall score
    score_match = re.search(r'SCORE:\s*(\d+)', validation_text)
    if score_match:
        result["score"] = int(score_match.group(1))

    # Extract component scores
    math_acc_match = re.search(r'MATHEMATICAL_ACCURACY:\s*(\d+)', validation_text)
    if math_acc_match:
        result["mathematical_accuracy"] = int(math_acc_match.group(1))

    sol_corr_match = re.search(r'SOLUTION_CORRECTNESS:\s*(\d+)', validation_text)
    if sol_corr_match:
        result["solution_correctness"] = int(sol_corr_match.group(1))

    clarity_match = re.search(r'CLARITY_COMPLETENESS:\s*(\d+)', validation_text)
    if clarity_match:
        result["clarity_completeness"] = int(clarity_match.group(1))

    edu_match = re.search(r'EDUCATIONAL_VALUE:\s*(\d+)', validation_text)
    if edu_match:
        result["educational_value"] = int(edu_match.group(1))

    # Extract feedback
    feedback_match = re.search(r'FEEDBACK:\s*(.+?)(?=ISSUES:|$)', validation_text, re.DOTALL)
    if feedback_match:
        result["feedback"] = feedback_match.group(1).strip()

    # Extract issues
    issues_match = re.search(r'ISSUES:\s*(.+?)(?=RECOMMENDATION:|$)', validation_text, re.DOTALL)
    if issues_match:
        result["issues"] = issues_match.group(1).strip()

    # Extract recommendation
    rec_match = re.search(r'RECOMMENDATION:\s*(ACCEPT|REVISE|REJECT)', validation_text, re.IGNORECASE)
    if rec_match:
        result["recommendation"] = rec_match.group(1).upper()

    return result
