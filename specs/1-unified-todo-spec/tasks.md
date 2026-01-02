# Tasks: The Evolution of Todo – Unified Implementation Plan (Colorful CLI)

**Input**: Design documents from `specs/1-unified-todo-spec/`
**Prerequisites**: plan.md, spec.md, data-model.md, research.md

## Phase 1: Project Foundation

**Timeline**: Week 1
**Dependencies**: None

- [X] T001 [P] Create project directory structure: `src/models`, `src/logic`, `src/cli`, `tests/unit`, `tests/integration`.
- [X] T002 [P] Create empty python files: `src/main.py`, `src/models/task.py`, `src/logic/task_manager.py`, `src/cli/menu.py`, `tests/unit/test_task.py`, `tests/unit/test_task_manager.py`, `tests/integration/test_cli.py`.
- [X] T003 [P] Create `requirements.txt` and add `rich`.
- [X] T004 Implement the core application loop in `src/main.py`.
- [X] T005 [P] Define shared input validation helpers in a new `src/cli/utils.py`.
- [X] T006 [P] Define console formatting helpers (color wrappers, headers) in `src/cli/utils.py` using `rich`.
- [X] T007 [P] Define Unicode symbols for status in `src/cli/utils.py`.

## Phase 2: Core Data Model

**Timeline**: Week 2
**Dependencies**: Phase 1 complete

- [X] T008 [P] [US1] Define the `Task` data class in `src/models/task.py` with all attributes from `data-model.md`.
- [X] T009 [P] [US1] Write unit tests for the `Task` model in `tests/unit/test_task.py`.
- [X] T010 [US1] Implement the in-memory task collection in `src/logic/task_manager.py`.
- [X] T011 [US1] Implement validation rules for task creation and updates in `src/logic/task_manager.py`.
- [X] T012 [P] [US1] Write unit tests for the `TaskManager` in `tests/unit/test_task_manager.py`.

## Phase 3: Core Essentials (Basic Level)

**Timeline**: Week 3-4
**Dependencies**: Phase 2 complete

- [X] T013 [US1] Implement "Add Task" functionality in `src/logic/task_manager.py` and `src/cli/menu.py`.
- [X] T014 [US1] Implement "View Task List" with colorful table output using `rich` in `src/cli/menu.py`.
- [X] T015 [US1] Implement "Update Task" functionality in `src/logic/task_manager.py` and `src/cli/menu.py`.
- [X] T016 [US1] Implement "Delete Task" functionality in `src/logic/task_manager.py` and `src/cli/menu.py`.
- [X] T017 [US1] Implement "Mark as Complete" functionality in `src/logic/task_manager.py` and `src/cli/menu.py`.
- [X] T018 [P] [US1] Write integration tests for the basic CLI features in `tests/integration/test_cli.py`.

## Phase 4: Organization & Usability Enhancements (Intermediate Level)

**Timeline**: Week 5-6
**Dependencies**: Phase 3 complete

- [X] T019 [US2] Implement priority assignment logic in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T020 [US2] Implement tag management logic in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T021 [US2] Implement search functionality in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T022 [US2] Implement filter functionality in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T023 [US2] Implement sorting functionality in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T024 [P] [US2] Write integration tests for organization and usability features in `tests/integration/test_cli.py`.

## Phase 5: Intelligent Task Behavior (Advanced Level)

**Timeline**: Week 7-8
**Dependencies**: Phase 4 complete

- [X] T025 [US3] Implement due date logic in `src/logic/task_manager.py` and UI in `src/cli/menu.py`.
- [X] T026 [US3] Implement time reminder display in `src/cli/menu.py`.
- [X] T027 [US3] Implement recurring task logic in `src/logic/task_manager.py`.
- [X] T028 [P] [US3] Write integration tests for intelligent task features in `tests/integration/test_cli.py`.

## Phase 6: CLI UX Refinement (Polish)

**Timeline**: Week 9
**Dependencies**: Phase 5 complete

- [X] T029 Refine the menu structure and display in `src/cli/menu.py` using `rich`.
- [X] T030 Improve visual formatting of tables and symbols in `src/cli/menu.py`.
- [X] T031 Standardize all feedback and messaging colors in `src/cli/menu.py`.
- [X] T032 Improve input resilience and error handling in `src/cli/menu.py`.

## Phase 7: Validation & Spec Compliance

**Timeline**: Week 10
**Dependencies**: Phase 6 complete

- [X] T033 [P] Verify all features against the `spec.md`.
- [X] T034 [P] Confirm separation of concerns between `models`, `logic`, and `cli`.
- [X] T035 [P] Manually validate the CLI experience for readability and usability.
- [X] T036 [P] Add any missing unit or integration tests to meet coverage goals.
