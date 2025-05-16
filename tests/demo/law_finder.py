#!/usr/bin/env python3
import requests
import json
import sys

# Common law name mappings
LAW_MAPPINGS = {
    # Tax laws
    '소득세': '소득세법',
    '법인세': '법인세법',
    '부가세': '부가가치세법',
    '상증세': '상속세 및 증여세법',
    '종부세': '종합부동산세법',
    
    # Commercial law
    '상법': '상법시행법',  # API quirk
    
    # Civil law
    '민법': '민법',
    
    
    # Labor law
    '노동법': '근로기준법',
    '근로법': '근로기준법'
}

# Direct MST mappings for common laws
DIRECT_MST = {
    '상법': 1099,  # Commercial Code
    '민법': 265307,  # Civil Code
}

def search_law(query, email_id='lee', display=10):
    """Search for laws with improved query handling"""
    
    # Check for mappings
    mapped_query = LAW_MAPPINGS.get(query, query)
    
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    params = {
        'OC': email_id,
        'target': 'law',
        'type': 'JSON',
        'query': mapped_query,
        'display': str(display)
    }
    
    print(f"검색어: '{query}' → '{mapped_query}'")
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'LawSearch' in data and 'law' in data['LawSearch']:
            laws = data['LawSearch']['law']
            if isinstance(laws, dict):
                laws = [laws]
            
            # Filter results to find exact matches
            exact_matches = []
            partial_matches = []
            
            for law in laws:
                law_name = law.get('법령명한글', '')
                if query in law_name or mapped_query in law_name:
                    if law_name == query or law_name == mapped_query:
                        exact_matches.insert(0, law)
                    else:
                        exact_matches.append(law)
                else:
                    partial_matches.append(law)
            
            # Combine results
            filtered_laws = exact_matches + partial_matches
            
            if not filtered_laws and query in DIRECT_MST:
                # Use direct MST for known laws
                print(f"직접 MST 사용: {DIRECT_MST[query]}")
                return [{'법령명한글': query, '법령일련번호': str(DIRECT_MST[query])}]
            
            return filtered_laws[:display]
        
        return []
        
    except Exception as e:
        print(f"오류: {e}")
        return []

def display_results(laws, query):
    """Display search results"""
    print(f"\n검색 결과: {len(laws)}개")
    print("-" * 50)
    
    for i, law in enumerate(laws, 1):
        print(f"\n{i}. {law.get('법령명한글', '')}")
        print(f"   법령구분: {law.get('법령구분명', '')}")
        print(f"   MST: {law.get('법령일련번호', '')}")
        print(f"   시행일: {law.get('시행일자', '')}")
    
    if laws:
        print("\n" + "-" * 50)
        print("전문 조회:")
        print(f"python code/get_law_full_text.py {laws[0].get('법령일련번호', '')}")
    
    # Save results
    filename = f"output/{query}_검색결과.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(laws, f, ensure_ascii=False, indent=2)
    print(f"\n결과 저장: {filename}")

def main():
    if len(sys.argv) < 2:
        print("사용법: python law_finder.py [검색어]")
        print("\n자주 사용하는 법령:")
        for key, value in LAW_MAPPINGS.items():
            print(f"  {key} → {value}")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    laws = search_law(query)
    display_results(laws, query)

if __name__ == "__main__":
    main()