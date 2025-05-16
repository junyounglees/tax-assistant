#!/usr/bin/env python3
"""Test article content parsing."""
import json
from src.domain.entities.article import Article, LawContent

# Load raw data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Parse the law content
law_content = LawContent.from_api_response(data)

# Find 제1조의2 (정의)
print("Looking for 제1조의2 (정의)...")
for article in law_content.articles[:10]:
    if article.article_title == '정의' and article.article_number == '1':
        print(f"\nFound: {article.formatted_number}")
        print(f"Title: {article.article_title}")
        print(f"Content length: {len(article.article_content)}")
        print(f"Content preview: {article.article_content[:200]}...")
        break

# Also check a regular article
print("\n\nChecking regular article (제3조)...")
for article in law_content.articles:
    if article.article_number == '3':
        print(f"Found: {article.formatted_number}")
        print(f"Title: {article.article_title}")
        print(f"Content length: {len(article.article_content)}")
        print(f"Content preview: {article.article_content[:200]}...")
        break