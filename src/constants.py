"""Constants and configuration for the Math Bank Curator"""

from typing import Final

# Model Configuration
DEFAULT_MODEL: Final[str] = "gemini-3-pro-preview"

# Generation Configuration
GENERATOR_TEMPERATURE: Final[float] = 0.9
GENERATOR_TOP_P: Final[float] = 0.95
GENERATOR_TOP_K: Final[int] = 40
GENERATOR_MAX_TOKENS: Final[int] = 2048

# Validation Configuration
VALIDATOR_TEMPERATURE: Final[float] = 0.3
VALIDATOR_TOP_P: Final[float] = 0.9
VALIDATOR_TOP_K: Final[int] = 20
VALIDATOR_MAX_TOKENS: Final[int] = 2048

# Validation Thresholds
MIN_PASSING_SCORE: Final[int] = 70
MAX_SCORE: Final[int] = 100

# Validation Score Weights
MATHEMATICAL_ACCURACY_WEIGHT: Final[int] = 40
SOLUTION_CORRECTNESS_WEIGHT: Final[int] = 30
CLARITY_COMPLETENESS_WEIGHT: Final[int] = 20
EDUCATIONAL_VALUE_WEIGHT: Final[int] = 10

# Valid Difficulty Levels
VALID_DIFFICULTIES: Final[set] = {"easy", "medium", "hard"}

# Default Values
DEFAULT_DIFFICULTY: Final[str] = "medium"
DEFAULT_TOPIC: Final[str] = "mathematics"
DEFAULT_NUM_VARIATIONS: Final[int] = 3
DEFAULT_NUM_SEEDS: Final[int] = 5

# API Configuration
MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[float] = 2.0  # seconds
TIMEOUT: Final[int] = 60  # seconds

# Storage Configuration
DEFAULT_STORAGE_PATH: Final[str] = "src/problem_bank/problems.json"
DEFAULT_SEED_PATH: Final[str] = "examples/seed_problems.json"

# Regex Patterns
VALIDATION_RESULT_PATTERN: Final[str] = r'VALIDATION RESULT:\s*(PASS|FAIL)'
SCORE_PATTERN: Final[str] = r'SCORE:\s*(\d+)'
MATHEMATICAL_ACCURACY_PATTERN: Final[str] = r'MATHEMATICAL_ACCURACY:\s*(\d+)'
SOLUTION_CORRECTNESS_PATTERN: Final[str] = r'SOLUTION_CORRECTNESS:\s*(\d+)'
CLARITY_COMPLETENESS_PATTERN: Final[str] = r'CLARITY_COMPLETENESS:\s*(\d+)'
EDUCATIONAL_VALUE_PATTERN: Final[str] = r'EDUCATIONAL_VALUE:\s*(\d+)'
FEEDBACK_PATTERN: Final[str] = r'FEEDBACK:\s*(.+?)(?=ISSUES:|$)'
ISSUES_PATTERN: Final[str] = r'ISSUES:\s*(.+?)(?=RECOMMENDATION:|$)'
RECOMMENDATION_PATTERN: Final[str] = r'RECOMMENDATION:\s*(ACCEPT|REVISE|REJECT)'

# Problem Parsing Patterns
PROBLEM_PATTERN: Final[str] = r'PROBLEM:\s*(.+?)(?=SOLUTION:|$)'
SOLUTION_PATTERN: Final[str] = r'SOLUTION:\s*(.+?)(?=DIFFICULTY:|TOPIC:|$)'
DIFFICULTY_PATTERN: Final[str] = r'DIFFICULTY:\s*(\w+)'
TOPIC_PATTERN: Final[str] = r'TOPIC:\s*(.+?)(?=\n|$)'
