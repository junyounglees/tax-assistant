#!/usr/bin/env python3
"""Final test of all the fixes."""
from src.infrastructure.container import Container

def simulate_user_flow():
    """Simulate the user flow with the fixed functionality."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print("Simulating user interactions...\n")
    
    # Option 1: Show articles with improved display
    print("1. Viewing article list (improved display):")
    controller.presenter.display_article_list(law_content.articles[:10])
    
    # Option 2: Search for article 5 (previously failing)
    print("\n\n2. Searching for article 5:")
    article_num = '5'
    matching_articles = [a for a in law_content.articles if a.article_number == article_num]
    
    if matching_articles:
        print(f"✓ Found {len(matching_articles)} article(s) with number {article_num}")
        controller.presenter.display_article_content(matching_articles[0])
    else:
        print(f"✗ No article found with number {article_num}")
    
    # Option 2: Search for article with duplicates
    print("\n\n3. Searching for article 1 (multiple matches):")
    article_num = '1'
    matching_articles = [a for a in law_content.articles if a.article_number == article_num]
    
    if len(matching_articles) > 1:
        print(f"✓ Found {len(matching_articles)} articles with number {article_num}:")
        controller.presenter.display_article_list(matching_articles)
    
    # Option 3: Keyword search with save
    print("\n\n4. Keyword search for '세율':")
    keyword = '세율'
    results = controller.view_articles_use_case.search_articles(law_content, keyword)
    
    if results:
        print(f"✓ Found {len(results)} articles containing '{keyword}'")
        controller.presenter.display_article_list(results[:5])
        
        # Save results
        success = controller.view_articles_use_case.save_article_search_results(
            results, law_content.law_name, keyword
        )
        if success:
            print(f"\n✓ Search results saved to output folder")


if __name__ == "__main__":
    simulate_user_flow()