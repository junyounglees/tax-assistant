#!/usr/bin/env python3
"""Test article parsing with updated structure."""
import json
from src.domain.entities.article import LawContent

# Load and parse test data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Parse the response
law_content = LawContent.from_api_response(data)

# Print results
print(f"Law Name: {law_content.law_name}")
print(f"Law ID: {law_content.law_id}")
print(f"MST: {law_content.mst}")
print(f"Total Articles: {len(law_content.articles)}")

# Show first 5 articles
print("\nFirst 5 articles:")
for i, article in enumerate(law_content.articles[:5]):
    print(f"\n{i+1}. {article.formatted_number}")
    print(f"   Title: {article.article_title or 'No title'}")
    print(f"   Content: {article.article_content[:100]}...")