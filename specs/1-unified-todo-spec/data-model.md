# Data Model: Task

This document defines the data model for the `Task` entity.

## Entity: Task

Represents a single to-do item in the application.

### Attributes

| Attribute | Type | Description | Constraints |
|---|---|---|---|
| `id` | integer | A unique identifier for the task. | Required, auto-incrementing, unique. |
| `title` | string | The title of the task. | Required, non-empty. |
| `description`| string | A more detailed description of the task. | Optional. |
| `is_completed`| boolean | The completion status of the task. | Required, defaults to `False`. |
| `priority` | string | The priority level of the task. | Optional, must be one of 'high', 'medium', 'low'. |
| `tags` | list of strings | A list of tags or categories for the task. | Optional. |
| `due_date` | datetime | The due date and time for the task. | Optional. |
| `recurrence_rule` | string | A rule for recurring tasks (e.g., "daily", "weekly"). | Optional. |

### Example

```json
{
  "id": 1,
  "title": "Implement the core data model",
  "description": "Define the Task entity with all its attributes.",
  "is_completed": false,
  "priority": "high",
  "tags": ["development", "core"],
  "due_date": "2026-01-05T10:00:00",
  "recurrence_rule": null
}
```
