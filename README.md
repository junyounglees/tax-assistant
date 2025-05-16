# Korean Law Search API Client

한국 법령정보 검색 API 클라이언트 (Clean Architecture)

## Directory Structure

```
tax-assisant/
├── src/                      # Source code (Clean Architecture)
│   ├── domain/              # Domain layer (entities, interfaces)
│   ├── data/                # Data layer (API, repositories)
│   ├── use_cases/           # Use case layer (business logic)
│   ├── presentation/        # Presentation layer (CLI)
│   ├── infrastructure/      # Infrastructure (config, DI)
│   └── main.py             # Main entry point
│
├── code/                     # Legacy code files
├── output/                   # Search results (JSON files)
├── law_search.py            # Backwards compatible wrapper
├── ARCHITECTURE.md          # Architecture documentation
└── README.md                # This file
```

## Quick Start

### 1. Interactive Search (Recommended)
```bash
python main.py
```
Or using the wrapper:
```bash
python law_search.py
```

This will show a numbered menu:
1. 소득세법
2. 법인세법
3. 부가가치세법
4. 상속세 및 증여세법
5. 민법
6. 상법
7. 근로기준법
8. 직접 입력
0. 종료

### 2. Command Line Search
```bash
python main.py 소득세법
python main.py 민법
python main.py 상법
```

### 3. Get Full Text
```bash
python main.py full-text 267581
```

## Architecture

This project follows Clean Architecture principles. See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

### Key Benefits:
- **Testable**: Each layer can be tested independently
- **Flexible**: Easy to change data sources or UI
- **Maintainable**: Clear separation of concerns
- **Scalable**: Easy to add new features

## Configuration

The application can be configured using environment variables:

- `LAW_API_EMAIL_ID`: Your email ID for the API (default: 'lee')
- `LAW_OUTPUT_DIR`: Output directory for results (default: 'output')

Example:
```bash
export LAW_API_EMAIL_ID=your_email
python main.py
```

## API Information

- **Search API**: `http://www.law.go.kr/DRF/lawSearch.do`
- **Full Text API**: `http://www.law.go.kr/DRF/lawService.do`
- **Format**: JSON

## Development

### Running Tests
```bash
python -m pytest tests/
```

### Adding New Features
1. Add domain entities/interfaces if needed
2. Implement repository methods if needed
3. Create use case for business logic
4. Update presentation layer
5. Wire dependencies in container

## Legacy Support

The old command-line tools are still available in the `code/` directory:
- `code/law_select.py`
- `code/law_menu.py`
- `code/law_finder.py`