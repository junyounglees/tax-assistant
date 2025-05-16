#!/usr/bin/env python3
"""Test the improved article search and display functionality."""
from src.infrastructure.container import Container

def test_duplicate_articles():
    """Test handling of duplicate article numbers."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print("Testing article display improvements...")
    
    # Show first 20 articles with improved titles
    controller.presenter.display_article_list(law_content.articles)
    
    # Test searching for duplicate article numbers
    print("\n\nTesting search for duplicate articles...")
    article_num = '1'  # Article 1 has multiple entries
    matching_articles = [a for a in law_content.articles if a.article_number == article_num]
    
    print(f"\nFound {len(matching_articles)} articles with number {article_num}:")
    for i, article in enumerate(matching_articles, 1):
        print(f"{i}. {article.formatted_number} - {article.article_title} - {article.article_content[:50]}...")
    
    # Test searching for article 5
    print("\n\nTesting search for article 5...")
    article_num = '5'
    matching_articles = [a for a in law_content.articles if a.article_number == article_num]
    
    if matching_articles:
        print(f"Found article {article_num}:")
        article = matching_articles[0]
        print(f"Title: {article.article_title}")
        print(f"Content: {article.article_content[:100]}...")
    else:
        print(f"No article found with number {article_num}")
    
    # Check actual article numbers in the data
    print("\n\nActual article numbers in the first 30 articles:")
    for i, article in enumerate(law_content.articles[:30]):
        print(f"{i+1}. Article number: '{article.article_number}' - {article.formatted_number}")


if __name__ == "__main__":
    test_duplicate_articles()