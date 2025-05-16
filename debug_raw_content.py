#!/usr/bin/env python3
"""Debug raw article content."""
import json

# Load raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles_data = data['법령']['조문']['조문단위']

# Find 제1조의2
print("Looking for 제1조의2 (정의)...")
for i, article in enumerate(articles_data):
    if article.get('조문제목') == '정의' and article.get('조문번호') == '1':
        print(f"\nFound at index {i}:")
        print(f"조문번호: {article.get('조문번호')}")
        print(f"조문제목: {article.get('조문제목')}")
        print(f"조문키: {article.get('조문키')}")
        
        # Check content structure
        content = article.get('조문내용')
        print(f"Content type: {type(content)}")
        
        if isinstance(content, str):
            print(f"Content length: {len(content)}")
            print(f"Content: {repr(content)}")
        elif isinstance(content, list):
            print(f"Content is a list with {len(content)} items")
            for j, item in enumerate(content):
                print(f"  Item {j}: type={type(item)}, value={repr(item)[:100]}...")
        
        # Also check for 항 (subsections)
        if '항' in article:
            print(f"\n항 (subsections) found: {type(article['항'])}")
        
        break