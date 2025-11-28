# Math Bank Curator

An agentic workflow for autonomously creating novel mathematical problems using Google's Agent Development Kit (ADK).

## Overview

Math Bank Curator establishes a multi-agent system that generates, validates, and curates high-quality mathematical problems. The system uses three specialized agents working together:

1. **Generation Agent**: Creates new problems from example problems
2. **Validation Agent**: Rigorously tests problems for accuracy and quality
3. **Orchestrator Agent**: Coordinates the workflow between agents

Only problems that pass rigorous validation are automatically stored in the problem bank.

## Architecture

```
┌─────────────────┐
│  Seed Problems  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Generator     │ ← Creates novel variations
│     Agent       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validator     │ ← Validates accuracy & quality
│     Agent       │
└────────┬────────┘
         │
         ▼ (if score >= 70)
┌─────────────────┐
│  Problem Bank   │ ← Curated repository
└─────────────────┘
```

## Features

- **Autonomous Generation**: AI agents create mathematical problems without human intervention
- **Natural Language Input**: Seed Prep Agent converts plain text problems to JSON automatically
- **Rigorous Validation**: Multi-criteria validation including mathematical accuracy, solution correctness, clarity, and educational value
- **Quality Threshold**: Only problems scoring 70+ out of 100 are accepted
- **Multi-Topic Support**: Handles algebra, geometry, probability, calculus, and more
- **Scalable Architecture**: Built on Google's ADK for production-ready agent systems
- **Problem Bank Storage**: JSON-based storage for validated problems

## Installation

### Prerequisites

- Python 3.10 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/math-bank-curator.git
cd math-bank-curator
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
```bash
export GOOGLE_API_KEY='your-api-key-here'
# Or create a .env file with: GOOGLE_API_KEY=your-api-key-here
```

## Usage

### Prepare Seeds from Natural Language (New!)

Convert natural language problems to JSON format:

```bash
# From a text file
python main.py prep --input examples/natural_language_problems.txt

# Or direct text
python main.py prep --text --input "What is 25% of 80?"
```

See [SEED_PREP_GUIDE.md](SEED_PREP_GUIDE.md) for complete documentation.

### Generate New Problems

Generate math problems from seed examples:

```bash
python main.py generate --variations 3 --num-seeds 5
```

Options:
- `--variations N`: Number of variations to generate per seed (default: 3)
- `--num-seeds N`: Number of seed problems to process (default: 5)
- `--model MODEL`: Gemini model to use (default: gemini-3-pro-preview)
- `--seeds FILE`: Path to seed problems JSON (default: examples/seed_problems.json)
- `--show-samples`: Display sample generated problems at the end

### View Problems in the Bank

View stored problems:

```bash
python main.py view --limit 10
```

Options:
- `--limit N`: Maximum number of problems to display (default: 10)
- `--topic TOPIC`: Filter by topic (algebra, geometry, etc.)
- `--show-solutions`: Display solutions along with problems

### View Statistics

```bash
python main.py stats
```

## How It Works

### 1. Generation Phase

The **Generator Agent** receives a seed problem and creates variations by:
- Maintaining the same mathematical concepts
- Changing numbers, contexts, and scenarios
- Ensuring solvability and rigor
- Providing complete step-by-step solutions

### 2. Validation Phase

The **Validator Agent** evaluates each generated problem across four dimensions:

- **Mathematical Accuracy** (40 points): Logical soundness, no contradictions
- **Solution Correctness** (30 points): Valid steps, correct final answer
- **Clarity & Completeness** (20 points): Clear problem statement, all necessary information
- **Educational Value** (10 points): Engaging, promotes mathematical thinking

**Passing Criteria**: Score ≥ 70 and no critical mathematical errors

### 3. Storage Phase

Validated problems are stored with metadata:
- Unique ID
- Problem text and solution
- Difficulty level and topic
- Validation score
- Creation timestamp
- Source problem reference

## Project Structure

```
math-bank-curator/
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── examples/
│   └── seed_problems.json      # Example seed problems
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── generator_agent.py  # Problem generation agent
│   │   ├── validator_agent.py  # Problem validation agent
│   │   └── orchestrator_agent.py # Workflow coordinator
│   ├── tools/
│   │   └── __init__.py         # Agent tools
│   └── problem_bank/
│       ├── __init__.py         # Problem storage models
│       └── problems.json       # Generated problems database
```

## Seed Problem Format

Seed problems should follow this JSON structure:

```json
{
  "problems": [
    {
      "id": "seed-001",
      "problem": "A rectangle has a length of 12 meters and a width of 8 meters. What is the perimeter?",
      "solution": "Perimeter = 2 × (length + width)\nPerimeter = 2 × (12 + 8) = 2 × 20 = 40 meters",
      "difficulty": "easy",
      "topic": "geometry"
    }
  ]
}
```

## About Google's Agent Development Kit (ADK)

This project is built using [Google's ADK](https://google.github.io/adk-docs/), a flexible and modular framework for developing and deploying AI agents. ADK features:

- **Model-agnostic**: Works with any LLM, optimized for Gemini
- **Multi-agent systems**: Compose agents into hierarchies
- **Production-ready**: Same framework powering Google's production agents
- **Code-first**: Flexible Python API for agent development

## Example Output

```
╔═══════════════════════════════════════════════════════════════╗
║           📚 MATH BANK CURATOR 📚                            ║
║         Agentic Math Problem Generator using ADK              ║
╚═══════════════════════════════════════════════════════════════╝

📖 Loading seed problems from: examples/seed_problems.json
✅ Loaded 5 seed problems

🚀 Initializing orchestrator with model: gemini-3-pro-preview

--- Generating variation 1/3 ---
🤖 Generator Agent: Creating new problem...
✅ Generated problem on topic: geometry
🔍 Validator Agent: Validating problem...
📊 Validation Score: 85/100
   Recommendation: ACCEPT
💾 Problem saved to bank with ID: a3f2d1e5-...

================================================
📈 PROCESSING RESULTS
================================================
Seeds Processed: 5
Problems Generated: 15
Problems Validated: 12
Problems Rejected: 3
Success Rate: 80.0%
================================================
```

## Configuration

### Environment Variables

- `GOOGLE_API_KEY` or `GEMINI_API_KEY`: Your Gemini API key (required)

### Model Selection

The system defaults to `gemini-3-pro-preview` (Google's most advanced model as of November 2025), but you can specify other Gemini models:

```bash
python main.py generate --model gemini-1.5-pro
```

#### Why Gemini 3 Pro?

**Gemini 3 Pro** is Google's latest and most intelligent AI model (released November 2025), offering significant advantages for this application:

- **State-of-the-art reasoning**: PhD-level reasoning with 37.5% on Humanity's Last Exam
- **Exceptional mathematical accuracy**: Top scores on GPQA Diamond (91.9%)
- **Superior multimodal understanding**: 81% on MMMU-Pro benchmark
- **Best-in-class performance**: #1 on LMArena leaderboard (1501 Elo)
- **Advanced agentic capabilities**: Optimized for autonomous agent workflows
- **Dynamic thinking**: Adjusts reasoning depth based on problem complexity

This makes Gemini 3 Pro ideal for both creative problem generation and rigorous validation tasks.

## Troubleshooting

### API Key Issues

```
Error: GOOGLE_API_KEY environment variable not set
```

Solution: Set your API key:
```bash
export GOOGLE_API_KEY='your-key-here'
```

### Rate Limiting

If you encounter rate limits, reduce the number of variations or add delays between generations.

### Low Validation Success Rate

If many problems are rejected:
- Check seed problem quality
- Ensure seed problems have complete solutions
- Try adjusting the validation threshold in `validator_agent.py`

## References

- **Kaggle Competition**: [Agents Intensive Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project)
- **Google ADK Documentation**: https://google.github.io/adk-docs/
- **ADK Python Repository**: https://github.com/google/adk-python
- **ADK Samples**: https://github.com/google/adk-samples

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

Built with Google's Agent Development Kit (ADK) and powered by Gemini models.
