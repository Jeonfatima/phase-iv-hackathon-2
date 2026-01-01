---
description: "Task list for Todo App Console feature implementation"
---

# Tasks: Todo App – Phase I: In-Memory Python Console Application

**Input**: Design documents from `/specs/[001-todo-app-console]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan in src/todo_app/
- [X] T002 Create __init__.py files for all directories in src/todo_app/
- [X] T003 [P] Create tests/ directory structure per plan

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Task model in src/todo_app/models/task.py with id, title, description, completed attributes
- [X] T005 Create TaskService in src/todo_app/services/task_service.py with in-memory storage
- [X] T006 Create console interface structure in src/todo_app/cli/console.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create a new task (Priority: P1) 🎯 MVP

**Goal**: Allow users to add new tasks to their list with required title and optional description

**Independent Test**: The application should allow users to input a task title and optional description, and successfully store it with a unique ID that can be viewed later.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T007 [P] [US1] Unit test for Task model validation in tests/unit/test_task.py
- [X] T008 [P] [US1] Unit test for TaskService create_task functionality in tests/unit/test_task_service.py

### Implementation for User Story 1

- [X] T009 [P] [US1] Implement Task model with validation in src/todo_app/models/task.py
- [X] T010 [US1] Implement create_task method in src/todo_app/services/task_service.py
- [X] T011 [US1] Implement add task functionality in src/todo_app/cli/console.py
- [X] T012 [US1] Connect add task to main menu in src/todo_app/cli/console.py
- [X] T013 [US1] Add input validation for task creation in src/todo_app/cli/console.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View all tasks (Priority: P1)

**Goal**: Allow users to view all tasks with their ID, title, completion status, and optional description

**Independent Test**: The application should display all tasks with their ID, title, completion status, and optional description in a clear format.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T014 [P] [US2] Unit test for TaskService get_all_tasks functionality in tests/unit/test_task_service.py
- [X] T015 [P] [US2] Integration test for viewing tasks in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T016 [US2] Implement get_all_tasks method in src/todo_app/services/task_service.py
- [X] T017 [US2] Implement view tasks functionality in src/todo_app/cli/console.py
- [X] T018 [US2] Connect view tasks to main menu in src/todo_app/cli/console.py
- [X] T019 [US2] Format task display with ID, title, status, and description in src/todo_app/cli/console.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update an existing task (Priority: P2)

**Goal**: Allow users to modify existing tasks by updating title and/or description

**Independent Test**: The application should allow users to select a task by ID and update its title and/or description fields.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T020 [P] [US3] Unit test for TaskService update_task functionality in tests/unit/test_task_service.py
- [X] T021 [P] [US3] Test for invalid task ID handling in tests/unit/test_task_service.py

### Implementation for User Story 3

- [X] T022 [US3] Implement update_task method in src/todo_app/services/task_service.py
- [X] T023 [US3] Implement update task functionality in src/todo_app/cli/console.py
- [X] T024 [US3] Connect update task to main menu in src/todo_app/cli/console.py
- [X] T025 [US3] Add validation and error handling for update operations in src/todo_app/cli/console.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Delete a task (Priority: P2)

**Goal**: Allow users to remove tasks by their ID with proper validation

**Independent Test**: The application should allow users to remove a task by its ID, with proper validation that the task exists.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T026 [P] [US4] Unit test for TaskService delete_task functionality in tests/unit/test_task_service.py
- [X] T027 [P] [US4] Test for delete non-existent task in tests/unit/test_task_service.py

### Implementation for User Story 4

- [X] T028 [US4] Implement delete_task method in src/todo_app/services/task_service.py
- [X] T029 [US4] Implement delete task functionality in src/todo_app/cli/console.py
- [X] T030 [US4] Connect delete task to main menu in src/todo_app/cli/console.py
- [X] T031 [US4] Add validation and error handling for delete operations in src/todo_app/cli/console.py

---

## Phase 7: User Story 5 - Mark tasks as complete/incomplete (Priority: P2)

**Goal**: Allow users to change the completion status of tasks

**Independent Test**: The application should allow users to change the completion status of tasks, which should be reflected when viewing the task list.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [X] T032 [P] [US5] Unit test for TaskService toggle completion functionality in tests/unit/test_task_service.py
- [X] T033 [P] [US5] Test for completion status display in tests/integration/test_cli.py

### Implementation for User Story 5

- [X] T034 [US5] Implement toggle_task_completion method in src/todo_app/services/task_service.py
- [X] T035 [US5] Implement mark task completion functionality in src/todo_app/cli/console.py
- [X] T036 [US5] Connect mark completion to main menu in src/todo_app/cli/console.py
- [X] T037 [US5] Add validation and error handling for completion operations in src/todo_app/cli/console.py

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Create main application entry point in src/todo_app/main.py
- [X] T039 [P] Add comprehensive error handling throughout application
- [X] T040 [P] Implement input validation with character limits (100 for title, 500 for description)
- [X] T041 [P] Add user-friendly error messages with guidance
- [X] T042 [P] Implement menu navigation and user experience improvements
- [X] T043 [P] Add docstrings and comments to all functions and classes
- [X] T044 Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with other stories but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Unit test for Task model validation in tests/unit/test_task.py"
Task: "Unit test for TaskService create_task functionality in tests/unit/test_task_service.py"

# Launch all models for User Story 1 together:
Task: "Implement Task model with validation in src/todo_app/models/task.py"
Task: "Implement create_task method in src/todo_app/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence