# Quick Start Guide

Get started with Math Bank Curator in 5 minutes!

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

## Step 2: Set API Key

Get your Gemini API key from https://makersuite.google.com/app/apikey

```bash
export GOOGLE_API_KEY='your-api-key-here'
```

## Step 3: Generate Problems

```bash
# Generate 9 problems (3 variations from 3 seeds)
python main.py generate --num-seeds 3 --variations 3 --show-samples
```

## Step 4: View Results

```bash
# View problems in the bank
python main.py view --limit 5 --show-solutions

# Check statistics
python main.py stats
```

## What Just Happened?

1. The **Generator Agent** created new math problems based on examples
2. The **Validator Agent** checked each problem for accuracy and quality
3. Problems scoring 70+ were saved to the problem bank
4. You now have a curated collection of validated problems!

## Next Steps

- Add your own seed problems to `examples/seed_problems.json`
- Increase `--variations` for more problems per seed
- Try different topics: algebra, geometry, probability, calculus
- Integrate the problem bank into your educational platform

## Troubleshooting

**No API key?**
```bash
export GOOGLE_API_KEY='your-key'
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**Want to reset the problem bank?**
```bash
rm src/problem_bank/problems.json
```

Happy problem generating! 🎓
