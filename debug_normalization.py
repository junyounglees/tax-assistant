"""Debug normalization logic."""
from src.infrastructure.container import Container

def debug_normalization():
    """Debug normalization logic."""
    container = Container()
    
    # Test the normalization function
    use_case = container.view_delegated_laws_use_case
    
    test_cases = [
        "1",
        "1_2", 
        "0001",
        "0001_2"
    ]
    
    print("=== Normalization Test ===")
    for test in test_cases:
        normalized = use_case._normalize_article_number(test)
        print(f"{test} -> {normalized}")
    
    # Get real articles and check normalization
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    print("\n=== Article Normalization ===")
    for article in law_content.articles[:10]:
        if article.article_title != "Chapter/Section Header":
            print(f"Article number: {article.article_number}")
            print(f"  Formatted: {article.formatted_number}")
            print(f"  Normalized: {article.normalized_number}")
            print()

if __name__ == "__main__":
    debug_normalization()