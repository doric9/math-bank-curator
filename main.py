#!/usr/bin/env python3
"""
Math Bank Curator - Agentic Math Problem Generator

This application uses Google's Agent Development Kit (ADK) to create an autonomous
workflow for generating and validating mathematical problems.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.orchestrator_agent import MathProblemOrchestrator
from src.agents.seed_prep_agent import prep_seeds_from_text
from src.agents.scraper_agent import scrape_and_prep, scrape_multiple_urls, read_file_content, extract_problems_from_text
from src.problem_bank import ProblemBank


def check_api_key() -> Optional[str]:
    """
    Check if API key is set and return it.

    Returns:
        API key if found, None otherwise
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  Warning: GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set.")
        print("   Please set your Gemini API key to use the application.")
        print("\n   Example:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("\n   You can get an API key from: https://makersuite.google.com/app/apikey")
    return api_key


def load_seed_problems(file_path: str = "examples/seed_problems.json") -> List[Dict]:
    """Load seed problems from JSON file"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data.get("problems", [])
    except FileNotFoundError:
        print(f"Error: Seed problems file not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}")
        return []


def display_banner():
    """Display application banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           📚 MATH BANK CURATOR 📚                            ║
║                                                               ║
║         Agentic Math Problem Generator using ADK              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def display_statistics(orchestrator: MathProblemOrchestrator):
    """Display problem bank statistics"""
    stats = orchestrator.get_bank_statistics()
    print("\n" + "="*60)
    print("📊 PROBLEM BANK STATISTICS")
    print("="*60)
    print(f"Total Problems: {stats['total_problems']}")
    print(f"Validated Problems: {stats['validated_problems']}")
    print("="*60 + "\n")


def display_results(results: Dict):
    """Display processing results"""
    print("\n" + "="*60)
    print("📈 PROCESSING RESULTS")
    print("="*60)
    print(f"Seeds Processed: {results['total_seeds']}")
    print(f"Problems Generated: {results['total_generated']}")
    print(f"Problems Validated: {results['total_validated']}")
    print(f"Problems Rejected: {results['total_rejected']}")

    if results['total_generated'] > 0:
        success_rate = (results['total_validated'] / results['total_generated']) * 100
        print(f"Success Rate: {success_rate:.1f}%")

    print("="*60)


def run_generator(args):
    """Run the problem generator workflow"""
    display_banner()

    # Check for API key
    if not check_api_key():
        return

    # Load seed problems
    print(f"📖 Loading seed problems from: {args.seeds}")
    seed_problems = load_seed_problems(args.seeds)

    if not seed_problems:
        print("❌ No seed problems found. Please check the seed file.")
        return

    print(f"✅ Loaded {len(seed_problems)} seed problems")

    # Initialize orchestrator
    print(f"🚀 Initializing orchestrator with model: {args.model}")
    orchestrator = MathProblemOrchestrator(model_name=args.model)

    # Display initial statistics
    display_statistics(orchestrator)

    # Process seeds
    print(f"\n🎯 Generating {args.variations} variations per seed problem...")
    print("   This may take a few minutes...\n")

    results = orchestrator.process_multiple_seeds(
        seed_problems[:args.num_seeds],
        variations_per_seed=args.variations
    )

    # Display results
    display_results(results)
    display_statistics(orchestrator)

    # Show sample problems if requested
    if args.show_samples and results['total_validated'] > 0:
        print("\n" + "="*60)
        print("📝 SAMPLE GENERATED PROBLEMS")
        print("="*60)

        bank = ProblemBank()
        problems = bank.get_validated_problems()[-3:]  # Show last 3

        for i, problem in enumerate(problems, 1):
            print(f"\n--- Problem {i} ---")
            print(f"Topic: {problem.topic}")
            print(f"Difficulty: {problem.difficulty}")
            print(f"Score: {problem.validation_score:.2f}")
            print(f"\nProblem:\n{problem.problem_text[:200]}...")
            print("="*60)


def run_scrape(args):
    """Run the scraping workflow"""
    display_banner()

    # Check for API key
    if not check_api_key():
        return

    print(f"🤖 Using model: {args.model}")
    print(f"📤 Output will be saved to: {args.output}\n")

    try:
        if args.url:
            # Scrape single URL
            print(f"🌐 Scraping URL: {args.url}")
            seed_json = scrape_and_prep(args.url, args.output, args.model)

        elif args.urls_file:
            # Scrape multiple URLs from file
            print(f"📋 Loading URLs from: {args.urls_file}")
            with open(args.urls_file, 'r') as f:
                urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]

            print(f"Found {len(urls)} URLs to scrape\n")
            seed_json = scrape_multiple_urls(urls, args.output, args.model)

        elif args.file:
            # Extract from local file
            print(f"📄 Reading file: {args.file}")
            text = read_file_content(args.file)

            print("🔍 Extracting problems from file...")
            problems = extract_problems_from_text(text, args.model)

            if not problems:
                print("❌ No problems found in file")
                return

            print(f"Found {len(problems)} problems")

            # Parse and create seeds
            from src.agents.seed_prep_agent import parse_natural_language_problem, create_seed_json
            parsed = []
            for problem in problems:
                try:
                    p = parse_natural_language_problem(problem, args.model)
                    parsed.append(p)
                except Exception as e:
                    print(f"⚠️  Warning: Failed to parse a problem: {e}")
                    continue

            seed_json = create_seed_json(parsed, args.output)

        else:
            print("❌ Error: Must specify --url, --urls-file, or --file")
            return

        # Display results
        print("\n" + "="*60)
        print("✅ SCRAPING COMPLETE")
        print("="*60)
        print(f"Problems extracted: {len(seed_json['problems'])}")
        print(f"Output file: {args.output}")
        print("="*60 + "\n")

        # Show summary
        print("📊 Scraped Problems Summary:\n")
        for i, prob in enumerate(seed_json['problems'], 1):
            print(f"{i}. {prob['topic'].title()} - {prob['difficulty'].title()}")
            print(f"   {prob['problem'][:80]}...")
            print()

        print(f"\n💡 Next step: Generate problems from these seeds:")
        print(f"   python main.py generate --seeds {args.output}")

    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")
        import traceback
        traceback.print_exc()


def run_prep(args):
    """Run the seed preparation workflow"""
    display_banner()

    # Check for API key
    if not check_api_key():
        return

    # Get input text
    if args.text:
        # Direct text input
        input_text = args.input
        print(f"📝 Processing direct text input...")
    else:
        # File input
        try:
            with open(args.input, 'r') as f:
                input_text = f.read()
            print(f"📖 Loaded problems from: {args.input}")
        except FileNotFoundError:
            print(f"❌ Error: File not found: {args.input}")
            return
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return

    print(f"🤖 Using model: {args.model}")
    print(f"📤 Output will be saved to: {args.output}\n")

    try:
        # Run seed preparation
        seed_json = prep_seeds_from_text(input_text, args.output, args.model)

        # Display results
        print("\n" + "="*60)
        print("✅ SEED PREPARATION COMPLETE")
        print("="*60)
        print(f"Problems parsed: {len(seed_json['problems'])}")
        print(f"Output file: {args.output}")
        print("="*60 + "\n")

        # Show summary of parsed problems
        print("📊 Parsed Problems Summary:\n")
        for i, prob in enumerate(seed_json['problems'], 1):
            print(f"{i}. {prob['topic'].title()} - {prob['difficulty'].title()}")
            print(f"   {prob['problem'][:80]}...")
            print()

        print(f"\n💡 Next step: Generate problems from these seeds:")
        print(f"   python main.py generate --seeds {args.output}")

    except Exception as e:
        print(f"\n❌ Error during seed preparation: {e}")
        import traceback
        traceback.print_exc()


def view_problems(args):
    """View problems in the problem bank"""
    display_banner()

    bank = ProblemBank()
    problems = bank.get_all_problems()

    if not problems:
        print("📭 The problem bank is empty.")
        return

    print(f"📚 Problem Bank contains {len(problems)} problems\n")

    # Filter by topic if specified
    if args.topic:
        problems = [p for p in problems if p.topic.lower() == args.topic.lower()]
        print(f"Filtered to topic '{args.topic}': {len(problems)} problems\n")

    # Display problems
    for i, problem in enumerate(problems[:args.limit], 1):
        print(f"\n{'='*60}")
        print(f"Problem {i} (ID: {problem.id[:8]}...)")
        print(f"{'='*60}")
        print(f"Topic: {problem.topic}")
        print(f"Difficulty: {problem.difficulty}")
        print(f"Validated: {problem.validated}")
        print(f"Score: {problem.validation_score:.2f}")
        print(f"\nProblem:\n{problem.problem_text}")
        if args.show_solutions:
            print(f"\nSolution:\n{problem.solution}")
        print(f"\nCreated: {problem.created_at}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Math Bank Curator - Agentic Math Problem Generator using ADK"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate new math problems")
    gen_parser.add_argument(
        "--seeds",
        default="examples/seed_problems.json",
        help="Path to seed problems JSON file"
    )
    gen_parser.add_argument(
        "--num-seeds",
        type=int,
        default=5,
        help="Number of seed problems to process (default: 5)"
    )
    gen_parser.add_argument(
        "--variations",
        type=int,
        default=3,
        help="Number of variations to generate per seed (default: 3)"
    )
    gen_parser.add_argument(
        "--model",
        default="gemini-3-pro-preview",
        help="Gemini model to use (default: gemini-3-pro-preview)"
    )
    gen_parser.add_argument(
        "--show-samples",
        action="store_true",
        help="Show sample generated problems at the end"
    )

    # View command
    view_parser = subparsers.add_parser("view", help="View problems in the bank")
    view_parser.add_argument(
        "--topic",
        help="Filter by topic"
    )
    view_parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Maximum number of problems to display (default: 10)"
    )
    view_parser.add_argument(
        "--show-solutions",
        action="store_true",
        help="Show solutions along with problems"
    )

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show problem bank statistics")

    # Prep command
    prep_parser = subparsers.add_parser("prep", help="Prepare seed problems from natural language")
    prep_parser.add_argument(
        "--input",
        required=True,
        help="Input file with natural language problems or direct text"
    )
    prep_parser.add_argument(
        "--output",
        default="examples/prepared_seeds.json",
        help="Output JSON file (default: examples/prepared_seeds.json)"
    )
    prep_parser.add_argument(
        "--text",
        action="store_true",
        help="Treat --input as direct text instead of file path"
    )
    prep_parser.add_argument(
        "--model",
        default="gemini-3-pro-preview",
        help="Gemini model to use (default: gemini-3-pro-preview)"
    )

    # Scrape command
    scrape_parser = subparsers.add_parser("scrape", help="Scrape math problems from URLs or files")
    scrape_parser.add_argument(
        "--url",
        help="URL to scrape problems from"
    )
    scrape_parser.add_argument(
        "--urls-file",
        help="File containing list of URLs (one per line)"
    )
    scrape_parser.add_argument(
        "--file",
        help="Local file to extract problems from (txt, pdf, html)"
    )
    scrape_parser.add_argument(
        "--output",
        default="examples/scraped_seeds.json",
        help="Output JSON file (default: examples/scraped_seeds.json)"
    )
    scrape_parser.add_argument(
        "--model",
        default="gemini-3-pro-preview",
        help="Gemini model to use (default: gemini-3-pro-preview)"
    )

    args = parser.parse_args()

    if args.command == "generate":
        run_generator(args)
    elif args.command == "view":
        view_problems(args)
    elif args.command == "stats":
        display_banner()
        orchestrator = MathProblemOrchestrator()
        display_statistics(orchestrator)
    elif args.command == "prep":
        run_prep(args)
    elif args.command == "scrape":
        run_scrape(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
