"""Generator Agent - Creates new math problems from examples"""

from google.adk import Agent
from google.genai import types
from typing import Optional
import logging

from src.constants import (
    DEFAULT_MODEL,
    GENERATOR_TEMPERATURE,
    GENERATOR_TOP_P,
    GENERATOR_TOP_K,
    GENERATOR_MAX_TOKENS
)
from src.utils import retry_on_exception, sanitize_text, run_agent_sync
from src.agent_factory import create_agent

logger = logging.getLogger(__name__)


def create_generator_agent(model_name: str = DEFAULT_MODEL) -> Agent:
    """
    Create the math problem generator agent.

    This agent generates new mathematical problems based on example problems,
    creating variations that maintain mathematical rigor while introducing novelty.

    Args:
        model_name: The Gemini model to use

    Returns:
        Configured ADK Agent
    """

    instructions = """You are a mathematical problem generator agent.

Your role is to create NEW, ORIGINAL mathematical problems based on example problems provided to you.

When generating problems:
1. Maintain the mathematical concepts and difficulty level of the source problem
2. Change the specific numbers, contexts, and scenarios to create novelty
3. Ensure the problem is solvable and mathematically rigorous
4. Provide a complete, step-by-step solution
5. Clearly state the difficulty level (easy, medium, hard) and topic
6. If the problem involves geometry, graphs, or visual data, provide Python code (using matplotlib) to generate the diagram.

Generate problems in this format:
---
PROBLEM:
[State the problem clearly with a question]

SOLUTION:
[Provide step-by-step solution with clear reasoning]

DIFFICULTY: [easy/medium/hard]
TOPIC: [e.g., algebra, geometry, calculus, probability]

DIAGRAM_CODE:
[Optional: Python code to generate the diagram. Use 'plt.show()' at the end. If no diagram is needed, write "NONE"]
---

Always generate problems that are:
- Mathematically accurate
- Educational and engaging
- Different enough from the source to be considered original
- Complete with both problem statement and solution
- Visually supported with code where applicable
"""

    return create_agent(
        name="generator",
        model=model_name,
        instructions=instructions,
        temperature=GENERATOR_TEMPERATURE,
        top_p=GENERATOR_TOP_P,
        top_k=GENERATOR_TOP_K,
        max_output_tokens=GENERATOR_MAX_TOKENS
    )


@retry_on_exception(max_retries=3, delay=2.0)
def generate_problem_from_example(
    example_problem: str,
    model_name: str = DEFAULT_MODEL
) -> str:
    """
    Generate a new problem based on an example.

    Args:
        example_problem: The example problem to base generation on
        model_name: The model to use

    Returns:
        Generated problem text

    Raises:
        ValueError: If example_problem is empty
        RuntimeError: If generation fails after retries
    """
    # Input validation
    if not example_problem or not example_problem.strip():
        raise ValueError("Example problem cannot be empty")

    # Sanitize input
    example_problem = sanitize_text(example_problem)

    try:
        agent = create_generator_agent(model_name)
        
        prompt = f"""Based on this example problem, generate a NEW and ORIGINAL problem:

{example_problem}

Generate a similar problem that:
1. Uses the same mathematical concepts
2. Has different numbers and context
3. Is equally challenging
4. Includes a complete solution
"""

        generated_text = run_agent_sync(agent, prompt)
        return generated_text

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        raise
