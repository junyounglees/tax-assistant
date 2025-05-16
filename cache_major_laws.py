#!/usr/bin/env python3
"""Cache major laws for quick access."""

from src.infrastructure.container import Container
import time

def cache_major_laws():
    """Cache search results and articles for major laws."""
    container = Container()
    
    # Laws to cache - including common abbreviations
    major_laws = [
        ("소득세법", "소득세법"),  # Income Tax Law
        ("법인세법", "법인세법"),  # Corporate Tax Law
        ("부가가치세법", "부가가치세법"),  # Value Added Tax Law
    ]
    
    # Initialize search use case and articles use case
    search_use_case = container.search_use_case
    articles_use_case = container.view_articles_use_case
    
    print("=== Caching Major Laws ===")
    print("This process will cache search results and articles for major tax laws.")
    print()
    
    for law_name, search_term in major_laws:
        print(f"\n{'='*50}")
        print(f"Caching {law_name}...")
        
        # 1. Cache search results
        print(f"\n1) Searching {search_term}...")
        laws = search_use_case.search_with_abbreviation(search_term)
        
        if laws:
            print(f"   Found {len(laws)} results:")
            for law in laws:
                print(f"   - {law.name} (MST: {law.mst})")
            
            # 2. Cache articles for each law found
            for law in laws:
                print(f"\n2) Caching articles for {law.name}...")
                law_content = articles_use_case.get_law_content(law.mst)
                
                if law_content:
                    print(f"   Cached {len(law_content.articles)} articles")
                else:
                    print(f"   Failed to cache articles")
                
                # Small delay to avoid overwhelming the API
                time.sleep(1)
        else:
            print(f"   No results found for {search_term}")
        
        # Small delay between major laws
        time.sleep(1)
    
    print(f"\n{'='*50}")
    print("Caching complete!")
    print("\nCached data is stored in output/.cache/ directory")
    print("Cache files will be valid for 7 days")
    
    # Show summary of cached files
    import os
    cache_dir = os.path.join('output', '.cache')
    if os.path.exists(cache_dir):
        files = os.listdir(cache_dir)
        print(f"\nTotal cache files created: {len(files)}")
        print("\nCache files:")
        for file in sorted(files):
            print(f"  - {file}")

if __name__ == '__main__':
    cache_major_laws()