"""
Web Documentation Scraper

Scrapes and cleans documentation from a website using httrack and BeautifulSoup.
Usage: python web_docs_scraper.py https://website.com/docs
"""

import subprocess
import os
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Parse command line arguments
parser = argparse.ArgumentParser(description='Scrape and clean documentation from a given URL.')
parser.add_argument('base_url', help='The base URL of the documentation to scrape')
args = parser.parse_args()

# Extract domain from URL for naming
domain = urlparse(args.base_url).netloc
base_name = domain.replace('.', '_')

# Dynamic paths based on domain
output_dir = f"docs_{base_name}"
combined_file = f"{base_name}_combined.html"
cleaned_file = f"{base_name}_cleaned.txt"

# Step 1: Download documentation using httrack
print(f"Downloading documentation from {args.base_url}...")
try:
    subprocess.run([
        "httrack",
        args.base_url,
        "-O", output_dir,
        "--mirror",
        "--robots=0",
        "-v",
        "-WqQ%v"  # Non-interactive mode
    ], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error running httrack: {e}")
    exit(1)

# Step 2: Combine HTML files
print("Combining HTML files...")
html_files = []

for root, dirs, files in os.walk(output_dir):
    for file in files:
        if file.endswith(".html"):
            html_files.append(os.path.join(root, file))

with open(combined_file, "w", encoding="utf-8") as outfile:
    for html_file in html_files:
        with open(html_file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read() + "\n")

# Step 3: Clean content with BeautifulSoup
print("Cleaning content...")

with open(combined_file, "r", encoding="utf-8") as f:
    raw_content = f.read()

soup = BeautifulSoup(raw_content, 'html.parser')
cleaned_content = soup.get_text()

# Save cleaned output
with open(cleaned_file, "w", encoding="utf-8") as f:
    f.write(cleaned_content)

print(f"Process completed! Cleaned output saved to {cleaned_file}") 