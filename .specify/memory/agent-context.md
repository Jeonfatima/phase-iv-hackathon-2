# Todo App Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-12-30

## Active Technologies

- Python 3.13+
- Standard library only (no external dependencies for Phase I)
- Console interface (no web framework required)
- In-memory storage using Python data structures

## Project Structure

```text
/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── task.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── task_service.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── console.py
│       └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
└── specs/
    └── 001-todo-app-console/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md
        └── contracts/
            └── task-api.md
```

## Commands

- `python src/todo_app/main.py` - Run the console application
- `pytest tests/` - Run all tests
- `pytest tests/unit/` - Run unit tests
- `pytest tests/integration/` - Run integration tests

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for all function parameters and return values
- Write docstrings for all classes and functions
- Keep functions focused on a single responsibility
- Use descriptive variable and function names

## Recent Changes

- Todo App Console: Added console-based todo application with menu-driven interface
- Todo App Console: Implemented in-memory task storage with Task model
- Todo App Console: Created task management service with full CRUD operations

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->