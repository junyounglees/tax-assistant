#!/usr/bin/env python3
"""Check article detail structure."""

import json
import os

def check_article_detail():
    """Check detailed structure of articles."""
    cache_file = os.path.join('output', '.cache', 'article-list_267581.json')
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Navigate to articles
    articles = data.get('법령', {}).get('조문', {})
    
    # Check structure
    if isinstance(articles, dict):
        print("조문 is a dictionary")
        
        # Check if there is '조문단위' key which contains the actual articles
        if '조문단위' in articles:
            article_units = articles['조문단위']
            print(f"조문단위 type: {type(article_units)}")
            
            if isinstance(article_units, list) and article_units:
                first_article = article_units[0]
                print(f"\nFirst article keys: {list(first_article.keys())}")
                
                # Check various link fields
                link_fields = ['법령상세링크', '조문상세링크', '조문링크', '링크', 'link', 'URL', '법령링크']
                found_links = {field: first_article.get(field) for field in link_fields if field in first_article}
                
                if found_links:
                    print(f"\nFound link fields: {found_links}")
                else:
                    print("\nNo standard link fields found")
                
                # Print whole structure of the first article
                print(f"\nFirst article structure:")
                print(json.dumps(first_article, ensure_ascii=False, indent=2))
                
                # Check if there's a pattern in article number vs URL
                if '조문번호' in first_article:
                    print(f"\nArticle number: {first_article['조문번호']}")
        else:
            article_keys = list(articles.keys())[:5]  # First 5 keys
            print(f"First 5 article keys: {article_keys}")
    else:
        print(f"조문 is of type: {type(articles)}")

if __name__ == '__main__':
    check_article_detail()