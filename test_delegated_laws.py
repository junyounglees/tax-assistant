#!/usr/bin/env python3
"""Test delegated law discovery and viewing feature."""

import sys
from src.infrastructure.container import Container
from src.domain.entities.article import Article


def test_article_delegation_detection():
    """Test that Article entity can detect delegated law references."""
    print("Testing delegation detection in Article entity...")
    
    # Create test articles
    article_with_delegation = Article(
        article_number="001",
        article_title="테스트 조문",
        article_content="이 사항은 대통령령으로 정한다.",
        enforcement_date="20241231"
    )
    
    article_without_delegation = Article(
        article_number="002", 
        article_title="일반 조문",
        article_content="이것은 일반적인 조문 내용입니다.",
        enforcement_date="20241231"
    )
    
    # Test detection
    assert article_with_delegation.has_delegated_law_references() == True
    assert article_without_delegation.has_delegated_law_references() == False
    
    # Test type extraction
    types = article_with_delegation.get_delegated_law_types()
    assert "시행령" in types
    
    print("✓ Delegation detection working correctly")


def test_view_delegated_laws_with_container():
    """Test the delegated law viewing feature using real data."""
    print("\nTesting delegated law viewing with real data...")
    
    container = Container()
    
    # Search for 소득세법
    laws = container.search_use_case.search_with_abbreviation("소득세법")
    
    if not laws:
        print("❌ No laws found")
        return
    
    law = laws[0]
    print(f"✓ Found law: {law.name} (MST: {law.mst})")
    
    # Get law content
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    if not law_content:
        print("❌ No law content found")
        return
        
    print(f"✓ Loaded {len(law_content.articles)} articles")
    
    # Find articles with delegated law references
    articles_with_delegation = []
    for article in law_content.articles[:20]:  # Check first 20 articles
        if article.has_delegated_law_references():
            articles_with_delegation.append(article)
    
    print(f"✓ Found {len(articles_with_delegation)} articles with delegated law references")
    
    if articles_with_delegation:
        # Test with first article that has delegation
        test_article = articles_with_delegation[0]
        print(f"\n테스트 조문: {test_article.formatted_number}")
        print(f"제목: {test_article.article_title}")
        print(f"위임 법령 유형: {', '.join(test_article.get_delegated_law_types())}")
        
        # Find delegated laws
        delegated_laws = container.view_delegated_laws_use_case.find_delegated_laws(law.name)
        print(f"\n✓ Found {len(delegated_laws)} delegated laws:")
        for d_law in delegated_laws:
            print(f"  - {d_law.name} ({d_law.law_type})")


def test_interactive_mode():
    """Test interactive mode (optional - requires user input)."""
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        print("\n=== Interactive Test Mode ===")
        container = Container()
        
        # Run the controller with delegated law functionality
        controller = container.cli_controller
        controller.run_interactive_search()


if __name__ == "__main__":
    print("=== Testing Delegated Law Discovery Feature ===\n")
    
    # Run automated tests
    test_article_delegation_detection()
    test_view_delegated_laws_with_container()
    
    # Run interactive test if specified
    test_interactive_mode()
    
    print("\n=== All tests completed ===")