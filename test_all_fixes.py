#!/usr/bin/env python3
"""Test all fixes together."""
from src.infrastructure.container import Container

def test_all_fixes():
    """Test all the fixes together."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print("Testing all fixes...\n")
    
    # 1. Show article list with corrected display
    print("1. Article list display:")
    controller.presenter.display_article_list(law_content.articles[:20])
    
    # 2. Check 제1조의2 content
    print("\n\n2. Testing 제1조의2 (정의) content:")
    for article in law_content.articles[:10]:
        if article.article_title == '정의' and article.article_number == '1':
            print(f"Found: {article.formatted_number}")
            controller.presenter.display_article_content(article)
            break
    
    # 3. Test search for article 1 (excluding chapters)
    print("\n\n3. Testing article 1 search (excluding chapters):")
    matching_articles = [
        a for a in law_content.articles 
        if a.article_number == '1' 
        and a.article_title != "Chapter/Section Header"
    ]
    
    print(f"Found {len(matching_articles)} articles with number 1:")
    controller.presenter.display_article_list(matching_articles)


if __name__ == "__main__":
    test_all_fixes()