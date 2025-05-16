# Korean Law Search API - Clean Architecture Documentation

## Project Overview
This is a Korean Law Search API client implemented using Clean Architecture principles. It allows searching for Korean laws and retrieving their full text via the law.go.kr API.

## Project Structure
- **src/** - Main application code following clean architecture
- **tests/** - Test files and demo scripts
- **utils/** - Standalone utility scripts
- **docs/** - Documentation files
- **output/** - API response outputs

## Architecture Layers

### 1. Domain Layer (`src/domain/`)
- **Purpose**: Core business logic, entities, and interfaces
- **Key Files**:
  - `entities/law.py`: Law entity with properties like MST, name, law_type, etc.
  - `interfaces/law_repository.py`: Repository interface defining data access contracts
- **No external dependencies**

### 2. Data Layer (`src/data/`)
- **Purpose**: External data access and API communication
- **Key Files**:
  - `api/law_api_client.py`: HTTP client for law.go.kr API
  - `repositories/law_repository.py`: Implementation of repository interface
- **API Endpoints**:
  - Search: `http://www.law.go.kr/DRF/lawSearch.do`
  - Full text: `http://www.law.go.kr/DRF/lawService.do`

### 3. Use Cases Layer (`src/use_cases/`)
- **Purpose**: Application-specific business logic
- **Key Files**:
  - `search_law.py`: Search laws with abbreviation mapping
  - `get_law_full_text.py`: Retrieve full text of laws
- **Features**:
  - Abbreviation mapping (e.g., "소득세" → "소득세법")
  - Automatic result saving to JSON

### 4. Presentation Layer (`src/presentation/`)
- **Purpose**: User interface (CLI)
- **Key Files**:
  - `cli/menu_presenter.py`: Display formatting and menus
  - `cli/controller.py`: User input handling and flow control
- **Menu Options**:
  1. 소득세법
  2. 법인세법
  3. 부가가치세법
  4. 상속세 및 증여세법
  5. 민법
  6. 상법
  7. 근로기준법
  8. 직접 입력
  0. 종료

### 5. Infrastructure Layer (`src/infrastructure/`)
- **Purpose**: Configuration and dependency injection
- **Key Files**:
  - `config/settings.py`: Application settings (email ID, output directory)
  - `container.py`: Dependency injection container
- **Environment Variables**:
  - `LAW_API_EMAIL_ID`: API authentication (default: 'lee')
  - `LAW_OUTPUT_DIR`: Output directory (default: 'output')

## Coding Guidelines

### General Coding Principles
- Always write code by testing one by one, incrementally
- Always keep in mind the 'clean architecture' principles like Open Closed Principles and others

(Rest of the existing content remains the same)