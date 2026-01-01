"""
Main entry point for the Todo Application.
"""
import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from todo_app.cli.console import ConsoleInterface


def main():
    """
    Main function to run the todo application.
    """
    app = ConsoleInterface()
    app.run()


if __name__ == "__main__":
    main()