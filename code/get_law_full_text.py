#!/usr/bin/env python3
import requests
import json
import sys

def get_law_full_text(mst, email_id='lee'):
    """Get full text of a law using MST number"""
    
    url = "http://www.law.go.kr/DRF/lawService.do"
    params = {
        'OC': email_id,
        'target': 'law',
        'type': 'JSON',
        'MST': mst
    }
    
    try:
        print(f"MST {mst} 법령 전문 조회 중...")
        response = requests.get(url, params=params)
        data = response.json()
        
        # Extract law information
        if 'law' in data:
            law_data = data['law'][0] if isinstance(data['law'], list) else data['law']
            
            law_info = {
                '법령명': law_data.get('법령명한글', ''),
                'MST': mst,
                '시행일': law_data.get('시행일자', ''),
                '공포일': law_data.get('공포일자', ''),
                '소관부처': law_data.get('소관부처명', ''),
                '조문수': len(law_data.get('조문', [])),
                '전문URL': response.url
            }
            
            print(f"\n법령명: {law_info['법령명']}")
            print(f"시행일: {law_info['시행일']}")
            print(f"조문수: {law_info['조문수']}")
            
            # Save full data
            filename = f"output/{law_info['법령명'].replace(' ', '_')}_전문.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"\n전문이 {filename}에 저장되었습니다.")
            
            # Show first few articles
            if '조문' in law_data:
                print("\n처음 3개 조문:")
                for i, article in enumerate(law_data['조문'][:3], 1):
                    print(f"\n{article.get('조문번호', '')}")
                    print(f"{article.get('조문내용', '')[:100]}...")
            
            return data
        else:
            print("법령 정보를 찾을 수 없습니다.")
            return None
            
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("사용법: python get_law_full_text.py [MST번호]")
        print("예시: python get_law_full_text.py 267581")
        sys.exit(1)
    
    mst = sys.argv[1]
    get_law_full_text(mst)

if __name__ == "__main__":
    main()