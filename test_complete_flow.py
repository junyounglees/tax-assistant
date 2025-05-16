#!/usr/bin/env python3
"""Test the complete flow."""
from src.infrastructure.container import Container

def test_complete_flow():
    """Test the complete flow with all fixes."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print("Complete flow test:\n")
    
    # Show improved article list
    print("1. Article list (first 10):")
    controller.presenter.display_article_list(law_content.articles[:10])
    
    # Test searching for article 1 (should exclude chapter header)
    print("\n\n2. Search for article 1:")
    article_num = '1'
    matching_articles = [
        a for a in law_content.articles 
        if a.article_number == article_num 
        and a.article_title != "Chapter/Section Header"
    ]
    
    if len(matching_articles) > 1:
        print(f"제{article_num}조에 해당하는 조문이 {len(matching_articles)}개 있습니다.")
        controller.presenter.display_article_list(matching_articles)
        
        # Simulate selecting 제1조의2
        print("\n선택: 2 (제1조의2 정의)")
        selected = matching_articles[1]
        controller.presenter.display_article_content(selected)


if __name__ == "__main__":
    test_complete_flow()