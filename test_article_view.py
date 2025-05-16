#!/usr/bin/env python3
"""Test script for article viewing functionality."""
from src.infrastructure.container import Container

def test_article_view():
    """Test the article viewing functionality."""
    container = Container()
    controller = container.cli_controller
    
    # Test with 소득세법 (Income Tax Act)
    print("Testing with 소득세법...")
    
    # Get law content
    laws = controller.search_use_case.execute('소득세법', display=5)
    
    if laws:
        law = laws[0]
        print(f"Found law: {law.name} (MST: {law.mst})")
        
        # Get law content with articles
        law_content = controller.view_articles_use_case.get_law_content(law.mst)
        
        if law_content:
            print(f"\nLaw: {law_content.law_name}")
            print(f"Total articles: {len(law_content.articles)}")
            
            # Show first 5 articles
            print("\nFirst 5 articles:")
            for i, article in enumerate(law_content.articles[:5]):
                print(f"\n{i+1}. {article.formatted_number}")
                print(f"   Title: {article.article_title or 'No title'}")
                print(f"   Content: {article.article_content[:100]}...")
        else:
            print("Failed to get law content")
    else:
        print("Law not found")


if __name__ == "__main__":
    test_article_view()