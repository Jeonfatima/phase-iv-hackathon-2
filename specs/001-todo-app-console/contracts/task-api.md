# Task API Contracts

## Overview
This document defines the functional contracts for task operations in the console application. These represent the internal service contracts that the CLI will use to interact with the task management system.

## Core Operations

### 1. Create Task
**Function**: `create_task(title: str, description: str = None) -> Task`
- **Input**:
  - title (required): string, 1-100 characters
  - description (optional): string, 0-500 characters
- **Output**: Task object with assigned ID and completed=False
- **Errors**:
  - ValueError if title is empty or exceeds 100 characters

### 2. Get All Tasks
**Function**: `get_all_tasks() -> List[Task]`
- **Input**: None
- **Output**: List of all Task objects, ordered by creation
- **Errors**: None

### 3. Get Task by ID
**Function**: `get_task_by_id(task_id: int) -> Task`
- **Input**: task_id (integer)
- **Output**: Task object matching the ID
- **Errors**:
  - ValueError if task ID does not exist

### 4. Update Task
**Function**: `update_task(task_id: int, title: str = None, description: str = None) -> Task`
- **Input**:
  - task_id (integer)
  - title (optional): string, 1-100 characters
  - description (optional): string, 0-500 characters
- **Output**: Updated Task object
- **Errors**:
  - ValueError if task ID does not exist
  - ValueError if title exceeds 100 characters

### 5. Delete Task
**Function**: `delete_task(task_id: int) -> bool`
- **Input**: task_id (integer)
- **Output**: True if task was deleted, False if not found
- **Errors**: None

### 6. Toggle Task Completion
**Function**: `toggle_task_completion(task_id: int) -> Task`
- **Input**: task_id (integer)
- **Output**: Task object with toggled completion status
- **Errors**:
  - ValueError if task ID does not exist

## Task Model Contract

### Properties
- **id**: Integer, unique, auto-incremented
- **title**: String, required, 1-100 characters
- **description**: String, optional, 0-500 characters
- **completed**: Boolean, default False

### Validation
- All string fields are trimmed of leading/trailing whitespace
- Title must not be empty after trimming
- Character limits are enforced
- ID is read-only after creation