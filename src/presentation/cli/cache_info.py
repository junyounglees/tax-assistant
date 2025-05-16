"""Cache information display utility."""
import os
from datetime import datetime


def get_cache_info(cache_dir: str) -> dict:
    """Get information about the cache directory."""
    if not os.path.exists(cache_dir):
        return {
            'exists': False,
            'files': 0,
            'size': 0,
            'oldest': None,
            'newest': None
        }
    
    files = []
    total_size = 0
    
    for filename in os.listdir(cache_dir):
        filepath = os.path.join(cache_dir, filename)
        if os.path.isfile(filepath):
            stat = os.stat(filepath)
            files.append({
                'name': filename,
                'size': stat.st_size,
                'mtime': stat.st_mtime
            })
            total_size += stat.st_size
    
    if not files:
        return {
            'exists': True,
            'files': 0,
            'size': 0,
            'oldest': None,
            'newest': None
        }
    
    files.sort(key=lambda x: x['mtime'])
    
    return {
        'exists': True,
        'files': len(files),
        'size': total_size,
        'oldest': datetime.fromtimestamp(files[0]['mtime']),
        'newest': datetime.fromtimestamp(files[-1]['mtime']),
        'file_list': files
    }


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def display_cache_info(cache_dir: str) -> None:
    """Display cache information."""
    info = get_cache_info(cache_dir)
    
    if not info['exists']:
        print("캐시 디렉토리가 존재하지 않습니다.")
        return
    
    print(f"\n=== 캐시 정보 ===")
    print(f"캐시 파일 수: {info['files']}개")
    print(f"전체 크기: {format_size(info['size'])}")
    
    if info['files'] > 0:
        print(f"가장 오래된 파일: {info['oldest'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"가장 최근 파일: {info['newest'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n캐시 파일 목록:")
        for file in info['file_list']:
            age_hours = (datetime.now().timestamp() - file['mtime']) / 3600
            print(f"  - {file['name']} ({format_size(file['size'])}, {age_hours:.1f}시간 전)")
    
    print("=" * 20)