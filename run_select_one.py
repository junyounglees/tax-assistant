#!/usr/bin/env python3
"""Direct test for cache file name display."""

import os
from src.infrastructure.container import Container

def run_manual_test():
    """Manually run the view_law_articles to test cache display."""
    container = Container()
    controller = container.cli_controller
    
    # 소득세법 MST
    mst = "267581"
    law_name = "소득세법"
    
    print("=== Manual Test: Cache File Name Display ===")
    print(f"Testing with: {law_name} (MST: {mst})")
    print()
    
    # Check if cache exists
    cache_file = os.path.join('output', '.cache', f'article-list_{mst}.json')
    old_cache_file = os.path.join('output', '.cache', f'law_content_{mst}.json')
    
    if os.path.exists(cache_file):
        print(f"Cache exists: {cache_file}")
    elif os.path.exists(old_cache_file):
        print(f"Cache exists: {old_cache_file}")
    else:
        print("No cache file found")
    
    print("\nCalling view_law_articles...")
    print()
    
    # This will display the cache file name
    try:
        from unittest.mock import patch
        # Simulate user selecting exit immediately
        with patch('builtins.input', return_value='0'):
            controller.view_law_articles(mst, law_name)
    except SystemExit:
        pass

if __name__ == '__main__':
    run_manual_test()