"""Test script for delegated law feature."""
import time
from src.infrastructure.container import Container

def test_delegated_laws():
    """Test the delegated law feature."""
    print("Testing Delegated Laws Feature")
    print("="*50)
    
    # Create container
    container = Container()
    
    # Search for 소득세법
    print("\n1. Searching for 소득세법...")
    laws = container.search_use_case.execute("소득세법")
    if not laws:
        print("Error: No laws found")
        return
    
    law = laws[0]
    print(f"Found: {law.name} (MST: {law.mst})")
    
    # Get law content
    print("\n2. Getting law content...")
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    if not law_content:
        print("Error: Could not get law content")
        return
    
    print(f"Total articles: {len(law_content.articles)}")
    
    # Find articles with delegated law references
    print("\n3. Finding articles with delegated law references...")
    delegated_articles = container.view_delegated_laws_use_case.get_articles_with_delegated_references(law_content)
    print(f"Found {len(delegated_articles)} articles with delegated law references")
    
    # Show first 5 articles with delegated references
    print("\nFirst 5 articles with delegated law references:")
    for i, article in enumerate(delegated_articles[:5], 1):
        references = article.get_delegated_law_references()
        print(f"{i}. {article.formatted_number} - {len(references)} references")
        for ref in references:
            print(f"   - {ref['type']}: {ref['text']}")
    
    # Test getting delegated laws for a specific article
    if delegated_articles:
        test_article = delegated_articles[0]
        print(f"\n4. Getting delegated laws for {test_article.formatted_number}...")
        print(f"   Article number: {test_article.article_number}")
        print(f"   Normalized: {test_article.normalized_number}")
        
        result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
            law.mst, test_article.article_number, law_content
        )
        
        if result['has_delegated_references']:
            print(f"Primary article: {result['primary_article'].formatted_number}")
            print(f"Delegated references: {len(result['delegated_references'])}")
            print(f"Delegated content found: {len(result['delegated_content'])}")
            
            if result['delegated_content']:
                for i, content in enumerate(result['delegated_content'], 1):
                    delegated_law = content['law']
                    delegated_articles = content['articles']
                    print(f"\n{i}. {delegated_law.name}")
                    print(f"   Articles: {len(delegated_articles)}")
                    for article in delegated_articles[:2]:  # Show first 2 articles
                        print(f"   - {article.formatted_number}: {article.article_title or 'No title'}")
            else:
                print("No delegated content retrieved")
        else:
            print("Article has no delegated law references")
    
    # Test API directly
    print("\n5. Testing delegated laws API directly...")
    api_result = container.api_client.get_delegated_laws(law.mst)
    
    if 'error' not in api_result:
        from src.domain.entities.delegated_law import DelegatedLawResponse
        delegated_response = DelegatedLawResponse.from_api_response(api_result)
        print(f"API returned {len(delegated_response.all_delegated_items)} delegated law items")
    else:
        print(f"API Error: {api_result['error']}")
    
    print("\n" + "="*50)
    print("Test completed!")

if __name__ == "__main__":
    test_delegated_laws()