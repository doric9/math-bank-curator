"""Generator Agent - Creates new math problems from examples"""

from google.genai.adk import Agent, Runner
from google.genai import types
import os


def create_generator_agent(model_name: str = "gemini-3-pro-preview") -> Agent:
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

Generate problems in this format:
---
PROBLEM:
[State the problem clearly with a question]

SOLUTION:
[Provide step-by-step solution with clear reasoning]

DIFFICULTY: [easy/medium/hard]
TOPIC: [e.g., algebra, geometry, calculus, probability]
---

Always generate problems that are:
- Mathematically accurate
- Educational and engaging
- Different enough from the source to be considered original
- Complete with both problem statement and solution
"""

    agent = Agent(
        model=model_name,
        system_instruction=instructions,
        generation_config=types.GenerationConfig(
            temperature=0.9,  # Higher temperature for creativity
            top_p=0.95,
            top_k=40,
            max_output_tokens=2048,
        )
    )

    return agent


def generate_problem_from_example(example_problem: str, model_name: str = "gemini-3-pro-preview") -> str:
    """
    Generate a new problem based on an example.

    Args:
        example_problem: The example problem to base generation on
        model_name: The model to use

    Returns:
        Generated problem text
    """
    agent = create_generator_agent(model_name)
    runner = Runner(agent=agent)

    prompt = f"""Based on this example problem, generate a NEW and ORIGINAL problem:

{example_problem}

Generate a similar problem that:
1. Uses the same mathematical concepts
2. Has different numbers and context
3. Is equally challenging
4. Includes a complete solution
"""

    result = runner.run(prompt)
    return result.messages[-1].content[0].text if result.messages else ""
