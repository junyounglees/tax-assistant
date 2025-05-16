#!/usr/bin/env python3
"""Test the menu flow for article viewing."""
from src.infrastructure.container import Container
from src.domain.entities.article import LawContent

def test_menu_flow():
    """Test the complete menu flow."""
    container = Container()
    controller = container.cli_controller
    
    # 1. User selects law
    selected_law = controller.search_use_case.execute('소득세법', display=1)[0]
    print(f"Selected: {selected_law.name}")
    
    # 2. View law content
    law_content = controller.view_articles_use_case.get_law_content(selected_law.mst)
    print(f"Found {len(law_content.articles)} articles")
    
    # 3. Display law content menu
    controller.presenter.display_law_content_menu(law_content)
    
    # 4. Simulate option 1: View all articles
    print("\n--- Option 1: View All Articles ---")
    controller.presenter.display_article_list(law_content.articles)
    
    # 5. Simulate option 2: Search by article number
    print("\n--- Option 2: Search by Article Number ---")
    article_number = '1'
    # Find articles with matching number
    found_articles = [a for a in law_content.articles if a.article_number == article_number]
    if found_articles:
        print(f"Found {len(found_articles)} articles with number {article_number}")
        controller.presenter.display_article_content(found_articles[0])
    
    # 6. Simulate option 3: Search by keyword
    print("\n--- Option 3: Search by Keyword ---")
    keyword = '목적'
    found_articles = controller.view_articles_use_case.search_articles(
        law_content, keyword
    )
    if found_articles:
        print(f"Found {len(found_articles)} articles containing '{keyword}'")
        controller.presenter.display_article_list(found_articles)


if __name__ == "__main__":
    test_menu_flow()