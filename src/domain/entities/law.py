"""Law entity representing the core business object."""
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class Law:
    """Domain entity representing a Law."""
    
    mst: str  # 법령일련번호
    name: str  # 법령명한글
    law_type: str  # 법령구분명
    department: str  # 소관부처명
    enforcement_date: str  # 시행일자
    promulgation_date: str  # 공포일자
    promulgation_number: Optional[str] = None  # 공포번호
    law_id: Optional[str] = None  # 법령ID
    detail_link: Optional[str] = None  # 법령상세링크
    
    @property
    def is_enforced(self) -> bool:
        """Check if the law is currently enforced."""
        try:
            enforcement = date.fromisoformat(self.enforcement_date[:4] + '-' + 
                                          self.enforcement_date[4:6] + '-' + 
                                          self.enforcement_date[6:8])
            return enforcement <= date.today()
        except:
            return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'mst': self.mst,
            'name': self.name,
            'law_type': self.law_type,
            'department': self.department,
            'enforcement_date': self.enforcement_date,
            'promulgation_date': self.promulgation_date,
            'promulgation_number': self.promulgation_number,
            'law_id': self.law_id,
            'detail_link': self.detail_link
        }
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'Law':
        """Create Law instance from API response data."""
        return cls(
            mst=data.get('법령일련번호', ''),
            name=data.get('법령명한글', ''),
            law_type=data.get('법령구분명', ''),
            department=data.get('소관부처명', ''),
            enforcement_date=data.get('시행일자', ''),
            promulgation_date=data.get('공포일자', ''),
            promulgation_number=data.get('공포번호'),
            law_id=data.get('법령ID'),
            detail_link=data.get('법령상세링크')
        )