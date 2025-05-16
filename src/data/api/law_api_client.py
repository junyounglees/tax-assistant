"""API client for Korean Law Search API."""
import requests
from typing import Dict, Any, Optional


class LawAPIClient:
    """Client for Korean Law Search API."""
    
    BASE_SEARCH_URL = "http://www.law.go.kr/DRF/lawSearch.do"
    BASE_SERVICE_URL = "http://www.law.go.kr/DRF/lawService.do"
    
    def __init__(self, email_id: str):
        self.email_id = email_id
    
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