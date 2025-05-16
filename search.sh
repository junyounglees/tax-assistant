#!/bin/bash
# Simple law search script

if [ $# -eq 0 ]; then
    echo "사용법: ./search.sh [검색어]"
    echo "예시: ./search.sh 소득세법"
    exit 1
fi

python code/law_search_cli.py "$@"