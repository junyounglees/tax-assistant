#!/usr/bin/env python3
"""Test article search result saving."""
from src.infrastructure.container import Container
import os
import json

def test_article_saving():
    """Test that article search results are saved."""
    container = Container()
    controller = container.cli_controller
    
    # Get 소득세법 content
    laws = controller.search_use_case.execute('소득세법', display=1)
    law = laws[0]
    law_content = controller.view_articles_use_case.get_law_content(law.mst)
    
    print(f"Testing article search for {law_content.law_name}")
    
    # Search for articles containing "세율"
    search_term = "세율"
    results = controller.view_articles_use_case.search_articles(law_content, search_term)
    print(f"Found {len(results)} articles containing '{search_term}'")
    
    # Save the results
    success = controller.view_articles_use_case.save_article_search_results(
        results, law_content.law_name, search_term
    )
    
    if success:
        print("Successfully saved article search results")
        
        # Check the output directory
        output_files = [f for f in os.listdir('output') if f.startswith(f"{law_content.law_name}_조문검색_{search_term}")]
        
        if output_files:
            latest_file = sorted(output_files)[-1]
            print(f"Saved to: output/{latest_file}")
            
            # Read and display the saved content
            with open(f'output/{latest_file}', 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                
            print(f"\nSaved data structure:")
            print(f"- Law name: {saved_data['law_name']}")
            print(f"- Search term: {saved_data['search_term']}")
            print(f"- Total results: {saved_data['total_results']}")
            print(f"- Articles saved: {len(saved_data['articles'])}")
            
            if saved_data['articles']:
                first_article = saved_data['articles'][0]
                print(f"\nFirst article:")
                print(f"- Number: {first_article['formatted_number']}")
                print(f"- Title: {first_article['article_title']}")
    else:
        print("Failed to save article search results")


if __name__ == "__main__":
    test_article_saving()