# Testing Guide

Complete guide for testing the Math Bank Curator system.

## Prerequisites

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
export GOOGLE_API_KEY='your-api-key-here'

# 3. Verify installation
python verify_api_key.py
```

## Quick Smoke Test

Run this to verify everything works:

```bash
# Test the complete pipeline
python main.py prep --text --input "What is 5 + 7?" --output test_seeds.json
python main.py generate --seeds test_seeds.json --num-seeds 1 --variations 1
python main.py stats
```

## Component Testing

### 1. Test API Key Setup

```bash
python verify_api_key.py
```

**Expected Output:**
```
✅ GOOGLE_API_KEY is set
✅ API key appears to be configured correctly!
```

### 2. Test Seed Prep Agent

**Test with direct text:**
```bash
python main.py prep \
  --text \
  --input "A circle has radius 5cm. What is its area?" \
  --output test_prep.json
```

**Expected Output:**
```
✅ SEED PREPARATION COMPLETE
Problems parsed: 1
```

**Verify output:**
```bash
cat test_prep.json
```

**Test with file:**
```bash
python main.py prep \
  --input examples/natural_language_problems.txt \
  --output test_file_prep.json
```

### 3. Test Generator Agent

```bash
python main.py generate \
  --seeds examples/seed_problems.json \
  --num-seeds 1 \
  --variations 2 \
  --show-samples
```

**Expected Output:**
```
🤖 Generator Agent: Creating new problem...
✅ Generated problem on topic: geometry
🔍 Validator Agent: Validating problem...
📊 Validation Score: 75/100
💾 Problem saved to bank
```

### 4. Test Validator Agent

The validator runs automatically during generation. Check the scores:

```bash
python main.py generate --num-seeds 1 --variations 3
```

Look for validation scores (should be 70+).

### 5. Test Scraper Agent

**Test with local file:**
```bash
# Create test file
cat > test_scrape.txt << 'EOF'
Practice Problems:

1. What is 15 + 27?

2. A square has side length 6cm. Find its area.

3. Solve: 2x - 5 = 11
EOF

python main.py scrape --file test_scrape.txt --output test_scrape.json
```

**Expected Output:**
```
✅ SCRAPING COMPLETE
Problems extracted: 3
```

**Test with URL (if you have internet):**
```bash
# Note: This requires a valid URL with math problems
python main.py scrape --url https://www.mathsisfun.com/numbers/addition.html
```

### 6. Test Problem Bank

```bash
# View stats
python main.py stats

# View problems
python main.py view --limit 5

# View with solutions
python main.py view --limit 3 --show-solutions
```

## Integration Testing

### Test Complete Workflow

**Workflow 1: Natural Language → Generation**

```bash
# Step 1: Create problems in natural language
cat > integration_test.txt << 'EOF'
A train travels at 60 mph for 3 hours. How far does it go?

What is 30% of 150?
EOF

# Step 2: Prep seeds
python main.py prep --input integration_test.txt --output integration_seeds.json

# Step 3: Generate variations
python main.py generate --seeds integration_seeds.json --variations 2

# Step 4: View results
python main.py view --limit 5
```

**Workflow 2: Scrape → Prep → Generate**

```bash
# Step 1: Create document to scrape
cat > doc_to_scrape.txt << 'EOF'
Math Problems for Practice

1. If a book costs $12 and you have $50, how many books can you buy?

2. A rectangle has length 8m and width 3m. What is its perimeter?

3. Calculate 7 × 8 - 15
EOF

# Step 2: Scrape
python main.py scrape --file doc_to_scrape.txt --output scraped_test.json

# Step 3: Generate
python main.py generate --seeds scraped_test.json --variations 2

# Step 4: View
python main.py view --show-solutions
```

## Error Testing

### Test Error Handling

**1. Test without API key:**
```bash
unset GOOGLE_API_KEY
unset GEMINI_API_KEY
python main.py generate
```

**Expected:** Warning about missing API key

**2. Test with invalid input:**
```bash
# Set key back
export GOOGLE_API_KEY='your-key'

# Test empty input
python main.py prep --text --input ""
```

**Expected:** Error message

**3. Test with non-existent file:**
```bash
python main.py prep --input nonexistent.txt
```

**Expected:** File not found error

## Performance Testing

### Test with Multiple Problems

```bash
# Generate many variations
time python main.py generate --num-seeds 3 --variations 5
```

**Expected:** Should complete in a few minutes (depends on API)

### Test Batch Scraping

```bash
# Create multiple URLs
cat > test_urls.txt << 'EOF'
# Add your test URLs here
# https://example1.com
# https://example2.com
EOF

# Note: Requires valid URLs
python main.py scrape --urls-file test_urls.txt
```

## Validation Testing

### Check Problem Quality

```bash
# Generate problems
python main.py generate --num-seeds 2 --variations 3

# View and check quality
python main.py view --show-solutions --limit 10
```

**Manually verify:**
- ✅ Problems are mathematically correct
- ✅ Solutions are accurate
- ✅ Difficulty levels are appropriate
- ✅ Topics are correctly identified

## Manual Test Checklist

### Core Functionality

- [ ] API key verification works
- [ ] Seed prep converts natural language to JSON
- [ ] Generator creates new problems
- [ ] Validator scores problems correctly
- [ ] Problem bank stores problems
- [ ] Scraper extracts from files
- [ ] CLI commands work
- [ ] Help text displays correctly

### Data Quality

- [ ] Generated problems are unique
- [ ] Solutions are mathematically correct
- [ ] Difficulty classification is appropriate
- [ ] Topics are accurate
- [ ] JSON format is valid

### Error Handling

- [ ] Missing API key shows warning
- [ ] Invalid input shows error
- [ ] File not found handled gracefully
- [ ] Network errors retry automatically
- [ ] Empty results handled properly

## Automated Testing (Optional)

Create a simple test script:

```bash
cat > run_tests.sh << 'EOF'
#!/bin/bash

echo "Running Math Bank Curator Tests..."

# Test 1: API Key
echo "Test 1: API Key Verification"
python verify_api_key.py || exit 1

# Test 2: Seed Prep
echo "Test 2: Seed Prep"
python main.py prep --text --input "What is 2 + 2?" --output test1.json || exit 1

# Test 3: Generate
echo "Test 3: Generate"
python main.py generate --seeds test1.json --num-seeds 1 --variations 1 || exit 1

# Test 4: View
echo "Test 4: View"
python main.py view --limit 1 || exit 1

# Test 5: Stats
echo "Test 5: Stats"
python main.py stats || exit 1

echo "✅ All tests passed!"

# Cleanup
rm -f test1.json
EOF

chmod +x run_tests.sh
./run_tests.sh
```

## Common Issues and Solutions

### Issue: "No API key found"

**Solution:**
```bash
export GOOGLE_API_KEY='your-key-here'
python verify_api_key.py
```

### Issue: "Import errors"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "No problems generated"

**Solution:**
- Check validation scores (may be too low)
- Verify seed problems are valid
- Try with different seed problems

### Issue: "Scraper returns no problems"

**Solution:**
- Check if source has math problems
- Verify file format is supported
- Try with example files first

## Test Results Verification

### Expected File Structure

After testing, you should have:

```
math-bank-curator/
├── src/problem_bank/
│   └── problems.json          # Generated problems
├── examples/
│   ├── prepared_seeds.json    # From prep command
│   └── scraped_seeds.json     # From scrape command
└── test files from testing
```

### Check Problem Bank

```bash
# Count problems
python -c "
import json
with open('src/problem_bank/problems.json') as f:
    data = json.load(f)
    print(f'Total problems: {len(data[\"problems\"])}')
"
```

### Validate JSON

```bash
# Check if JSON is valid
python -m json.tool examples/prepared_seeds.json > /dev/null && echo "✅ Valid JSON" || echo "❌ Invalid JSON"
```

## Quick Test Commands

Copy and paste these for quick testing:

```bash
# Quick test 1: End-to-end
python main.py prep --text --input "What is 10 × 5?" && \
python main.py generate --seeds examples/prepared_seeds.json --num-seeds 1 --variations 1 && \
python main.py stats

# Quick test 2: Scraper
echo "What is the area of a square with side 4cm?" > quick_test.txt && \
python main.py scrape --file quick_test.txt && \
cat examples/scraped_seeds.json

# Quick test 3: View results
python main.py view --limit 3 --show-solutions
```

## Success Criteria

Your system is working correctly if:

✅ All commands run without errors
✅ Problems are generated and validated
✅ Validation scores are 70+
✅ JSON files are properly formatted
✅ Problem bank contains problems
✅ Scraped content is extracted correctly

## Next Steps

After testing:

1. **Clean up test files:**
   ```bash
   rm -f test*.json quick_test.txt integration_test.txt
   ```

2. **Use with real data:**
   ```bash
   python main.py scrape --url https://your-favorite-math-site.com
   python main.py generate --seeds examples/scraped_seeds.json
   ```

3. **Monitor quality:**
   ```bash
   python main.py view --show-solutions
   ```

Happy testing! 🧪
