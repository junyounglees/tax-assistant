"""Debug API response structure."""
import json
from src.infrastructure.container import Container

def debug_api_structure():
    """Debug the API response structure."""
    container = Container()
    
    mst = "267581"  # 소득세법
    print(f"Testing with MST: {mst}")
    
    # Get raw response
    result = container.api_client.get_delegated_laws(mst)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        return
    
    # Inspect structure
    print("\n=== API Response Structure ===")
    print(f"Top level keys: {list(result.keys())}")
    
    if 'lsDelegated' in result:
        ls_delegated = result['lsDelegated']
        print(f"\nlsDelegated keys: {list(ls_delegated.keys())}")
        
        if '법령' in ls_delegated:
            law_data = ls_delegated['법령']
            print(f"\n법령 keys: {list(law_data.keys())}")
            
            if '위임조문정보' in law_data:
                delegated_info = law_data['위임조문정보']
                print(f"\n위임조문정보 type: {type(delegated_info)}")
                print(f"위임조문정보 length: {len(delegated_info)}")
                
                if delegated_info and len(delegated_info) > 0:
                    first_item = delegated_info[0]
                    print(f"\nFirst item keys: {list(first_item.keys())}")
                    
                    # Pretty print the first item
                    print("\nFirst delegated item:")
                    print(json.dumps(first_item, ensure_ascii=False, indent=2)[:1000])
    
    # Save full response for analysis
    with open('debug_delegated_response.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\nFull response saved to debug_delegated_response.json")

if __name__ == "__main__":
    debug_api_structure()