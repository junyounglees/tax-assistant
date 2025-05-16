import requests
import json

def get_income_tax_law_list():
    """Get Income Tax Law list using the Open API with proper formatting"""
    
    # API endpoint
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    
    # Parameters with your specifications
    params = {
        'OC': 'lee',          # Your email ID
        'target': 'law',      # Law search
        'type': 'JSON',       # JSON format  
        'query': '소득세법',    # Income Tax Law
        'display': '100',     # Get up to 100 results
        'sort': 'lawNm',      # Sort by law name
    }
    
    try:
        print("소득세법 목록 조회 중...")
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
            with open('income_tax_law_list_full.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("전체 응답 데이터를 income_tax_law_list_full.json 파일로 저장했습니다.")
            
            # Extract laws from response
            if 'LawSearch' in data and 'law' in data['LawSearch']:
                laws = data['LawSearch']['law']
                
                print(f"\n총 {len(laws)}개의 소득세법 관련 법령을 찾았습니다.")
                print("="*50)
                
                # Create formatted list
                law_list = []
                
                for i, law in enumerate(laws):
                    law_info = {
                        '순번': i + 1,
                        '법령명': law.get('법령명한글', ''),
                        '법령구분': law.get('법령구분명', ''),
                        '시행일': law.get('시행일자', ''),
                        '공포일': law.get('공포일자', ''),
                        '소관부처': law.get('소관부처명', ''),
                        '법령일련번호': law.get('법령일련번호', ''),
                        'MST': law.get('법령일련번호', ''),  # MST is the same as 법령일련번호
                        '상세링크': law.get('법령상세링크', '')
                    }
                    law_list.append(law_info)
                    
                    # Print summary of each law
                    print(f"\n{i+1}. {law_info['법령명']}")
                    print(f"   법령구분: {law_info['법령구분']}")
                    print(f"   시행일: {law_info['시행일']}")
                    print(f"   공포일: {law_info['공포일']}")
                    print(f"   소관부처: {law_info['소관부처']}")
                    print(f"   법령일련번호 (MST): {law_info['MST']}")
                    
                # Save formatted list
                with open('income_tax_law_list_formatted.json', 'w', encoding='utf-8') as f:
                    json.dump(law_list, f, ensure_ascii=False, indent=2)
                
                print("\n정리된 목록을 income_tax_law_list_formatted.json 파일로 저장했습니다.")
                
                # Show how to access full text
                print("\n각 법령의 전문을 조회하려면:")
                print("API URL: http://www.law.go.kr/DRF/lawService.do")
                print("파라미터: OC=lee, target=law, type=JSON, MST=[법령일련번호]")
                
                if laws:
                    first_law = laws[0]
                    print(f"\n예시 - {first_law.get('법령명한글')} 전문 조회:")
                    print(f"http://www.law.go.kr/DRF/lawService.do?OC=lee&target=law&type=JSON&MST={first_law.get('법령일련번호')}")
                
                return law_list
                
            else:
                print("\n법령 목록을 찾을 수 없습니다.")
                print(f"응답 구조: {list(data.keys())}")
                
        else:
            print(f"API 오류: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"오류 발생: {e}")
    
    return None

if __name__ == "__main__":
    law_list = get_income_tax_law_list()
    
    if law_list:
        print(f"\n\n총 {len(law_list)}개의 법령을 성공적으로 조회했습니다.")