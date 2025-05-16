"""Test final URL fix with proper encoding."""
import webbrowser
from urllib.parse import quote, unquote

# Let's try different approaches
def test_url_approaches():
    law_name = "소득세법"
    
    # Approach 1: Direct Korean URL
    url1 = f"https://www.law.go.kr/법령/{law_name}"
    print(f"1. Direct Korean: {url1}")
    
    # Approach 2: Fully encoded URL
    url2 = f"https://www.law.go.kr/{quote('법령')}/{quote(law_name)}"
    print(f"2. Fully encoded: {url2}")
    
    # Approach 3: Mixed encoding (keep domain, encode path)
    url3 = f"https://www.law.go.kr/%EB%B2%95%EB%A0%B9/{quote(law_name)}"
    print(f"3. Mixed encoding: {url3}")
    
    # Approach 4: Using quote_plus
    from urllib.parse import quote_plus
    url4 = f"https://www.law.go.kr/{quote_plus('법령')}/{quote_plus(law_name)}"
    print(f"4. Quote plus: {url4}")
    
    return url3  # This is the most likely to work

# Test the URL
test_url_approaches()
print()

# Let's use the approach that matches the expected format from the user's examples
def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    # Remove spaces for compound law names
    clean_name = law_name.replace(" ", "")
    
    # Use the encoded path for 법령
    encoded_path = "%EB%B2%95%EB%A0%B9"  # This is '법령' encoded
    encoded_name = quote(clean_name)
    
    return f"https://www.law.go.kr/{encoded_path}/{encoded_name}"

# Test with examples
test_cases = [
    "소득세법",
    "소득세법 시행령",
]

print("Final approach:")
for law_name in test_cases:
    url = generate_law_url(law_name)
    print(f"Law: {law_name}")
    print(f"URL: {url}")
    print()

# Open in browser
test_url = generate_law_url("소득세법")
print(f"Opening: {test_url}")
webbrowser.open(test_url)