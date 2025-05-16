"""Controller for CLI application."""
import os
from .menu_presenter import MenuPresenter
from ...use_cases.search_law import SearchLawUseCase
from ...use_cases.get_law_full_text import GetLawFullTextUseCase
from ...use_cases.view_law_articles import ViewLawArticlesUseCase
from ...use_cases.view_delegated_laws import ViewDelegatedLawsUseCase
from ...domain.entities.article import Article, LawContent


class CLIController:
    """Controller for command line interface."""
    
    def __init__(self, search_use_case: SearchLawUseCase, 
                 full_text_use_case: GetLawFullTextUseCase,
                 view_articles_use_case: ViewLawArticlesUseCase,
                 view_delegated_laws_use_case: ViewDelegatedLawsUseCase):
        self.search_use_case = search_use_case
        self.full_text_use_case = full_text_use_case
        self.view_articles_use_case = view_articles_use_case
        self.view_delegated_laws_use_case = view_delegated_laws_use_case
        self.presenter = MenuPresenter()
    
    def run_interactive_search(self):
        """Run interactive search mode."""
        while True:
            self.presenter.show_main_menu()
            choice = self.presenter.get_user_choice()
            
            if choice == '0':
                self.presenter.display_success("종료합니다.")
                break
            
            # Get query based on choice
            if choice == '8':
                query = self.presenter.get_custom_query()
                if not query:
                    continue
            else:
                query = self.presenter.get_selected_law_from_menu(choice)
                if not query:
                    self.presenter.display_error("잘못된 선택입니다.")
                    continue
            
            # Search for laws
            # Check if cached data exists (using new filename format)
            cache_file = os.path.join('output', '.cache', f'law-list_{query}_20.json')
            # Also check old filename format for backward compatibility
            old_cache_file = os.path.join('output', '.cache', f'search_{query}_20.json')
            
            print("\n" + "="*50)  # Add separator
            if os.path.exists(cache_file):
                self.presenter.display_success(f"'{query}' 검색 중... (캐시: law-list_{query}_20.json)")
            elif os.path.exists(old_cache_file):
                self.presenter.display_success(f"'{query}' 검색 중... (캐시: search_{query}_20.json)")
            else:
                self.presenter.display_success(f"'{query}' 검색 중...")
            
            laws = self.search_use_case.search_with_abbreviation(query)
            
            if laws:
                self.presenter.display_search_results(laws, query)
                self.presenter.display_success(f"결과 저장: output/{query}_검색결과.json")
                
                # Show command-line options (removed per user request)
                # self.presenter.display_command_line_options(laws)
                
                # If there's only one result, ask if user wants to view articles
                if len(laws) == 1:
                    selected_law = laws[0]
                    response = self.presenter.ask_view_articles(selected_law.name)
                    if response.lower() in ['y', 'yes', '예', '네']:
                        self.view_law_articles(selected_law.mst, selected_law.name)
                else:
                    # Multiple results - let user select which one to view
                    selection = self.presenter.get_law_selection(laws)
                    if selection:
                        self.view_law_articles(selection.mst, selection.name)
            else:
                self.presenter.display_error("검색 결과가 없습니다.")
    
    def run_direct_search(self, query: str):
        """Run direct search mode."""
        self.presenter.display_success(f"'{query}' 검색 중...")
        laws = self.search_use_case.search_with_abbreviation(query)
        
        if laws:
            self.presenter.display_search_results(laws, query)
            self.presenter.display_success(f"결과 저장: output/{query}_검색결과.json")
            
            # Command line option removed per user request
            # if laws:
            #     self.presenter.display_full_text_command(laws[0].mst)
        else:
            self.presenter.display_error("검색 결과가 없습니다.")
    
    def get_full_text(self, mst: str):
        """Get full text of a law."""
        self.presenter.display_success(f"MST {mst} 법령 전문 조회 중...")
        law_data = self.full_text_use_case.execute(mst)
        
        if law_data:
            law_name = "법령"
            if 'law' in law_data:
                law_info = law_data['law'][0] if isinstance(law_data['law'], list) else law_data['law']
                law_name = law_info.get('법령명한글', '법령')
            
            self.presenter.display_success(f"전문이 output/{law_name}_전문.json에 저장되었습니다.")
        else:
            self.presenter.display_error("법령 전문을 가져올 수 없습니다.")
    
    def view_law_articles(self, mst: str, law_name: str):
        """View law articles interactively."""
        # Check if cached data exists (using new filename format)
        cache_file = os.path.join('output', '.cache', f'article-list_{mst}.json')
        # Also check old filename format for backward compatibility
        old_cache_file = os.path.join('output', '.cache', f'law_content_{mst}.json')
        
        print("\n" + "="*50)  # Add separator
        used_cache_file = None
        if os.path.exists(cache_file):
            self.presenter.display_success(f"'{law_name}' 조문 정보 가져오는 중... (캐시: article-list_{mst}.json)")
            used_cache_file = cache_file
        elif os.path.exists(old_cache_file):
            self.presenter.display_success(f"'{law_name}' 조문 정보 가져오는 중... (캐시: law_content_{mst}.json)")
            used_cache_file = old_cache_file
        else:
            self.presenter.display_success(f"'{law_name}' 조문 정보 가져오는 중...")
        
        law_content = self.view_articles_use_case.get_law_content(mst)
        
        if not law_content:
            self.presenter.display_error("법령 내용을 가져올 수 없습니다.")
            return
        
        while True:
            self.presenter.display_law_content_menu(law_content)
            choice = self.presenter.get_article_selection()
            
            if choice == '0':
                break
            elif choice == '1':
                # Show article list
                self.presenter.display_article_list(law_content.articles)
                # Note: Article list display doesn't show individual cache status
            elif choice == '2':
                # Search by article number
                article_num = self.presenter.get_article_number()
                # Search in the already loaded articles, excluding chapter headers
                matching_articles = [
                    a for a in law_content.articles 
                    if a.article_number == article_num 
                    and a.article_title != "Chapter/Section Header"
                ]
                
                if len(matching_articles) == 1:
                    # Single match, show it directly
                    self.presenter.display_article_content(matching_articles[0], law_content.from_cache, used_cache_file)
                    # Ask if user wants to see delegated laws
                    self._prompt_for_delegated_laws(matching_articles[0], mst, law_content)
                elif len(matching_articles) > 1:
                    # Multiple matches, show selection menu
                    self.presenter.display_success(f"제{article_num}조에 해당하는 조문이 {len(matching_articles)}개 있습니다.")
                    self.presenter.display_article_list(matching_articles)
                    
                    # Let user select which one to view
                    selection = self.presenter.get_user_choice()
                    try:
                        index = int(selection) - 1
                        if 0 <= index < len(matching_articles):
                            self.presenter.display_article_content(matching_articles[index], law_content.from_cache, used_cache_file)
                            # Ask if user wants to see delegated laws
                            self._prompt_for_delegated_laws(matching_articles[index], mst, law_content)
                        else:
                            self.presenter.display_error("잘못된 선택입니다.")
                    except ValueError:
                        self.presenter.display_error("숫자를 입력해주세요.")
                else:
                    self.presenter.display_error(f"조문 {article_num}을(를) 찾을 수 없습니다.")
            elif choice == '3':
                # Search by keyword
                keyword = self.presenter.get_search_keyword()
                results = self.view_articles_use_case.search_articles(law_content, keyword)
                if results:
                    self.presenter.display_article_list(results)
                    # Save search results
                    success = self.view_articles_use_case.save_article_search_results(
                        results, law_content.law_name, keyword
                    )
                    if success:
                        filename = f"{law_content.law_name}_조문검색_{keyword}"
                        self.presenter.display_success(f"\n검색 결과 저장: output/{filename}_*.json")
                else:
                    self.presenter.display_error(f"'{keyword}'에 대한 검색 결과가 없습니다.")
            elif choice == '4':
                # Open website
                url = self._generate_law_url(law_content.law_name)
                self.presenter.display_success(f"법령 웹사이트 열기: {url}")
                try:
                    import webbrowser
                    webbrowser.open(url)
                    self.presenter.display_success("웹사이트가 브라우저에서 열렸습니다.")
                except Exception as e:
                    self.presenter.display_error(f"웹사이트를 열 수 없습니다: {e}")
            elif choice == '5':
                # View delegated law articles
                self.view_delegated_law_articles(mst, law_content)
            else:
                self.presenter.display_error("잘못된 선택입니다.")
    
    def view_delegated_law_articles(self, mst: str, law_content: LawContent):
        """View delegated law articles related to the primary law."""
        while True:
            self.presenter.display_delegated_law_menu()
            choice = self.presenter.get_user_choice()
            
            if choice == '0':
                break
            elif choice == '1':
                # View specific article with delegated content
                article_num = self.presenter.get_article_number()
                
                # Get article with delegated content
                result = self.view_delegated_laws_use_case.get_delegated_laws_for_article(
                    mst, article_num, law_content
                )
                
                if result and result.get('primary_article'):
                    self.presenter.display_article_with_delegated_content(result)
                else:
                    self.presenter.display_error(f"조문 {article_num}을(를) 찾을 수 없습니다.")
            elif choice == '2':
                # List all articles with delegated law references
                articles_with_delegated = [
                    article for article in law_content.articles 
                    if article.has_delegated_law_references()
                ]
                
                if articles_with_delegated:
                    self.presenter.display_articles_with_delegated_references(law_content.articles)
                    
                    # Let user select an article to view
                    try:
                        selection = input("\n조문 번호를 선택하세요 (0: 뒤로가기): ").strip()
                        if selection != '0':
                            article_num = selection
                            result = self.view_delegated_laws_use_case.get_delegated_laws_for_article(
                                mst, article_num, law_content
                            )
                            if result and result.get('primary_article'):
                                self.presenter.display_article_with_delegated_content(result)
                            else:
                                self.presenter.display_error(f"조문을 찾을 수 없습니다.")
                    except Exception:
                        pass
                else:
                    self.presenter.display_error("위임 법령을 참조하는 조문이 없습니다.")
            else:
                self.presenter.display_error("잘못된 선택입니다.")
    
    def _prompt_for_delegated_laws(self, article, mst: str, law_content):
        """Prompt user to view delegated laws for the article."""
        if article.has_delegated_law_references():
            print("\n이 조문은 위임 법령을 참조하고 있습니다.")
            choice = input("위임 법령 내용을 보시겠습니까? (y/N): ").strip().lower()
            
            if choice == 'y':
                result = self.view_delegated_laws_use_case.get_delegated_laws_for_article(
                    mst, article.article_number, law_content
                )
                
                if result and result.get('delegated_content'):
                    self.presenter.display_article_with_delegated_content(result)
                else:
                    self.presenter.display_error("위임 법령 내용을 찾을 수 없습니다.")
    
    def _generate_law_url(self, law_name: str) -> str:
        """Generate law.go.kr URL from law name."""
        from urllib.parse import quote
        
        # Remove spaces for compound law names
        clean_name = law_name.replace(" ", "")
        
        # Use the pre-encoded path for '법령' to avoid encoding issues
        encoded_path = "%EB%B2%95%EB%A0%B9"  # This is '법령' encoded
        encoded_name = quote(clean_name)
        
        return f"https://www.law.go.kr/{encoded_path}/{encoded_name}"