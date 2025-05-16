"""Debug script for delegated laws API."""
import json
from src.infrastructure.container import Container

def debug_delegated_api():
    """Debug the delegated laws API."""
    container = Container()
    
    # Test with a known MST
    mst = "267581"  # 소득세법
    print(f"Testing with MST: {mst}")
    
    # Direct API call
    print("\n1. Direct API call...")
    result = container.api_client.get_delegated_laws(mst)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Response keys: {result.keys()}")
        print(f"Full response: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
    
    # Test with wrong target
    print("\n2. Testing with wrong target...")
    import requests
    params = {
        'OC': container.api_client.email_id,
        'target': 'lsDelegated',  # Correct target
        'type': 'JSON',
        'MST': mst
    }
    
    response = requests.get("http://www.law.go.kr/DRF/lawService.do", params=params)
    print(f"Status code: {response.status_code}")
    print(f"Response headers: {dict(response.headers)}")
    print(f"Response text: {response.text[:500]}...")
    
    # Try with different MST formats
    print("\n3. Testing different MST formats...")
    test_msts = [
        mst,           # As-is
        f"00{mst}",    # With leading zeros
        mst[:6],       # First 6 digits only
    ]
    
    for test_mst in test_msts:
        print(f"\nTrying MST: {test_mst}")
        result = container.api_client.get_delegated_laws(test_mst)
        if 'error' not in result:
            from src.domain.entities.delegated_law import DelegatedLawResponse
            response = DelegatedLawResponse.from_api_response(result)
            print(f"Success! Found {len(response.all_delegated_items)} items")
        else:
            print(f"Error: {result['error']}")

if __name__ == "__main__":
    debug_delegated_api()