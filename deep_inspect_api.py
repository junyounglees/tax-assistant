"""Deep inspect the API response variations."""
import json
from src.infrastructure.container import Container

def deep_inspect_api():
    """Deep inspect API response variations."""
    container = Container()
    
    mst = "267581"  # 소득세법
    result = container.api_client.get_delegated_laws(mst)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    # Navigate to the structure
    ls_delegated = result.get('lsDelegated', {})
    law_section = ls_delegated.get('법령', {})
    delegated_articles = law_section.get('위임조문정보', [])
    
    # Find variations in the data structure
    variations = {}
    
    for i, article_item in enumerate(delegated_articles):
        article_info = article_item.get('조정보', {})
        delegated_info = article_item.get('위임정보', {})
        
        # Track the types we see
        article_type = type(article_info).__name__
        delegated_type = type(delegated_info).__name__
        
        key = f"{article_type}_{delegated_type}"
        if key not in variations:
            variations[key] = []
        variations[key].append(i)
        
        # Special handling for list types
        if isinstance(delegated_info, list):
            print(f"\nItem {i}: delegated_info is a list with {len(delegated_info)} items")
            for j, sub_item in enumerate(delegated_info):
                print(f"  Sub-item {j} type: {type(sub_item).__name__}")
                if isinstance(sub_item, dict):
                    print(f"  Sub-item {j} keys: {list(sub_item.keys())}")
                    print(f"  Sub-item {j} preview: {str(sub_item)[:200]}...")
        
        # If we see any unusual type combinations, investigate further
        if key != "dict_dict":
            print(f"\nItem {i}: Unusual type combination - {key}")
            print(f"  Article info: {article_info}")
            print(f"  Delegated info: {delegated_info}")
    
    print("\n=== Structure Variations ===")
    for key, indices in variations.items():
        print(f"{key}: {len(indices)} occurrences")
        print(f"  First few indices: {indices[:5]}")

if __name__ == "__main__":
    deep_inspect_api()