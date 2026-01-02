import pytest
from datetime import datetime
from src.models.task import Task

def test_task_creation():
    task = Task(id=1, title="Test Task")
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.is_completed == False
    assert task.description is None
    assert task.priority is None
    assert task.tags == []
    assert task.due_date is None
    assert task.recurrence_rule is None

def test_task_creation_with_all_attributes():
    due_date = datetime(2026, 1, 10, 10, 30)
    task = Task(
        id=2,
        title="Complex Task",
        description="A task with all details",
        is_completed=True,
        priority="high",
        tags=["work", "urgent"],
        due_date=due_date,
        recurrence_rule="daily"
    )
    assert task.id == 2
    assert task.title == "Complex Task"
    assert task.description == "A task with all details"
    assert task.is_completed == True
    assert task.priority == "high"
    assert task.tags == ["work", "urgent"]
    assert task.due_date == due_date
    assert task.recurrence_rule == "daily"

def test_task_priority_validation():
    with pytest.raises(ValueError, match="Priority must be 'high', 'medium', or 'low'"):
        Task(id=3, title="Invalid Priority", priority="invalid")

def test_task_due_date_type_validation():
    with pytest.raises(TypeError, match="due_date must be a datetime object"):
        Task(id=4, title="Invalid Due Date", due_date="2026-01-10")

def test_task_tags_default_empty_list():
    task = Task(id=5, title="No Tags")
    assert task.tags == []
    assert isinstance(task.tags, list)

def test_task_is_completed_default_false():
    task = Task(id=6, title="New Task")
    assert task.is_completed == False
