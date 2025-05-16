#!/usr/bin/env python3
"""Test the article fixes."""
from src.infrastructure.container import Container

def test_article_fixes():
    """Test the fixed article handling."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print("Testing article fixes...\n")
    
    # Show first few articles with proper numbers
    print("1. First 5 articles with proper formatting:")
    for i, article in enumerate(law_content.articles[:5]):
        print(f"{i+1}. {article.formatted_number} - {article.article_title} - {article.article_content[:30]}...")
    
    # Test article search excluding chapter headers
    print("\n2. Search for article 1 (excluding chapter headers):")
    article_num = '1'
    matching_articles = [
        a for a in law_content.articles 
        if a.article_number == article_num 
        and a.article_title != "Chapter/Section Header"
    ]
    
    print(f"Found {len(matching_articles)} actual articles with number {article_num}:")
    for article in matching_articles:
        print(f"  - {article.formatted_number} {article.article_title}")
    
    # Test 제1조의2 display
    print("\n3. Looking for 제1조의2 (정의):")
    for article in law_content.articles[:10]:
        if '정의' in str(article.article_title) and article.article_number == '1':
            print(f"Found: {article.formatted_number} - {article.article_title}")
            controller.presenter.display_article_content(article)
            break


if __name__ == "__main__":
    test_article_fixes()