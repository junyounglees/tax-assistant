# Coding Guidelines for Korean Law Search Project

## Architecture Rules

### 1. Dependency Direction
- Dependencies must flow **inward only**
- Domain layer should have **NO external dependencies**
- Use interfaces for dependency inversion
- Never import from outer layers into inner layers

```python
# ✅ Good: Use case depends on domain interface
from ..domain.interfaces.law_repository import LawRepositoryInterface

# ❌ Bad: Use case depends on concrete implementation
from ..data.repositories.law_repository import LawRepository
```

### 2. Layer Responsibilities

#### Domain Layer
- Pure business logic and entities
- No framework dependencies
- No I/O operations
- Define interfaces for external services

```python
# ✅ Good: Pure domain entity
@dataclass
class Law:
    mst: str
    name: str
    
    def is_enforced(self) -> bool:
        # Business logic only
        return True

# ❌ Bad: Domain entity with I/O
class Law:
    def save_to_file(self):  # Wrong! I/O in domain
        with open('law.json', 'w') as f:
            json.dump(self, f)
```

#### Use Cases Layer
- Application-specific business logic
- Orchestrate data flow
- Handle errors gracefully
- Return domain entities, not raw data

```python
# ✅ Good: Use case returns domain entities
def execute(self, query: str) -> List[Law]:
    laws = self.repository.search_laws(query)
    return laws

# ❌ Bad: Use case returns raw API data
def execute(self, query: str) -> dict:
    return self.api_client.search(query)  # Wrong!
```

#### Data Layer
- Implement repository interfaces
- Handle API communication
- Transform data to/from domain entities
- Handle API-specific errors

```python
# ✅ Good: Repository transforms data
def search_laws(self, query: str) -> List[Law]:
    response = self.api_client.search(query)
    return [Law.from_api_response(data) for data in response['laws']]

# ❌ Bad: Repository returns raw API response
def search_laws(self, query: str) -> dict:
    return self.api_client.search(query)  # Wrong!
```

## Coding Standards

### 1. Type Hints
Always use type hints for better code clarity:

```python
from typing import List, Optional, Dict, Any

def search_laws(self, query: str, display: int = 20) -> List[Law]:
    """Search for laws by query."""
    pass
```

### 2. Error Handling
Use specific exceptions and handle errors at appropriate layers:

```python
# Define custom exceptions
class LawNotFoundError(Exception):
    """Raised when a law is not found."""
    pass

# Handle errors in use cases
try:
    laws = self.repository.search_laws(query)
except APIError as e:
    logger.error(f"API error: {e}")
    return []
```

### 3. Naming Conventions
- Classes: PascalCase (`SearchLawUseCase`)
- Functions/methods: snake_case (`search_laws`)
- Constants: UPPER_SNAKE_CASE (`BASE_API_URL`)
- Private methods: prefix with underscore (`_validate_query`)

### 4. File Organization
Each layer should have its own directory with `__init__.py`:

```
src/
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   └── law.py
│   └── interfaces/
│       ├── __init__.py
│       └── law_repository.py
```

## API Integration Guidelines

### 1. API Client
- Keep API-specific logic in the data layer
- Use session for connection pooling
- Add appropriate timeouts
- Log API requests for debugging

```python
class LawAPIClient:
    def __init__(self, email_id: str):
        self.email_id = email_id
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Korean Law Search Client'
        })
    
    def search(self, query: str, timeout: int = 30) -> Dict[str, Any]:
        try:
            response = self.session.get(
                self.BASE_URL,
                params={'query': query},
                timeout=timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise APIError(f"Failed to search: {e}")
```

### 2. Data Transformation
Always validate and transform API responses:

```python
@classmethod
def from_api_response(cls, data: dict) -> 'Law':
    """Create Law instance from API response."""
    # Validate required fields
    required = ['법령일련번호', '법령명한글']
    for field in required:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    return cls(
        mst=data.get('법령일련번호', ''),
        name=data.get('법령명한글', ''),
        # Use get() with defaults for optional fields
        law_type=data.get('법령구분명', ''),
    )
```

## Testing Guidelines

### 1. Test Structure
Mirror the source structure in tests:

```
tests/
├── domain/
│   ├── entities/
│   │   └── test_law.py
│   └── interfaces/
├── data/
│   └── repositories/
│       └── test_law_repository.py
├── use_cases/
│   └── test_search_law.py
```

### 2. Mocking
Use dependency injection for easy mocking:

```python
def test_search_law_use_case():
    # Mock the repository
    mock_repo = Mock(spec=LawRepositoryInterface)
    mock_repo.search_laws.return_value = [
        Law(mst='123', name='Test Law')
    ]
    
    # Test use case
    use_case = SearchLawUseCase(mock_repo)
    results = use_case.execute('test')
    
    assert len(results) == 1
    assert results[0].name == 'Test Law'
    mock_repo.search_laws.assert_called_once_with('test', 20)
```

### 3. Integration Tests
Test API integration separately:

```python
@pytest.mark.integration
def test_law_api_client():
    client = LawAPIClient('test@example.com')
    response = client.search('소득세법')
    assert 'LawSearch' in response
```

## Common Tasks

### 1. Adding a New Law Type
1. Update domain entity if needed
2. Add mapping in use case
3. Update menu in presentation layer

```python
# In SearchLawUseCase
ABBREVIATIONS = {
    '소득세': '소득세법',
    '새로운법': '새로운법령명',  # Add here
}
```

### 2. Adding a New API Endpoint
1. Add method to API client
2. Add interface method to repository interface
3. Implement in repository
4. Create new use case if needed

### 3. Adding Configuration
1. Add to Settings dataclass
2. Use environment variable with default
3. Access via container.settings

```python
@dataclass
class Settings:
    new_setting: str = os.getenv('NEW_SETTING', 'default')
```

## Best Practices

### 1. Keep It Simple
- Don't over-engineer
- Use simple solutions first
- Refactor when needed

### 2. Document Important Decisions
- Use docstrings for complex logic
- Add comments for non-obvious code
- Update ARCHITECTURE.md for major changes

### 3. Consistent Error Messages
- Use Korean for user-facing messages
- Use English for logs and exceptions
- Be specific about what went wrong

```python
# User-facing (Korean)
self.presenter.display_error("검색 결과가 없습니다.")

# Logs/exceptions (English)
logger.error(f"API request failed: {response.status_code}")
raise APIError(f"Search failed for query: {query}")
```

### 4. File Naming
- Use descriptive names
- Group related functionality
- Follow Python conventions

```
search_law.py          # Use case for searching
law_repository.py      # Repository implementation
law_api_client.py      # API client
```

## Quick Reference

### File Creation Template
```python
"""Module description."""
from typing import List, Optional
from ..domain.entities.law import Law


class NewFeature:
    """Class description."""
    
    def __init__(self, dependency: Interface):
        """Initialize with dependencies."""
        self.dependency = dependency
    
    def execute(self, param: str) -> List[Law]:
        """Method description.
        
        Args:
            param: Parameter description
            
        Returns:
            List of Law entities
            
        Raises:
            CustomError: When something goes wrong
        """
        # Implementation
        pass
```

### Common Imports
```python
# Type hints
from typing import List, Dict, Optional, Any

# Domain
from ..domain.entities.law import Law
from ..domain.interfaces.law_repository import LawRepositoryInterface

# Standard library
import os
import json
from dataclasses import dataclass
```