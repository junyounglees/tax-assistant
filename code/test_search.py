import requests
import json

# Test different search terms
search_terms = [
    "상법",
    "commercial",
    "회사법",
    "주식회사",
    "유한회사"
]

url = "http://www.law.go.kr/DRF/lawSearch.do"

for term in search_terms:
    params = {
        'OC': 'lee',
        'target': 'law',
        'type': 'JSON',
        'query': term,
        'display': '5'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    print(f"\n검색어: '{term}'")
    
    if 'LawSearch' in data and 'law' in data['LawSearch']:
        laws = data['LawSearch']['law']
        if isinstance(laws, dict):
            laws = [laws]
        
        for law in laws[:3]:
            print(f"  - {law.get('법령명한글', '')}")
    else:
        print("  검색 결과 없음")