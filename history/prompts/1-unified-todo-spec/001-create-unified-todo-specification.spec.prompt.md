---
id: 1
title: Create Unified Todo Specification
stage: spec
date: 2026-01-02
surface: agent
model: gemini
feature: 1-unified-todo-spec
branch: 1-unified-todo-spec
user: unknown
command: /sp.specify
labels: ["specification", "todo-app"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-unified-todo-spec/spec.md
 - specs/1-unified-todo-spec/checklists/requirements.md
tests: []
---

## Prompt

---
description: Create or update the feature specification from a natural language feature description.
handoffs: 
  - label: Build Technical Plan
    agent: sp.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: sp.clarify
    prompt: Clarify specification requirements
    send: true
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/sp.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `{{args}}` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **Check for existing branches before creating new one**:

   a. First, fetch all remote branches to ensure we have the latest information:

      ```bash
      git fetch --all --prune
      ```

   b. Find the highest feature number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`

   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number

   d. Run the script `.specify/scripts/powershell/create-new-feature.ps1 -Json "{{args}}"` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `.specify/scripts/powershell/create-new-feature.ps1 -Json "{{args}}" --json --number 5 --short-name "user-auth" "Add user authentication"`
      - PowerShell example: `.specify/scripts/powershell/create-new-feature.ps1 -Json "{{args}}" -Json -Number 5 -ShortName "user-auth" "Add user authentication"`

   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, specs directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per feature
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. Fill User Scenarios & Testing section
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME] 
      
      **Purpose**: Validate specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]
      
      ## Content Quality
      
      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Requirement Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified
      
      ## Feature Readiness
      
      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification
      
      ## Notes
      
      - Items marked incomplete require spec updates before `/sp.clarify` or `/sp.plan`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic] 
           
           **Context**: [Quote relevant spec section] 
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**: 
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input]
           
           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/sp.clarify` or `/sp.plan`).

**NOTE**: The script creates and checks out the new branch and initializes the spec file before writing.

## General Guidelines

## Quick Guidelines

- Focus on **WHAT** users need and **WHY**.
- Avoid HOW to implement (no tech stack, APIs, code structure).
- Written for business stakeholders, not developers.
- DO NOT create any checklists that are embedded in the spec. That will be a separate command.

### Section Requirements

- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation

When creating this spec from a user prompt:

1. **Make informed guesses**: Use context, industry standards, and common patterns to fill gaps
2. **Document assumptions**: Record reasonable defaults in the Assumptions section
3. **Limit clarifications**: Maximum 3 [NEEDS CLARIFICATION] markers - use only for critical decisions that:
   - Significantly impact feature scope or user experience
   - Have multiple reasonable interpretations with different implications
   - Lack any reasonable default
4. **Prioritize clarifications**: scope > security/privacy > user experience > technical details
5. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
6. **Common areas needing clarification** (only if no reasonable default exists):
   - Feature scope and boundaries (include/exclude specific use cases)
   - User types and permissions (if multiple conflicting interpretations possible)
   - Security/compliance requirements (when legally/financially significant)

**Examples of reasonable defaults** (don't ask about these):

- Data retention: Industry-standard practices for the domain
- Performance targets: Standard web/mobile app expectations unless specified
- Error handling: User-friendly messages with appropriate fallbacks
- Authentication method: Standard session-based or OAuth2 for web apps
- Integration patterns: RESTful APIs unless specified otherwise

### Success Criteria Guidelines

Success criteria must be:

1. **Measurable**: Include specific metrics (time, percentage, count, rate)
2. **Technology-agnostic**: No mention of frameworks, languages, databases, or tools
3. **User-focused**: Describe outcomes from user/business perspective, not system internals
4. **Verifiable**: Can be tested/validated without knowing implementation details

**Good examples**:

- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"
- "Task completion rate improves by 40%"

**Bad examples** (implementation-focused):

- "API response time is under 200ms" (too technical, use "Users see results instantly")
- "Database can handle 1000 TPS" (implementation detail, use user-facing metric)
- "React components render efficiently" (framework-specific)
- "Redis cache hit rate above 80%" (technology-specific)

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

The Evolution of Todo – Unified Specification (All level:Basic,Intermediate, Advanced) Primary objective: Define a complete, spec-driven blueprint for a Todo application that evolves from a simple in-memory console program into a feature-rich task management system. This specification governs all functional levels while ensuring a cohesive architecture, consistent behavior, and an exceptional command-line user experience. Scope of this specification: This document specifies all Todo features across: - Basic Level (Core Essentials) - Intermediate Level (Organization & Usability) - Advanced Level (Intelligent Features) All features are defined conceptually in this spec, even if they are implemented incrementally in separate phases. In-Scope Functional Features: Basic Level (Core Essentials): - Add Task - Create new todo items with a required title and optional description. - View Task List - Display all tasks with clear formatting and status indicators. - Update Task - Modify task title and/or description using a task ID. - Delete Task - Remove tasks from the list using a task ID. - Mark as Complete - Toggle task completion status between complete and incomplete. Intermediate Level (Organization & Usability): - Priorities - Assign priority levels (high, medium, low) to tasks. - Tags / Categories - Assign one or more labels (e.g., work, personal, study). - Search - Search tasks by keyword in title or description. - Filter - Filter tasks by completion status, priority, or category. - Sort - Reorder tasks by due date, priority, or alphabetically by title. Advanced Level (Intelligent Features): - Due Dates - Assign optional due dates and times to tasks. - Time Reminders - Trigger reminders based on due dates within the application context. - Recurring Tasks - Define repeating tasks (daily, weekly, custom intervals) that auto-reschedule after completion. Out-of-Scope (Global Constraints): - No web UI, mobile UI, or graphical interface. - No external databases or cloud services in the console implementation. - No AI, NLP, or chatbot interfaces in the CLI version. - No authentication or multi-user support. - No background daemons or OS-level notifications. CLI User Experience Standards: - Menu-driven interaction with clearly numbered options. - Visually structured output using spacing, alignment, and symbols. - Task list must display: - ID - Title - Completion status indicator - Priority (if set) - Due date (if set) - Tags (if any) - Consistent symbols for task status (e.g., [ ] pending, [✓] completed). - Clear prompts, confirmations, and error messages. - Graceful handling of invalid inputs and edge cases. - Screen refresh or logical separation between actions for readability. - Intuitive navigation with minimal cognitive load. Data Model Requirements: - Each task must support the following attributes: - id (unique integer) - title (string, required) - description (string, optional) - is_completed (boolean) - priority (optional: high | medium | low) - tags (optional list of strings) - due_date (optional date/time) - recurrence_rule (optional) - Tasks may exist purely in memory for early phases but must be designed to support persistence later. Behavioral Rules: - Task IDs must remain stable and unique. - All operations must validate task existence before execution. - Sorting and filtering must not mutate underlying task data. - Recurring tasks must reschedule based on defined rules after completion. - Reminders must trigger only when due dates are defined. Architecture & Quality Standards: - Clean separation between: - Task data model - Business logic - CLI interaction layer - Modular structure suitable for future web, API, and AI interfaces. - Python 3.13+ compatibility. - Readable naming, small functions, and clear responsibilities. - No unused or unreachable logic. Spec-Driven Development Constraints: - Every feature must be implemented strictly from this specification. - No manual code writing is allowed. - All code must be generated using Claude Code. - Specifications must be refined until generated output matches behavior. - Changes must be reflected through spec updates, not code edits. Success Criteria: - All defined features behave consistently with this specification. - Console application remains usable and readable despite feature growth. - The architecture supports seamless expansion into later hackathon phases. - Generated implementation aligns fully with the written spec.

## Response snapshot

I have created the feature specification for "The Evolution of Todo – Unified Specification".

## Outcome

- ✅ Impact: Created a comprehensive specification for the unified todo application.
- 🧪 Tests: none
- 📁 Files: Created the spec file and a requirements checklist.
- 🔁 Next prompts: /sp.plan
- 🧠 Reflection: The detailed user input allowed for a very complete specification.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none

Task: Analyze the potentially_problematic_string. If it's syntactically invalid due to incorrect escaping (e.g., "\n", "\t", "\\", "\'", '"'), correct the invalid syntax. The goal is to ensure the text will be a valid and correctly interpreted.

For example, if potentially_problematic_string is "bar\nbaz", the corrected_new_string_escaping should be "bar\nbaz".
If potentially_problematic_string is console.log(\"Hello World\"), it should be console.log("Hello World").

Return ONLY the corrected string in the specified JSON format with the key 'corrected_string_escaping'. If no escaping correction is needed, return the original potentially_problematic_string.
