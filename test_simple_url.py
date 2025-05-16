"""Test simple URL generation."""
import webbrowser

def generate_law_url(law_name: str) -> str:
    """Generate law.go.kr URL from law name."""
    # Remove all spaces from law name
    clean_name = law_name.replace(" ", "")
    
    # Return direct URL with Korean characters - browsers will handle encoding
    return f"https://www.law.go.kr/법령/{clean_name}"

# Test cases
test_cases = [
    "소득세법",
    "소득세법 시행령",
    "소득세법 시행규칙",
]

print("Testing simplified URL generation:\n")
for law_name in test_cases:
    url = generate_law_url(law_name)
    print(f"Law: {law_name}")
    print(f"URL: {url}")
    print()

# Test opening in browser
test_url = generate_law_url("소득세법 시행령")
print(f"Opening in browser: {test_url}")
webbrowser.open(test_url)