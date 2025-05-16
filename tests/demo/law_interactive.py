#!/usr/bin/env python3
import requests
import json
import sys

# Common law name mappings
LAW_MAPPINGS = {
    '소득세': '소득세법',
    '법인세': '법인세법',
    '부가세': '부가가치세법',
    '상증세': '상속세 및 증여세법',
    '종부세': '종합부동산세법',
    '상법': '상법시행법',
    '민법': '민법',
    '노동법': '근로기준법',
    '근로법': '근로기준법'
}

def search_law(query, email_id='lee'):
    """Search for laws"""
    mapped_query = LAW_MAPPINGS.get(query, query)
    
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        'OC': email_id,
        'target': 'law',
        'type': 'JSON',
        'query': mapped_query,
        'display': '20'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'LawSearch' in data and 'law' in data['LawSearch']:
            laws = data['LawSearch']['law']
            if isinstance(laws, dict):
                laws = [laws]
            return laws
        return []
    except Exception as e:
        print(f"오류: {e}")
        return []

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("법령 검색 시스템")
    print("="*50)
    print("1. 법령 검색")
    print("2. 자주 찾는 법령")
    print("3. 최근 검색 기록")
    print("4. 종료")
    print("="*50)

def display_common_laws():
    """Display frequently searched laws"""
    print("\n자주 찾는 법령:")
    print("-"*30)
    common_laws = [
        ('1', '소득세법'),
        ('2', '법인세법'),
        ('3', '부가가치세법'),
        ('4', '상속세 및 증여세법'),
        ('5', '민법'),
        ('6', '상법'),
        ('7', '근로기준법'),
        ('8', '뒤로가기')
    ]
    
    for num, law in common_laws:
        print(f"{num}. {law}")
    
    choice = input("\n선택: ").strip()
    
    if choice == '8':
        return None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(common_laws) - 1:
            return common_laws[idx][1]
    except:
        pass
    
    print("잘못된 선택입니다.")
    return None

def display_search_results(laws):
    """Display search results with numbers"""
    print(f"\n검색 결과: {len(laws)}개")
    print("-"*50)
    
    for i, law in enumerate(laws, 1):
        print(f"{i}. {law.get('법령명한글', '')}")
        print(f"   법령구분: {law.get('법령구분명', '')}")
        print(f"   MST: {law.get('법령일련번호', '')}")
        print(f"   시행일: {law.get('시행일자', '')}")
        print()
    
    print("0. 새로운 검색")
    print("-"*50)

def get_law_actions(law):
    """Display actions for selected law"""
    print(f"\n선택한 법령: {law.get('법령명한글', '')}")
    print("-"*30)
    print("1. 법령 정보 저장")
    print("2. 전문 조회 URL 보기")
    print("3. 전문 다운로드")
    print("4. 뒤로가기")
    
    choice = input("\n선택: ").strip()
    
    if choice == '1':
        save_law_info(law)
    elif choice == '2':
        show_full_text_url(law)
    elif choice == '3':
        download_full_text(law)
    elif choice == '4':
        return
    else:
        print("잘못된 선택입니다.")

def save_law_info(law):
    """Save law information"""
    filename = f"output/{law.get('법령명한글', '').replace(' ', '_')}_정보.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(law, f, ensure_ascii=False, indent=2)
    print(f"\n정보가 {filename}에 저장되었습니다.")
    input("\n계속하려면 Enter를 누르세요...")

def show_full_text_url(law):
    """Show full text URL"""
    mst = law.get('법령일련번호', '')
    url = f"http://www.law.go.kr/DRF/lawService.do?OC=lee&target=law&type=JSON&MST={mst}"
    print(f"\n전문 조회 URL:")
    print(url)
    print(f"\n명령어: python code/get_law_full_text.py {mst}")
    input("\n계속하려면 Enter를 누르세요...")

def download_full_text(law):
    """Download full text of law"""
    mst = law.get('법령일련번호', '')
    print(f"\n전문 다운로드 중...")
    
    # Call the full text downloader
    import subprocess
    try:
        result = subprocess.run(
            ['python', 'code/get_law_full_text.py', mst],
            capture_output=True,
            text=True
        )
        print(result.stdout)
    except Exception as e:
        print(f"오류: {e}")
    
    input("\n계속하려면 Enter를 누르세요...")

def load_search_history():
    """Load recent search history"""
    try:
        with open('output/search_history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_search_history(query, history):
    """Save search history"""
    if query not in history:
        history.insert(0, query)
        history = history[:10]  # Keep only last 10
    
    with open('output/search_history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def display_search_history(history):
    """Display search history"""
    if not history:
        print("\n최근 검색 기록이 없습니다.")
        input("\nEnter를 눌러 계속...")
        return None
    
    print("\n최근 검색:")
    print("-"*30)
    for i, query in enumerate(history, 1):
        print(f"{i}. {query}")
    print("0. 뒤로가기")
    
    choice = input("\n선택: ").strip()
    
    if choice == '0':
        return None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(history):
            return history[idx]
    except:
        pass
    
    print("잘못된 선택입니다.")
    return None

def main():
    """Main interactive loop"""
    print("법령 검색 프로그램")
    
    search_history = load_search_history()
    current_results = []
    
    while True:
        if not current_results:
            display_menu()
            choice = input("선택: ").strip()
            
            if choice == '1':
                # Direct search
                query = input("\n검색할 법령명: ").strip()
                if query:
                    print(f"\n'{query}' 검색 중...")
                    current_results = search_law(query)
                    if current_results:
                        save_search_history(query, search_history)
                        search_history = load_search_history()
                    else:
                        print("검색 결과가 없습니다.")
                        input("\nEnter를 눌러 계속...")
            
            elif choice == '2':
                # Common laws
                selected = display_common_laws()
                if selected:
                    print(f"\n'{selected}' 검색 중...")
                    current_results = search_law(selected)
                    if current_results:
                        save_search_history(selected, search_history)
                        search_history = load_search_history()
            
            elif choice == '3':
                # Search history
                selected = display_search_history(search_history)
                if selected:
                    print(f"\n'{selected}' 검색 중...")
                    current_results = search_law(selected)
            
            elif choice == '4':
                print("\n프로그램을 종료합니다.")
                break
            
            else:
                print("잘못된 선택입니다.")
        
        else:
            # Show search results
            display_search_results(current_results)
            choice = input("번호 선택 (0: 새 검색): ").strip()
            
            if choice == '0':
                current_results = []
                continue
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(current_results):
                    selected_law = current_results[idx]
                    get_law_actions(selected_law)
                else:
                    print("잘못된 선택입니다.")
            except:
                print("숫자를 입력하세요.")

if __name__ == "__main__":
    main()