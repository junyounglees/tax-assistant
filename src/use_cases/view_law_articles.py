"""Use case for viewing law articles."""
from typing import Optional
from ..domain.interfaces.law_repository import LawRepositoryInterface
from ..domain.entities.article import LawContent, Article


class ViewLawArticlesUseCase:
    """Use case for viewing law articles."""
    
    def __init__(self, repository: LawRepositoryInterface):
        self.repository = repository
    
    def get_law_content(self, mst: str) -> Optional[LawContent]:
        """Get complete law content with all articles."""
        return self.repository.get_law_content(mst)
    
    def get_specific_article(self, mst: str, article_number: str) -> Optional[Article]:
        """Get a specific article by number."""
        return self.repository.get_law_article(mst, article_number)
    
    def search_articles(self, law_content: LawContent, search_term: str) -> list[Article]:
        """Search articles by keyword."""
        results = []
        search_term_lower = search_term.lower()
        
        for article in law_content.articles:
            if (search_term_lower in article.article_content.lower() or 
                (article.article_title and search_term_lower in article.article_title.lower())):
                results.append(article)
        
        return results
    
    def save_article_search_results(self, articles: list[Article], law_name: str, search_term: str) -> bool:
        """Save article search results."""
        return self.repository.save_article_search_results(articles, law_name, search_term)