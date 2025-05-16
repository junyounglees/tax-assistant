#!/usr/bin/env python3
"""Test cache file display during search."""

from unittest.mock import patch
from src.infrastructure.container import Container

def test_search_cache_display():
    """Test cache file display during law search."""
    container = Container()
    controller = container.cli_controller
    
    print("=== Test: Search Cache File Display ===")
    
    # Simulate user selecting option 1 (소득세법) then exiting
    user_inputs = ['1', '0', '0']  # 1=select 소득세법, 0=don't view articles, 0=exit
    
    with patch('builtins.input', side_effect=user_inputs):
        try:
            controller.run_interactive_search()
        except (SystemExit, StopIteration):
            pass

if __name__ == '__main__':
    test_search_cache_display()