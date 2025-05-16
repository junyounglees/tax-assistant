"""Test the 7-day cache configuration."""
from src.infrastructure.container import Container

# Create container
container = Container()
repo = container.repository

# Check the cache hours setting
print(f"Current cache expiration: {repo.cache_hours} hours")
print(f"That's {repo.cache_hours / 24:.1f} days")
print()

# Test with a simple search
print("Testing cache with 7-day expiration...")
laws = repo.search_laws("민법")
print(f"Found {len(laws)} laws")

# Show cache info
import os
from src.presentation.cli.cache_info import display_cache_info

cache_dir = os.path.join('output', '.cache')
display_cache_info(cache_dir)