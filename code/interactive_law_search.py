import requests
import json
import sys

class LawSearcher:
    def __init__(self, email_id='lee'):
        self.email_id = email_id
        self.current_laws = []
        self.current_query = ''
    
    def search_law(self, query):
        """Search for laws matching the query"""
        url = "http://www.law.go.kr/DRF/lawSearch.do"
        params = {
            'OC': self.email_id,
            'target': 'law',
            'type': 'JSON',
            'query': query,
            'display': '100',
            'sort': 'lawNm'
        }
        
        try:
            response = requests.get(url, params=params)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                data = response.json()
                
                if 'LawSearch' in data and 'law' in data['LawSearch']:
                    laws = data['LawSearch']['law']
                    # Handle single result case
                    if isinstance(laws, dict):
                        laws = [laws]
                    
                    self.current_laws = laws
                    self.current_query = query
                    return True
                else:
                    print(f"\n'{query}'에 대한 검색 결과가 없습니다.")
                    return False
            else:
                print(f"API 오류: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"오류 발생: {e}")
            return False
    
    def display_results(self):
        """Display search results with numbers"""
        print(f"\n'{self.current_query}' 검색 결과: {len(self.current_laws)}개")
        print("="*60)
        
        for i, law in enumerate(self.current_laws, 1):
            print(f"\n{i}. {law.get('법령명한글', '')}")
            print(f"   법령구분: {law.get('법령구분명', '')}")
            print(f"   시행일: {law.get('시행일자', '')}")
            print(f"   MST: {law.get('법령일련번호', '')}")
    
    def get_full_text_url(self, law_index):
        """Get the full text URL for a selected law"""
        if 0 <= law_index < len(self.current_laws):
            law = self.current_laws[law_index]
            mst = law.get('법령일련번호', '')
            return f"http://www.law.go.kr/DRF/lawService.do?OC={self.email_id}&target=law&type=JSON&MST={mst}"
        return None
    
    def save_selected_law(self, law_index):
        """Save information about the selected law"""
        if 0 <= law_index < len(self.current_laws):
            law = self.current_laws[law_index]
            filename = f"{law.get('법령명한글', '').replace(' ', '_')}_정보.json"
            
            law_info = {
                '법령명': law.get('법령명한글', ''),
                'MST': law.get('법령일련번호', ''),
                '시행일': law.get('시행일자', ''),
                '전문조회URL': self.get_full_text_url(law_index),
                '상세정보': law
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(law_info, f, ensure_ascii=False, indent=2)
            
            print(f"\n법령 정보가 '{filename}'에 저장되었습니다.")
            return filename
        return None
    
    def run_interactive(self):
        """Run interactive search session"""
        print("=== 법령 검색 프로그램 ===")
        print("종료하려면 'exit' 또는 'quit'를 입력하세요.\n")
        
        while True:
            # Get search query
            query = input("\n검색할 법령명 입력 (예: 소득세법, 민법, 상증세법): ").strip()
            
            if query.lower() in ['exit', 'quit', '종료']:
                print("\n프로그램을 종료합니다.")
                break
            
            if not query:
                print("검색어를 입력해주세요.")
                continue
            
            # Search for laws
            if self.search_law(query):
                self.display_results()
                
                # Get user selection
                while True:
                    print("\n" + "="*60)
                    print("옵션: 번호 입력(1,2,3...) | 다시 검색(s) | 종료(q)")
                    choice = input("선택: ").strip().lower()
                    
                    if choice == 'q':
                        print("\n프로그램을 종료합니다.")
                        return
                    elif choice == 's':
                        break
                    elif choice.isdigit():
                        num = int(choice)
                        if 1 <= num <= len(self.current_laws):
                            law = self.current_laws[num-1]
                            print(f"\n선택한 법령: {law.get('법령명한글', '')}")
                            
                            # Show options for selected law
                            print("\n1. 법령 정보 저장")
                            print("2. 전문 조회 URL 보기")
                            print("3. 돌아가기")
                            
                            sub_choice = input("\n선택: ").strip()
                            
                            if sub_choice == '1':
                                self.save_selected_law(num-1)
                            elif sub_choice == '2':
                                url = self.get_full_text_url(num-1)
                                print(f"\n전문 조회 URL:\n{url}")
                                print("\n이 URL로 법령 전문을 JSON 형식으로 받을 수 있습니다.")
                            
                        else:
                            print(f"1부터 {len(self.current_laws)} 사이의 숫자를 입력하세요.")
                    else:
                        print("올바른 옵션을 선택하세요.")

def main():
    # Check for command line arguments
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
        searcher = LawSearcher()
        if searcher.search_law(query):
            searcher.display_results()
    else:
        # Interactive mode
        searcher = LawSearcher()
        searcher.run_interactive()

if __name__ == "__main__":
    main()