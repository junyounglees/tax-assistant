#!/usr/bin/env python3
"""Cache Value Added Tax Law."""

from src.infrastructure.container import Container
import time

def cache_vat_law():
    """Cache search results and articles for VAT law."""
    container = Container()
    
    search_use_case = container.search_use_case
    articles_use_case = container.view_articles_use_case
    
    print("=== Caching 부가가치세법 ===")
    
    # Try searching with the full name
    search_term = "부가가치세법"
    print(f"\nSearching {search_term}...")
    laws = search_use_case.search_with_abbreviation(search_term)
    
    if laws:
        print(f"Found {len(laws)} results:")
        for law in laws:
            print(f"- {law.name} (MST: {law.mst})")
            
        # Cache articles for each law found
        for law in laws:
            print(f"\nCaching articles for {law.name}...")
            law_content = articles_use_case.get_law_content(law.mst)
            
            if law_content:
                print(f"Cached {len(law_content.articles)} articles")
            else:
                print(f"Failed to cache articles")
            
            time.sleep(1)
    else:
        print(f"No results found for {search_term}")
    
    print("\nCaching complete!")

if __name__ == '__main__':
    cache_vat_law()