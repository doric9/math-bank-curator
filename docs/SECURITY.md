# Security Guide

This document outlines security best practices for the Math Bank Curator project.

## API Key Security ✅

### Current Protection

Your API key is protected by the following measures:

1. **Environment Variables Only**
   - The code NEVER hardcodes API keys
   - Keys are read from `GOOGLE_API_KEY` or `GEMINI_API_KEY` environment variables
   - See `main.py:84` for implementation

2. **Git Ignore Configuration**
   - `.env` and `.env.local` are excluded from git (see `.gitignore:30-31`)
   - Virtual environments are excluded
   - Generated problem bank data is excluded

3. **Safe Template Provided**
   - `.env.example` contains only placeholder text
   - Safe to commit to public repositories

## Best Practices

### ✅ DO

1. **Use Environment Variables**
   ```bash
   # Option 1: Export directly
   export GOOGLE_API_KEY='your-actual-key'

   # Option 2: Create .env file (automatically ignored by git)
   echo "GOOGLE_API_KEY=your-actual-key" > .env
   ```

2. **Use .env files for local development**
   ```bash
   # Copy the template
   cp .env.example .env

   # Edit .env with your actual key
   nano .env  # or use your preferred editor
   ```

3. **Verify before committing**
   ```bash
   # Check what will be committed
   git status

   # Verify .env is ignored
   git status --ignored | grep ".env"
   ```

4. **Use different keys for different environments**
   - Development: Personal API key
   - Production: Service account or restricted key
   - Testing: Separate API key with quotas

### ❌ DON'T

1. **Never hardcode API keys in source code**
   ```python
   # ❌ NEVER DO THIS
   api_key = "AIzaSyC-abc123..."  # WRONG!

   # ✅ ALWAYS DO THIS
   api_key = os.getenv("GOOGLE_API_KEY")  # CORRECT!
   ```

2. **Never commit .env files**
   - The `.gitignore` already prevents this
   - But always double-check before pushing

3. **Never share API keys in issues or pull requests**
   - If you accidentally expose a key, regenerate it immediately
   - Go to: https://makersuite.google.com/app/apikey

4. **Never include API keys in screenshots or logs**
   - Redact sensitive information before sharing

## Verification Checklist

Before pushing to GitHub, verify:

- [ ] `.env` file is NOT tracked by git
- [ ] No hardcoded API keys in source code
- [ ] `.gitignore` includes `.env` and `.env.local`
- [ ] Only `.env.example` with placeholder text is committed

### Quick Verification Commands

```bash
# Check if .env is tracked (should return nothing)
git ls-files | grep "\.env$"

# Search for potential API keys in tracked files
git grep -i "AIza" || echo "No API keys found ✅"

# Verify .gitignore is working
git check-ignore .env && echo ".env is properly ignored ✅"
```

## What If I Accidentally Commit an API Key?

If you accidentally commit an API key:

1. **Immediately regenerate the API key**
   - Go to https://makersuite.google.com/app/apikey
   - Delete the compromised key
   - Create a new one

2. **Remove from git history**
   ```bash
   # If not yet pushed
   git reset HEAD~1
   git commit --amend

   # If already pushed (requires force push)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch .env" \
     --prune-empty --tag-name-filter cat -- --all
   git push --force
   ```

3. **Consider using git-secrets**
   ```bash
   # Install git-secrets to prevent future accidents
   git secrets --install
   git secrets --register-aws
   ```

## Additional Security Measures

### 1. API Key Restrictions (Recommended)

Configure your Gemini API key with restrictions:

- **Application restrictions**: Limit to specific IP addresses
- **API restrictions**: Limit to Gemini API only
- **Quota limits**: Set daily/monthly limits

### 2. Use GitHub Secrets for CI/CD

If you set up GitHub Actions:

```yaml
# .github/workflows/test.yml
env:
  GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
```

Add the key via: Repository Settings → Secrets and variables → Actions

### 3. Rotate Keys Regularly

- Change your API key every 90 days
- Use different keys for different projects
- Audit key usage in Google Cloud Console

## Security Scan Results

✅ **Status: SECURE**

- No API keys found in committed files
- `.env` properly excluded from git
- Environment variable usage implemented correctly
- `.env.example` safe for public repository

## Questions?

If you're unsure about API key security:
- Review this guide
- Check the `.gitignore` file
- Run the verification commands above
- When in doubt, regenerate your API key

**Remember: An exposed API key can be used by anyone and may incur unexpected costs!**
