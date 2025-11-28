# Smart Scraper Agent - Quick Start

The **Smart Scraper Agent** automatically extracts math problems from websites, PDFs, and documents, converting them into seed JSON format.

## Installation

```bash
# Install scraping dependencies
pip install -r requirements.txt
```

## Quick Examples

### 1. Scrape from URL

```bash
python main.py scrape --url https://example.com/math-problems
```

### 2. Scrape from Local File

```bash
# Text, PDF, or HTML file
python main.py scrape --file my_problems.pdf
```

### 3. Scrape Multiple URLs

```bash
# Create a file with URLs (one per line)
cat > urls.txt << 'EOF'
https://site1.com/problems
https://site2.com/worksheets
https://site3.com/exercises
EOF

python main.py scrape --urls-file urls.txt
```

## Complete Workflow

```bash
# 1. Scrape from web
python main.py scrape --url https://example.com/problems

# 2. Generate variations
python main.py generate --seeds examples/scraped_seeds.json

# 3. View results
python main.py view --show-solutions
```

## How It Works

```
URL/File → [Scraper Agent] → Extract Problems → [Seed Prep Agent] → JSON Seeds → Ready for Generation
```

### Step 1: Scraping
- Fetches content from URL or reads from file
- Cleans HTML, removes navigation/ads
- Extracts text content

### Step 2: Problem Extraction
- AI identifies mathematical problems in text
- Filters out non-problem content
- Extracts complete problem statements

### Step 3: Parsing
- Converts to structured format
- Infers difficulty and topic
- Generates solutions if missing

### Step 4: JSON Creation
- Creates properly formatted seed JSON
- Ready to feed to generator

## Supported Sources

- ✅ **Websites** - Any URL with text content
- ✅ **PDF files** - Extracts text from PDFs
- ✅ **HTML files** - Local HTML documents
- ✅ **Text files** - Plain text or markdown

## Command Options

| Option | Description | Example |
|--------|-------------|---------|
| `--url` | Single URL to scrape | `--url https://site.com` |
| `--urls-file` | File with multiple URLs | `--urls-file urls.txt` |
| `--file` | Local file (txt/pdf/html) | `--file problems.pdf` |
| `--output` | Output JSON file | `--output my_seeds.json` |
| `--model` | Model to use | `--model gemini-3-pro-preview` |

## Examples

### Example 1: Educational Website

```bash
python main.py scrape \
  --url https://mathisfun.com/algebra-problems.html \
  --output algebra_seeds.json
```

### Example 2: PDF Worksheet

```bash
python main.py scrape \
  --file math_worksheet.pdf \
  --output worksheet_seeds.json
```

### Example 3: Batch Scraping

```bash
# urls.txt contains:
# https://site1.com/easy-problems
# https://site2.com/medium-problems
# https://site3.com/hard-problems

python main.py scrape --urls-file urls.txt
```

## Tips

- **Be respectful**: Don't overload servers with too many requests
- **Check robots.txt**: Respect website scraping policies
- **Use delays**: For multiple URLs, the scraper has built-in retry logic
- **Verify results**: Always check the output JSON before generating

## Troubleshooting

### "Failed to scrape URL"
- Check if URL is accessible
- Some sites block scrapers
- Try with `--file` if you can download manually

### "No problems found"
- Content may not contain math problems
- Try different URLs or sources
- Check if site requires JavaScript (scraper only gets static HTML)

### PDF not working
- Ensure PyPDF2 is installed: `pip install PyPDF2`
- Some PDFs with images won't extract text
- Try converting to text first

## Integration

The scraper integrates seamlessly with the full pipeline:

```bash
# Complete autonomous workflow
python main.py scrape --url https://problems.com
python main.py generate --seeds examples/scraped_seeds.json --variations 5
python main.py view
```

Now you can scrape problems from anywhere on the web! 🌐
