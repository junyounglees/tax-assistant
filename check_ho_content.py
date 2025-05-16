#!/usr/bin/env python3
"""Check 호 content structure."""
import json

# Load raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

articles_data = data['법령']['조문']['조문단위']

# Check 호 content structure
print("Checking 호 content structure...")
for i, article in enumerate(articles_data[:20]):
    if '항' in article:
        for j, para in enumerate(article['항']):
            if isinstance(para, dict) and '호' in para:
                print(f"\nArticle {i}, Paragraph {j} has 호:")
                for k, item in enumerate(para['호']):
                    if isinstance(item, dict):
                        ho_content = item.get('호내용')
                        print(f"  호 {k}: type={type(ho_content)}")
                        if isinstance(ho_content, list):
                            print(f"    List with {len(ho_content)} items")
                            for l, sub_item in enumerate(ho_content):
                                print(f"      Item {l}: {type(sub_item)}")
                                if isinstance(sub_item, str):
                                    print(f"        {repr(sub_item[:50])}")
                        elif isinstance(ho_content, str):
                            print(f"    String: {repr(ho_content[:50])}")
                    break  # Just check first few
                break  # Just check first few