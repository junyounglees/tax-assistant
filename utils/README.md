# Utility Scripts

This directory contains standalone utility scripts for working with the Korean Law Search API.

## Scripts

- **get_law_full_text.py** - Retrieve full text of a law by MST number
- **get_law_list_formatted.py** - Get formatted list of laws
- **search_any_law.py** - General law search utility

## Usage

These scripts can be run directly from the command line:

```bash
# Search for any law
python utils/search_any_law.py

# Get full text of a specific law
python utils/get_law_full_text.py [MST_NUMBER]

# Get formatted law list
python utils/get_law_list_formatted.py
```

## Note

These scripts are standalone utilities and do not depend on the main application structure. They're kept for reference and quick testing purposes.