"""Test final URL generation."""
from urllib.parse import quote

def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    # Remove spaces for certain law types (시행령, 시행규칙)
    clean_name = law_name
    if " 시행령" in law_name or " 시행규칙" in law_name:
        clean_name = law_name.replace(" ", "")
    
    # Use unencoded Korean for the path - browsers will handle encoding
    base_url = "https://www.law.go.kr/법령/"
    encoded_name = quote(clean_name, safe='')
    return f"{base_url}{encoded_name}"

# Test with examples
test_cases = {
    "소득세법": "https://www.law.go.kr/법령/소득세법",
    "소득세법 시행령": "https://www.law.go.kr/법령/소득세법시행령",
    "소득세법 시행규칙": "https://www.law.go.kr/법령/소득세법시행규칙",
}

print("Testing final URL generation:\n")
for law_name, expected_url in test_cases.items():
    generated_url = generate_law_url(law_name)
    print(f"Law: {law_name}")
    print(f"Generated: {generated_url}")
    print(f"Expected:  {expected_url}")
    print(f"Match: {generated_url == expected_url}")
    print()

# Test with browser
import webbrowser
test_url = generate_law_url("소득세법")
print(f"Opening test URL in browser: {test_url}")
webbrowser.open(test_url)