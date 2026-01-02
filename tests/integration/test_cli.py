import pytest
from unittest.mock import patch
import sys
from io import StringIO
from src.main import main
from src.logic.task_manager import TaskManager
from datetime import datetime

# Fixture to reset TaskManager and capture stdout
@pytest.fixture
def cli_test_setup():
    TaskManager._tasks = []
    TaskManager._next_id = 1
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = new_stdout = StringIO()
    yield new_stdout
    sys.stdout = old_stdout

def simulate_input(monkeypatch, inputs):
    inputs_iter = iter(inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_iter))
    monkeypatch.setattr('rich.console.Console.input', lambda _, prompt: next(inputs_iter))

def test_add_task_and_view(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, ["1", "Test Task 1", "Description 1", "", "", "", "1", "Test Task 2", "", "tag1, tag2", "2026-01-15 10:00", "weekly", "2", "0"])
    
    with pytest.raises(SystemExit):
        main()
    
    output = cli_test_setup.getvalue()
    
    assert "Task 'Test Task 1' (ID: 1) added successfully!" in output
    assert "Task 'Test Task 2' (ID: 2) added successfully!" in output
    assert "Test Task 1" in output
    assert "Description 1" in output
    assert "Test Task 2" in output
    assert "tag1, tag2" in output
    assert "2026-01-15 10:00" in output
    assert "weekly" in output

def test_update_task(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, ["1", "Task to Update", "", "", "", "", "3", "1", "Updated Title", "Updated Description", "high", "newtag1, newtag2", "2026-01-20 12:00", "daily", "2", "0"])
    
    with pytest.raises(SystemExit):
        main()
    
    output = cli_test_setup.getvalue()
    
    assert "Task (ID: 1) updated successfully!" in output
    assert "Updated Title" in output
    assert "Updated Description" in output
    assert "high" in output
    assert "newtag1, newtag2" in output
    assert "2026-01-20 12:00" in output
    assert "daily" in output
    assert "Task to Update" not in output # Original title should not be present

def test_delete_task(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, ["1", "Task to Delete", "", "", "", "", "4", "1", "yes", "2", "0"])
    
    with pytest.raises(SystemExit):
        main()
    
    output = cli_test_setup.getvalue()
    
    assert "Task 'Task to Delete' (ID: 1) deleted successfully!" in output
    assert "No tasks to display." in output # After deletion, list should be empty

def test_mark_task_complete(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, ["1", "Task to Complete", "", "", "", "", "5", "1", "yes", "2", "0"])
    
    with pytest.raises(SystemExit):
        main()
    
    output = cli_test_setup.getvalue()
    
    assert "Task 'Task to Complete' (ID: 1) marked as completed!" in output
    assert "☑" in output # Check for filled checkbox symbol in output
    assert "☐" not in output # Original empty checkbox should not be present

def test_search_tasks(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Task A with keyword", "", "", "", "",
        "1", "Task B", "Another keyword here", "", "", "",
        "1", "Task C", "", "", "", "",
        "6", "1", "keyword", "0", "0"
    ])

    with pytest.raises(SystemExit):
        main()

    output = cli_test_setup.getvalue()
    assert "Search Results for 'keyword'" in output
    assert "Task A with keyword" in output
    assert "Another keyword here" in output
    assert "Task C" not in output

def test_filter_tasks_by_status_and_priority(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Task High Incomplete", "", "", "", "",
        "5", "1", "yes", # Mark Task 1 complete
        "1", "Task Medium Incomplete", "", "", "high", "",
        "1", "Task Low Complete", "", "", "low", "",
        "5", "3", "yes", # Mark Task 3 complete
        "6", "2", "complete", "low", "", "0", "0" # Filter complete and low priority
    ])

    with pytest.raises(SystemExit):
        main()

    output = cli_test_setup.getvalue()
    assert "Filtered Tasks" in output
    assert "Task Low Complete" in output # Should be the only one matching
    assert "Task High Incomplete" not in output
    assert "Task Medium Incomplete" not in output

def test_filter_tasks_by_tag(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Task A", "", "work", "", "",
        "1", "Task B", "", "home, urgent", "", "",
        "1", "Task C", "", "work", "", "",
        "6", "2", "", "", "work", "0", "0" # Filter by tag "work"
    ])

    with pytest.raises(SystemExit):
        main()

    output = cli_test_setup.getvalue()
    assert "Filtered Tasks" in output
    assert "Task A" in output
    assert "Task C" in output
    assert "Task B" not in output

def test_sort_tasks_by_priority(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Task Medium", "", "", "medium", "",
        "1", "Task High", "", "", "high", "",
        "1", "Task Low", "", "", "low", "",
        "6", "3", "priority", "desc", "0", "0" # Sort by priority descending
    ])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    # Check order manually, Rich table might be tricky. Look for relative order.
    # High should come before Medium, Medium before Low
    high_index = output.find("Task High")
    medium_index = output.find("Task Medium")
    low_index = output.find("Task Low")
    assert high_index < medium_index < low_index, "Tasks not sorted by priority descending correctly"

def test_sort_tasks_by_title_asc(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Task C", "", "", "", "",
        "1", "Task A", "", "", "", "",
        "1", "Task B", "", "", "", "",
        "6", "3", "title", "asc", "0", "0" # Sort by title ascending
    ])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    a_index = output.find("Task A")
    b_index = output.find("Task B")
    c_index = output.find("Task C")
    assert a_index < b_index < c_index, "Tasks not sorted by title ascending correctly"

def test_add_task_with_due_date_and_recurrence(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, ["1", "Meeting", "Team sync", "work", "2026-01-05 09:00", "weekly", "2", "0"])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    assert "Task 'Meeting' (ID: 1) added successfully!" in output
    assert "2026-01-05 09:00" in output
    assert "weekly" in output

def test_update_task_due_date_and_recurrence(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "1", "Initial Task", "", "", "", "",
        "3", "1", "", "", "", "", "2026-01-10 14:00", "monthly",
        "2", "0"
    ])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    assert "Task (ID: 1) updated successfully!" in output
    assert "2026-01-10 14:00" in output
    assert "monthly" in output

def test_overdue_task_highlight(monkeypatch, cli_test_setup):
    # Simulate a task with a past due date
    past_date = datetime.now() - timedelta(days=1)
    simulate_input(monkeypatch, [
        "1", "Overdue Task", "", "", past_date.strftime("%Y-%m-%d %H:%M"), "",
        "2", "0" # View tasks and exit
    ])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    assert "(Overdue)" in output
    assert "bold red" in output # Rich adds style tags
    assert "Overdue Task" in output

def test_create_recurring_task_menu(monkeypatch, cli_test_setup):
    simulate_input(monkeypatch, [
        "7", "1", "Daily Standup", "Quick team sync", "work", "2026-01-02 09:00", "daily",
        "0", "0" # Back to main, then exit
    ])
    with pytest.raises(SystemExit):
        main()
    output = cli_test_setup.getvalue()
    assert "Recurring Task 'Daily Standup' (ID: 1) with rule 'daily' added successfully!" in output
    assert "Note: Simulating recurrence" in output # Check for the placeholder message
