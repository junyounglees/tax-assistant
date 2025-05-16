#!/usr/bin/env python3
"""Test improved display with separators."""

from unittest.mock import patch
from src.infrastructure.container import Container

def test_improved_display():
    """Test the improved display with visual separators."""
    container = Container()
    controller = container.cli_controller
    
    print("=== Test: Improved Display with Separators ===")
    
    # Simulate user flow: search, select law, view article
    user_inputs = ['1', '1', '2', '1', '1', '0', '0', '0']  
    # 1=소득세법, 1=select 소득세법, 2=specific article, 1=article 1, 1=first match, 0=back, 0=back, 0=exit
    
    with patch('builtins.input', side_effect=user_inputs):
        try:
            controller.run_interactive_search()
        except (SystemExit, StopIteration):
            pass

if __name__ == '__main__':
    test_improved_display()