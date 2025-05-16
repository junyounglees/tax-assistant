#!/usr/bin/env python3
import requests
import json
import sys

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

def main():
    # If argument provided, search directly
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        # Show menu and get input
        print("\n=== 법령 검색 ===")
        print("1. 소득세법")
        print("2. 법인세법") 
        print("3. 부가가치세법")
        print("4. 상속세 및 증여세법")
        print("5. 민법")
        print("6. 상법")
        print("7. 근로기준법")
        print("8. 직접 입력")
        
        try:
            choice = input("\n번호 선택: ").strip()
            
            laws = {
                '1': '소득세법',
                '2': '법인세법',
                '3': '부가가치세법',
                '4': '상속세 및 증여세법',
                '5': '민법',
                '6': '상법',
                '7': '근로기준법'
            }
            
            if choice in laws:
                query = laws[choice]
            elif choice == '8':
                query = input("검색어: ").strip()
            else:
                print("잘못된 선택")
                return
        except:
            return
    
    # Search
    print(f"\n'{query}' 검색 중...")
    results = search_law(query)
    
    if results:
        print(f"\n검색 결과: {len(results)}개\n")
        
        for i, law in enumerate(results[:10], 1):
            print(f"{i}. {law.get('법령명한글', '')}")
            print(f"   MST: {law.get('법령일련번호', '')}")
            print(f"   시행일: {law.get('시행일자', '')}\n")
        
        # Save results
        filename = f"output/{query}_검색결과.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"결과 저장: {filename}")
        
        # Show full text command for first result
        if results:
            mst = results[0].get('법령일련번호', '')
            print(f"\n전문 조회: python code/get_law_full_text.py {mst}")
    else:
        print("검색 결과 없음")

if __name__ == "__main__":
    main()