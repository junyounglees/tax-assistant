# Clean Architecture

This project follows the Clean Architecture principles by Robert C. Martin.

## Architecture Layers

### 1. Domain Layer (`src/domain/`)
- **Entities**: Core business objects (e.g., `Law`, `Article`, `DelegatedLaw`)
- **Interfaces**: Repository interfaces defining contracts
- No external dependencies
- Contains business rules and domain logic
- Key entities:
  - `Law`: Represents a Korean law
  - `Article`: Represents an article within a law
  - `LawContent`: Complete law with all articles
  - `DelegatedLaw`: Information about delegated legislation

### 2. Data Layer (`src/data/`)
- **API Client**: Handles HTTP requests to the Korean Law API
  - Law search and full text retrieval
  - Delegated law lookup (위임법령 조회)
- **Repositories**: Implements repository interfaces
  - `LawRepository`: Manages law and article data
  - `DelegatedLawRepository`: Manages delegated law data with caching
- Manages data access and persistence
- Depends only on domain layer
- Features:
  - 7-day cache for law content and delegated laws
  - Automatic retry with exponential backoff

### 3. Use Cases Layer (`src/use_cases/`)
- **Use Cases**: Application-specific business logic
- Orchestrates data flow between layers
- Depends on domain interfaces, not concrete implementations
- Key use cases:
  - `SearchLawUseCase`: Search for laws with abbreviation mapping
  - `GetLawFullTextUseCase`: Retrieve full text of a law
  - `ViewLawArticlesUseCase`: View and search articles within a law
  - `ViewDelegatedLawsUseCase`: View delegated laws for specific articles

### 4. Presentation Layer (`src/presentation/`)
- **Controllers**: Handle user input and orchestrate use cases
- **Presenters**: Format and display output
- CLI-specific implementation
- Depends on use cases

### 5. Infrastructure Layer (`src/infrastructure/`)
- **Configuration**: Application settings
- **Dependency Injection**: Container for managing dependencies
- Cross-cutting concerns

## Dependency Flow
```
Presentation → Use Cases → Domain ← Data
                ↑                    ↑
                └── Infrastructure ──┘
```

## Benefits

1. **Testability**: Each layer can be tested independently
2. **Flexibility**: Easy to change implementations (e.g., different UI, different data source)
3. **Maintainability**: Clear separation of concerns
4. **Scalability**: Easy to add new features without affecting existing code

## Usage

### Interactive Mode
```bash
python src/main.py
```

### Command Line Mode
```bash
python src/main.py 소득세법
python src/main.py full-text 267581
```

### Legacy Support
```bash
python law_search.py
```

## Features

### Law Search and Article Viewing
- Search laws by name or abbreviation
- View full text of laws with article navigation
- Search articles by number or keyword
- Open law articles in web browser

### Delegated Laws (위임법령)
- Identify articles that reference delegated laws (시행령, 시행규칙, etc.)
- Retrieve delegated law content for specific articles
- View related articles from delegated laws
- Automatic caching of delegated law lookups

### Caching
- 7-day cache for law content and delegated laws
- Separate cache directories for different data types
- Automatic cache validation and cleanup