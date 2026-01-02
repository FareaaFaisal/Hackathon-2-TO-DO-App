---
id: 1
title: Establish Project Constitution
stage: constitution
date: 2026-01-02
surface: agent
model: gemini
feature: none
branch: main
user: unknown
command: /sp.constitution
labels: ["constitution", "project-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
tests:
 - none
---

## Prompt

---
description: Create or update the project constitution from interactive or provided principle inputs, ensuring all dependent templates stay in sync.
handoffs: 
  - label: Build Specification
    agent: sp.specify
    prompt: Implement the feature specification based on the updated constitution. I want to build...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.


/sp.constitution Project: Phase I – In-Memory Console-Based Todo Application

Purpose:
Design and implement Phase I of "The Evolution of Todo" as a Python-based, in-memory, console application using strict Spec-Driven Development. The system must demonstrate foundational todo management capabilities while establishing a clean architectural baseline for future AI-native and cloud-native evolution.

Core Principles:
- Spec-Driven Development First: Every feature must originate from a written specification before any implementation.
- No Manual Coding: All source code must be generated exclusively by Claude Code based on approved specs.
- Deterministic Behavior: Console interactions and outputs must be predictable, consistent, and testable.
- Simplicity with Extensibility: The design must remain minimal while allowing smooth evolution into later phases.
- Clean Architecture: Clear separation between data models, business logic, and console interface.

Scope Boundaries (Phase I Only):
- Application is fully in-memory; no persistence, files, or databases.
- Console-based interaction only; no GUI, web, or chatbot interfaces.
- No AI, NLP, cloud, or Kubernetes components in this phase.
- No priorities, tags, search, filters, or reminders.

Functional Requirements:
- Add Task:
  - Create a todo item with a title and optional description.
  - Each task must receive a unique, incremental ID.
- View Task List:
  - Display all tasks with ID, title, description, and completion status.
- Update Task:
  - Modify title and/or description of an existing task using its ID.
- Delete Task:
  - Remove a task by its ID.
- Mark Task as Complete:
  - Toggle completion status between complete and incomplete.

Data Model Standards:
- Task entity must minimally include:
  - id (integer, unique)
  - title (string, required)
  - description (string, optional)
  - is_completed (boolean)
- Tasks must be stored in an in-memory data structure for the app lifecycle.

Interaction Standards:
- Console menus must be clear, numbered, and user-friendly.
- Invalid input must be handled gracefully with helpful messages.
- All user actions must produce explicit console feedback.

Code Quality Standards:
- Python version: 3.13 or higher.
- Follow clean code principles: readable naming, small functions, clear responsibilities.
- Modular project structure suitable for future phases.
- No dead code, no unused imports.

Project Structure Constraints:
- /src directory must contain all Python source code.
- A clear entry point for running the console application.
- Logic must be organized to support future migration to web and AI interfaces.

Spec Governance Rules:
- Each feature must have:
  - A written specification
  - Clear inputs, outputs, and edge cases
- Specs must be refined iteratively until Claude Code produces correct behavior.
- All specification versions must be stored in a specs history folder.

Documentation Requirements:
- Constitution file defining rules and principles.
- README.md with setup and run instructions.
- CLAUDE.md describing how Claude Code was used and guided.

Success Criteria:
- All five basic todo features work correctly in the console.
- Application runs without errors using generated code only.
- Specs fully align with observed behavior.
- Codebase is ready for extension into Phase II without refactoring.

Non-Negotiable Constraints:
- Manual code writing is prohibited.
- Skipping specifications is prohibited.
- Features outside Phase I scope are prohibited.

## Response snapshot

I have successfully updated the project constitution based on your input. I have also updated the `plan-template.md` to align with the new principles.

## Outcome

- ✅ Impact: Established the foundational principles and governance for the project.
- 🧪 Tests: none
- 📁 Files: Created the constitution file and updated the plan template to reflect the new principles.
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: The constitution provides a strong foundation for spec-driven development.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
