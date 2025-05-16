#!/usr/bin/env python3
"""Debug article content structure."""
import json
from src.domain.entities.article import LawContent, Article

# Load and parse test data
with open('debug_law_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Parse the response
law_content = LawContent.from_api_response(data)

# Check an article that has content
for article in law_content.articles[:5]:
    print(f"Article {article.article_number}:")
    print(f"  Title: {article.article_title}")
    print(f"  Content type: {type(article.article_content)}")
    print(f"  Content: {repr(article.article_content[:100])}")
    print()