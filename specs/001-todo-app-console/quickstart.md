# Quickstart: Todo App Console

## Prerequisites
- Python 3.13 or higher
- No additional dependencies required (uses standard library only)

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Ensure Python 3.13+ is installed: `python --version`
4. No installation required - the application runs directly from source

## Running the Application
```bash
python src/todo_app/main.py
```

## Basic Usage
1. Run the application to see the main menu
2. Select options by entering the corresponding number
3. Follow the on-screen prompts for each operation

### Available Operations
- **Add Task**: Create a new task with title and optional description
- **View Tasks**: Display all tasks with ID, title, status, and description
- **Update Task**: Modify an existing task by ID
- **Delete Task**: Remove a task by ID
- **Mark Complete/Incomplete**: Toggle the completion status of a task

## Development
1. The main entry point is `src/todo_app/main.py`
2. Task model is defined in `src/todo_app/models/task.py`
3. Task operations are handled in `src/todo_app/services/task_service.py`
4. Console interface is implemented in `src/todo_app/cli/console.py`

## Testing
Run the tests with pytest:
```bash
pytest tests/
```

Unit tests are in `tests/unit/`
Integration tests are in `tests/integration/`