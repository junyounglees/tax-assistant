"""Debug article matching between law content and delegated laws."""
from src.infrastructure.container import Container

def debug_article_matching():
    """Debug article matching issue."""
    container = Container()
    
    # Search for 소득세법
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    
    # Get law content
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    # Get delegated laws
    delegated_response = container.delegated_law_repository.get_delegated_laws(law.mst)
    
    print("=== Article Number Formats in Law Content ===")
    # Show first 10 articles with delegated references
    for i, article in enumerate(law_content.articles[:20]):
        if article.has_delegated_law_references():
            print(f"Article number: {article.article_number} (formatted: {article.formatted_number})")
            print(f"  Title: {article.article_title}")
            print(f"  Has references: {article.has_delegated_law_references()}")
    
    print("\n=== Article Number Formats in Delegated Laws ===")
    if delegated_response:
        # Show first 10 delegated items
        for i, item in enumerate(delegated_response.all_delegated_items[:10]):
            print(f"Source article: {item.article_number}")
            print(f"  Article title: {item.article_title}")
            print(f"  Delegated to: {item.delegated_title}")
            print(f"  Link text: {item.link_text}")
    
    # Test specific article
    print("\n=== Test Specific Article ===")
    test_article_num = "0001_2"  # 제1조의2
    print(f"Looking for article: {test_article_num}")
    
    # Find in law content
    found_in_content = False
    for article in law_content.articles:
        if article.article_number == test_article_num:
            print(f"Found in content: {article.formatted_number}")
            found_in_content = True
            break
    
    if not found_in_content:
        print("Not found in law content")
        # Show what article numbers we have that might match
        for article in law_content.articles:
            if "1" in article.article_number and "2" in article.article_number:
                print(f"  Possible match: {article.article_number} -> {article.formatted_number}")
    
    # Find in delegated laws
    found_in_delegated = False
    if delegated_response:
        for item in delegated_response.all_delegated_items:
            if item.article_number == test_article_num:
                print(f"Found in delegated: {item.article_number}")
                found_in_delegated = True
                break
    
    if not found_in_delegated:
        print("Not found in delegated laws")
        # Show what we have
        if delegated_response:
            for item in delegated_response.all_delegated_items:
                if item.article_number == "1_2":
                    print(f"  Found with different format: {item.article_number}")

if __name__ == "__main__":
    debug_article_matching()