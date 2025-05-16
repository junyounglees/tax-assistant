"""Debug article format and numbering."""
from src.infrastructure.container import Container

def debug_article_format():
    """Debug article format between content and delegated laws."""
    container = Container()
    
    # Search for 소득세법
    laws = container.search_use_case.execute("소득세법")
    law = laws[0]
    
    # Get law content
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    # Show how "제1조의2" is stored
    for article in law_content.articles[:10]:
        print(f"Article: {article.article_number}")
        print(f"  Formatted: {article.formatted_number}")
        print(f"  Title: {article.article_title}")
        print(f"  Content preview: {article.article_content[:50]}...")
        print()
        
    # Check the actual content
    print("\n=== Looking for 제1조의2 ===")
    for article in law_content.articles:
        if "제1조의2" in article.article_content[:20]:
            print(f"Found! Article number: {article.article_number}")
            print(f"Formatted: {article.formatted_number}")
            print(f"Content: {article.article_content[:100]}...")
            break

if __name__ == "__main__":
    debug_article_format()