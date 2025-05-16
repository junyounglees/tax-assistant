"""Law article entity."""
from dataclasses import dataclass
from typing import Optional, List
import re


@dataclass 
class Article:
    """Domain entity representing a law article."""
    
    article_number: str  # 조문번호
    article_title: Optional[str]  # 조문제목
    article_content: str  # 조문내용
    enforcement_date: Optional[str]  # 조문시행일자
    
    # Common patterns for delegated law references
    DELEGATION_PATTERNS = [
        r'대통령령으로\s+정하[는다]',
        r'대통령령으로\s+정한다',
        r'기획재정부령으로\s+정하[는다]',
        r'기획재정부령으로\s+정한다',
        r'시행령으로\s+정하[는다]',
        r'시행령으로\s+정한다',
        r'시행규칙으로\s+정하[는다]',
        r'시행규칙으로\s+정한다',
    ]
    
    @property
    def formatted_number(self) -> str:
        """Get formatted article number from content or article_number."""
        # First try to extract from content (more accurate)
        if self.article_content:
            import re
            # Match patterns like 제1조, 제1조의2, etc.
            match = re.match(r'^(제\d+조(?:의\d+)?)', self.article_content.strip())
            if match:
                return match.group(1)
        
        # Fallback to article_number
        try:
            num = int(self.article_number[:4])  # First 4 digits
            return f"제{num}조"
        except:
            return self.article_number
    
    def has_delegated_law_references(self) -> bool:
        """Check if article contains references to delegated laws."""
        for pattern in self.DELEGATION_PATTERNS:
            if re.search(pattern, self.article_content):
                return True
        return False
    
    def get_delegated_law_types(self) -> List[str]:
        """Extract types of delegated laws referenced in the article."""
        types = []
        if re.search(r'대통령령으로\s+정하', self.article_content):
            types.append('시행령')
        if re.search(r'기획재정부령으로\s+정하', self.article_content):
            types.append('시행규칙')
        if re.search(r'시행령으로\s+정하', self.article_content):
            types.append('시행령')
        if re.search(r'시행규칙으로\s+정하', self.article_content):
            types.append('시행규칙')
        return list(set(types))  # Remove duplicates
    
    def get_delegated_law_references(self) -> List[dict]:
        """Extract detailed references to delegated laws."""
        references = []
        
        # Extract specific pattern matches with context
        for pattern in self.DELEGATION_PATTERNS:
            matches = re.finditer(pattern, self.article_content)
            for match in matches:
                context_start = max(0, match.start() - 20)
                context_end = min(len(self.article_content), match.end() + 20)
                context = self.article_content[context_start:context_end]
                
                law_type = '시행령'  # Default
                if '기획재정부령' in match.group():
                    law_type = '시행규칙'
                elif '시행규칙' in match.group():
                    law_type = '시행규칙'
                
                references.append({
                    'type': law_type,
                    'text': match.group(),
                    'context': context.strip()
                })
        
        return references
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'Article':
        """Create Article from API response."""
        # Handle cases where the article might not have a title
        article_title = data.get('조문제목')
        if not article_title and data.get('조문여부') == '전문':
            article_title = 'Chapter/Section Header'
        
        # Handle content that might be a list
        content = data.get('조문내용', '')
        if isinstance(content, list):
            # If content is a list, join all parts
            if content and isinstance(content[0], list):
                # Nested list - join all parts of the first item
                content = '\n'.join(content[0])
            else:
                # Simple list - join all items
                content = '\n'.join(content)
        
        # Check if there are paragraph units (항) with actual content
        if '항' in data and isinstance(data['항'], list):
            paragraph_content = []
            for para in data['항']:
                if isinstance(para, dict):
                    # Add paragraph number and content
                    para_text = para.get('항내용', '')
                    if para_text:
                        paragraph_content.append(para_text)
                    
                    # Add any sub-items (호)
                    if '호' in para and isinstance(para['호'], list):
                        for item in para['호']:
                            if isinstance(item, dict):
                                item_text = item.get('호내용', '')
                                # Handle ho content that might be a list
                                if isinstance(item_text, list):
                                    if item_text and isinstance(item_text[0], list):
                                        # Nested list - flatten it
                                        item_text = '\n'.join(str(i) for sublist in item_text for i in sublist if i)
                                    else:
                                        item_text = '\n'.join(str(i) for i in item_text if i)
                                
                                if item_text:
                                    paragraph_content.append(f"  {item_text}")
            
            # If we have paragraph content, use it (possibly in addition to title from 조문내용)
            if paragraph_content:
                if content and content.startswith('제'):
                    # Article number as title - add all paragraph content
                    full_content = [content] + paragraph_content
                else:
                    # Use content as is, append paragraph content
                    full_content = [content] if content else []
                    full_content.extend(paragraph_content)
                
                content = '\n'.join(str(item) for item in full_content)
            
        return cls(
            article_number=str(data.get('조문번호', '')),
            article_title=article_title,
            article_content=content,
            enforcement_date=str(data.get('조문시행일자', ''))
        )


@dataclass
class LawContent:
    """Complete law content with articles."""
    
    law_name: str  # 법령명_한글
    law_id: str  # 법령ID
    mst: str  # 법령마스터번호
    promulgation_date: str  # 공포일자
    enforcement_date: str  # 시행일자
    department: str  # 소관부처
    articles: List[Article]  # 조문목록
    from_cache: bool = False  # Whether data came from cache
    
    @classmethod
    def from_api_response(cls, data: dict) -> 'LawContent':
        """Create LawContent from API response."""
        law_info = {}
        articles = []
        
        # Handle different API response structures
        if isinstance(data, dict):
            # Check for nested structure
            if '법령' in data:
                law_data = data['법령']
                if isinstance(law_data, dict):
                    # Extract basic info
                    if '기본정보' in law_data:
                        law_info = law_data['기본정보']
                    else:
                        law_info = law_data
                    # Extract articles from law data
                    if '조문' in law_data:
                        article_container = law_data['조문']
                        if isinstance(article_container, dict):
                            # Get the actual articles from "조문단위"
                            if '조문단위' in article_container:
                                articles_data = article_container['조문단위']
                                if isinstance(articles_data, list):
                                    articles = [Article.from_api_response(a) for a in articles_data if a]
                                elif isinstance(articles_data, dict):
                                    articles = [Article.from_api_response(articles_data)]
            elif 'law' in data:
                if isinstance(data['law'], list) and data['law']:
                    law_info = data['law'][0]
                elif isinstance(data['law'], dict):
                    law_info = data['law']
            else:
                law_info = data
            
            # Extract articles from various possible locations if not already found
            if not articles:
                articles_data = None
                if '조문' in law_info:
                    article_container = law_info['조문']
                    if isinstance(article_container, dict) and '조문단위' in article_container:
                        articles_data = article_container['조문단위']
                    else:
                        articles_data = article_container
                elif '조문' in data:
                    articles_data = data['조문']
                
                if articles_data:
                    if isinstance(articles_data, list):
                        articles = [Article.from_api_response(a) for a in articles_data if a]
                    elif isinstance(articles_data, dict):
                        articles = [Article.from_api_response(articles_data)]
        
        # Extract MST from 법령키 if available
        mst = ''
        if isinstance(data, dict) and '법령' in data and '법령키' in data['법령']:
            law_key = data['법령']['법령키']
            # Extract first 6 digits from 법령키 as MST
            if len(law_key) >= 6:
                mst = law_key[:6]
        
        # Extract department info
        department = ''
        if '소관부처' in law_info and isinstance(law_info['소관부처'], dict):
            department = law_info['소관부처'].get('content', '')
        else:
            department = law_info.get('소관부처명', law_info.get('소관부처', ''))
        
        return cls(
            law_name=law_info.get('법령명한글', law_info.get('법령명_한글', '')),
            law_id=str(law_info.get('법령ID', '')),
            mst=mst,
            promulgation_date=str(law_info.get('공포일자', '')),
            enforcement_date=str(law_info.get('시행일자', '')),
            department=department,
            articles=articles
        )