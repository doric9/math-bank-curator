# Seed Prep Agent Guide

The **Seed Prep Agent** automatically converts natural language math problems into properly formatted JSON seed files, making it easy to create problem seeds without manually writing JSON.

## Features

- 🤖 **AI-Powered Parsing** - Uses Gemini 3 Pro to understand natural language
- 📝 **Flexible Input** - Accepts text files or direct text input
- 🔄 **Auto-Formatting** - Generates proper JSON structure automatically
- ✅ **Validation** - Validates difficulty levels and required fields
- 🧠 **Smart Inference** - Automatically infers difficulty and topic if not specified
- 📦 **Batch Processing** - Handles multiple problems at once

## Quick Start

### Option 1: From Text File

```bash
# Create a file with problems in natural language
python main.py prep --input examples/natural_language_problems.txt
```

### Option 2: Direct Text Input

```bash
python main.py prep --text --input "A circle has a radius of 7cm. What is its area?"
```

### Option 3: Specify Output Location

```bash
python main.py prep \
  --input my_problems.txt \
  --output examples/my_seeds.json
```

## Input Format

### Minimal Format (AI infers everything)

```
What is 25% of 80?

A rectangle is 10m long and 5m wide. Find its perimeter.

Solve for x: 5x - 3 = 17
```

### With Solutions

```
A store sells apples for $2 each. How much do 5 apples cost?

Solution: Multiply the price per apple by the number of apples.
Cost = $2 × 5 = $10
```

### Complete Format (Specify Everything)

```
Problem: A circular garden has a diameter of 14 meters. Calculate its area.

Solution:
Step 1: Find the radius
Radius = diameter ÷ 2 = 14 ÷ 2 = 7 meters

Step 2: Use the area formula
Area = πr² = 3.14 × 7² = 3.14 × 49 = 153.86 m²

Difficulty: medium
Topic: geometry
```

## Separating Multiple Problems

You can separate problems using:
- **Blank lines** (recommended)
- **Numbered lists** (1., 2., 3., etc.)
- **Horizontal lines** (---)

Example:
```
1. What is 15 + 27?

2. A triangle has sides of 3, 4, and 5 cm. Is it a right triangle?

3. Solve: 2x + 7 = 15
```

## Output Format

The agent creates properly formatted JSON:

```json
{
  "problems": [
    {
      "id": "seed-a3f2d1e5",
      "problem": "What is 15 + 27?",
      "solution": "Add the two numbers: 15 + 27 = 42",
      "difficulty": "easy",
      "topic": "arithmetic"
    }
  ]
}
```

## Complete Workflow

### Step 1: Create Natural Language Problems

Create a text file with your problems:

```bash
cat > my_problems.txt << 'EOF'
A car travels at 60 mph for 2.5 hours. How far does it travel?

The price of a book increased from $20 to $25. What is the percentage increase?

Find the volume of a cube with side length 4 cm.
EOF
```

### Step 2: Run Seed Prep

```bash
python main.py prep --input my_problems.txt --output examples/my_seeds.json
```

Output:
```
╔═══════════════════════════════════════════════════════════════╗
║           📚 MATH BANK CURATOR 📚                            ║
║         Agentic Math Problem Generator using ADK              ║
╚═══════════════════════════════════════════════════════════════╝

📖 Loaded problems from: my_problems.txt
🤖 Using model: gemini-3-pro-preview
📤 Output will be saved to: examples/my_seeds.json

============================================================
✅ SEED PREPARATION COMPLETE
============================================================
Problems parsed: 3
Output file: examples/my_seeds.json
============================================================

📊 Parsed Problems Summary:

1. Algebra - Easy
   A car travels at 60 mph for 2.5 hours. How far does it travel?...

2. Algebra - Medium
   The price of a book increased from $20 to $25. What is the percentage increase?...

3. Geometry - Easy
   Find the volume of a cube with side length 4 cm....

💡 Next step: Generate problems from these seeds:
   python main.py generate --seeds examples/my_seeds.json
```

### Step 3: Generate Problems

```bash
python main.py generate --seeds examples/my_seeds.json --variations 3
```

## Advanced Usage

### Custom Model

```bash
python main.py prep \
  --input problems.txt \
  --model gemini-1.5-pro
```

### Chain with Generation

```bash
# Prep seeds and immediately generate
python main.py prep --input problems.txt --output temp_seeds.json
python main.py generate --seeds temp_seeds.json --variations 5
```

### Direct Text for Quick Testing

```bash
python main.py prep --text --input "What is the square root of 144?"
```

## How It Works

### 1. Natural Language Understanding

The agent uses Gemini 3 Pro to:
- Extract the problem statement
- Identify or generate the solution
- Classify difficulty (easy/medium/hard)
- Determine the mathematical topic

### 2. Validation

Checks that:
- All required fields are present
- Problem contains a question
- Solution is not empty
- Difficulty is valid (easy/medium/hard)

### 3. JSON Generation

Creates properly structured JSON with:
- Unique IDs for each problem
- All required fields
- Proper escaping for special characters

## Tips for Best Results

### ✅ DO

- **Be Clear**: Write problems clearly and completely
- **Include Context**: Provide all necessary information
- **Show Solutions**: Include solutions when possible (agent can infer, but explicit is better)
- **Separate Problems**: Use blank lines between problems
- **Use Questions**: End problems with question marks or imperative verbs

### ❌ DON'T

- **Be Vague**: "Solve this" without context
- **Mix Languages**: Keep to one language per file
- **Use Images**: Text only (no diagrams)
- **Skip Information**: Include all given values

## Examples

### Example 1: Minimal Input

**Input:**
```
If 3 apples cost $6, how much do 5 apples cost?
```

**Output:**
```json
{
  "id": "seed-12345678",
  "problem": "If 3 apples cost $6, how much do 5 apples cost?",
  "solution": "First find cost per apple: $6 ÷ 3 = $2 per apple. Then multiply by 5: $2 × 5 = $10. Five apples cost $10.",
  "difficulty": "easy",
  "topic": "arithmetic"
}
```

### Example 2: With Solution

**Input:**
```
Calculate the compound interest on $1000 at 5% annual rate for 2 years.

Solution:
Use the formula A = P(1 + r)^t
where P = $1000, r = 0.05, t = 2

A = 1000(1 + 0.05)^2
A = 1000(1.05)^2
A = 1000 × 1.1025
A = $1102.50

Interest = $1102.50 - $1000 = $102.50
```

**Output:**
```json
{
  "id": "seed-87654321",
  "problem": "Calculate the compound interest on $1000 at 5% annual rate for 2 years.",
  "solution": "Use the formula A = P(1 + r)^t...",
  "difficulty": "medium",
  "topic": "finance"
}
```

## Error Handling

### Missing API Key

```
⚠️  Warning: GOOGLE_API_KEY environment variable not set.
   Please set your Gemini API key to use the seed prep agent.
```

**Solution:** Set your API key
```bash
export GOOGLE_API_KEY='your-key-here'
```

### Invalid JSON

If the agent generates invalid JSON, it will retry automatically (up to 3 times).

### Empty Input

```
❌ Error: Input text cannot be empty
```

**Solution:** Ensure your input file or text is not empty.

## Integration with Main Workflow

```bash
# Complete workflow
python main.py prep --input raw_problems.txt
python main.py generate --seeds examples/prepared_seeds.json
python main.py view --show-solutions
```

## API Reference

### Command Line Arguments

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--input` | Yes | - | Input file path or text |
| `--output` | No | `examples/prepared_seeds.json` | Output JSON file |
| `--text` | No | False | Treat input as text instead of file |
| `--model` | No | `gemini-3-pro-preview` | Model to use |

### Python API

```python
from src.agents.seed_prep_agent import prep_seeds_from_text

# Prepare seeds
text = "What is 5 + 7?"
seed_json = prep_seeds_from_text(
    text=text,
    output_file="my_seeds.json",
    model_name="gemini-3-pro-preview"
)

print(f"Parsed {len(seed_json['problems'])} problems")
```

## Troubleshooting

### Problem: Agent infers wrong difficulty

**Solution:** Explicitly specify in your input:
```
Problem: ...
Difficulty: hard
```

### Problem: Solutions are too brief

**Solution:** Provide detailed solutions in your input, and the agent will learn from them.

### Problem: Topics are generic

**Solution:** Use specific mathematical terms in your problems, or specify the topic:
```
Problem: ...
Topic: trigonometry
```

## Summary

The Seed Prep Agent makes it easy to create problem seeds by:
1. Writing problems in plain English
2. Running one command to parse them
3. Getting properly formatted JSON ready for generation

No more manual JSON formatting! 🎉
