"""Use case for getting law full text."""
from typing import Optional
from ..domain.interfaces.law_repository import LawRepositoryInterface


class GetLawFullTextUseCase:
    """Use case for getting law full text."""
    
    def __init__(self, repository: LawRepositoryInterface):
        self.repository = repository
    
    def execute(self, mst: str, save_result: bool = True) -> Optional[dict]:
        """Execute get law full text use case."""
        # Get full text
        law_data = self.repository.get_law_full_text(mst)
        
        if not law_data:
            return None
        
        # Extract law name for filename
        law_name = "법령"
        if 'law' in law_data:
            law_info = law_data['law'][0] if isinstance(law_data['law'], list) else law_data['law']
            law_name = law_info.get('법령명한글', '법령')
        
        # Save if requested
        if save_result:
            filename = f"{law_name.replace(' ', '_')}_전문.json"
            self.repository.save_law_full_text(law_data, filename)
        
        return law_data