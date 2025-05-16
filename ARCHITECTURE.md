# Clean Architecture

This project follows the Clean Architecture principles by Robert C. Martin.

## Architecture Layers

### 1. Domain Layer (`src/domain/`)
- **Entities**: Core business objects (e.g., `Law`)
- **Interfaces**: Repository interfaces defining contracts
- No external dependencies
- Contains business rules and domain logic

### 2. Data Layer (`src/data/`)
- **API Client**: Handles HTTP requests to the Korean Law API
- **Repositories**: Implements repository interfaces
- Manages data access and persistence
- Depends only on domain layer

### 3. Use Cases Layer (`src/use_cases/`)
- **Use Cases**: Application-specific business logic
- Orchestrates data flow between layers
- Depends on domain interfaces, not concrete implementations

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