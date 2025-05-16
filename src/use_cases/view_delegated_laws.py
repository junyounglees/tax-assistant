"""Use case for viewing delegated law articles."""
from typing import Optional, List, Dict
from ..domain.interfaces.law_repository import LawRepositoryInterface
from ..domain.entities.article import LawContent, Article
from ..domain.entities.law import Law


class ViewDelegatedLawsUseCase:
    """Use case for discovering and viewing delegated law articles."""
    
    def __init__(self, repository: LawRepositoryInterface):
        self.repository = repository
    
    def find_delegated_laws(self, primary_law_name: str) -> List[Law]:
        """Find delegated laws (시행령, 시행규칙) for a primary law."""
        
        # Map primary law names to corresponding delegated law names
        delegated_patterns = {
            '시행령': [f'{primary_law_name} 시행령', f'{primary_law_name}시행령'],
            '시행규칙': [f'{primary_law_name} 시행규칙', f'{primary_law_name}시행규칙']
        }
        
        delegated_laws = []
        
        # Search for each type of delegated law
        for law_type, patterns in delegated_patterns.items():
            for pattern in patterns:
                # Use existing search functionality to find delegated laws
                results = self.repository.search_laws(pattern, display=10)
                if results:
                    # Filter to ensure we get the correct delegated law
                    for law in results:
                        if law.law_type in ['대통령령', '기획재정부령', '부령']:
                            delegated_laws.append(law)
                            break  # Found one, move to next type
                    break  # Found one pattern match, don't try alternative patterns
        
        return delegated_laws
    
    def find_related_articles(self, primary_article: Article, delegated_law_mst: str, context_keywords: List[str] = None) -> List[Article]:
        """Find articles in delegated law that relate to a primary law article."""
        
        # Get the full content of the delegated law
        delegated_law_content = self.repository.get_law_content(delegated_law_mst)
        if not delegated_law_content:
            return []
        
        related_articles = []
        
        # First, try to find articles with the same number
        if primary_article.article_number:
            for article in delegated_law_content.articles:
                if article.article_number == primary_article.article_number:
                    related_articles.append(article)
        
        # If no direct number match, search by context keywords
        if not related_articles and context_keywords:
            for article in delegated_law_content.articles:
                content_lower = article.article_content.lower()
                for keyword in context_keywords:
                    if keyword.lower() in content_lower:
                        related_articles.append(article)
                        break  # Found keyword match, add article once
        
        # If still no matches, search for title similarities
        if not related_articles and primary_article.article_title:
            title_words = primary_article.article_title.split()
            for article in delegated_law_content.articles:
                if article.article_title:
                    for word in title_words:
                        if len(word) > 2 and word in article.article_title:
                            related_articles.append(article)
                            break
        
        return related_articles
    
    def get_article_with_delegated_content(self, primary_law_mst: str, article_number: str) -> Dict:
        """Get an article along with its related delegated law content."""
        
        # Get the primary article
        primary_article = self.repository.get_law_article(primary_law_mst, article_number)
        if not primary_article:
            return {}
        
        result = {
            'primary_article': primary_article,
            'has_delegated_references': primary_article.has_delegated_law_references(),
            'delegated_law_types': primary_article.get_delegated_law_types(),
            'delegated_references': primary_article.get_delegated_law_references(),
            'delegated_content': []
        }
        
        # If article has delegated law references, find related content
        if result['has_delegated_references']:
            # First get the primary law content to get its name
            primary_law_content = self.repository.get_law_content(primary_law_mst)
            if primary_law_content:
                primary_law_name = primary_law_content.law_name.replace('법', '').strip()
                
                # Find delegated laws
                delegated_laws = self.find_delegated_laws(primary_law_name + '법')
                
                # Extract context keywords from the references
                context_keywords = []
                for ref in result['delegated_references']:
                    # Extract meaningful words from context
                    words = ref['context'].split()
                    for word in words:
                        if len(word) > 2 and word not in ['대통령령으로', '정하는', '정한다', '따라', '의한']:
                            context_keywords.append(word)
                
                # Search for related articles in each delegated law
                for delegated_law in delegated_laws:
                    related_articles = self.find_related_articles(
                        primary_article, 
                        delegated_law.mst, 
                        context_keywords[:5]  # Limit keywords to avoid over-matching
                    )
                    
                    if related_articles:
                        result['delegated_content'].append({
                            'law': delegated_law,
                            'articles': related_articles
                        })
        
        return result