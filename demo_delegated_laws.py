#!/usr/bin/env python3
"""Demonstration of delegated law discovery feature."""

from src.infrastructure.container import Container
from src.domain.entities.article import Article


def demo_delegated_law_discovery():
    """Demonstrate the delegated law discovery feature."""
    container = Container()
    
    print("=== 위임 법령 조회 기능 데모 ===\n")
    
    # 1. Search for 소득세법
    print("1. 소득세법 검색...")
    laws = container.search_use_case.search_with_abbreviation("소득세법")
    
    if not laws:
        print("법령을 찾을 수 없습니다.")
        return
    
    law = laws[0]
    print(f"✓ {law.name} 찾음 (MST: {law.mst})")
    
    # 2. Get law content
    print("\n2. 법령 조문 가져오기...")
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    
    if not law_content:
        print("조문을 가져올 수 없습니다.")
        return
    
    print(f"✓ {len(law_content.articles)}개 조문 로드됨")
    
    # 3. Find articles with delegated law references
    print("\n3. 위임 법령을 참조하는 조문 찾기...")
    delegated_articles = []
    
    for article in law_content.articles[:50]:  # Check first 50 articles
        if article.has_delegated_law_references():
            delegated_articles.append(article)
    
    print(f"✓ {len(delegated_articles)}개 조문이 위임 법령을 참조함")
    
    # 4. Show examples
    if delegated_articles:
        print("\n4. 위임 법령 참조 예시:")
        for i, article in enumerate(delegated_articles[:3]):  # Show first 3
            print(f"\n[{i+1}] {article.formatted_number} - {article.article_title or '제목 없음'}")
            references = article.get_delegated_law_references()
            for ref in references:
                print(f"   위임 유형: {ref['type']}")
                print(f"   컨텍스트: \"{ref['context']}\"")
        
        # 5. Find delegated laws
        print("\n5. 관련 위임 법령 찾기...")
        delegated_laws = container.view_delegated_laws_use_case.find_delegated_laws(law.name)
        
        if delegated_laws:
            print(f"✓ {len(delegated_laws)}개 위임 법령 찾음:")
            for d_law in delegated_laws:
                print(f"   - {d_law.name} ({d_law.law_type}, MST: {d_law.mst})")
            
            # 6. Show related articles from delegated law
            if delegated_articles and delegated_laws:
                print("\n6. 위임 법령의 관련 조문 예시:")
                test_article = delegated_articles[0]
                delegated_law = delegated_laws[0]
                
                print(f"\n주 법령 조문: {test_article.formatted_number}")
                print(f"위임 법령: {delegated_law.name}")
                
                # Extract keywords from article
                context_keywords = []
                content_words = test_article.article_content.split()
                for word in content_words:
                    if len(word) > 2 and word not in ['대통령령으로', '정하는', '정한다']:
                        context_keywords.append(word)
                
                related_articles = container.view_delegated_laws_use_case.find_related_articles(
                    test_article,
                    delegated_law.mst,
                    context_keywords[:3]
                )
                
                if related_articles:
                    print(f"✓ {len(related_articles)}개 관련 조문 찾음:")
                    for r_article in related_articles[:2]:
                        print(f"   - {r_article.formatted_number}: {r_article.article_title or '제목 없음'}")
                else:
                    print("관련 조문을 찾지 못했습니다.")


def demo_specific_article():
    """Demo viewing a specific article with its delegated content."""
    container = Container()
    
    print("\n\n=== 특정 조문과 위임 법령 내용 보기 ===\n")
    
    # Get 소득세법
    laws = container.search_use_case.search_with_abbreviation("소득세법")
    if not laws:
        return
    
    law = laws[0]
    
    # Get first article with delegation
    law_content = container.view_articles_use_case.get_law_content(law.mst)
    if not law_content:
        return
    
    # Find an article with delegation
    for article in law_content.articles[:50]:
        if article.has_delegated_law_references():
            print(f"조문 번호 {article.article_number}의 위임 법령 내용 조회...")
            
            result = container.view_delegated_laws_use_case.get_article_with_delegated_content(
                law.mst,
                article.article_number
            )
            
            if result and result['primary_article']:
                primary = result['primary_article']
                print(f"\n주 법령 조문: {primary.formatted_number}")
                print(f"제목: {primary.article_title}")
                print(f"위임 법령 참조: {result['has_delegated_references']}")
                
                if result['delegated_content']:
                    print("\n관련 위임 법령 조문:")
                    for item in result['delegated_content']:
                        d_law = item['law']
                        d_articles = item['articles']
                        print(f"\n{d_law.name} ({d_law.law_type}):")
                        for d_article in d_articles[:2]:
                            print(f"  - {d_article.formatted_number}: {d_article.article_title or '제목 없음'}")
                
                break


if __name__ == "__main__":
    demo_delegated_law_discovery()
    demo_specific_article()
    
    print("\n\n=== 데모 완료 ===")
    print("실제 사용하려면: python main.py")
    print("법령 조문을 보고 메뉴에서 '5. 위임 법령 조문 확인'을 선택하세요.")