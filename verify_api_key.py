#!/usr/bin/env python3
"""Quick script to verify your API key is set correctly"""

import os
import sys

def verify_api_key():
    """Check if API key is configured"""

    google_key = os.getenv("GOOGLE_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    print("🔍 Checking API Key Configuration...\n")

    if google_key:
        print("✅ GOOGLE_API_KEY is set")
        print(f"   Key starts with: {google_key[:10]}...")
        print(f"   Key length: {len(google_key)} characters")

        if google_key == "your-api-key-here":
            print("\n⚠️  WARNING: You're still using the placeholder!")
            print("   Please replace 'your-api-key-here' with your actual API key")
            return False

        if not google_key.startswith("AIza"):
            print("\n⚠️  WARNING: Key doesn't start with 'AIza'")
            print("   Google API keys typically start with 'AIzaSy'")
            print("   Please verify you copied the correct key")
            return False

        print("\n✅ API key appears to be configured correctly!")
        return True

    elif gemini_key:
        print("✅ GEMINI_API_KEY is set")
        print(f"   Key starts with: {gemini_key[:10]}...")
        print(f"   Key length: {len(gemini_key)} characters")

        if gemini_key == "your-api-key-here":
            print("\n⚠️  WARNING: You're still using the placeholder!")
            print("   Please replace 'your-api-key-here' with your actual API key")
            return False

        print("\n✅ API key appears to be configured correctly!")
        return True

    else:
        print("❌ No API key found!")
        print("\nPlease set your API key using one of these methods:\n")
        print("Method 1: Create a .env file (recommended)")
        print("  cp .env.example .env")
        print("  # Then edit .env and add your key\n")
        print("Method 2: Export environment variable")
        print("  export GOOGLE_API_KEY='your-actual-key-here'\n")
        print("Get your API key from: https://makersuite.google.com/app/apikey")
        return False

if __name__ == "__main__":
    success = verify_api_key()
    sys.exit(0 if success else 1)
