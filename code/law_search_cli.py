#!/usr/bin/env python3
import requests
import json
import sys

def search_law(query, email_id='lee'):
    """Search for laws and display results"""
    
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
            
            # Handle single result
            if isinstance(laws, dict):
                laws = [laws]
            
            # Display results
            print(f"\n검색어: '{query}'")
            print(f"검색 결과: {len(laws)}개")
            print("-" * 50)
            
            for i, law in enumerate(laws, 1):
                print(f"\n{i}. {law.get('법령명한글', '')}")
                print(f"   법령구분: {law.get('법령구분명', '')}")
                print(f"   MST: {law.get('법령일련번호', '')}")
                print(f"   시행일: {law.get('시행일자', '')}")
            
            print("\n" + "-" * 50)
            print("전문 조회하려면:")
            print("python code/get_law_full_text.py [MST번호]")
            
            # Save results
            filename = f"output/{query.replace(' ', '_')}_검색결과.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(laws, f, ensure_ascii=False, indent=2)
            print(f"\n결과가 {filename}에 저장되었습니다.")
            
            return laws
        else:
            print(f"'{query}'에 대한 검색 결과가 없습니다.")
            return []
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("사용법: python law_search_cli.py [검색어]")
        print("예시: python law_search_cli.py 소득세법")
        print("     python law_search_cli.py 민법")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search_law(query)

if __name__ == "__main__":
    main()