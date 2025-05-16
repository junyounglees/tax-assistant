"""Use case for searching laws."""
from typing import List
from ..domain.entities.law import Law
from ..domain.interfaces.law_repository import LawRepositoryInterface


class SearchLawUseCase:
    """Use case for searching laws."""
    
    def __init__(self, repository: LawRepositoryInterface):
        self.repository = repository
    
    def execute(self, query: str, display: int = 20, save_results: bool = True) -> List[Law]:
        """Execute law search use case."""
        # Search for laws
        laws = self.repository.search_laws(query, display)
        
        # Save results if requested
        if save_results and laws:
            filename = f"{query.replace(' ', '_')}_검색결과.json"
            self.repository.save_search_results(laws, filename)
        
        return laws
    
    def search_with_abbreviation(self, query: str, display: int = 20) -> List[Law]:
        """Search with common abbreviation mapping."""
        # Common abbreviation mappings
        abbreviations = {
            '소득세': '소득세법',
            '법인세': '법인세법',
            '부가세': '부가가치세법',
            '상증세': '상속세 및 증여세법',
            '종부세': '종합부동산세법',
            '상법': '상법',
            '민법': '민법',
            '노동법': '근로기준법',
            '근로법': '근로기준법'
        }
        
        mapped_query = abbreviations.get(query, query)
        return self.execute(mapped_query, display)