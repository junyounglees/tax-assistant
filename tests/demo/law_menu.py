#!/usr/bin/env python3
import requests
import json
import sys
import os

def search_law(query, email_id='lee'):
    """Search for laws"""
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        'OC': email_id,
        'target': 'law',
        'type': 'JSON',
        'query': query,
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
    except:
        return []

def clear_screen():
    """Clear terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def main_menu():
    """Simple interactive menu"""
    while True:
        clear_screen()
        print("=== 법령 검색 시스템 ===")
        print("\n자주 찾는 법령:")
        print("1. 소득세법")
        print("2. 법인세법")
        print("3. 부가가치세법")
        print("4. 상속세 및 증여세법")
        print("5. 민법")
        print("6. 상법")
        print("7. 근로기준법")
        print("\n8. 직접 검색")
        print("0. 종료")
        print("\n" + "="*20)
        
        choice = input("선택: ").strip()
        
        if choice == '0':
            print("종료합니다.")
            break
        
        # Search query based on choice
        queries = {
            '1': '소득세법',
            '2': '법인세법',
            '3': '부가가치세법',
            '4': '상속세 및 증여세법',
            '5': '민법',
            '6': '상법',
            '7': '근로기준법'
        }
        
        if choice in queries:
            query = queries[choice]
        elif choice == '8':
            query = input("\n검색어 입력: ").strip()
            if not query:
                continue
        else:
            print("잘못된 선택입니다.")
            input("\nEnter를 눌러 계속...")
            continue
        
        # Search and display results
        print(f"\n'{query}' 검색 중...")
        results = search_law(query)
        
        if results:
            clear_screen()
            print(f"=== '{query}' 검색 결과 ===")
            print(f"총 {len(results)}개 발견\n")
            
            for i, law in enumerate(results[:10], 1):
                print(f"{i}. {law.get('법령명한글', '')}")
                print(f"   MST: {law.get('법령일련번호', '')}")
                print(f"   시행일: {law.get('시행일자', '')}")
                print()
            
            print("\n옵션:")
            print("번호 입력: 상세 정보 보기")
            print("s: 결과 저장")
            print("m: 메인 메뉴")
            
            choice = input("\n선택: ").strip()
            
            if choice.lower() == 'm':
                continue
            elif choice.lower() == 's':
                filename = f"output/{query}_검색결과.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"\n저장완료: {filename}")
                input("Enter를 눌러 계속...")
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    law = results[idx]
                    clear_screen()
                    print(f"=== {law.get('법령명한글', '')} ===")
                    print(f"법령구분: {law.get('법령구분명', '')}")
                    print(f"MST: {law.get('법령일련번호', '')}")
                    print(f"시행일: {law.get('시행일자', '')}")
                    print(f"공포일: {law.get('공포일자', '')}")
                    print(f"소관부처: {law.get('소관부처명', '')}")
                    
                    mst = law.get('법령일련번호', '')
                    print(f"\n전문 조회 명령어:")
                    print(f"python code/get_law_full_text.py {mst}")
                    
                    input("\nEnter를 눌러 계속...")
        else:
            print("검색 결과가 없습니다.")
            input("\nEnter를 눌러 계속...")

if __name__ == "__main__":
    main_menu()