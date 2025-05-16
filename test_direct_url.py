"""Test direct URL opening without encoding."""
import webbrowser

# Direct URLs as expected
urls = [
    "https://www.law.go.kr/법령/소득세법",
    "https://www.law.go.kr/법령/소득세법시행령",
]

print("Testing direct URL opening:")
for url in urls:
    print(f"Opening: {url}")
    webbrowser.open(url)
    input("Press Enter to continue...")

# Test a simpler approach - just construct the URL directly
def generate_law_url_simple(law_name: str) -> str:
    """Generate law.go.kr URL from law name - simple version."""
    # Remove spaces for certain law types
    clean_name = law_name.replace(" ", "")
    return f"https://www.law.go.kr/법령/{clean_name}"

test_names = ["소득세법", "소득세법 시행령"]
print("\nTesting simple URL generation:")
for name in test_names:
    url = generate_law_url_simple(name)
    print(f"Law: {name}")
    print(f"URL: {url}")
    print()