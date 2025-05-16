"""Test URL generation fix."""
from urllib.parse import quote

def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    base_url = "https://www.law.go.kr/"
    # Encode the Korean path component and law name
    path = "법령"
    encoded_path = quote(path, safe='')
    encoded_name = quote(law_name, safe='')
    return f"{base_url}{encoded_path}/{encoded_name}"

# Test with examples
test_cases = {
    "소득세법": "https://www.law.go.kr/법령/소득세법",
    "소득세법 시행령": "https://www.law.go.kr/법령/소득세법시행령",
}

print("Testing URL generation with proper encoding:\n")
for law_name, expected_url in test_cases.items():
    generated_url = generate_law_url(law_name)
    print(f"Law: {law_name}")
    print(f"Generated: {generated_url}")
    print(f"Expected:  {expected_url}")
    
    # Print encoded components for debugging
    encoded_path = quote("법령", safe='')
    encoded_name = quote(law_name, safe='')
    print(f"Encoded path: {encoded_path}")
    print(f"Encoded name: {encoded_name}")
    print()