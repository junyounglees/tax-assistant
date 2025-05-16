#!/usr/bin/env python3
"""Main entry point for the Korean Law Search application."""
import sys
from src.infrastructure.container import Container


def main():
    """Main application entry point."""
    container = Container()
    controller = container.cli_controller
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'full-text' and len(sys.argv) > 2:
            # Get full text mode
            mst = sys.argv[2]
            controller.get_full_text(mst)
        elif command == 'articles' and len(sys.argv) > 2:
            # View articles mode
            mst = sys.argv[2]
            law_name = sys.argv[3] if len(sys.argv) > 3 else "법령"
            controller.view_law_articles(mst, law_name)
        else:
            # Direct search mode
            query = ' '.join(sys.argv[1:])
            controller.run_direct_search(query)
    else:
        # Interactive mode
        controller.run_interactive_search()


if __name__ == "__main__":
    main()