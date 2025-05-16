#!/usr/bin/env python3
"""Test law URL generation."""
from urllib.parse import quote

def test_law_url_generation():
    """Test generating law.go.kr URLs."""
    laws = [
        '소득세법',
        '소득세법 시행령',
        '소득세법 시행규칙',
        '법인세법',
        '부가가치세법'
    ]
    
    base_url = "https://www.law.go.kr/법령/"
    
    print("Law URL generation test:\n")
    for law_name in laws:
        encoded_name = quote(law_name)
        url = f"{base_url}{encoded_name}"
        print(f"{law_name}")
        print(f"  → {url}")
        print()
    
    # Show expected URLs from your examples
    print("\nExpected URLs:")
    print("소득세법: https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%86%8C%EB%93%9D%EC%84%B8%EB%B2%95")
    print("소득세법 시행령: https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EC%86%8C%EB%93%9D%EC%84%B8%EB%B2%95%EC%8B%9C%ED%96%89%EB%A0%B9")


if __name__ == "__main__":
    test_law_url_generation()