"""Agent Factory - Unified creation of ADK agents"""

from google.adk import Agent
from google.genai import types
from typing import Optional

def create_agent(
    name: str,
    model: str,
    instructions: str,
    temperature: float = 0.3,
    top_p: float = 0.9,
    top_k: int = 40,
    max_output_tokens: int = 4096
) -> Agent:
    """
    Create a configured ADK Agent.

    Args:
        name: Agent name
        model: Gemini model name
        instructions: System instructions
        temperature: Generation temperature
        top_p: Nucleus sampling probability
        top_k: Top-k sampling
        max_output_tokens: Max output tokens

    Returns:
        Configured ADK Agent
    """
    return Agent(
        name=name,
        model=model,
        instruction=instructions,
        generate_content_config=types.GenerationConfig(
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            max_output_tokens=max_output_tokens,
        )
    )
