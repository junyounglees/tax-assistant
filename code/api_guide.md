# 법령 목록 조회 API 사용 가이드

## 1. API 엔드포인트
```
http://www.law.go.kr/DRF/lawSearch.do
```

## 2. 필수 파라미터
- `OC`: 이메일 ID (필수) - 예: 'lee'
- `target`: 검색 대상 (필수) - 'law' 고정
- `type`: 응답 형식 (필수) - 'JSON', 'XML', 'HTML' 중 선택

## 3. 선택 파라미터
- `query`: 법령명 검색어 - 예: '소득세법'
- `display`: 결과 개수 - 기본값 20, 최대 100
- `sort`: 정렬 기준 - 'lawNm'(법령명), 'date'(날짜) 등
- `page`: 페이지 번호

## 4. Python 코드 구조

### 기본 구조
```python
import requests
import json

def get_law_list():
    # API 엔드포인트
    url = "http://www.law.go.kr/DRF/lawSearch.do"
    
    # 파라미터 설정
    params = {
        'OC': 'lee',          # 이메일 ID
        'target': 'law',      # 검색 대상
        'type': 'JSON',       # 응답 형식
        'query': '소득세법',    # 검색어
        'display': '100'      # 결과 개수
    }
    
    # API 요청
    response = requests.get(url, params=params)
    response.encoding = 'utf-8'
    
    # JSON 파싱
    data = response.json()
    
    # 법령 목록 추출
    laws = data['LawSearch']['law']
    
    return laws
```

### 결과 처리
```python
# 목록 조회
laws = get_law_list()

# 결과 출력
for i, law in enumerate(laws):
    print(f"{i+1}. {law['법령명한글']}")
    print(f"   MST: {law['법령일련번호']}")
    print(f"   시행일: {law['시행일자']}")
```

## 5. 응답 데이터 구조
```json
{
  "LawSearch": {
    "law": [
      {
        "법령명한글": "소득세법",
        "법령일련번호": "267581",
        "시행일자": "20250101",
        "공포일자": "20241231",
        "소관부처명": "기획재정부",
        "법령구분명": "법률",
        "법령상세링크": "/DRF/lawService.do?..."
      }
    ]
  }
}
```

## 6. 전체 예제
```python
import requests
import json

# 1. 법령 목록 조회
url = "http://www.law.go.kr/DRF/lawSearch.do"
params = {
    'OC': 'lee',
    'target': 'law',
    'type': 'JSON',
    'query': '소득세법',
    'display': '100'
}

response = requests.get(url, params=params)
data = response.json()

# 2. 결과 저장
with open('law_list.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 3. 목록 출력
laws = data['LawSearch']['law']
for law in laws:
    print(f"법령명: {law['법령명한글']}")
    print(f"MST: {law['법령일련번호']}")
```

## 7. 주의사항
- API 응답은 UTF-8로 인코딩되어 있음
- 검색어는 URL 인코딩이 자동으로 처리됨
- 'test' 이메일 ID는 작동하지 않을 수 있음
- 실제 사용시 자신의 이메일 ID 사용 필요