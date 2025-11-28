"""Smart Scraper Agent - Scrapes and extracts math problems from various sources"""

from google.genai.adk import Agent, Runner
from google.genai import types
from typing import List, Dict, Any, Optional
import logging
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from src.constants import DEFAULT_MODEL
from src.utils import retry_on_exception, sanitize_text
from src.agents.seed_prep_agent import parse_natural_language_problem, create_seed_json

logger = logging.getLogger(__name__)


def create_scraper_agent(model_name: str = DEFAULT_MODEL) -> Agent:
    """
    Create the smart scraper agent.

    This agent extracts and cleans mathematical problems from scraped content,
    identifying problems and their context from unstructured text.

    Args:
        model_name: The Gemini model to use

    Returns:
        Configured ADK Agent
    """

    instructions = """You are a mathematical problem extraction agent.

Your role is to extract mathematical problems from unstructured text that may come from:
- Websites
- PDFs
- Educational materials
- Forums and discussion boards
- Problem sets and worksheets

For each piece of text provided, identify and extract all mathematical problems.

Output format:
For each problem found, output on a new line:
---PROBLEM---
[The extracted problem text]
---END---

Rules:
1. Extract complete problems (don't cut off mid-sentence)
2. Include all necessary context (given values, conditions)
3. Include solutions if they are present in the text
4. Ignore navigation text, headers, footers, ads
5. Ignore non-mathematical content
6. Clean up formatting issues (extra spaces, line breaks)
7. If a problem has multiple parts, include all parts
8. Preserve mathematical notation and symbols
9. If no problems are found, output "NO_PROBLEMS_FOUND"

Examples of what to extract:
✓ "What is the area of a circle with radius 5cm?"
✓ "Solve for x: 2x + 5 = 13"
✓ "A train travels at 60 mph for 2 hours. How far does it travel?"

Examples of what to ignore:
✗ Navigation menus
✗ Copyright notices
✗ "Click here to learn more"
✗ Advertisements
✗ Social media links
"""

    agent = Agent(
        model=model_name,
        system_instruction=instructions,
        generation_config=types.GenerationConfig(
            temperature=0.3,  # Lower for accurate extraction
            top_p=0.9,
            top_k=20,
            max_output_tokens=4096,
        )
    )

    return agent


@retry_on_exception(max_retries=3, delay=2.0)
def scrape_url(url: str, timeout: int = 30) -> str:
    """
    Scrape text content from a URL.

    Args:
        url: The URL to scrape
        timeout: Request timeout in seconds

    Returns:
        Extracted text content

    Raises:
        ValueError: If URL is invalid
        RuntimeError: If scraping fails
    """
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {url}")

    logger.info(f"Scraping URL: {url}")

    try:
        # Set user agent to avoid blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script, style, and nav elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            element.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)

        logger.info(f"Scraped {len(text)} characters from {url}")
        return text

    except requests.RequestException as e:
        logger.error(f"Failed to scrape {url}: {e}")
        raise RuntimeError(f"Failed to scrape URL: {e}")


@retry_on_exception(max_retries=3, delay=2.0)
def extract_problems_from_text(
    text: str,
    model_name: str = DEFAULT_MODEL
) -> List[str]:
    """
    Extract mathematical problems from text using AI.

    Args:
        text: Text to extract problems from
        model_name: Model to use

    Returns:
        List of extracted problem texts

    Raises:
        ValueError: If text is empty
        RuntimeError: If extraction fails
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    # Sanitize and truncate if needed
    text = sanitize_text(text, max_length=20000)

    logger.info("Extracting problems from text...")

    try:
        agent = create_scraper_agent(model_name)
        runner = Runner(agent=agent)

        prompt = f"""Extract all mathematical problems from this text:

{text}

Remember to output each problem in the format:
---PROBLEM---
[problem text]
---END---
"""

        result = runner.run(prompt)
        response = result.messages[-1].content[0].text if result.messages else ""

        if not response or "NO_PROBLEMS_FOUND" in response:
            logger.warning("No problems found in text")
            return []

        # Parse extracted problems
        problems = re.findall(r'---PROBLEM---(.*?)---END---', response, re.DOTALL)
        problems = [p.strip() for p in problems if p.strip()]

        logger.info(f"Extracted {len(problems)} problems")
        return problems

    except Exception as e:
        logger.error(f"Problem extraction failed: {e}")
        raise


def scrape_and_prep(
    url: str,
    output_file: str = "examples/scraped_seeds.json",
    model_name: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """
    Complete workflow: scrape URL, extract problems, convert to seeds.

    Args:
        url: URL to scrape
        output_file: Output JSON file
        model_name: Model to use

    Returns:
        Seed JSON structure

    Raises:
        ValueError: If URL is invalid
        RuntimeError: If process fails
    """
    logger.info(f"Starting scrape and prep workflow for: {url}")

    # Step 1: Scrape the URL
    text = scrape_url(url)

    # Step 2: Extract problems
    problems = extract_problems_from_text(text, model_name)

    if not problems:
        raise RuntimeError("No problems found at URL")

    logger.info(f"Found {len(problems)} problems")

    # Step 3: Parse each problem into structured format
    parsed_problems = []
    for i, problem_text in enumerate(problems, 1):
        try:
            logger.info(f"Parsing problem {i}/{len(problems)}...")
            parsed = parse_natural_language_problem(problem_text, model_name)
            parsed_problems.append(parsed)
        except Exception as e:
            logger.warning(f"Failed to parse problem {i}: {e}")
            continue

    if not parsed_problems:
        raise RuntimeError("No problems could be parsed")

    logger.info(f"Successfully parsed {len(parsed_problems)} problems")

    # Step 4: Create seed JSON
    seed_json = create_seed_json(parsed_problems, output_file)

    logger.info(f"Scrape and prep complete: {output_file}")

    return seed_json


def scrape_multiple_urls(
    urls: List[str],
    output_file: str = "examples/scraped_seeds.json",
    model_name: str = DEFAULT_MODEL
) -> Dict[str, Any]:
    """
    Scrape multiple URLs and combine into one seed file.

    Args:
        urls: List of URLs to scrape
        output_file: Output JSON file
        model_name: Model to use

    Returns:
        Combined seed JSON structure
    """
    all_parsed_problems = []

    for i, url in enumerate(urls, 1):
        try:
            logger.info(f"Processing URL {i}/{len(urls)}: {url}")

            # Scrape and extract
            text = scrape_url(url)
            problems = extract_problems_from_text(text, model_name)

            # Parse problems
            for problem_text in problems:
                try:
                    parsed = parse_natural_language_problem(problem_text, model_name)
                    all_parsed_problems.append(parsed)
                except Exception as e:
                    logger.warning(f"Failed to parse problem from {url}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Failed to process {url}: {e}")
            continue

    if not all_parsed_problems:
        raise RuntimeError("No problems could be extracted from any URL")

    logger.info(f"Total problems extracted: {len(all_parsed_problems)}")

    # Create seed JSON
    seed_json = create_seed_json(all_parsed_problems, output_file)

    return seed_json


def read_file_content(file_path: str) -> str:
    """
    Read content from various file types.

    Args:
        file_path: Path to file

    Returns:
        File content as text

    Raises:
        ValueError: If file type not supported
        RuntimeError: If reading fails
    """
    import os

    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == '.txt' or ext == '.md':
            # Plain text files
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        elif ext == '.pdf':
            # PDF files - requires PyPDF2
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            except ImportError:
                raise RuntimeError(
                    "PyPDF2 not installed. Install with: pip install PyPDF2"
                )

        elif ext in ['.html', '.htm']:
            # HTML files
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator='\n', strip=True)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    except Exception as e:
        logger.error(f"Failed to read file {file_path}: {e}")
        raise RuntimeError(f"Failed to read file: {e}")
