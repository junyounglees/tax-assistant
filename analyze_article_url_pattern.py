#!/usr/bin/env python3
"""Analyze URL pattern for specific articles."""

import json
import os
from urllib.parse import urlparse, parse_qs

def analyze_url_pattern():
    """Analyze the URL pattern from law detail link."""
    # Check law search results
    search_file = os.path.join('output', '소득세법_검색결과.json')
    
    with open(search_file, 'r', encoding='utf-8') as f:
        search_results = json.load(f)
    
    if search_results:
        first_law = search_results[0]
        detail_link = first_law.get('detail_link', '')
        
        print(f"Law name: {first_law['name']}")
        print(f"Detail link: {detail_link}")
        
        # Parse the URL to understand parameters
        if detail_link:
            parsed = urlparse(detail_link)
            params = parse_qs(parsed.query)
            
            print("\nURL parameters:")
            for key, value in params.items():
                print(f"  {key}: {value}")
            
            # Try to construct example article URLs
            print("\nExample article URL patterns:")
            # Pattern 1: Add jo parameter
            article_url_1 = f"{detail_link}&jo=1"
            print(f"Pattern 1 (with jo): {article_url_1}")
            
            # Pattern 2: Replace lawService with articleService
            article_url_2 = detail_link.replace('lawService.do', 'articleService.do') + "&jo=1"
            print(f"Pattern 2 (articleService): {article_url_2}")
            
            # Check cache structure for more hints
            cache_file = os.path.join('output', '.cache', 'article-list_267581.json')
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # Check if there's a base URL in the cache
            if '법령' in cache_data:
                law_data = cache_data['법령']
                if '기본정보' in law_data:
                    basic_info = law_data['기본정보']
                    print("\n기본정보 keys:", list(basic_info.keys()))

if __name__ == '__main__':
    analyze_url_pattern()