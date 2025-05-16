import requests
import json
import sys

def search_law(email_id='lee', query='', display=100):
    """Search for any law using the Open API"""
    
    # API endpoint
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    
    # Parameters
    params = {
        'OC': email_id,       # Email ID
        'target': 'law',      # Law search
        'type': 'JSON',       # JSON format  
        'query': query,       # Search query
        'display': str(display),  # Number of results
        'sort': 'lawNm',      # Sort by law name
    }
    
    try:
        print(f"\n'{query}' 관련 법령 검색 중...")
        print(f"요청 URL: {url}")
        print(f"파라미터: {params}")
        
        # Make the API request
        response = requests.get(url, params=params)
        response.encoding = 'utf-8'
        
        print(f"\n응답 상태 코드: {response.status_code}")
        
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Save the response
            filename = f"{query.replace(' ', '_')}_법령목록.json" if query else "법령목록.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"전체 응답 데이터를 {filename} 파일로 저장했습니다.")
            
            # Extract laws from response
            if 'LawSearch' in data and 'law' in data['LawSearch']:
                laws = data['LawSearch']['law']
                
                print(f"\n총 {len(laws)}개의 '{query}' 관련 법령을 찾았습니다.")
                print("="*60)
                
                # Display results
                for i, law in enumerate(laws):
                    print(f"\n{i+1}. {law.get('법령명한글', '')}")
                    print(f"   법령구분: {law.get('법령구분명', '')}")
                    print(f"   시행일: {law.get('시행일자', '')}")
                    print(f"   공포일: {law.get('공포일자', '')}")
                    print(f"   소관부처: {law.get('소관부처명', '')}")
                    print(f"   법령일련번호 (MST): {law.get('법령일련번호', '')}")
                
                # Show how to access full text
                if laws:
                    print("\n" + "="*60)
                    print("각 법령의 전문을 조회하려면:")
                    print("API URL: http://www.law.go.kr/DRF/lawService.do")
                    print(f"파라미터: OC={email_id}, target=law, type=JSON, MST=[법령일련번호]")
                    
                    first_law = laws[0]
                    print(f"\n예시 - {first_law.get('법령명한글')} 전문 조회:")
                    print(f"http://www.law.go.kr/DRF/lawService.do?OC={email_id}&target=law&type=JSON&MST={first_law.get('법령일련번호')}")
                
                return laws
                
            else:
                print("\n법령 목록을 찾을 수 없습니다.")
                
        else:
            print(f"API 오류: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    
    return None

def main():
    """Main function for interactive law search"""
    
    # Check if query is provided as command line argument
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    else:
        # Interactive mode
        query = input("\n검색할 법령명을 입력하세요 (예: 소득세법, 민법, 형법): ").strip()
    
    if not query:
        print("검색어를 입력해주세요.")
        return
    
    # Email ID (change this if needed)
    email_id = 'lee'
    
    # Number of results
    display = 100
    
    # Search for laws
    laws = search_law(email_id=email_id, query=query, display=display)
    
    if laws:
        print(f"\n\n총 {len(laws)}개의 법령을 성공적으로 조회했습니다.")

if __name__ == "__main__":
    main()