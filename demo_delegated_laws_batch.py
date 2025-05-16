"""Non-interactive demo of delegated laws feature."""
from src.infrastructure.container import Container

def demo_delegated_laws_batch():
    """Demo the delegated laws feature without user input."""
    container = Container()
    
    print("Korean Law Search - Delegated Laws Demo")
    print("=" * 50)
    
    # Search for 소득세법
    print("\n1. Searching for 소득세법...")
    laws = container.search_use_case.execute("소득세법")
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
    
    # Show first 5 articles with delegated references
    print("\n4. Examples of articles with delegated laws:")
    
    for i, article in enumerate(articles_with_refs[:5], 1):
        print(f"\n{i}. {article.formatted_number} - {article.article_title or 'No title'}")
        
        # Get delegated laws for this article
        result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
            law.mst, article.normalized_number, law_content
        )
        
        if result['has_delegated_references']:
            print(f"   References in article:")
            for ref in result['delegated_references']:
                print(f"     - {ref['type']}: \"{ref['text']}\"")
            
            if result['delegated_content']:
                print(f"   Delegated laws found: {len(result['delegated_content'])}")
                for j, content in enumerate(result['delegated_content'], 1):
                    delegated_law = content['law']
                    delegated_articles = content['articles']
                    print(f"     {j}. {delegated_law.name} ({delegated_law.law_type})")
                    print(f"        Articles: {len(delegated_articles)}")
                    if delegated_articles:
                        print(f"        First article: {delegated_articles[0].formatted_number} - {delegated_articles[0].article_title}")
            else:
                print("   No delegated law content retrieved")
    
    # Show specific example with full content
    print("\n\n5. Detailed Example: 제12조 (비과세소득)")
    target_article = None
    for article in law_content.articles:
        if article.formatted_number == "제12조" and article.article_title == "비과세소득":
            target_article = article
            break
    
    if target_article:
        print(f"Article: {target_article.formatted_number} - {target_article.article_title}")
        
        # Get delegated laws
        result = container.view_delegated_laws_use_case.get_delegated_laws_for_article(
            law.mst, target_article.normalized_number, law_content
        )
        
        if result['has_delegated_references']:
            references = result['delegated_references']
            print(f"\nFound {len(references)} delegation references in the article")
            
            # Show unique types of delegations
            delegation_types = {}
            for ref in references:
                ref_type = ref['type']
                if ref_type not in delegation_types:
                    delegation_types[ref_type] = []
                delegation_types[ref_type].append(ref['text'])
            
            for ref_type, texts in delegation_types.items():
                print(f"\n{ref_type} references: {len(texts)}")
                for text in texts[:3]:  # Show first 3
                    print(f"  - \"{text}\"")
            
            if result['delegated_content']:
                print(f"\nDelegated law content retrieved: {len(result['delegated_content'])} items")
                for i, content in enumerate(result['delegated_content'][:3], 1):  # Show first 3
                    delegated_law = content['law']
                    print(f"\n{i}. {delegated_law.name}")
                    print(f"   Type: {delegated_law.law_type}")
                    print(f"   MST: {delegated_law.mst}")
    
    print("\n" + "=" * 50)
    print("Demo completed successfully!")

if __name__ == "__main__":
    demo_delegated_laws_batch()