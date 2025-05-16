"""Inspect the API response to understand data types."""
import json
from src.infrastructure.container import Container

def inspect_api_data():
    """Inspect API response types."""
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
    
    print(f"Total delegated articles: {len(delegated_articles)}")
    
    # Inspect the first few items
    for i, article_item in enumerate(delegated_articles[:3]):
        print(f"\n=== Item {i} ===")
        article_info = article_item.get('조정보', {})
        delegated_info = article_item.get('위임정보', {})
        
        print(f"Article info type: {type(article_info)}")
        print(f"Delegated info type: {type(delegated_info)}")
        
        if delegated_info:
            delegated_article_info_list = delegated_info.get('위임법령조문정보', [])
            print(f"위임법령조문정보 type: {type(delegated_article_info_list)}")
            
            if delegated_article_info_list:
                first_item = delegated_article_info_list[0] if isinstance(delegated_article_info_list, list) else delegated_article_info_list
                print(f"First item type: {type(first_item)}")
                print(f"First item: {first_item}")

if __name__ == "__main__":
    inspect_api_data()