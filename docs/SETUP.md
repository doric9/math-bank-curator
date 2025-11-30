# Quick Setup Guide

Get started with Math Bank Curator in 3 easy steps!

## Prerequisites

- Python 3.10 or higher
- A Google account (to get API key)

## Step 1: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install packages
pip install -r requirements.txt
```

## Step 2: Get and Set Your API Key

### 2a. Get Your API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click **"Create API Key"** or **"Get API Key"**
4. Copy the key (it starts with `AIza...`)

### 2b. Set Your API Key

**Method 1: .env File (Recommended)** ⭐

```bash
# Copy the template
cp .env.example .env

# Edit the .env file
nano .env  # or use any text editor
```

Change this line in `.env`:
```bash
GOOGLE_API_KEY=your-api-key-here
```

To your actual key:
```bash
GOOGLE_API_KEY=AIzaSyC-your-actual-key-here
```

**Method 2: Export Variable (Temporary)**

```bash
export GOOGLE_API_KEY='AIzaSyC-your-actual-key-here'
```

### 2c. Verify Your Key

```bash
python verify_api_key.py
```

You should see:
```
✅ GOOGLE_API_KEY is set
✅ API key appears to be configured correctly!
```

## Step 3: Generate Problems!

```bash
# Generate 3 problems from 2 seed examples
python main.py generate --num-seeds 2 --variations 3 --show-samples
```

## Next Steps

- **View generated problems**: `python main.py view --show-solutions`
- **Check statistics**: `python main.py stats`
- **Read the full guide**: See `README.md`
- **Security info**: See `SECURITY.md`

## Troubleshooting

### "No module named 'google.genai.adk'"

```bash
# Make sure you activated the virtual environment
source .venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "API key not set"

```bash
# Verify your key is set
python verify_api_key.py

# If not, follow Step 2b above
```

### "Permission denied"

```bash
# Make scripts executable
chmod +x main.py verify_api_key.py
```

## Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Generate problems
python main.py generate --variations 3

# View problems in bank
python main.py view --limit 5

# Check bank statistics
python main.py stats

# Verify API key
python verify_api_key.py

# Deactivate virtual environment
deactivate
```

## Project Structure

```
math-bank-curator/
├── main.py                  # Main CLI application
├── verify_api_key.py        # API key verification tool
├── requirements.txt         # Python dependencies
├── .env.example            # API key template
├── .env                    # Your actual API key (create this!)
├── examples/
│   └── seed_problems.json  # Example problems
└── src/
    ├── agents/             # ADK agents
    └── problem_bank/       # Generated problems storage
```

## Help & Documentation

- **Quick Start**: `QUICKSTART.md`
- **Full Documentation**: `README.md`
- **Security Guide**: `SECURITY.md`
- **This Guide**: `SETUP.md`

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your API key with `python verify_api_key.py`
3. Review `SECURITY.md` for API key best practices
4. Check `README.md` for detailed documentation

Happy problem generating! 🎓✨
