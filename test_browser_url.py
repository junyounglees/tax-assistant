"""Test browser opening with different URL formats."""
import webbrowser
from urllib.parse import quote

# Test 1: URL with percent-encoded Korean path
url1 = f"https://www.law.go.kr/{quote('법령', safe='')}/{quote('소득세법', safe='')}"
print(f"Test 1 - Fully encoded: {url1}")

# Test 2: URL with mixed encoding (our current implementation)
url2 = f"https://www.law.go.kr/법령/{quote('소득세법', safe='')}"
print(f"Test 2 - Mixed encoding: {url2}")

# Test 3: URL with no encoding (raw Korean)
url3 = "https://www.law.go.kr/법령/소득세법"
print(f"Test 3 - No encoding: {url3}")

# Let's test which one works best in the browser
print("\nTesting URL 2 (Mixed encoding) in browser...")
webbrowser.open(url2)

# Create a simple test for the actual function
print("\n\nActual function test:")
def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    from urllib.parse import quote
    
    # Remove spaces for certain law types (시행령, 시행규칙)
    clean_name = law_name
    if " 시행령" in law_name or " 시행규칙" in law_name:
        clean_name = law_name.replace(" ", "")
    
    # Use unencoded Korean for the path - browsers will handle encoding
    base_url = "https://www.law.go.kr/법령/"
    encoded_name = quote(clean_name, safe='')
    return f"{base_url}{encoded_name}"

test_url = generate_law_url("소득세법")
print(f"Generated URL: {test_url}")
print("This is the URL that will be opened when you select option 4.")