"""Utility functions and helpers for the Math Bank Curator"""

import re
import time
from typing import Optional, Callable, TypeVar, Dict, Any
from functools import wraps
import logging

from google.adk import Agent, Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

from src.constants import (
    MAX_RETRIES,
    RETRY_DELAY,
    VALID_DIFFICULTIES,
    DEFAULT_DIFFICULTY
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

T = TypeVar('T')


def validate_difficulty(difficulty: str) -> str:
    """
    Validate and normalize difficulty level.

    Args:
        difficulty: The difficulty string to validate

    Returns:
        Validated difficulty level (lowercased)

    Raises:
        ValueError: If difficulty is not valid
    """
    normalized = difficulty.lower().strip()
    if normalized not in VALID_DIFFICULTIES:
        logger.warning(
            f"Invalid difficulty '{difficulty}', using default '{DEFAULT_DIFFICULTY}'"
        )
        return DEFAULT_DIFFICULTY
    return normalized


def validate_positive_int(value: int, name: str, min_value: int = 1) -> int:
    """
    Validate that an integer is positive.

    Args:
        value: The value to validate
        name: Name of the parameter (for error messages)
        min_value: Minimum allowed value (default: 1)

    Returns:
        The validated value

    Raises:
        ValueError: If value is less than min_value
    """
    if value < min_value:
        raise ValueError(f"{name} must be at least {min_value}, got {value}")
    return value


def sanitize_text(text: str, max_length: int = 10000) -> str:
    """
    Sanitize text input by removing potentially problematic characters.

    Args:
        text: The text to sanitize
        max_length: Maximum allowed length

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Truncate if too long
    if len(text) > max_length:
        logger.warning(f"Text truncated from {len(text)} to {max_length} characters")
        text = text[:max_length]

    # Remove null bytes and other control characters
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)

    return text.strip()


def retry_on_exception(
    max_retries: int = MAX_RETRIES,
    delay: float = RETRY_DELAY,
    exceptions: tuple = (Exception,)
) -> Callable:
    """
    Decorator to retry a function on exception.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        exceptions: Tuple of exceptions to catch

    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = delay * (2 ** attempt)  # Exponential backoff
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                            f"Retrying in {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed")

            raise last_exception

        return wrapper
    return decorator


def safe_regex_search(
    pattern: str,
    text: str,
    group: int = 1,
    default: Any = None,
    flags: int = 0
) -> Optional[str]:
    """
    Safely search for a regex pattern and return a group.

    Args:
        pattern: Regex pattern to search for
        text: Text to search in
        group: Group number to return (default: 1)
        default: Default value if no match found
        flags: Regex flags

    Returns:
        Matched group or default value
    """
    try:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(group)
        return default
    except Exception as e:
        logger.error(f"Regex search failed: {e}")
        return default


def safe_int_extraction(
    pattern: str,
    text: str,
    default: int = 0,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None
) -> int:
    """
    Safely extract an integer from text using regex.

    Args:
        pattern: Regex pattern to search for
        text: Text to search in
        default: Default value if extraction fails
        min_value: Minimum allowed value
        max_value: Maximum allowed value

    Returns:
        Extracted integer or default
    """
    try:
        match = re.search(pattern, text)
        if match:
            value = int(match.group(1))

            # Apply bounds if specified
            if min_value is not None and value < min_value:
                logger.warning(f"Value {value} below minimum {min_value}, using {min_value}")
                return min_value
            if max_value is not None and value > max_value:
                logger.warning(f"Value {value} above maximum {max_value}, using {max_value}")
                return max_value

            return value
        return default
    except (ValueError, AttributeError) as e:
        logger.error(f"Integer extraction failed: {e}")
        return default

def run_agent_sync(
    agent: Agent,
    prompt: str | list[types.Part],
    app_name: str = "math-bank-curator",
    user_id: str = "user",
    session_id: str = "session"
) -> str:
    """
    Run an ADK agent synchronously and return the response text.
    Encapsulates session creation, runner initialization, and event loop handling.

    Args:
        agent: The ADK Agent instance to run
        prompt: The input prompt (string) or list of Parts (multimodal)
        app_name: Application name for the session (default: "math-bank-curator")
        user_id: User ID for the session (default: "user")
        session_id: Session ID (default: "session")

    Returns:
        The text response from the agent

    Raises:
        RuntimeError: If the agent returns an empty response
    """
    session_service = InMemorySessionService()
    session_service.create_session_sync(app_name=app_name, user_id=user_id, session_id=session_id)
    runner = Runner(agent=agent, session_service=session_service, app_name=app_name)

    if isinstance(prompt, str):
        prompt_content = types.Content(parts=[types.Part(text=prompt)])
    else:
        prompt_content = types.Content(parts=prompt)
    
    response_text = ""
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=prompt_content):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_text += part.text

    if not response_text:
        logger.error(f"Agent {agent.name} returned empty response")
        raise RuntimeError(f"Agent {agent.name} returned empty response")

    return response_text
