"""Orchestrator Agent - Coordinates the multi-agent workflow"""

from google.genai.adk import Agent, Runner
from google.genai import types
from typing import List, Dict, Any
import json
import re

from src.agents.generator_agent import generate_problem_from_example
from src.agents.validator_agent import validate_problem
from src.problem_bank import MathProblem, ProblemBank
from datetime import datetime
import uuid


class MathProblemOrchestrator:
    """
    Orchestrates the multi-agent workflow for generating and validating math problems.

    This orchestrator:
    1. Takes seed problems as input
    2. Uses the Generator Agent to create new problems
    3. Uses the Validator Agent to check problem quality
    4. Stores validated problems in the Problem Bank
    """

    def __init__(self, model_name: str = "gemini-3-pro-preview"):
        self.model_name = model_name
        self.problem_bank = ProblemBank()

    def process_seed_problem(
        self,
        seed_problem: Dict[str, str],
        num_variations: int = 3
    ) -> Dict[str, Any]:
        """
        Process a single seed problem to generate and validate variations.

        Args:
            seed_problem: Dictionary with 'problem', 'solution', 'difficulty', 'topic'
            num_variations: Number of variations to generate

        Returns:
            Dictionary with processing results
        """
        results = {
            "seed_problem_id": seed_problem.get("id", str(uuid.uuid4())),
            "generated": 0,
            "validated": 0,
            "rejected": 0,
            "problems": []
        }

        print(f"\n{'='*60}")
        print(f"Processing seed problem: {seed_problem.get('topic', 'Unknown')}")
        print(f"{'='*60}\n")

        for i in range(num_variations):
            print(f"\n--- Generating variation {i+1}/{num_variations} ---")

            try:
                # Format the seed problem
                seed_text = self._format_seed_problem(seed_problem)

                # Step 1: Generate new problem
                print("🤖 Generator Agent: Creating new problem...")
                generated_text = generate_problem_from_example(seed_text, self.model_name)
                results["generated"] += 1

                # Parse generated problem
                parsed = self._parse_generated_problem(generated_text)

                if not parsed:
                    print("❌ Failed to parse generated problem")
                    results["rejected"] += 1
                    continue

                print(f"✅ Generated problem on topic: {parsed['topic']}")

                # Step 2: Validate the problem
                print("🔍 Validator Agent: Validating problem...")
                validation_result = validate_problem(
                    parsed["problem"],
                    parsed["solution"],
                    self.model_name
                )

                print(f"📊 Validation Score: {validation_result['score']}/100")
                print(f"   Recommendation: {validation_result['recommendation']}")

                # Step 3: Store if validated
                if validation_result["passed"] and validation_result["recommendation"] == "ACCEPT":
                    problem = MathProblem(
                        id=str(uuid.uuid4()),
                        problem_text=parsed["problem"],
                        solution=parsed["solution"],
                        difficulty=parsed["difficulty"],
                        topic=parsed["topic"],
                        created_at=datetime.now().isoformat(),
                        validated=True,
                        validation_score=validation_result["score"] / 100,
                        source_problem_id=results["seed_problem_id"]
                    )

                    if self.problem_bank.add_problem(problem):
                        print(f"💾 Problem saved to bank with ID: {problem.id}")
                        results["validated"] += 1
                        results["problems"].append({
                            "id": problem.id,
                            "topic": problem.topic,
                            "score": validation_result["score"]
                        })
                    else:
                        print("⚠️  Failed to save problem (may be duplicate)")
                        results["rejected"] += 1
                else:
                    print(f"❌ Problem rejected: {validation_result.get('issues', 'Quality threshold not met')}")
                    results["rejected"] += 1

            except Exception as e:
                print(f"❌ Error processing variation: {e}")
                results["rejected"] += 1

        return results

    def process_multiple_seeds(
        self,
        seed_problems: List[Dict[str, str]],
        variations_per_seed: int = 3
    ) -> Dict[str, Any]:
        """
        Process multiple seed problems.

        Args:
            seed_problems: List of seed problem dictionaries
            variations_per_seed: Number of variations to generate per seed

        Returns:
            Overall processing statistics
        """
        overall_results = {
            "total_seeds": len(seed_problems),
            "total_generated": 0,
            "total_validated": 0,
            "total_rejected": 0,
            "seed_results": []
        }

        for idx, seed in enumerate(seed_problems, 1):
            print(f"\n{'#'*60}")
            print(f"# Seed {idx}/{len(seed_problems)}")
            print(f"{'#'*60}")

            result = self.process_seed_problem(seed, variations_per_seed)

            overall_results["total_generated"] += result["generated"]
            overall_results["total_validated"] += result["validated"]
            overall_results["total_rejected"] += result["rejected"]
            overall_results["seed_results"].append(result)

        return overall_results

    def _format_seed_problem(self, seed: Dict[str, str]) -> str:
        """Format a seed problem for the generator agent"""
        return f"""PROBLEM:
{seed.get('problem', '')}

SOLUTION:
{seed.get('solution', '')}

DIFFICULTY: {seed.get('difficulty', 'medium')}
TOPIC: {seed.get('topic', 'mathematics')}
"""

    def _parse_generated_problem(self, generated_text: str) -> Dict[str, str]:
        """Parse the generated problem text into components"""
        result = {
            "problem": "",
            "solution": "",
            "difficulty": "medium",
            "topic": "mathematics"
        }

        # Extract problem
        problem_match = re.search(r'PROBLEM:\s*(.+?)(?=SOLUTION:|$)', generated_text, re.DOTALL | re.IGNORECASE)
        if problem_match:
            result["problem"] = problem_match.group(1).strip()

        # Extract solution
        solution_match = re.search(r'SOLUTION:\s*(.+?)(?=DIFFICULTY:|TOPIC:|$)', generated_text, re.DOTALL | re.IGNORECASE)
        if solution_match:
            result["solution"] = solution_match.group(1).strip()

        # Extract difficulty
        difficulty_match = re.search(r'DIFFICULTY:\s*(\w+)', generated_text, re.IGNORECASE)
        if difficulty_match:
            result["difficulty"] = difficulty_match.group(1).lower()

        # Extract topic
        topic_match = re.search(r'TOPIC:\s*(.+?)(?=\n|$)', generated_text, re.IGNORECASE)
        if topic_match:
            result["topic"] = topic_match.group(1).strip()

        # Validate that we got the essential parts
        if not result["problem"] or not result["solution"]:
            return None

        return result

    def get_bank_statistics(self) -> Dict[str, Any]:
        """Get current problem bank statistics"""
        return {
            "total_problems": self.problem_bank.get_problem_count(),
            "validated_problems": self.problem_bank.get_validated_count(),
        }
