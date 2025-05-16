#!/usr/bin/env python3
"""Test script to check cache file name printing."""

import sys
from unittest.mock import patch
from src.infrastructure.container import Container

def test_cache_filename_display():
    """Test if cache filename is displayed when using cached data."""
    container = Container()
    controller = container.cli_controller
    
    # Simulate user selecting '소득세법' (option 1) then viewing articles
    user_inputs = ['1', 'y', '0', '0']
    
    with patch('builtins.input', side_effect=user_inputs):
        print("Testing cache filename display...")
        controller.run_interactive_search()

if __name__ == '__main__':
    test_cache_filename_display()