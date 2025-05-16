import requests
import json

def search_and_select():
    """Simple interactive law search"""
    
    while True:
        # Get search query
        query = input("\n법령 검색 (종료:q): ").strip()
        
        if query.lower() in ['q', 'quit', 'exit']:
            print("종료합니다.")
            break
            
        if not query:
            continue
        
        # Search
        url = "http://www.law.go.kr/DRF/lawSearch.do"
        params = {
            'OC': 'lee',
            'target': 'law',
            'type': 'JSON',
            'query': query,
            'display': '20'
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'LawSearch' in data and 'law' in data['LawSearch']:
            laws = data['LawSearch']['law']
            
            # Handle single result
            if isinstance(laws, dict):
                laws = [laws]
            
            # Display results
            print(f"\n검색 결과 ({len(laws)}개):")
            print("-" * 40)
            
            for i, law in enumerate(laws, 1):
                print(f"{i}. {law.get('법령명한글', '')}")
                print(f"   MST: {law.get('법령일련번호', '')}")
                print()
            
            # Select
            choice = input("번호 선택 (검색으로 돌아가기: Enter): ").strip()
            
            if choice.isdigit():
                num = int(choice)
                if 1 <= num <= len(laws):
                    selected = laws[num-1]
                    print(f"\n선택: {selected.get('법령명한글', '')}")
                    mst = selected.get('법령일련번호', '')
                    
                    print(f"전문 조회 URL:")
                    print(f"http://www.law.go.kr/DRF/lawService.do?OC=lee&target=law&type=JSON&MST={mst}")
        else:
            print("검색 결과가 없습니다.")

if __name__ == "__main__":
    print("=== 법령 검색 프로그램 ===")
    search_and_select()