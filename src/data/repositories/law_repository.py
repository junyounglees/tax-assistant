"""Implementation of the law repository interface."""
import json
import os
from typing import List, Optional
from ...domain.interfaces.law_repository import LawRepositoryInterface
from ...domain.entities.law import Law
from ...domain.entities.article import LawContent, Article
from ..api.law_api_client import LawAPIClient
from datetime import datetime


class LawRepository(LawRepositoryInterface):
    """Repository for law data access using the API."""
    
    def __init__(self, api_client: LawAPIClient, output_dir: str = 'output', cache_hours: int = 168):
        self.api_client = api_client
        self.output_dir = output_dir
        self.cache_dir = os.path.join(output_dir, '.cache')
        self.cache_hours = cache_hours  # Cache validity in hours
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def _get_cache_filename(self, cache_key: str, cache_type: str) -> str:
        """Generate cache filename with descriptive names."""
        # More descriptive cache filenames
        if cache_type == "search":
            filename = f"law-list_{cache_key}.json"
        elif cache_type == "law_content":
            filename = f"article-list_{cache_key}.json"
        elif cache_type == "full_text":
            filename = f"full-text_{cache_key}.json"
        else:
            filename = f"{cache_type}_{cache_key}.json"
        
        return os.path.join(self.cache_dir, filename)
    
    def _load_from_cache(self, cache_key: str, cache_type: str) -> Optional[dict]:
        """Load data from cache if exists."""
        cache_file = self._get_cache_filename(cache_key, cache_type)
        if os.path.exists(cache_file):
            try:
                # Check if cache is recent (default: 7 days)
                mtime = os.path.getmtime(cache_file)
                cache_age_hours = (datetime.now().timestamp() - mtime) / 3600
                if cache_age_hours < self.cache_hours:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
            except Exception:
                pass
        return None
    
    def _save_to_cache(self, data: dict, cache_key: str, cache_type: str) -> None:
        """Save data to cache."""
        cache_file = self._get_cache_filename(cache_key, cache_type)
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def clear_old_cache(self) -> int:
        """Clear cache files older than cache_hours."""
        cleared_count = 0
        try:
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    mtime = os.path.getmtime(filepath)
                    cache_age_hours = (datetime.now().timestamp() - mtime) / 3600
                    if cache_age_hours > self.cache_hours:
                        os.remove(filepath)
                        cleared_count += 1
        except Exception:
            pass
        return cleared_count
    
    def search_laws(self, query: str, display: int = 20) -> List[Law]:
        """Search for laws by query."""
        # Check cache first
        cache_key = f"{query}_{display}"
        cached_data = self._load_from_cache(cache_key, "search")
        
        if cached_data:
            # Return cached results
            if 'LawSearch' in cached_data and 'law' in cached_data['LawSearch']:
                laws_data = cached_data['LawSearch']['law']
                if isinstance(laws_data, dict):
                    laws_data = [laws_data]
                return [Law.from_api_response(data) for data in laws_data]
            return []
        
        # Cache miss, fetch from API
        response = self.api_client.search(query, display)
        
        if 'error' in response:
            return []
        
        # Save to cache
        self._save_to_cache(response, cache_key, "search")
        
        if 'LawSearch' in response and 'law' in response['LawSearch']:
            laws_data = response['LawSearch']['law']
            
            # Handle single result case
            if isinstance(laws_data, dict):
                laws_data = [laws_data]
            
            return [Law.from_api_response(data) for data in laws_data]
        
        return []
    
    def get_law_full_text(self, mst: str) -> Optional[dict]:
        """Get full text of a law by MST."""
        # Check cache first
        cache_key = f"full_{mst}"
        cached_data = self._load_from_cache(cache_key, "full_text")
        
        if cached_data:
            return cached_data
        
        # Cache miss, fetch from API
        response = self.api_client.get_full_text(mst)
        
        if 'error' in response:
            return None
        
        # Save to cache
        self._save_to_cache(response, cache_key, "full_text")
        
        return response
    
    def save_search_results(self, laws: List[Law], filename: str) -> bool:
        """Save search results to file."""
        try:
            filepath = os.path.join(self.output_dir, filename)
            laws_data = [law.to_dict() for law in laws]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(laws_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def save_law_full_text(self, law_data: dict, filename: str) -> bool:
        """Save law full text to file."""
        try:
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(law_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False
    
    def get_law_content(self, mst: str) -> Optional[LawContent]:
        """Get law content with articles."""
        # Check cache first
        cache_key = mst
        cached_data = self._load_from_cache(cache_key, "law_content")
        
        if cached_data:
            try:
                law_content = LawContent.from_api_response(cached_data)
                if law_content:
                    law_content.from_cache = True  # Mark as from cache
                return law_content
            except Exception:
                pass
        
        # Cache miss, fetch from API
        response = self.api_client.get_full_text(mst)
        
        if 'error' in response:
            return None
        
        # Save to cache
        self._save_to_cache(response, cache_key, "law_content")
        
        try:
            law_content = LawContent.from_api_response(response)
            if law_content:
                law_content.from_cache = False  # Mark as from API
            return law_content
        except Exception:
            return None
    
    def get_law_article(self, mst: str, article_number: str) -> Optional[Article]:
        """Get specific article of a law."""
        # Convert article number to 6-digit format
        # e.g., "1" -> "000100", "10-2" -> "001002"
        jo_number = self._format_article_number(article_number)
        
        response = self.api_client.get_full_text(mst, jo=jo_number)
        
        if 'error' in response:
            return None
        
        try:
            # Try different response structures
            if '조문' in response:
                article_data = response['조문']
            elif 'law' in response and isinstance(response['law'], dict) and '조문' in response['law']:
                article_data = response['law']['조문']
            else:
                # Look for article data in the response
                return None
            
            if isinstance(article_data, list) and article_data:
                article_data = article_data[0]
            
            return Article.from_api_response(article_data)
        except Exception:
            return None
    
    def _format_article_number(self, article_number: str) -> str:
        """Format article number to 6-digit format."""
        # Simple implementation - can be enhanced
        try:
            if '-' in article_number:
                main, sub = article_number.split('-')
                return f"{int(main):04d}{int(sub):02d}"
            else:
                return f"{int(article_number):04d}00"
        except:
            return "000100"  # Default to Article 1
    
    def save_article_search_results(self, articles: List[Article], law_name: str, search_term: str) -> bool:
        """Save article search results to file."""
        try:
            # Create output directory if it doesn't exist
            os.makedirs('output', exist_ok=True)
            
            # Generate filename based on law name and search term
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{law_name}_조문검색_{search_term}_{timestamp}.json"
            filepath = os.path.join('output', filename)
            
            # Convert articles to dictionary format
            article_data = []
            for article in articles:
                article_dict = {
                    'article_number': article.article_number,
                    'formatted_number': article.formatted_number,
                    'article_title': article.article_title,
                    'article_content': article.article_content,
                    'enforcement_date': article.enforcement_date
                }
                article_data.append(article_dict)
            
            # Create result structure
            result = {
                'law_name': law_name,
                'search_term': search_term,
                'search_time': datetime.now().isoformat(),
                'total_results': len(articles),
                'articles': article_data
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception:
            return False