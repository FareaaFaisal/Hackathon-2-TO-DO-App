--- 
id: 2
title: Create Implementation Plan for Todo App
stage: plan
date: 2026-01-02
surface: agent
model: gemini
feature: 1-unified-todo-spec
branch: 1-unified-todo-spec
user: unknown
command: /sp.plan
labels: ["plan", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-unified-todo-spec/plan.md
 - specs/1-unified-todo-spec/research.md
 - specs/1-unified-todo-spec/data-model.md
 - specs/1-unified-todo-spec/quickstart.md
tests:
 - none
---

## Prompt

---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: sp.tasks
    prompt: Break the plan into tasks
    send: true
  - label: Create Checklist
    agent: sp.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

4. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType gemini`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications

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


/sp.plan The Evolution of Todo – Unified Implementation Plan (Colorful CLI)

Planning Objective:
Translate the unified specification into a structured, stepwise implementation plan that enables Claude Code to generate a visually appealing, colorized, and user-friendly CLI Todo application. All stages follow the specification while maximizing readability, user experience, and future extensibility.

Governing Rules:
- All work must strictly follow the approved specification.
- Implementation proceeds in ordered stages, not hackathon phases.
- No manual code writing is permitted; all code is generated via Claude Code.
- UI enhancements must be console-only, using colors, symbols, and formatting.

────────────────────────
Stage 1: Project Foundation
────────────────────────
1. Initialize Python project structure
   - Create /src directory
   - Define a single entry point (e.g., main.py)
   - Prepare modular layout for models, logic, and CLI interface
2. Establish core application loop
   - Persistent menu-driven console loop
   - Clean program exit handling
3. Define shared utilities
   - Input validation helpers
   - Console formatting helpers (color wrappers, spacing, headers)
   - Unicode symbols for status: ✔ for completed, ✖ for pending

Deliverable:
- Empty CLI shell ready for colorful menus and placeholder options

────────────────────────
Stage 2: Core Data Model
────────────────────────
1. Define Task data structure with attributes:
   - id, title, description, is_completed, priority, tags, due_date, recurrence_rule
2. Define in-memory task collection
   - Maintain unique, incremental task IDs
3. Implement validation rules
   - Required fields, allowed values, proper formatting

Deliverable:
- Core task model ready for all feature levels

────────────────────────
Stage 3: Core Essentials (Basic Level)
────────────────────────
1. Implement Add Task
   - Prompt for title (bold/color) and description (dim color)
   - Display confirmation message in green
2. Implement View Task List
   - Display table with columns: ID, Title, Status, Priority, Due Date, Tags
   - Completed tasks in green ✔, pending tasks in yellow ✖
   - Alternate row shading (light/dark backgrounds or color intensity)
3. Implement Update Task
   - Highlight editable fields in cyan
   - Success message in green
4. Implement Delete Task
   - Confirm deletion in red
   - Success message in green
5. Implement Mark as Complete
   - Toggle status symbol: ✔ (green) or ✖ (yellow)
   - Update display immediately

Deliverable:
- Fully functional, colorful in-memory CLI Todo app

────────────────────────
Stage 4: Organization & Usability Enhancements (Intermediate Level)
────────────────────────
1. Priority Assignment
   - Color-code priorities: High (red), Medium (yellow), Low (blue)
2. Tag Management
   - Display tags in distinct colors or enclosed in brackets [Work], [Home]
3. Search & Filter
   - Highlight matching keywords in title/description
   - Filtered results visually separated with headers
4. Sort
   - Indicate sorting method in colored header
   - Highlight changed order dynamically

Deliverable:
- Colorful, organized CLI experience with intuitive visual cues

────────────────────────
Stage 5: Intelligent Task Behavior (Advanced Level)
────────────────────────
1. Due Dates
   - Display due dates in cyan
   - Overdue tasks highlighted in red
2. Time Reminders
   - Show reminder notifications in blinking/yellow text (where supported)
3. Recurring Tasks
   - Recurrence info displayed in magenta
   - Auto-reschedule message in green

Deliverable:
- Intelligent CLI task behaviors with clear color-coded statuses

────────────────────────
Stage 6: CLI UX Refinement (Polish)
────────────────────────
1. Menu Structure
   - Numbered options with bold/colorized headers
   - Separator lines using Unicode (═, ─, ░)
2. Visual Formatting
   - Tables, columns aligned
   - Alternate row coloring or background shading
   - Symbols for task completion, overdue, recurring, priority
3. Feedback & Messaging
   - Success messages in green
   - Errors in red
   - Warnings in yellow
4. Input Resilience
   - Highlight invalid entries in red
   - Prompt users with color-coded suggestions

Deliverable:
- Fully polished, vibrant CLI experience that is visually appealing and readable

────────────────────────
Stage 7: Validation & Spec Compliance
────────────────────────
1. Verify all features against specification
2. Ensure colors, symbols, and formatting enhance readability without breaking functionality
3. Confirm separation of concerns: model, logic, CLI
4. Validate that all code is generated exclusively via Claude Code

Final Deliverable:
- Complete, colorful, spec-compliant console-based Todo application
- Architecture ready for expansion into later hackathon phases
- High visual impact CLI, clean, readable, and enjoyable to use

## Response snapshot

I have created the implementation plan for "The Evolution of Todo – Unified Implementation Plan (Colorful CLI)".

## Outcome

- ✅ Impact: Created a comprehensive implementation plan for the unified todo application.
- 🧪 Tests: none
- 📁 Files: Created the plan file and associated artifacts (research, data-model, quickstart).
- 🔁 Next prompts: /sp.tasks
- 🧠 Reflection: The detailed user input allowed for a very complete implementation plan.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none
