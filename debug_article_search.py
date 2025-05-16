#!/usr/bin/env python3
"""Debug article search functionality."""
from src.infrastructure.container import Container
import json

def test_article_search():
    """Test the article search functionality."""
    container = Container()
    controller = container.cli_controller
    
    # Test with 소득세법 (Income Tax Act)
    print("Testing with 소득세법...")
    
    # Get the law first
    laws = controller.search_use_case.execute('소득세법', display=5)
    
    if not laws:
        print("Law not found")
        return
    
    law = laws[0]
    print(f"Found law: {law.name} (MST: {law.mst})")
    
    # Test direct API call
    api_client = container.law_api_client
    
    # Test with article 5
    for article_num in ["5", "14", "1"]:
        print(f"\n--- Testing article {article_num} ---")
        
        # Test the format function
        formatted = controller.view_articles_use_case.repository._format_article_number(article_num)
        print(f"Formatted article number: {article_num} -> {formatted}")
        
        # Test API directly
        print("\nDirect API call:")
        response = api_client.get_full_text(law.mst, jo=formatted)
        print(f"Response: {json.dumps(response, ensure_ascii=False, indent=2)[:500]}...")
        
        # Test through use case
        print("\nThrough use case:")
        article = controller.view_articles_use_case.get_specific_article(law.mst, article_num)
        if article:
            print(f"Found article: {article.formatted_number}")
            print(f"Title: {article.article_title}")
            print(f"Content: {article.article_content[:100]}...")
        else:
            print("Article not found")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    test_article_search()