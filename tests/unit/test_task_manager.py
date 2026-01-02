import pytest
from src.logic.task_manager import TaskManager
from src.models.task import Task

@pytest.fixture
def task_manager():
    # Reset TaskManager for each test to ensure isolation
    TaskManager._tasks = []
    TaskManager._next_id = 1
    return TaskManager()

def test_add_task(task_manager):
    task = task_manager.add_task("Buy groceries")
    assert task.id == 1
    assert task.title == "Buy groceries"
    assert len(task_manager.get_all_tasks()) == 1

def test_add_task_with_description(task_manager):
    task = task_manager.add_task("Read a book", "Chapter 5")
    assert task.id == 1
    assert task.title == "Read a book"
    assert task.description == "Chapter 5"

def test_add_task_empty_title_raises_error(task_manager):
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        task_manager.add_task("")
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        task_manager.add_task("   ")

def test_get_task_by_id(task_manager):
    task1 = task_manager.add_task("Task One")
    task2 = task_manager.add_task("Task Two")
    assert task_manager.get_task_by_id(task1.id) == task1
    assert task_manager.get_task_by_id(task2.id) == task2
    assert task_manager.get_task_by_id(999) is None

def test_get_all_tasks(task_manager):
    assert len(task_manager.get_all_tasks()) == 0
    task_manager.add_task("Task One")
    task_manager.add_task("Task Two")
    all_tasks = task_manager.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0].title == "Task One"
    assert all_tasks[1].title == "Task Two"

def test_update_task_title(task_manager):
    task = task_manager.add_task("Old Title")
    updated_task = task_manager.update_task(task.id, title="New Title")
    assert updated_task.title == "New Title"
    assert task_manager.get_task_by_id(task.id).title == "New Title"

def test_update_task_description(task_manager):
    task = task_manager.add_task("Task", "Old Description")
    updated_task = task_manager.update_task(task.id, description="New Description")
    assert updated_task.description == "New Description"
    assert task_manager.get_task_by_id(task.id).description == "New Description"

def test_update_task_description_to_none(task_manager):
    task = task_manager.add_task("Task", "Description")
    updated_task = task_manager.update_task(task.id, description=None)
    assert updated_task.description is None
    assert task_manager.get_task_by_id(task.id).description is None

def test_update_task_nonexistent_id(task_manager):
    updated_task = task_manager.update_task(999, title="Nonexistent")
    assert updated_task is None

def test_update_task_empty_title_raises_error(task_manager):
    task = task_manager.add_task("Valid Task")
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        task_manager.update_task(task.id, title="")
    with pytest.raises(ValueError, match="Task title cannot be empty."):
        task_manager.update_task(task.id, title="   ")
    # Ensure task title was not changed
    assert task_manager.get_task_by_id(task.id).title == "Valid Task"

def test_delete_task(task_manager):
    task = task_manager.add_task("Task to delete")
    assert len(task_manager.get_all_tasks()) == 1
    assert task_manager.delete_task(task.id) is True
    assert len(task_manager.get_all_tasks()) == 0
    assert task_manager.get_task_by_id(task.id) is None

def test_delete_task_nonexistent_id(task_manager):
    task_manager.add_task("Task One")
    assert task_manager.delete_task(999) is False
    assert len(task_manager.get_all_tasks()) == 1

def test_mark_task_complete(task_manager):
    task = task_manager.add_task("Incomplete Task")
    assert task.is_completed is False
    completed_task = task_manager.mark_task_complete(task.id)
    assert completed_task.is_completed is True
    assert task_manager.get_task_by_id(task.id).is_completed is True

def test_mark_task_incomplete(task_manager):
    task = task_manager.add_task("Completed Task")
    task.is_completed = True
    incomplete_task = task_manager.mark_task_complete(task.id, is_completed=False)
    assert incomplete_task.is_completed is False
    assert task_manager.get_task_by_id(task.id).is_completed is False

def test_mark_task_complete_nonexistent_id(task_manager):
    result = task_manager.mark_task_complete(999)
    assert result is None
