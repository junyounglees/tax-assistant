#!/usr/bin/env python3
"""Find articles with list content."""
import json

# Load the raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get the articles array
articles_data = data['법령']['조문']['조문단위']

# Find articles with list content
list_articles = []
for i, article in enumerate(articles_data):
    content = article.get('조문내용')
    if isinstance(content, list):
        list_articles.append((i, article))

print(f"Found {len(list_articles)} articles with list content out of {len(articles_data)} total")

# Show first few
for idx, article in list_articles[:3]:
    print(f"\nArticle at index {idx}:")
    print(f"  Number: {article.get('조문번호')}")
    print(f"  Title: {article.get('조문제목')}")
    content = article.get('조문내용')
    print(f"  Content structure: {type(content)}")
    if isinstance(content, list) and content:
        print(f"  Content has {len(content)} items")
        if isinstance(content[0], list):
            print(f"  First item has {len(content[0])} parts")
            print(f"  First part: {repr(content[0][0][:100])}")