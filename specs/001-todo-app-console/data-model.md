# Data Model: Todo App Console

## Task Entity

### Attributes
- **id**: Integer (unique, auto-incrementing)
  - Primary identifier for the task
  - Auto-generated when task is created
  - Never changes once assigned
  - Required for all operations

- **title**: String (required, max 100 characters)
  - Descriptive name for the task
  - Required field (cannot be empty)
  - Maximum 100 characters as per specification
  - Must be validated for non-empty input

- **description**: String (optional, max 500 characters)
  - Additional details about the task
  - Optional field (can be null/empty)
  - Maximum 500 characters as per specification
  - Can be updated after creation

- **completed**: Boolean (default: False)
  - Status indicator for task completion
  - Boolean value (True/False)
  - Defaults to False when task is created
  - Can be toggled between True/False

### Validation Rules
- Title must not be empty or whitespace-only
- Title must be 100 characters or less
- Description must be 500 characters or less (if provided)
- ID must be unique within the task collection
- ID must be a positive integer

### State Transitions
- New Task: id (auto-assigned), title (from input), description (from input or null), completed (False)
- Update Task: Any field except ID can be modified
- Complete Task: completed status changes from False to True
- Incomplete Task: completed status changes from True to False
- Delete Task: Task is removed from collection

## Task Collection

### Structure
- In-memory storage using Python list/dictionary
- Maintains all tasks during application runtime
- Provides O(1) lookup by ID
- Preserves insertion order for display purposes

### Operations
- Add: Insert new task with auto-generated ID
- Get: Retrieve task by ID
- Update: Modify existing task fields by ID
- Delete: Remove task by ID
- List: Retrieve all tasks
- Filter: Get completed/incomplete tasks