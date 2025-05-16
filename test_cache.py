"""Test caching functionality."""
from src.infrastructure.container import Container

# Create container
container = Container()
repo = container.repository

# Test 1: First search (no cache)
print("Test 1: First search")
laws = repo.search_laws("소득세법")
print(f"Found {len(laws)} laws")

# Test 2: Second search (should use cache)
print("\nTest 2: Second search (should use cache)")
laws = repo.search_laws("소득세법")
print(f"Found {len(laws)} laws")

# Test 3: Check cache directory
import os
cache_dir = os.path.join('output', '.cache')
if os.path.exists(cache_dir):
    cache_files = os.listdir(cache_dir)
    print(f"\nCache files: {cache_files}")
else:
    print("\nNo cache directory found")

# Test 4: First law content fetch
print("\nTest 3: First law content fetch")
if laws:
    content = repo.get_law_content(laws[0].mst)
    if content:
        print(f"Got law content with {len(content.articles)} articles")
    
    # Second fetch (should use cache)
    print("\nTest 4: Second law content fetch (should use cache)")
    content = repo.get_law_content(laws[0].mst)
    if content:
        print(f"Got law content with {len(content.articles)} articles")