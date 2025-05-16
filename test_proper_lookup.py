"""Test proper article lookup."""
from src.infrastructure.container import Container

def test_proper_lookup():
    """Test proper article lookup with delegated laws."""
    container = Container()
    
    # Get law content
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    # Find 제1조의2 specifically
    target_article = None
    for article in law_content.articles:
        if article.formatted_number == "제1조의2":
            target_article = article
            break
    
    if not target_article:
        print("Article not found!")
        return
    
    print(f"Found article: {target_article.formatted_number}")
    print(f"Article number: {target_article.article_number}")
    print(f"Normalized: {target_article.normalized_number}")
    print(f"Has references: {target_article.has_delegated_law_references()}")
    
    # Test with different lookup methods
    print("\n=== Method 1: Using article_number ===")
    result1 = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
        law.mst, target_article.article_number, law_content
    )
    print(f"Primary article: {result1['primary_article'].formatted_number if result1['primary_article'] else 'None'}")
    print(f"Delegated content: {len(result1['delegated_content'])}")
    
    print("\n=== Method 2: Using normalized number ===")
    result2 = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
        law.mst, "1_2", law_content
    )
    print(f"Primary article: {result2['primary_article'].formatted_number if result2['primary_article'] else 'None'}")
    print(f"Delegated content: {len(result2['delegated_content'])}")
    
    # Direct API check
    print("\n=== Direct API Check ===")
    delegated_response = container.delegated_law_repository.get_delegated_laws(law.mst)
    if delegated_response:
        count = 0
        for item in delegated_response.all_delegated_items:
            if item.article_number == "1_2":
                count += 1
                if count <= 3:
                    print(f"- {item.delegated_title}: {item.delegated_article_title}")
        print(f"Total matches for 1_2: {count}")

if __name__ == "__main__":
    test_proper_lookup()