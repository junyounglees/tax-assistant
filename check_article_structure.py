#!/usr/bin/env python3
"""Check the structure of cached article data."""

import json
import os

def check_article_structure():
    """Check if articles contain detail links."""
    cache_file = os.path.join('output', '.cache', 'article-list_267581.json')
    
    print(f"Checking cache file: {cache_file}")
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Check what keys are available
    print("\nTop-level keys:", list(data.keys()))
    
    # Check different possible structures
    if '법령' in data:
        law_data = data['법령']
        print(f"\n법령 keys: {list(law_data.keys())}")
        
        # Check for articles
        if '조문' in law_data and isinstance(law_data['조문'], list):
            articles = law_data['조문']
            if articles and len(articles) > 0:
                first_article = articles[0]
                print(f"\nFirst article keys: {list(first_article.keys())}")
                print(f"\nFirst article structure:")
                print(json.dumps(first_article, ensure_ascii=False, indent=2))
                
                # Check if any article has detail link
                has_detail_link = any('법령상세링크' in article or '조문상세링크' in article 
                                     for article in articles)
                print(f"\nHas detail link in articles: {has_detail_link}")
                
                # Check for article URL patterns
                if '조문키' in first_article:
                    print(f"Article key: {first_article['조문키']}")
                if '조문단위' in first_article:
                    print(f"Article unit: {first_article['조문단위']}")
        
        # Check law info
        if '기본정보' in law_data:
            law_info = law_data['기본정보']
            print(f"\nLaw info keys: {list(law_info.keys())}")
            if '법령상세링크' in law_info:
                print(f"Law detail link: {law_info['법령상세링크']}")

if __name__ == '__main__':
    check_article_structure()