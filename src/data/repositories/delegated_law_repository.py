"""Implementation of delegated law repository."""
import json
import os
from datetime import datetime, timedelta
from typing import Optional
from pathlib import Path

from ...domain.interfaces.delegated_law_repository import DelegatedLawRepository
from ...domain.entities.delegated_law import DelegatedLawResponse
from ..api.law_api_client import LawAPIClient


class DelegatedLawRepositoryImpl(DelegatedLawRepository):
    """Implementation of delegated law repository with API and caching."""
    
    def __init__(self, api_client: LawAPIClient, cache_dir: str = '.cache/delegated_laws', cache_ttl_days: int = 7):
        self.api_client = api_client
        self.cache_dir = Path(cache_dir)
        self.cache_ttl = timedelta(days=cache_ttl_days)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_delegated_laws(self, mst: str) -> Optional[DelegatedLawResponse]:
        """Get delegated laws for a given law MST."""
        # Check cache first
        cached_response = self.get_delegated_laws_from_cache(mst)
        if cached_response is not None:
            return cached_response
        
        # Make API call
        result = self.api_client.get_delegated_laws(mst)
        
        if 'error' not in result:
            response = DelegatedLawResponse.from_api_response(result)
            # Save to cache
            self.save_delegated_laws_to_cache(mst, response)
            return response
        
        print(f"Error fetching delegated laws: {result.get('error')}")
        return None
    
    def get_delegated_laws_from_cache(self, mst: str) -> Optional[DelegatedLawResponse]:
        """Get delegated laws from cache if available."""
        cache_file = self._get_cache_file_path(mst)
        
        if not cache_file.exists():
            return None
        
        # Check if cache is still valid
        if not self.is_cache_valid(mst):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Create response object from cached data
                return DelegatedLawResponse(
                    law_mst=data['law_mst'],
                    law_name=data['law_name'],
                    law_id=data['law_id'],
                    promulgation_date=data['promulgation_date'],
                    promulgation_number=data['promulgation_number'],
                    department_code=data['department_code'],
                    phone_number=data['phone_number'],
                    enforcement_date=data['enforcement_date'],
                    delegated_laws=self._deserialize_delegated_items(data['delegated_laws']),
                    administrative_rules=self._deserialize_delegated_items(data['administrative_rules']),
                    local_regulations=self._deserialize_delegated_items(data['local_regulations'])
                )
        except Exception as e:
            print(f"Error reading cache: {e}")
            return None
    
    def save_delegated_laws_to_cache(self, mst: str, response: DelegatedLawResponse) -> None:
        """Save delegated laws to cache."""
        cache_file = self._get_cache_file_path(mst)
        
        try:
            # Serialize the response
            cache_data = {
                'law_mst': response.law_mst,
                'law_name': response.law_name,
                'law_id': response.law_id,
                'promulgation_date': response.promulgation_date,
                'promulgation_number': response.promulgation_number,
                'department_code': response.department_code,
                'phone_number': response.phone_number,
                'enforcement_date': response.enforcement_date,
                'delegated_laws': self._serialize_delegated_items(response.delegated_laws),
                'administrative_rules': self._serialize_delegated_items(response.administrative_rules),
                'local_regulations': self._serialize_delegated_items(response.local_regulations),
                'cached_at': datetime.now().isoformat()
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    def is_cache_valid(self, mst: str) -> bool:
        """Check if cached data is still valid."""
        cache_file = self._get_cache_file_path(mst)
        
        if not cache_file.exists():
            return False
        
        try:
            # Check file modification time
            file_mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - file_mtime > self.cache_ttl:
                return False
            
            # Also check the cached_at field if available
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'cached_at' in data:
                    cached_at = datetime.fromisoformat(data['cached_at'])
                    if datetime.now() - cached_at > self.cache_ttl:
                        return False
            
            return True
        except Exception:
            return False
    
    def _get_cache_file_path(self, mst: str) -> Path:
        """Get cache file path for a specific MST."""
        return self.cache_dir / f"{mst}_delegated.json"
    
    def _serialize_delegated_items(self, items):
        """Serialize delegated items for caching."""
        return [{
            'delegated_type': item.delegated_type,
            'delegated_mst': item.delegated_mst,
            'delegated_title': item.delegated_title,
            'delegated_article_number': item.delegated_article_number,
            'delegated_article_sub_number': item.delegated_article_sub_number,
            'delegated_article_title': item.delegated_article_title,
            'link_text': item.link_text,
            'line_text': item.line_text,
            'clause_text': item.clause_text,
            'article_number': item.article_number,
            'article_title': item.article_title
        } for item in items]
    
    def _deserialize_delegated_items(self, data):
        """Deserialize delegated items from cache."""
        from ...domain.entities.delegated_law import DelegatedLawItem
        return [DelegatedLawItem(**item) for item in data]