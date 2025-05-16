"""API client for Korean Law Search API."""
import requests
from typing import Dict, Any, Optional, List
import time


class LawAPIClient:
    """Client for Korean Law Search API."""
    
    BASE_SEARCH_URL = "http://www.law.go.kr/DRF/lawSearch.do"
    BASE_SERVICE_URL = "http://www.law.go.kr/DRF/lawService.do"
    
    def __init__(self, email_id: str):
        self.email_id = email_id
        self.max_retries = 3
        self.retry_delay = 1.0  # seconds
    
    def search(self, query: str, display: int = 20, format_type: str = 'JSON') -> Dict[str, Any]:
        """Search for laws using the API."""
        params = {
            'OC': self.email_id,
            'target': 'law',
            'type': format_type,
            'query': query,
            'display': str(display),
            'sort': 'lawNm'
        }
        
        try:
            response = requests.get(self.BASE_SEARCH_URL, params=params)
            response.encoding = 'utf-8'
            
            if response.status_code == 200 and format_type == 'JSON':
                return response.json()
            
            return {'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_delegated_laws(self, mst: str, format_type: str = 'JSON') -> Dict[str, Any]:
        """Get delegated laws for a given law using MST.
        
        Args:
            mst: Law master number (법령 마스터 번호)
            format_type: Output format (JSON/XML)
            
        Returns:
            Dictionary containing delegated law information
        """
        params = {
            'OC': self.email_id,
            'target': 'lsDelegated',
            'type': format_type,
            'MST': mst
        }
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.BASE_SERVICE_URL, params=params)
                response.encoding = 'utf-8'
                
                if response.status_code == 200 and format_type == 'JSON':
                    return response.json()
                
                last_error = f'HTTP {response.status_code}'
                
            except Exception as e:
                last_error = str(e)
                
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
                print(f"Retry {attempt + 1}/{self.max_retries} for delegated laws API...")
        
        return {'error': last_error}
    
    def get_full_text(self, mst: str, jo: Optional[str] = None, format_type: str = 'JSON') -> Dict[str, Any]:
        """Get full text of a law using MST.
        
        Args:
            mst: Law master number (법령 마스터 번호)
            jo: Article number (조번호) - Optional, 6-digit format
            format_type: Output format (JSON/XML/HTML)
        """
        params = {
            'OC': self.email_id,
            'target': 'law',
            'type': format_type,
            'MST': mst
        }
        
        if jo:  # Add article number if specified
            params['JO'] = jo
        
        try:
            response = requests.get(self.BASE_SERVICE_URL, params=params)
            response.encoding = 'utf-8'
            
            if response.status_code == 200 and format_type == 'JSON':
                return response.json()
            
            return {'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'error': str(e)}
    
    def get_delegated_laws(self, mst: str, format_type: str = 'JSON') -> Dict[str, Any]:
        """Get delegated laws for a given law using MST.
        
        Args:
            mst: Law master number (법령 마스터 번호)
            format_type: Output format (JSON/XML)
            
        Returns:
            Dictionary containing delegated law information
        """
        params = {
            'OC': self.email_id,
            'target': 'lsDelegated',
            'type': format_type,
            'MST': mst
        }
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.get(self.BASE_SERVICE_URL, params=params)
                response.encoding = 'utf-8'
                
                if response.status_code == 200 and format_type == 'JSON':
                    return response.json()
                
                last_error = f'HTTP {response.status_code}'
                
            except Exception as e:
                last_error = str(e)
                
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay)
                print(f"Retry {attempt + 1}/{self.max_retries} for delegated laws API...")
        
        return {'error': last_error}