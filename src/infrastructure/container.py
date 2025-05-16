"""Dependency injection container."""
from .config.settings import Settings
from ..data.api.law_api_client import LawAPIClient
from ..data.repositories.law_repository import LawRepository
from ..use_cases.search_law import SearchLawUseCase
from ..use_cases.get_law_full_text import GetLawFullTextUseCase
from ..use_cases.view_law_articles import ViewLawArticlesUseCase
from ..use_cases.view_delegated_laws import ViewDelegatedLawsUseCase
from ..presentation.cli.controller import CLIController


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self.settings = Settings.from_env()
        self._api_client = None
        self._repository = None
        self._search_use_case = None
        self._full_text_use_case = None
        self._view_articles_use_case = None
        self._view_delegated_laws_use_case = None
        self._cli_controller = None
    
    @property
    def api_client(self) -> LawAPIClient:
        """Get API client instance."""
        if self._api_client is None:
            self._api_client = LawAPIClient(self.settings.email_id)
        return self._api_client
    
    @property
    def repository(self) -> LawRepository:
        """Get repository instance."""
        if self._repository is None:
            self._repository = LawRepository(self.api_client, self.settings.output_dir)
        return self._repository
    
    @property
    def search_use_case(self) -> SearchLawUseCase:
        """Get search use case instance."""
        if self._search_use_case is None:
            self._search_use_case = SearchLawUseCase(self.repository)
        return self._search_use_case
    
    @property
    def full_text_use_case(self) -> GetLawFullTextUseCase:
        """Get full text use case instance."""
        if self._full_text_use_case is None:
            self._full_text_use_case = GetLawFullTextUseCase(self.repository)
        return self._full_text_use_case
    
    @property
    def view_articles_use_case(self) -> ViewLawArticlesUseCase:
        """Get view articles use case instance."""
        if self._view_articles_use_case is None:
            self._view_articles_use_case = ViewLawArticlesUseCase(self.repository)
        return self._view_articles_use_case
    
    @property
    def view_delegated_laws_use_case(self) -> ViewDelegatedLawsUseCase:
        """Get view delegated laws use case instance."""
        if self._view_delegated_laws_use_case is None:
            self._view_delegated_laws_use_case = ViewDelegatedLawsUseCase(self.repository)
        return self._view_delegated_laws_use_case
    
    @property
    def cli_controller(self) -> CLIController:
        """Get CLI controller instance."""
        if self._cli_controller is None:
            self._cli_controller = CLIController(
                self.search_use_case,
                self.full_text_use_case,
                self.view_articles_use_case,
                self.view_delegated_laws_use_case
            )
        return self._cli_controller