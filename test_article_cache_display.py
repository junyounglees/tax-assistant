#!/usr/bin/env python3
"""Test cache file name display for individual articles."""

import os
from unittest.mock import patch
from src.infrastructure.container import Container

def test_article_cache_display():
    """Test cache file name display when viewing specific articles."""
    container = Container()
    controller = container.cli_controller
    
    # 소득세법 MST
    mst = "267581"
    law_name = "소득세법"
    
    print("=== Test: Article Cache File Name Display ===")
    print(f"Testing with: {law_name} (MST: {mst})")
    print()
    
    # Check if cache exists
    cache_file = os.path.join('output', '.cache', f'article-list_{mst}.json')
    if os.path.exists(cache_file):
        print(f"Cache exists: {cache_file}")
    else:
        print("No cache file found - will fetch from API")
    
    print("\nTesting article view...")
    print()
    
    try:
        # Simulate user flow: go to law articles, select article 1, then exit
        user_inputs = ['2', '1', '1', '0', '0']  # 2=specific article, 1=article number, 1=select first match, 0=back, 0=exit
        
        with patch('builtins.input', side_effect=user_inputs):
            controller.view_law_articles(mst, law_name)
    except (SystemExit, StopIteration):
        pass

if __name__ == '__main__':
    test_article_cache_display()