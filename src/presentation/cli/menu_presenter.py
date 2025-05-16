"""Menu presenter for CLI interface."""
from typing import List, Optional
from ...domain.entities.law import Law
from ...domain.entities.article import LawContent, Article


class MenuPresenter:
    """Presenter for menu-based CLI interface."""
    
    COMMON_LAWS = [
        ('1', '소득세법'),
        ('2', '법인세법'),
        ('3', '부가가치세법'),
        ('4', '상속세 및 증여세법'),
        ('5', '민법'),
        ('6', '상법'),
        ('7', '근로기준법')
    ]
    
    @staticmethod
    def show_main_menu():
        """Display main menu."""
        print("\n=== 법령 검색 ===")
        for num, law in MenuPresenter.COMMON_LAWS:
            print(f"{num}. {law}")
        print("8. 직접 입력")
        print("0. 종료")
        print("="*20)
    
    @staticmethod
    def get_user_choice() -> str:
        """Get user choice."""
        return input("\n번호 선택: ").strip()
    
    @staticmethod
    def get_custom_query() -> str:
        """Get custom search query."""
        return input("검색어: ").strip()
    
    @staticmethod
    def display_search_results(laws: List[Law], query: str):
        """Display search results."""
        print(f"\n'{query}' 검색 결과: {len(laws)}개\n")
        
        for i, law in enumerate(laws[:10], 1):
            print(f"{i}. {law.name}")
            print(f"   MST: {law.mst}")
            print(f"   시행일: {law.enforcement_date}\n")
    
    @staticmethod
    def display_law_details(law: Law):
        """Display detailed law information."""
        print(f"\n=== {law.name} ===")
        print(f"법령구분: {law.law_type}")
        print(f"MST: {law.mst}")
        print(f"시행일: {law.enforcement_date}")
        print(f"공포일: {law.promulgation_date}")
        print(f"소관부처: {law.department}")
    
    @staticmethod
    def display_full_text_command(mst: str):
        """Display command to get full text."""
        print(f"\n전문 조회: python main.py full-text {mst}")
    
    @staticmethod
    def display_command_line_options(laws: List[Law]):
        """Display command-line options for laws."""
        print("\n명령어 옵션:")
        for i, law in enumerate(laws, 1):
            print(f"조문 보기: python main.py articles {law.mst}")
            print(f"전문 조회: python main.py full-text {law.mst}")
            if i < len(laws):
                print()
    
    @staticmethod
    def ask_view_articles(law_name: str) -> str:
        """Ask if user wants to view articles."""
        return input(f"\n'{law_name}' 조문을 보시겠습니까? (Y/N): ").strip()
    
    @staticmethod
    def get_law_selection(laws: List[Law]) -> Optional[Law]:
        """Get user selection from multiple laws."""
        print("\n어떤 법령의 조문을 보시겠습니까?")
        for i, law in enumerate(laws, 1):
            print(f"{i}. {law.name}")
        print("0. 뒤로가기")
        
        try:
            choice = int(input("\n번호 선택: ").strip())
            if 1 <= choice <= len(laws):
                return laws[choice - 1]
            return None
        except ValueError:
            return None
    
    @staticmethod
    def display_error(message: str):
        """Display error message."""
        print(f"\n오류: {message}")
    
    @staticmethod
    def display_success(message: str):
        """Display success message."""
        print(f"\n{message}")
    
    @staticmethod
    def get_selected_law_from_menu(choice: str) -> Optional[str]:
        """Get law name from menu choice."""
        for num, law_name in MenuPresenter.COMMON_LAWS:
            if choice == num:
                return law_name
        return None
    
    @staticmethod
    def display_law_content_menu(law_content: LawContent):
        """Display law content with options."""
        print(f"\n=== {law_content.law_name} 조문 보기 ===")
        print(f"시행일: {law_content.enforcement_date}")
        print(f"총 조문 수: {len(law_content.articles)}개")
        print("\n1. 전체 조문 목록 보기")
        print("2. 특정 조문 번호로 검색")
        print("3. 키워드로 조문 검색")
        print("4. 웹사이트 열기")
        print("5. 위임 법령 조문 확인")
        print("0. 뒤로가기")
        print("="*40)
    
    @staticmethod
    def display_article_list(articles: List[Article]):
        """Display list of articles."""
        print("\n=== 조문 목록 ===")
        for i, article in enumerate(articles[:20], 1):  # Show first 20
            # Better handling of titles and chapter headers
            if article.article_title == "Chapter/Section Header":
                # For chapter headers, don't show article number, just the content
                content_preview = article.article_content.strip()[:50]
                display_text = f"[{content_preview}...]"
            elif not article.article_title:
                # If no title, show content preview
                content_preview = article.article_content.strip()[:30]
                # Check if this is a deleted article
                if "삭제" in content_preview:
                    display_text = f"{article.formatted_number} {content_preview}..."
                else:
                    display_text = f"{article.formatted_number} ({content_preview}...)"
            else:
                display_text = f"{article.formatted_number} {article.article_title}"
            
            print(f"{i}. {display_text}")
        
        if len(articles) > 20:
            print(f"\n... 총 {len(articles)}개 조문 중 20개만 표시")
    
    @staticmethod
    def display_article_content(article: Article, from_cache: bool = False, cache_file: str = None):
        """Display full article content."""
        cache_indicator = " (캐시)" if from_cache else ""
        print(f"\n=== {article.formatted_number}{cache_indicator} ===")
        if article.article_title:
            print(f"제목: {article.article_title}")
        print(f"시행일: {article.enforcement_date}")
        print("\n법령 내용:")
        print("-"*50)
        # If content is very short, it might be truncated - show what we have
        content = article.article_content
        if len(content) < 50 and not content.strip().endswith('.'):
            print(f"{content} [내용이 더 있을 수 있습니다]")
        else:
            print(content)
        print("-"*50)
    
    @staticmethod
    def get_article_selection() -> str:
        """Get article selection from user."""
        return input("\n선택: ").strip()
    
    @staticmethod
    def get_article_number() -> str:
        """Get article number from user."""
        return input("\n조문 번호 (예: 1, 10-2): ").strip()
    
    @staticmethod
    def get_search_keyword() -> str:
        """Get search keyword from user."""
        return input("\n검색 키워드: ").strip()
    
    @staticmethod
    def display_delegated_law_menu():
        """Display delegated law search menu."""
        print("\n=== 위임 법령 조문 확인 ===")
        print("1. 조문 번호로 위임 법령 확인")
        print("2. 위임 법령이 있는 조문 목록 보기")
        print("0. 뒤로가기")
        print("="*30)
    
    @staticmethod  
    def display_articles_with_delegated_references(articles: List[Article]):
        """Display articles that have delegated law references."""
        print("\n=== 위임 법령 참조 조문 목록 ===")
        count = 0
        for i, article in enumerate(articles):
            if article.has_delegated_law_references():
                count += 1
                delegated_types = article.get_delegated_law_types()
                types_str = ", ".join(delegated_types)
                print(f"{count}. {article.formatted_number} {article.article_title or '제목 없음'}")
                print(f"   - 위임: {types_str}")
                print(f"   - 조문번호: {article.article_number}")
        
        if count == 0:
            print("위임 법령을 참조하는 조문이 없습니다.")
        else:
            print(f"\n총 {count}개 조문이 위임 법령을 참조합니다.")
    
    @staticmethod
    def display_article_with_delegated_content(result: dict):
        """Display article with delegated law content."""
        primary_article = result['primary_article']
        
        # Display primary article
        print(f"\n=== {primary_article.formatted_number} (주 법령) ===")
        if primary_article.article_title:
            print(f"제목: {primary_article.article_title}")
        print("\n조문 내용:")
        print("-"*50)
        print(primary_article.article_content)
        print("-"*50)
        
        # Display delegated references
        if result['has_delegated_references']:
            print("\n위임 법령 참조:")
            for ref in result['delegated_references']:
                print(f"  - {ref['type']}: \"{ref['context']}\"")
        
        # Display delegated content
        if result['delegated_content']:
            for delegated_item in result['delegated_content']:
                law = delegated_item['law']
                articles = delegated_item['articles']
                
                print(f"\n\n=== {law.name} 관련 조문 ===")
                print(f"법령구분: {law.law_type}")
                print(f"시행일: {law.enforcement_date}")
                
                for article in articles:
                    print(f"\n{article.formatted_number}")
                    if article.article_title:
                        print(f"제목: {article.article_title}")
                    print("내용:")
                    print("-"*30)
                    print(article.article_content)
                    print("-"*30)
        else:
            print("\n관련 위임 법령 조문을 찾지 못했습니다.")