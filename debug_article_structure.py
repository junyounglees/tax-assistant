#!/usr/bin/env python3
"""Debug article structure to understand the data better."""
import json

# Load the raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get the articles
articles_data = data['법령']['조문']['조문단위']

# Look at the first few articles to understand structure
print("First 10 articles raw structure:")
for i, article in enumerate(articles_data[:10]):
    print(f"\n{i+1}. Article data:")
    print(f"   조문번호: {article.get('조문번호')}")
    print(f"   조문키: {article.get('조문키')}")
    print(f"   조문제목: {article.get('조문제목')}")
    print(f"   조문여부: {article.get('조문여부')}")
    content = article.get('조문내용')
    if isinstance(content, str):
        print(f"   조문내용: {content[:100]}...")
    elif isinstance(content, list):
        print(f"   조문내용 (list): {len(content)} items")
    
    # Check if this might be 제1조의2
    if '정의' in str(article.get('조문제목', '')) or '정의' in str(article.get('조문내용', '')):
        print(f"   *** This might be 제1조의2 (정의) ***")
        print(f"   Full content: {content[:200]}...")