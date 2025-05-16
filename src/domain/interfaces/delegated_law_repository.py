"""Interface for delegated law repository."""
from abc import ABC, abstractmethod
from typing import Optional
from ..entities.delegated_law import DelegatedLawResponse


class DelegatedLawRepository(ABC):
    """Interface for delegated law repository."""
    
    @abstractmethod
    def get_delegated_laws(self, mst: str) -> Optional[DelegatedLawResponse]:
        """Get delegated laws for a given law MST.
        
        Args:
            mst: Law master number
            
        Returns:
            DelegatedLawResponse if found, None otherwise
        """
        raise NotImplementedError
    
    @abstractmethod
    def get_delegated_laws_from_cache(self, mst: str) -> Optional[DelegatedLawResponse]:
        """Get delegated laws from cache if available.
        
        Args:
            mst: Law master number
            
        Returns:
            DelegatedLawResponse if cached, None otherwise
        """
        raise NotImplementedError
    
    @abstractmethod
    def save_delegated_laws_to_cache(self, mst: str, response: DelegatedLawResponse) -> None:
        """Save delegated laws to cache.
        
        Args:
            mst: Law master number
            response: DelegatedLawResponse to cache
        """
        raise NotImplementedError
    
    @abstractmethod
    def is_cache_valid(self, mst: str) -> bool:
        """Check if cached data is still valid.
        
        Args:
            mst: Law master number
            
        Returns:
            True if cache is valid, False otherwise
        """
        raise NotImplementedError