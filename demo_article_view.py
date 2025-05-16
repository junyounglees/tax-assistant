#!/usr/bin/env python3
"""Demonstrate the article viewing functionality."""
from src.infrastructure.container import Container

def demo_article_view():
    """Demonstrate the complete flow of law article viewing."""
    container = Container()
    controller = container.cli_controller
    
    print("=== 한국 법령 검색 시스템 데모 ===\n")
    
    # Step 1: Search for a law
    print("1. 법령 검색: '소득세법'")
    laws = controller.search_use_case.execute('소득세법', display=1)
    
    if laws:
        selected_law = laws[0]
        print(f"   → 검색 결과: {selected_law.name} (MST: {selected_law.mst})")
        
        # Step 2: Get law content
        print("\n2. 법령 본문 조회")
        law_content = controller.view_articles_use_case.get_law_content(selected_law.mst)
        
        if law_content:
            print(f"   → 총 {len(law_content.articles)}개 조문 발견")
            
            # Show articles with complex content
            print("\n3. 특수 형식을 가진 조문 예시 (표/차트 포함):")
            complex_articles = []
            for article in law_content.articles:
                if '\n' in article.article_content and len(article.article_content) > 200:
                    complex_articles.append(article)
            
            if complex_articles:
                example = complex_articles[0]
                print(f"   → {example.formatted_number} {example.article_title}")
                print(f"   내용 미리보기:")
                lines = example.article_content.split('\n')
                for line in lines[:5]:
                    print(f"     {line}")
                print("     ...")
            
            # Show search functionality
            print("\n4. 키워드 검색 기능")
            keyword = '세율'
            results = controller.view_articles_use_case.search_articles(law_content, keyword)
            print(f"   → '{keyword}' 검색 결과: {len(results)}개 조문")
            
            if results:
                for i, article in enumerate(results[:3]):
                    print(f"     {i+1}. {article.formatted_number} {article.article_title or '제목 없음'}")
            
            # Show by article number
            print("\n5. 특정 조문 번호로 검색")
            article_no = '81'
            matching = [a for a in law_content.articles if a.article_number == article_no]
            print(f"   → 제{article_no}조 검색 결과: {len(matching)}개")
            
            if matching:
                for article in matching:
                    print(f"     - {article.formatted_number} {article.article_title}")
    
    print("\n=== 데모 종료 ===")


if __name__ == "__main__":
    demo_article_view()