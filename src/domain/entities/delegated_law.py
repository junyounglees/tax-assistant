"""Delegated law entity."""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class DelegatedLawItem:
    """Single delegated law reference item."""
    
    # Delegated law info
    delegated_type: str  # 위임구분 (시행령, 시행규칙, 행정규칙, 자치법규)
    delegated_mst: str  # 위임법령일련번호
    delegated_title: str  # 위임법령제목
    delegated_article_number: str  # 위임법령조문번호
    delegated_article_sub_number: Optional[str]  # 위임법령조문가지번호
    delegated_article_title: Optional[str]  # 위임법령조문제목
    
    # Reference info
    link_text: str  # 링크텍스트 (referenced text in main law)
    line_text: str  # 라인텍스트 (full text containing link)
    clause_text: str  # 조항호목
    
    # Source article info
    article_number: str  # 조문번호 (from main law)
    article_title: Optional[str]  # 조문제목 (from main law)
    
    @property
    def law_url(self) -> Optional[str]:
        """Generate URL for viewing this delegated law on law.go.kr."""
        if self.delegated_mst:
            # Format: https://www.law.go.kr/법령/법령명/(일련번호)
            return f"https://www.law.go.kr/법령/{self.delegated_title}/({self.delegated_mst})"
        return None
    
    @property
    def article_url(self) -> Optional[str]:
        """Generate URL for viewing specific article if available."""
        if self.delegated_mst and self.delegated_article_number:
            # Format includes article number in the URL
            clean_article = self.delegated_article_number.replace("제", "").replace("조", "")
            return f"https://www.law.go.kr/법령/{self.delegated_title}/({self.delegated_mst})/{clean_article}"
        return None


@dataclass
class DelegatedLawResponse:
    """Complete response for delegated laws of a specific law."""
    
    # Law info
    law_mst: str  # 법령일련번호
    law_name: str  # 법령명
    law_id: str  # 법령ID
    promulgation_date: str  # 공포일자
    promulgation_number: str  # 공포번호
    department_code: str  # 소관부처코드
    phone_number: str  # 전화번호
    enforcement_date: str  # 시행일자
    
    # Delegated law items
    delegated_laws: List[DelegatedLawItem]  # 위임 법령 목록
    administrative_rules: List[DelegatedLawItem]  # 위임 행정규칙 목록
    local_regulations: List[DelegatedLawItem]  # 위임 자치법규 목록
    
    @property
    def all_delegated_items(self) -> List[DelegatedLawItem]:
        """Get all delegated items regardless of type."""
        return self.delegated_laws + self.administrative_rules + self.local_regulations
    
    @property
    def has_delegated_laws(self) -> bool:
        """Check if there are any delegated laws."""
        return bool(self.all_delegated_items)
    
    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'DelegatedLawResponse':
        """Create DelegatedLawResponse from API response."""
        # Navigate to the correct structure
        ls_delegated = data.get('lsDelegated', {})
        law_section = ls_delegated.get('법령', {})
        
        # Extract basic law info
        law_info = law_section.get('법령정보', {})
        
        # Initialize lists for different types of delegated items
        delegated_laws = []
        administrative_rules = []
        local_regulations = []
        
        # Parse delegated info from 위임조문정보
        delegated_articles = law_section.get('위임조문정보', [])
        
        for article_item in delegated_articles:
            article_info = article_item.get('조정보', {})
            delegated_info_data = article_item.get('위임정보', {})
            
            if not delegated_info_data:
                continue
            
            # Handle case where 위임정보 might be a list
            if isinstance(delegated_info_data, list):
                delegated_info_list = delegated_info_data
            else:
                delegated_info_list = [delegated_info_data]
            
            # Get source article info
            source_article_number = str(article_info.get('조문번호', ''))
            source_article_sub_number = str(article_info.get('조문가지번호', '')) if article_info.get('조문가지번호') else ''
            if source_article_sub_number:
                source_article_number = f"{source_article_number}_{source_article_sub_number}"
            source_article_title = article_info.get('조문제목', '')
            
            # Process each delegated info item
            for delegated_info in delegated_info_list:
                # Skip empty items
                if not delegated_info or not isinstance(delegated_info, dict):
                    continue
                
                # Check if this is actually a delegated law or just contains article info
                if not any(key in delegated_info for key in ['위임구분', '위임법령일련번호', '위임법령제목']):
                    # This might be just an article reference without specific law info
                    article_info_data = delegated_info.get('위임법령조문정보', [])
                    if article_info_data:
                        # Process these as generic references
                        if isinstance(article_info_data, dict):
                            article_info_list = [article_info_data]
                        else:
                            article_info_list = article_info_data
                        
                        for article_info_item in article_info_list:
                            if isinstance(article_info_item, dict):
                                delegated_item = DelegatedLawItem(
                                    delegated_type='시행령',  # Default type
                                    delegated_mst='',
                                    delegated_title='',
                                    delegated_article_number=str(article_info_item.get('위임법령조문번호', '')),
                                    delegated_article_sub_number=str(article_info_item.get('위임법령조문가지번호', '')) if article_info_item.get('위임법령조문가지번호') else None,
                                    delegated_article_title=article_info_item.get('위임법령조문제목', ''),
                                    link_text=article_info_item.get('링크텍스트', ''),
                                    line_text=article_info_item.get('라인텍스트', ''),
                                    clause_text=article_info_item.get('조항호목', ''),
                                    article_number=source_article_number,
                                    article_title=source_article_title
                                )
                                delegated_laws.append(delegated_item)
                    
                    # Check for administrative rules
                    admin_info = delegated_info.get('위임행정규칙조문정보', {})
                    if admin_info:
                        if isinstance(admin_info, dict):
                            admin_list = [admin_info]
                        else:
                            admin_list = admin_info
                        
                        for admin_item in admin_list:
                            if isinstance(admin_item, dict):
                                delegated_item = DelegatedLawItem(
                                    delegated_type='행정규칙',
                                    delegated_mst=str(admin_item.get('위임행정규칙일련번호', '')),
                                    delegated_title=admin_item.get('위임행정규칙제목', ''),
                                    delegated_article_number='',
                                    delegated_article_sub_number=None,
                                    delegated_article_title=None,
                                    link_text=admin_item.get('링크텍스트', ''),
                                    line_text=admin_item.get('라인텍스트', ''),
                                    clause_text=admin_item.get('조항호목', ''),
                                    article_number=source_article_number,
                                    article_title=source_article_title
                                )
                                administrative_rules.append(delegated_item)
                    continue
                
                # Get delegated law info
                delegated_type = delegated_info.get('위임구분', '')
                delegated_mst = str(delegated_info.get('위임법령일련번호', ''))
                delegated_title = delegated_info.get('위임법령제목', '')
                
                # Get delegated article references
                delegated_article_info_data = delegated_info.get('위임법령조문정보', [])
                
                # Handle case where it might be a single dict instead of a list
                if isinstance(delegated_article_info_data, dict):
                    delegated_article_info_list = [delegated_article_info_data]
                else:
                    delegated_article_info_list = delegated_article_info_data
                
                for delegated_article_info in delegated_article_info_list:
                    delegated_item = DelegatedLawItem(
                        delegated_type=delegated_type,
                        delegated_mst=delegated_mst,
                        delegated_title=delegated_title,
                        delegated_article_number=str(delegated_article_info.get('위임법령조문번호', '')),
                        delegated_article_sub_number=str(delegated_article_info.get('위임법령조문가지번호', '')) if delegated_article_info.get('위임법령조문가지번호') else None,
                        delegated_article_title=delegated_article_info.get('위임법령조문제목', ''),
                        link_text=delegated_article_info.get('링크텍스트', ''),
                        line_text=delegated_article_info.get('라인텍스트', ''),
                        clause_text=delegated_article_info.get('조항호목', ''),
                        article_number=source_article_number,
                        article_title=source_article_title
                    )
                    
                    # Categorize by type
                    if delegated_type in ['시행령', '대통령령']:
                        delegated_laws.append(delegated_item)
                    elif delegated_type in ['시행규칙', '부령']:
                        administrative_rules.append(delegated_item)
                    elif delegated_type in ['자치법규', '조례']:
                        local_regulations.append(delegated_item)
                    else:
                        # Default to delegated laws
                        delegated_laws.append(delegated_item)
        
        return cls(
            law_mst=str(law_info.get('법령일련번호', '')),
            law_name=law_info.get('법령명한글', ''),
            law_id=str(law_info.get('법령ID', '')),
            promulgation_date=str(law_info.get('공포일자', '')),
            promulgation_number=str(law_info.get('공포번호', '')),
            department_code=str(law_info.get('소관부처코드', '')),
            phone_number=law_info.get('전화번호', ''),
            enforcement_date=str(law_info.get('시행일자', '')),
            delegated_laws=delegated_laws,
            administrative_rules=administrative_rules,
            local_regulations=local_regulations
        )