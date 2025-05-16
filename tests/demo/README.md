# Demo and Test Scripts

This directory contains test and demo scripts that were used during the development of the Korean Law Search API project.

## Files

- **test_search.py** - Basic search functionality tests
- **simple_interactive.py** - Simple interactive search demo
- **interactive_law_search.py** - Interactive law search with class structure
- **law_menu.py** - Menu-based law search system
- **law_search_cli.py** - Command-line interface demo
- **law_finder.py** - Law search with name mappings
- **law_interactive.py** - Interactive search demo
- **law_select.py** - Law selection interface demo

## Usage

These scripts demonstrate various ways to interact with the law.go.kr API:

```bash
# Run interactive search demo
python tests/demo/simple_interactive.py

# Run menu-based search
python tests/demo/law_menu.py

# Test search functionality
python tests/demo/test_search.py
```

## Note

These scripts are kept for reference but should not be used in production. Use the main application in the `src/` directory instead.