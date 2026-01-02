<!--
Sync Impact Report:
- Version change: 0.0.0 → 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] → I. Spec-Driven Development First
  - [PRINCIPLE_2_NAME] → II. No Manual Coding
  - [PRINCIPLE_3_NAME] → III. Deterministic Behavior
  - [PRINCIPLE_4_NAME] → IV. Simplicity with Extensibility
  - [PRINCIPLE_5_NAME] → V. Clean Architecture
- Added sections:
  - Scope and Functional Requirements
  - Code, Project, and Spec Standards
  - Governance
- Removed sections:
  - [PRINCIPLE_6_NAME]
- Templates requiring updates:
  - ⚠ .specify/templates/plan-template.md
  - ⚠ .specify/templates/spec-template.md
  - ⚠ .specify/templates/tasks-template.md
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): Set the date when this constitution is formally adopted.
-->
# Phase I – In-Memory Console-Based Todo Application Constitution

## Core Principles

### I. Spec-Driven Development First
Every feature must originate from a written specification before any implementation.

### II. No Manual Coding
All source code must be generated exclusively by Claude Code based on approved specs.

### III. Deterministic Behavior
Console interactions and outputs must be predictable, consistent, and testable.

### IV. Simplicity with Extensibility
The design must remain minimal while allowing smooth evolution into later phases.

### V. Clean Architecture
Clear separation between data models, business logic, and console interface.

## Scope and Functional Requirements

### Scope Boundaries (Phase I Only)
- Application is fully in-memory; no persistence, files, or databases.
- Console-based interaction only; no GUI, web, or chatbot interfaces.
- No AI, NLP, cloud, or Kubernetes components in this phase.
- No priorities, tags, search, filters, or reminders.

### Functional Requirements
- **Add Task**: Create a todo item with a title and optional description. Each task must receive a unique, incremental ID.
- **View Task List**: Display all tasks with ID, title, description, and completion status.
- **Update Task**: Modify title and/or description of an existing task using its ID.
- **Delete Task**: Remove a task by its ID.
- **Mark Task as Complete**: Toggle completion status between complete and incomplete.

### Data Model Standards
- Task entity must minimally include: `id` (integer, unique), `title` (string, required), `description` (string, optional), `is_completed` (boolean).
- Tasks must be stored in an in-memory data structure for the app lifecycle.

### Interaction Standards
- Console menus must be clear, numbered, and user-friendly.
- Invalid input must be handled gracefully with helpful messages.
- All user actions must produce explicit console feedback.

## Code, Project, and Spec Standards

### Code Quality Standards
- Python version: 3.13 or higher.
- Follow clean code principles: readable naming, small functions, clear responsibilities.
- Modular project structure suitable for future phases.
- No dead code, no unused imports.

### Project Structure Constraints
- `/src` directory must contain all Python source code.
- A clear entry point for running the console application.
- Logic must be organized to support future migration to web and AI interfaces.

### Spec Governance Rules
- Each feature must have a written specification with clear inputs, outputs, and edge cases.
- Specs must be refined iteratively until Claude Code produces correct behavior.
- All specification versions must be stored in a specs history folder.

## Governance
This Constitution is the guiding document for all development practices within this project.

### Documentation Requirements
- Constitution file defining rules and principles.
- README.md with setup and run instructions.
- CLAUDE.md describing how Claude Code was used and guided.

### Success Criteria
- All five basic todo features work correctly in the console.
- Application runs without errors using generated code only.
- Specs fully align with observed behavior.
- Codebase is ready for extension into Phase II without refactoring.

### Non-Negotiable Constraints
- Manual code writing is prohibited.
- Skipping specifications is prohibited.
- Features outside Phase I scope are prohibited.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE): Set the date when this constitution is formally adopted. | **Last Amended**: 2026-01-02