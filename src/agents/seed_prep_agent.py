"""Seed Prep Agent - Parses natural language problems into JSON format"""

from google.adk import Agent
from google.genai import types
from typing import Dict, Any, List, Optional
import json
import logging
import uuid
from datetime import datetime

from src.constants import DEFAULT_MODEL, DEFAULT_DIFFICULTY, DEFAULT_TOPIC
from src.utils import retry_on_exception, sanitize_text, validate_difficulty, run_agent_sync
from src.agent_factory import create_agent

logger = logging.getLogger(__name__)


def create_seed_prep_agent(model_name: str = DEFAULT_MODEL) -> Agent:
    """
    Create the seed preparation agent.

    This agent parses natural language math problems into structured JSON format
    suitable for the problem bank system.

    Args:
        model_name: The Gemini model to use

    Returns:
        Configured ADK Agent
    """

    instructions = """You are a mathematical problem parsing agent.

Your role is to parse natural language mathematical problems into a structured JSON format.

For each problem provided, extract:
1. **Problem Statement** - The problem text with the question
2. **Solution** - The complete step-by-step solution
3. **Difficulty** - Classify as "easy", "medium", or "hard"
4. **Topic** - Identify the math topic (algebra, geometry, calculus, probability, etc.)

If the input doesn't include a solution, generate one.
If the input doesn't specify difficulty, infer it from the problem complexity.
If the input doesn't specify a topic, identify it from the mathematical concepts used.

Output ONLY valid JSON in this EXACT format:
```json
{
  "problem": "The complete problem statement with question",
  "solution": "Step-by-step solution with clear reasoning",
  "difficulty": "easy|medium|hard",
  "topic": "algebra|geometry|calculus|probability|etc"
}
```

Rules:
- Always output valid JSON (use proper escaping for quotes)
- Problem must end with a question
- Solution must have clear steps
- Difficulty must be one of: easy, medium, hard (lowercase)
- Topic should be a single word or hyphenated phrase
- Do not include extra text outside the JSON
- Ensure mathematical accuracy
"""

    return create_agent(
        name="seed_prep",
        model=model_name,
        instructions=instructions,
        temperature=0.3,
        top_p=0.9,
        top_k=20,
        max_output_tokens=8192
    )


@retry_on_exception(max_retries=3, delay=2.0)
def parse_natural_language_problem(
    natural_language_text: str,
    model_name: str = DEFAULT_MODEL
) -> Dict[str, str]:
    """
    Parse natural language math problem into structured format.

    Args:
        natural_language_text: Problem in natural language
        model_name: The model to use

    Returns:
        Dictionary with problem, solution, difficulty, topic

    Raises:
        ValueError: If input is invalid
        RuntimeError: If parsing fails
    """
    # Input validation
    if not natural_language_text or not natural_language_text.strip():
        raise ValueError("Input text cannot be empty")

    # Sanitize input
    natural_language_text = sanitize_text(natural_language_text, max_length=5000)

    try:
        agent = create_seed_prep_agent(model_name)

        prompt = f"""Parse this mathematical problem into JSON format:

{natural_language_text}

Remember to output ONLY the JSON object, nothing else.
"""

        response_text = run_agent_sync(agent, prompt)

        if not response_text:
            logger.error("Seed prep agent returned empty response")
            raise RuntimeError("Seed prep agent returned empty response")

        # Extract JSON from response (in case there's markdown formatting)
        parsed = extract_json_from_response(response_text)

        # Validate the parsed problem
        validate_parsed_problem(parsed)

        return parsed

    except Exception as e:
        logger.error(f"Problem parsing failed: {e}")
        raise


def extract_json_from_response(response_text: str) -> Dict[str, str]:
    """
    Extract JSON from response text, handling markdown code blocks.

    Args:
        response_text: Raw response from agent

    Returns:
        Parsed JSON dictionary

    Raises:
        ValueError: If JSON cannot be extracted or parsed
    """
    # Remove markdown code blocks if present
    import re
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
    if json_match:
        json_text = json_match.group(1)
    else:
        # Try to find JSON directly
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
        else:
            raise ValueError("No JSON found in response")

    try:
        parsed = json.loads(json_text)
        return parsed
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        raise ValueError(f"Invalid JSON in response: {e}")


def validate_parsed_problem(parsed: Dict[str, str]) -> None:
    """
    Validate that parsed problem has all required fields.

    Args:
        parsed: Parsed problem dictionary

    Raises:
        ValueError: If validation fails
    """
    required_fields = ["problem", "solution", "difficulty", "topic"]

    for field in required_fields:
        if field not in parsed:
            raise ValueError(f"Missing required field: {field}")
        if not parsed[field] or not parsed[field].strip():
            raise ValueError(f"Field '{field}' cannot be empty")

    # Validate difficulty
    parsed["difficulty"] = validate_difficulty(parsed["difficulty"])

    # Ensure problem ends with question mark or question word
    problem_text = parsed["problem"].strip()
    if not any(q in problem_text.lower() for q in ["?", "what", "how", "find", "calculate", "solve"]):
        logger.warning("Problem may not contain a clear question")


def parse_multiple_problems(
    problems_text: str,
    model_name: str = DEFAULT_MODEL
) -> List[Dict[str, str]]:
    """
    Parse multiple problems from text (separated by blank lines or numbers).

    Args:
        problems_text: Text containing multiple problems
        model_name: The model to use

    Returns:
        List of parsed problem dictionaries
    """
    # Split by double newlines or numbered lists
    import re
    problems = re.split(r'\n\n+|\n\d+\.\s+', problems_text)
    problems = [p.strip() for p in problems if p.strip()]

    parsed_problems = []
    for i, problem_text in enumerate(problems, 1):
        try:
            logger.info(f"Parsing problem {i}/{len(problems)}...")
            parsed = parse_natural_language_problem(problem_text, model_name)
            parsed_problems.append(parsed)
        except Exception as e:
            logger.error(f"Failed to parse problem {i}: {e}")
            # Continue with other problems

    return parsed_problems


def create_seed_json(
    parsed_problems: List[Dict[str, str]],
    output_file: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create seed JSON structure from parsed problems.

    Args:
        parsed_problems: List of parsed problem dictionaries
        output_file: Optional file path to save JSON

    Returns:
        Complete seed JSON structure
    """
    seed_json = {
        "problems": []
    }

    for i, problem in enumerate(parsed_problems, 1):
        seed_json["problems"].append({
            "id": f"seed-{uuid.uuid4().hex[:8]}",
            "problem": problem["problem"],
            "solution": problem["solution"],
            "difficulty": problem["difficulty"],
            "topic": problem["topic"]
        })

    # Save to file if specified
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(seed_json, f, indent=2)
        logger.info(f"Saved {len(parsed_problems)} problems to {output_file}")

    return seed_json


def prep_seeds_from_text(
    text: str,
    output_file: str = "examples/prepared_seeds.json",
    model_name: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """
    Complete workflow: parse text and create seed JSON.

    Args:
        text: Natural language problem(s)
        output_file: Output JSON file path
        model_name: Model to use

    Returns:
        Seed JSON structure
    """
    logger.info("Starting seed preparation...")

    # Parse problems
    parsed_problems = parse_multiple_problems(text, model_name)

    if not parsed_problems:
        raise RuntimeError("No problems could be parsed")

    logger.info(f"Successfully parsed {len(parsed_problems)} problems")

    # Create seed JSON
    seed_json = create_seed_json(parsed_problems, output_file)

    logger.info(f"Seed preparation complete: {output_file}")

    return seed_json
