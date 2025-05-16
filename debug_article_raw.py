#!/usr/bin/env python3
"""Debug raw article structure."""
import json

# Load the raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get the articles array
articles_data = data['법령']['조문']['조문단위']

# Show structure of first few articles
for i, article in enumerate(articles_data[:5]):
    print(f"\nArticle {i+1}:")
    print(f"  Number: {article.get('조문번호')}")
    print(f"  Title: {article.get('조문제목')}")
    content = article.get('조문내용')
    print(f"  Content type: {type(content)}")
    if isinstance(content, list):
        print(f"  Content is a list with {len(content)} items")
        if content and isinstance(content[0], list):
            print(f"  First item is a list with {len(content[0])} parts")
    else:
        print(f"  Content value: {repr(content[:100])}")