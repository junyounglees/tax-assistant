"""Debug has_delegated_references check."""
from src.infrastructure.container import Container

def debug_has_references():
    """Debug the has_delegated_references check."""
    container = Container()
    
    # Search for 소득세법
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    
    # Get law content
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    # Find article 제1조의2
    for article in law_content.articles:
        if article.formatted_number == "제1조의2":
            print(f"Found article: {article.formatted_number}")
            print(f"Article number: {article.article_number}")
            print(f"Normalized: {article.normalized_number}")
            print(f"Has references check: {article.has_delegated_law_references()}")
            print(f"References: {article.get_delegated_law_references()}")
            
            # Check the content
            print(f"\nContent preview: {article.article_content[:200]}...")
            
            # Check pattern matching
            from src.domain.entities.article import Article
            for i, pattern in enumerate(Article.DELEGATION_PATTERNS):
                if re.search(pattern, article.article_content):
                    print(f"\nPattern {i} matched: {pattern}")
                    match = re.search(pattern, article.article_content)
                    print(f"Match: {match.group()}")
            
            # Test with use case
            result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
                law.mst, article.article_number, law_content
            )
            
            print(f"\nUse case result:")
            print(f"Has references: {result['has_delegated_references']}")
            if result['primary_article']:
                print(f"Primary article: {result['primary_article'].formatted_number}")
                print(f"Primary has refs: {result['primary_article'].has_delegated_law_references()}")
            
            break

if __name__ == "__main__":
    import re
    debug_has_references()