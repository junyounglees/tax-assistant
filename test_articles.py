#!/usr/bin/env python3
"""Test script for article viewing functionality."""
from src.infrastructure.container import Container


def test_article_viewing():
    """Test the article viewing functionality."""
    container = Container()
    
    # Get the use case
    view_articles = container.view_articles_use_case
    
    # Test with Income Tax Law MST
    mst = "267581"
    print(f"Testing with MST: {mst} (소득세법)")
    
    # Get law content
    law_content = view_articles.get_law_content(mst)
    
    if law_content:
        print(f"\n법령명: {law_content.law_name}")
        print(f"시행일: {law_content.enforcement_date}")
        print(f"총 조문 수: {len(law_content.articles)}")
        
        # Display first 5 articles
        print("\n처음 5개 조문:")
        for i, article in enumerate(law_content.articles[:5], 1):
            print(f"\n{i}. {article.formatted_number}")
            if article.article_title:
                print(f"   제목: {article.article_title}")
            print(f"   내용: {article.article_content[:100]}...")
        
        # Test specific article retrieval
        print("\n\n특정 조문 조회 테스트 (제1조):")
        article_1 = view_articles.get_specific_article(mst, "1")
        if article_1:
            print(f"조문: {article_1.formatted_number}")
            print(f"제목: {article_1.article_title}")
            print(f"내용:\n{article_1.article_content[:200]}...")
        
        # Test keyword search
        print("\n\n키워드 검색 테스트 ('과세'):")
        results = view_articles.search_articles(law_content, "과세")
        print(f"검색 결과: {len(results)}개")
        for i, article in enumerate(results[:3], 1):
            print(f"{i}. {article.formatted_number} - {article.article_title or '제목 없음'}")
    else:
        print("법령 내용을 가져올 수 없습니다.")


if __name__ == "__main__":
    test_article_viewing()