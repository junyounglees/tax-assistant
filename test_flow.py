#!/usr/bin/env python3
"""Test the flow from law selection to article viewing."""
from src.infrastructure.container import Container

def test_flow():
    """Test the integrated flow."""
    container = Container()
    controller = container.cli_controller
    
    # Simulate user selecting "1" for 소득세법
    print("Simulating user selecting '1' for 소득세법...\n")
    
    # Get the law name for option 1
    query = controller.presenter.get_selected_law_from_menu('1')
    print(f"Selected: {query}")
    
    # Search for laws
    controller.presenter.display_success(f"'{query}' 검색 중...")
    laws = controller.search_use_case.search_with_abbreviation(query)
    
    if laws:
        controller.presenter.display_search_results(laws, query)
        controller.presenter.display_success(f"결과 저장: output/{query}_검색결과.json")
        
        # Automatically proceed to article viewing
        selected_law = laws[0]
        print(f"\nAutomatically proceeding to article view for {selected_law.name}...")
        
        # Get law content
        law_content = controller.view_articles_use_case.get_law_content(selected_law.mst)
        
        if law_content:
            # Display the article menu
            controller.presenter.display_law_content_menu(law_content)
            print("\nUser is now in the article viewing menu!")


if __name__ == "__main__":
    test_flow()