#!/usr/bin/env python3
"""Test the law selection flow."""
from src.infrastructure.container import Container

def test_law_selection():
    """Test the improved law selection flow."""
    container = Container()
    controller = container.cli_controller
    
    # Test with 소득세법 search (multiple results)
    query = '소득세법'
    print(f"Testing search for '{query}'...")
    
    controller.presenter.display_success(f"'{query}' 검색 중...")
    laws = controller.search_use_case.search_with_abbreviation(query)
    
    if laws:
        controller.presenter.display_search_results(laws, query)
        controller.presenter.display_success(f"결과 저장: output/{query}_검색결과.json")
        
        # Show command-line options
        controller.presenter.display_command_line_options(laws)
        
        # Since there are multiple results, show selection menu
        print("\n(Simulating user flow - multiple results)")
        if len(laws) > 1:
            print("\n어떤 법령의 조문을 보시겠습니까?")
            for i, law in enumerate(laws, 1):
                print(f"{i}. {law.name}")
            print("0. 뒤로가기")
            
            print("\n번호 선택: 1 (simulated)")
            selected_law = laws[0]
            print(f"\nSelected: {selected_law.name}")
            
            # Now it would proceed to view articles
            print(f"Would proceed to view articles for: {selected_law.name}")


if __name__ == "__main__":
    test_law_selection()