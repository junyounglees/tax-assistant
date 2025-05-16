#!/usr/bin/env python3
"""Debug subsections structure."""
import json

# Load raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles_data = data['법령']['조문']['조문단위']

# Find articles with '항' (subsections)
print("Looking for articles with subsections...")
for i, article in enumerate(articles_data[:20]):
    if '항' in article:
        print(f"\nArticle at index {i}:")
        print(f"조문번호: {article.get('조문번호')}")
        print(f"조문제목: {article.get('조문제목')}")
        print(f"조문내용: {repr(article.get('조문내용', '')[:50])}")
        
        subsections = article['항']
        print(f"항 structure: {type(subsections)}")
        
        if isinstance(subsections, list):
            print(f"Number of subsections: {len(subsections)}")
            if subsections:
                first_sub = subsections[0]
                print(f"First subsection type: {type(first_sub)}")
                if isinstance(first_sub, dict):
                    print(f"Keys: {first_sub.keys()}")
                    if '항내용' in first_sub:
                        print(f"First subsection content: {repr(first_sub['항내용'][:100])}")
        
        if i >= 5:  # Just check first few
            break