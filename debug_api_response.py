#!/usr/bin/env python3
"""Debug API response format."""
import json
from src.data.api.law_api_client import LawAPIClient


def debug_api_response():
    """Debug the actual API response."""
    client = LawAPIClient(email_id='lee')
    
    # Test with Income Tax Law MST
    mst = "267581"
    print(f"Testing API with MST: {mst}")
    
    # Get full text
    response = client.get_full_text(mst)
    
    # Save raw response for inspection
    with open('debug_law_response.json', 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=2)
    
    print("\nResponse saved to debug_law_response.json")
    
    # Print response structure
    print("\nResponse keys:", list(response.keys()) if isinstance(response, dict) else type(response))
    
    # Check for specific keys
    if isinstance(response, dict):
        for key in ['error', 'law', '법령', '조문']:
            print(f"Has '{key}': {key in response}")
    
    # Try to find articles in various locations
    articles = None
    if isinstance(response, dict):
        if '조문' in response:
            articles = response['조문']
            print(f"\nFound articles directly: {type(articles)}")
        elif 'law' in response:
            law_data = response['law']
            print(f"\nFound law data: {type(law_data)}")
            if isinstance(law_data, list) and law_data:
                law_data = law_data[0]
            if isinstance(law_data, dict) and '조문' in law_data:
                articles = law_data['조문']
                print(f"Found articles in law data: {type(articles)}")
    
    if articles:
        if isinstance(articles, list):
            print(f"Number of articles: {len(articles)}")
            if articles:
                print(f"First article keys: {list(articles[0].keys())}")
        else:
            print(f"Articles type: {type(articles)}")
    else:
        print("\nNo articles found in response")


if __name__ == "__main__":
    debug_api_response()