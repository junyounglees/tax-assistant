"""Application settings."""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Application settings."""
    
    # API Configuration
    email_id: str = os.getenv('LAW_API_EMAIL_ID', 'lee')
    
    # Application settings
    output_dir: str = os.getenv('LAW_OUTPUT_DIR', 'output')
    default_display_count: int = 20
    
    # API URLs
    search_api_url: str = "http://www.law.go.kr/DRF/lawSearch.do"
    service_api_url: str = "http://www.law.go.kr/DRF/lawService.do"
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Create settings from environment variables."""
        return cls()