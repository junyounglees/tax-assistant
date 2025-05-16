"""Test the new cache system with descriptive filenames."""
import os
import shutil
from src.infrastructure.container import Container
from src.presentation.cli.cache_info import display_cache_info

# Create container
container = Container()
repo = container.repository

# Start fresh
cache_dir = os.path.join('output', '.cache')
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    os.makedirs(cache_dir)
    print("캐시 초기화 완료")

# Test 1: Search (should create new cache file with new name)
print("\n=== 테스트 1: 법령 검색 (API) ===")
laws = repo.search_laws("소득세법")
print(f"검색 결과: {len(laws)}개 법령")

# Check cache
print("\n=== 캐시 상태 확인 ===")
cache_files = os.listdir(cache_dir) if os.path.exists(cache_dir) else []
print(f"캐시 파일: {cache_files}")

# Test 2: Get law content (should create new cache file)
print("\n=== 테스트 2: 조문 조회 (API) ===")
if laws:
    content = repo.get_law_content(laws[0].mst)
    print(f"조문 수: {len(content.articles)}개")
    print(f"캐시에서 가져옴: {content.from_cache}")

# Check cache again
print("\n=== 캐시 상태 확인 ===")
cache_files = os.listdir(cache_dir) if os.path.exists(cache_dir) else []
print(f"캐시 파일: {cache_files}")

# Test 3: Re-fetch law content (should use cache)
print("\n=== 테스트 3: 조문 재조회 (캐시) ===")
content = repo.get_law_content(laws[0].mst)
print(f"조문 수: {len(content.articles)}개")
print(f"캐시에서 가져옴: {content.from_cache}")

# Test 4: Search different law
print("\n=== 테스트 4: 다른 법령 검색 ===")
laws2 = repo.search_laws("법인세법")
print(f"검색 결과: {len(laws2)}개 법령")

# Final cache state
print("\n=== 최종 캐시 상태 ===")
display_cache_info(cache_dir)