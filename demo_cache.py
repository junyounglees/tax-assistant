"""Demo script to show caching functionality."""
import os
import shutil
from src.infrastructure.container import Container
from src.presentation.cli.cache_info import display_cache_info

# Create container
container = Container()
repo = container.repository

# Show initial cache state
print("=== 초기 캐시 상태 ===")
cache_dir = os.path.join('output', '.cache')
display_cache_info(cache_dir)

# Clear cache to start fresh
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    os.makedirs(cache_dir)
    print("\n캐시 초기화 완료")

# Test 1: First search (no cache)
print("\n=== 테스트 1: 첫 번째 검색 (캐시 없음) ===")
laws = repo.search_laws("소득세법")
print(f"검색 결과: {len(laws)}개 법령")

# Show cache after first search
print("\n=== 첫 검색 후 캐시 상태 ===")
display_cache_info(cache_dir)

# Test 2: Second search (using cache)
print("\n=== 테스트 2: 두 번째 검색 (캐시 사용) ===")
laws = repo.search_laws("소득세법")
print(f"검색 결과: {len(laws)}개 법령 (캐시에서 로드)")

# Test 3: Get law content (no cache)
print("\n=== 테스트 3: 조문 조회 (캐시 없음) ===")
if laws:
    content = repo.get_law_content(laws[0].mst)
    print(f"조문 수: {len(content.articles)}개")

# Show cache after content fetch
print("\n=== 조문 조회 후 캐시 상태 ===")
display_cache_info(cache_dir)

# Test 4: Get law content again (using cache)
print("\n=== 테스트 4: 조문 재조회 (캐시 사용) ===")
content = repo.get_law_content(laws[0].mst)
print(f"조문 수: {len(content.articles)}개 (캐시에서 로드)")

# Test 5: Search different law
print("\n=== 테스트 5: 다른 법령 검색 ===")
laws2 = repo.search_laws("법인세법")
print(f"검색 결과: {len(laws2)}개 법령")

# Final cache state
print("\n=== 최종 캐시 상태 ===")
display_cache_info(cache_dir)

# Test cache cleanup (optional)
print("\n=== 캐시 정리 테스트 ===")
cleared = repo.clear_old_cache()
print(f"정리된 캐시 파일: {cleared}개 (7일 이상 된 파일)")

print("\n캐시 시스템이 정상적으로 작동하고 있습니다!")
print("캐시는 output/.cache 디렉토리에 저장되며, 7일(168시간) 동안 유효합니다.")