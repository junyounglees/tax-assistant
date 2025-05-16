"""Use case for viewing delegated laws."""
from typing import Dict, List, Optional
from ..domain.interfaces.delegated_law_repository import DelegatedLawRepository
from ..domain.interfaces.law_repository import LawRepositoryInterface
from ..domain.entities.article import Article, LawContent
from ..domain.entities.delegated_law import DelegatedLawResponse, DelegatedLawItem


class ViewDelegatedLawsUseCase:
    """Use case for viewing delegated laws."""
    
    def __init__(self, delegated_law_repository: DelegatedLawRepository, 
                 law_repository: LawRepositoryInterface):
        self.delegated_law_repository = delegated_law_repository
        self.law_repository = law_repository
    
    def _normalize_article_number(self, article_number: str) -> str:
        """Normalize article number to match between different formats.
        
        Handles conversions like:
        - '1' -> '1'
        - '1_2' -> '1_2' 
        - '0001' -> '1'
        - '0001_2' -> '1_2'
        """
        # Remove leading zeros
        parts = article_number.split('_')
        normalized_parts = []
        for part in parts:
            try:
                # Convert to int to remove leading zeros, then back to string
                normalized_parts.append(str(int(part)))
            except ValueError:
                # Keep as is if not a number
                normalized_parts.append(part)
        
        return '_'.join(normalized_parts)
    
    def get_delegated_laws_for_article(self, mst: str, article_number: str, law_content: LawContent) -> Dict:
        """Get delegated laws for a specific article.
        
        Args:
            mst: Law master number
            article_number: Article number to check
            law_content: Full law content with articles
            
        Returns:
            Dictionary containing:
            - primary_article: The main article
            - has_delegated_references: Boolean indicating if article has delegated law references
            - delegated_references: List of references in the article
            - delegated_content: List of delegated law content if found
        """
        # Find the article in law_content
        primary_article = None
        
        # First, try to find by formatted number if the article_number looks like one
        if article_number.startswith('제') and '조' in article_number:
            # This is a formatted number like "제1조의2"
            for article in law_content.articles:
                if article.formatted_number == article_number:
                    primary_article = article
                    break
        
        # If not found, normalize the requested number
        if not primary_article:
            normalized_requested = self._normalize_article_number(article_number)
            
            # Try to find by normalized number
            for article in law_content.articles:
                article_normalized = article.normalized_number
                if article_normalized == normalized_requested:
                    primary_article = article
                    break
        
        # Last resort: raw article_number match
        if not primary_article:
            for article in law_content.articles:
                if article.article_number == article_number:
                    primary_article = article
                    break
        
        if not primary_article:
            return {
                'primary_article': None,
                'has_delegated_references': False,
                'delegated_references': [],
                'delegated_content': []
            }
        
        # Check if article has delegated law references
        has_references = primary_article.has_delegated_law_references()
        references = primary_article.get_delegated_law_references()
        
        result = {
            'primary_article': primary_article,
            'has_delegated_references': has_references,
            'delegated_references': references,
            'delegated_content': []
        }
        
        if not has_references:
            return result
        
        # Get delegated laws from repository
        delegated_response = self.delegated_law_repository.get_delegated_laws(mst)
        
        if not delegated_response or not delegated_response.has_delegated_laws:
            return result
        
        # Find relevant delegated laws for this article
        # Use the article's normalized number for comparison
        normalized_article_num = primary_article.normalized_number
        
        relevant_items = []
        for item in delegated_response.all_delegated_items:
            # Normalize the item's article number for comparison
            item_normalized = self._normalize_article_number(item.article_number)
            if item_normalized == normalized_article_num:
                relevant_items.append(item)
        
        # Fetch content for each delegated law
        for item in relevant_items:
            delegated_content = self._fetch_delegated_law_content(item)
            if delegated_content:
                result['delegated_content'].append(delegated_content)
        
        return result
    
    def get_articles_with_delegated_references(self, law_content: LawContent) -> List[Article]:
        """Get all articles that have delegated law references.
        
        Args:
            law_content: Full law content
            
        Returns:
            List of articles that reference delegated laws
        """
        articles_with_refs = []
        
        for article in law_content.articles:
            if article.has_delegated_law_references():
                articles_with_refs.append(article)
        
        return articles_with_refs
    
    def _fetch_delegated_law_content(self, item: DelegatedLawItem) -> Optional[Dict]:
        """Fetch the actual content of a delegated law.
        
        Args:
            item: Delegated law item
            
        Returns:
            Dictionary with law info and relevant articles
        """
        # Search for the delegated law
        search_results = self.law_repository.search_laws(item.delegated_title)
        
        if not search_results:
            return None
        
        # Find the exact match by MST if available
        matching_law = None
        for law in search_results:
            if law.mst == item.delegated_mst:
                matching_law = law
                break
        
        # If no exact match, use the first result
        if not matching_law and search_results:
            matching_law = search_results[0]
        
        if not matching_law:
            return None
        
        # Get full content of the delegated law
        law_content = self.law_repository.get_law_content(matching_law.mst)
        
        if not law_content:
            return None
        
        # Find relevant articles based on the reference
        relevant_articles = []
        
        if item.delegated_article_number:
            # Find specific article mentioned in the reference
            article_num = item.delegated_article_number.replace("제", "").replace("조", "")
            for article in law_content.articles:
                if article.article_number.startswith(article_num):
                    relevant_articles.append(article)
        else:
            # If no specific article, include first few relevant articles
            relevant_articles = law_content.articles[:5]
        
        return {
            'law': matching_law,
            'articles': relevant_articles
        }