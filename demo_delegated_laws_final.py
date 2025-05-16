"""Demo script for delegated laws feature."""
from src.infrastructure.container import Container

def demo_delegated_laws():
    """Demo the delegated laws feature."""
    container = Container()
    
    print("Korean Law Search - Delegated Laws Demo")
    print("=" * 50)
    
    # Search for 소득세법
    print("\n1. Searching for 소득세법...")
    laws = container.search_use_case.execute("소득세법")
    if not laws:
        print("No laws found!")
        return
    
    law = laws[0]
    print(f"Found: {law.name}")
    
    # Get law content
    print("\n2. Loading law content...")
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    print(f"Total articles: {len(law_content.articles)}")
    
    # Find articles with delegated law references
    print("\n3. Finding articles with delegated law references...")
    articles_with_refs = container.view_delegated_laws_use_case.get_articles_with_delegated_references(law_content)
    print(f"Found {len(articles_with_refs)} articles with delegated law references")
    
    # Show a specific example
    print("\n4. Example: 제1조의2 (정의)")
    target_article = None
    for article in law_content.articles:
        if article.formatted_number == "제1조의2":
            target_article = article
            break
    
    if target_article:
        print(f"Article: {target_article.formatted_number} - {target_article.article_title}")
        print(f"Content preview: {target_article.article_content[:100]}...")
        
        # Get delegated laws for this article
        print("\n5. Getting delegated laws...")
        result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
            law.mst, target_article.normalized_number, law_content
        )
        
        if result['has_delegated_references']:
            print(f"Found {len(result['delegated_references'])} references in the article")
            for ref in result['delegated_references']:
                print(f"  - {ref['type']}: {ref['text']}")
            
            print(f"\nFound {len(result['delegated_content'])} delegated law contents")
            for i, content in enumerate(result['delegated_content'], 1):
                delegated_law = content['law']
                delegated_articles = content['articles']
                print(f"\n{i}. {delegated_law.name}")
                print(f"   Type: {delegated_law.law_type}")
                print(f"   Articles found: {len(delegated_articles)}")
                for j, article in enumerate(delegated_articles[:2], 1):  # Show first 2
                    print(f"   {j}. {article.formatted_number} - {article.article_title}")
    
    # Interactive selection
    print("\n\n6. Interactive Article Selection")
    print("Enter an article number to see its delegated laws (or 'q' to quit)")
    print("Examples: 12 (for 제12조), 1_2 (for 제1조의2)")
    
    while True:
        choice = input("\nArticle number: ").strip()
        if choice.lower() == 'q':
            break
        
        # Find the article
        found_article = None
        for article in law_content.articles:
            if article.normalized_number == choice or article.article_number == choice:
                found_article = article
                break
        
        if not found_article:
            print(f"Article {choice} not found")
            continue
        
        print(f"\nArticle: {found_article.formatted_number} - {found_article.article_title or 'No title'}")
        
        # Get delegated laws
        result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
            law.mst, found_article.normalized_number, law_content
        )
        
        if result['has_delegated_references']:
            print(f"Delegated law references: {len(result['delegated_references'])}")
            for ref in result['delegated_references']:
                print(f"  - {ref['type']}: {ref['text']}")
            
            if result['delegated_content']:
                print(f"\nDelegated law content found: {len(result['delegated_content'])} items")
                for content in result['delegated_content']:
                    print(f"  - {content['law'].name}: {len(content['articles'])} articles")
            else:
                print("No delegated law content retrieved")
        else:
            print("This article has no delegated law references")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    demo_delegated_laws()