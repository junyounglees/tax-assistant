"""Test specific article matching."""
from src.infrastructure.container import Container

def test_specific_article():
    """Test delegated laws for specific article."""
    container = Container()
    
    # Search for 소득세법
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    
    # Get law content
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    # Find the article 제1조의2
    article_1_2 = None
    for article in law_content.articles:
        if "제1조의2" in article.formatted_number:
            article_1_2 = article
            print(f"Found article: {article.article_number}")
            print(f"Formatted: {article.formatted_number}")
            print(f"Normalized: {article.normalized_number}")
            print(f"Has references: {article.has_delegated_law_references()}")
            break
    
    if not article_1_2:
        print("Article not found!")
        return
    
    # Test the use case method
    result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
        law.mst, article_1_2.article_number, law_content
    )
    
    print(f"\nResult:")
    print(f"Primary article: {result['primary_article'].formatted_number if result['primary_article'] else 'None'}")
    print(f"Has references: {result['has_delegated_references']}")
    print(f"Delegated references: {len(result['delegated_references'])}")
    print(f"Delegated content: {len(result['delegated_content'])}")
    
    # Get delegated laws directly
    delegated_response = container.delegated_law_repository.get_delegated_laws(law.mst)
    if delegated_response:
        # Find matches for article 1_2
        matches = []
        for item in delegated_response.all_delegated_items:
            if item.article_number == "1_2":
                matches.append(item)
        
        print(f"\nDirect matches for 1_2: {len(matches)}")
        for match in matches[:3]:
            print(f"  - {match.delegated_title} ({match.delegated_type})")
            print(f"    Article: {match.delegated_article_number} - {match.delegated_article_title}")

if __name__ == "__main__":
    test_specific_article()