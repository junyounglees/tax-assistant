"""Test URL encoding fix."""
from urllib.parse import quote
import webbrowser

def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    # Remove spaces for certain law types (시행령, 시행규칙)
    clean_name = law_name
    if " 시행령" in law_name or " 시행규칙" in law_name:
        clean_name = law_name.replace(" ", "")
    
    # Fully encode the entire URL path to avoid character encoding issues
    base_url = "https://www.law.go.kr/"
    path = "법령"
    # Use quote to encode both path and law name
    encoded_path = quote(path.encode('utf-8'), safe='')
    encoded_name = quote(clean_name.encode('utf-8'), safe='')
    return f"{base_url}{encoded_path}/{encoded_name}"

# Test cases
test_cases = {
    "소득세법": "https://www.law.go.kr/법령/소득세법",
    "소득세법 시행령": "https://www.law.go.kr/법령/소득세법시행령",
}

print("Testing URL encoding with UTF-8:\n")
for law_name, expected_url in test_cases.items():
    generated_url = generate_law_url(law_name)
    print(f"Law: {law_name}")
    print(f"Generated: {generated_url}")
    print(f"Expected:  {expected_url}")
    print()

# Test the actual URL in browser
test_url = generate_law_url("소득세법")
print(f"Opening URL in browser: {test_url}")
webbrowser.open(test_url)