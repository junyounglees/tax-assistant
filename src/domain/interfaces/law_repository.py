"""Repository interface for law data access."""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.law import Law
from ..entities.article import LawContent, Article


class LawRepositoryInterface(ABC):
    """Interface for law data repository."""
    
    @abstractmethod
    def search_laws(self, query: str, display: int = 20) -> List[Law]:
        """Search for laws by query."""
        pass
    
    @abstractmethod
    def get_law_full_text(self, mst: str) -> Optional[dict]:
        """Get full text of a law by MST."""
        pass
    
    @abstractmethod
    def get_law_content(self, mst: str) -> Optional[LawContent]:
        """Get law content with articles."""
        pass
    
    @abstractmethod
    def get_law_article(self, mst: str, article_number: str) -> Optional[Article]:
        """Get specific article of a law."""
        pass
    
    @abstractmethod
    def save_search_results(self, laws: List[Law], filename: str) -> bool:
        """Save search results to file."""
        pass
    
    @abstractmethod
    def save_law_full_text(self, law_data: dict, filename: str) -> bool:
        """Save law full text to file."""
        pass
    
    @abstractmethod
    def save_article_search_results(self, articles: List[Article], law_name: str, search_term: str) -> bool:
        """Save article search results to file."""
        pass