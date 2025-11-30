
import sys
import os
sys.path.insert(0, os.getcwd())
from src.agents.scraper_agent import read_file_content

try:
    content = read_file_content("amc8_2025.pdf")
    text = content["text"]
    print(f"Text length: {len(text)}")
    print("-" * 20)
    print("First 500 chars:")
    print(text[:500])
    print("-" * 20)
    print("Last 500 chars:")
    print(text[-500:])
except Exception as e:
    print(f"Error: {e}")
