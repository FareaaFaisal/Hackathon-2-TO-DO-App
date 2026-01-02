from typing import List, Optional
from models.task import Task
from datetime import datetime


class TaskManager:
    _next_id = 1
    _tasks: List[Task] = []

    def __init__(self):
        if not hasattr(TaskManager, "_initialized"):
            TaskManager._tasks = []
            TaskManager._next_id = 1
            TaskManager._initialized = True

    # ---------------- ADD / GET ----------------

    def add_task(
        self,
        title: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_rule: Optional[str] = None,
    ) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        if recurrence_rule and recurrence_rule not in ["daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Invalid recurrence rule.")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            tags=tags or [],
            due_date=due_date,
            recurrence_rule=recurrence_rule,
        )

        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def get_all_tasks(self) -> List[Task]:
        return list(self._tasks)

    # ---------------- UPDATE / DELETE ----------------

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        tags: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_rule: Optional[str] = None,
    ) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty.")
            task.title = title.strip()

        if description is not None:
            task.description = description

        if priority is not None:
            if priority not in ["high", "medium", "low", ""]:
                raise ValueError("Invalid priority.")
            task.priority = priority or None

        if tags is not None:
            task.tags = tags

        if due_date is not None:
            task.due_date = due_date or None

        if recurrence_rule is not None:
            if recurrence_rule not in ["daily", "weekly", "monthly", "yearly", ""]:
                raise ValueError("Invalid recurrence rule.")
            task.recurrence_rule = recurrence_rule or None

        return task

    def delete_task(self, task_id: int) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        return len(self._tasks) < before

    # ---------------- STATUS ----------------

    def mark_task_complete(self, task_id: int, is_completed: bool = True) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.is_completed = is_completed

        if task.is_completed and task.recurrence_rule:
            self._create_next_recurring_instance(task)

        return task

    def _create_next_recurring_instance(self, original_task: Task):
        # Simulation only
        pass

    # ---------------- SEARCH / FILTER / SORT ----------------

    def search_tasks(self, keyword: str) -> List[Task]:
        keyword = keyword.lower()
        return [
            t for t in self._tasks
            if keyword in t.title.lower()
            or (t.description and keyword in t.description.lower())
            or any(keyword in tag.lower() for tag in t.tags)
        ]

    def filter_tasks(
        self,
        status: Optional[bool] = None,
        priority: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> List[Task]:
        tasks = self._tasks

        if status is not None:
            tasks = [t for t in tasks if t.is_completed == status]

        if priority:
            tasks = [t for t in tasks if t.priority == priority]

        if tag:
            tasks = [t for t in tasks if tag.lower() in [x.lower() for x in t.tags]]

        return tasks

    def sort_tasks(self, tasks: List[Task], sort_by: str, order: str = "asc") -> List[Task]:
        reverse = order == "desc"

        if sort_by == "title":
            return sorted(tasks, key=lambda t: t.title.lower(), reverse=reverse)

        if sort_by == "priority":
            priority_map = {"high": 3, "medium": 2, "low": 1, None: 0}
            return sorted(tasks, key=lambda t: priority_map[t.priority], reverse=reverse)

        if sort_by == "due_date":
            return sorted(
                tasks,
                key=lambda t: t.due_date or datetime.max,
                reverse=reverse,
            )

        return sorted(tasks, key=lambda t: t.id, reverse=reverse)

    # ---------------- REMINDERS ----------------

    def get_overdue_tasks(self) -> List[Task]:
        now = datetime.now()
        return [
            t for t in self._tasks
            if t.due_date and t.due_date < now and not t.is_completed
        ]
