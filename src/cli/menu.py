from typing import List
from datetime import datetime

from logic.task_manager import TaskManager
from models.task import Task

from cli.utils import (
    console,
    print_header,
    print_success,
    print_error,
    print_warning,
    get_integer_input,
    get_confirmation,
    CHECK_BOX_EMPTY,
    CHECK_BOX_FILLED,
)

from rich.table import Table


# ================= MAIN MENU =================

def display_main_menu():
    print_header("Todo Application Menu")
    console.print("1. Add Task")
    console.print("2. View Task List")
    console.print("3. Update Task")
    console.print("4. Delete Task")
    console.print("5. Mark Task as Complete/Incomplete")
    console.print("6. Search, Filter, or Sort Tasks (Intermediate Level)")
    console.print("7. Advanced Task Features (Advanced Level)")
    console.print("0. Exit")


def get_user_choice():
    return input("Enter your choice: ").strip()


# ================= TABLE =================

def _display_tasks_table(tasks: List[Task], title_text: str):
    table = Table(title=title_text)

    table.add_column("ID", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Priority")
    table.add_column("Due Date")
    table.add_column("Tags")
    table.add_column("Recurrence")

    for task in tasks:
        status = CHECK_BOX_FILLED if task.is_completed else CHECK_BOX_EMPTY
        due = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else ""

        table.add_row(
            str(task.id),
            status,
            task.title,
            task.description or "",
            task.priority or "",
            due,
            ", ".join(task.tags) if task.tags else "",
            task.recurrence_rule or "",
        )

    console.print(table)


# ================= ADD =================

def add_task_menu(task_manager: TaskManager):
    print_header("Add Task")

    title = input("Title: ").strip()
    description = input("Description (optional): ").strip() or None
    tags = input("Tags (comma separated): ").strip()
    due = input("Due date (YYYY-MM-DD HH:MM, optional): ").strip()
    recurrence = input("Recurrence (daily/weekly/monthly/yearly, optional): ").strip() or None

    tags_list = [t.strip() for t in tags.split(",")] if tags else []

    due_date = None
    if due:
        due_date = datetime.strptime(due, "%Y-%m-%d %H:%M")

    try:
        task_manager.add_task(
            title=title,
            description=description,
            tags=tags_list,
            due_date=due_date,
            recurrence_rule=recurrence,
        )
        print_success("Task added successfully!")
    except Exception as e:
        print_error(str(e))


# ================= VIEW =================

def view_task_list_menu(task_manager: TaskManager):
    print_header("View Task List")

    tasks = task_manager.get_all_tasks()
    if not tasks:
        print_warning("No tasks available.")
        return

    _display_tasks_table(tasks, "Your Tasks")


# ================= UPDATE =================

def update_task_menu(task_manager: TaskManager):
    print_header("Update Task")

    task_id = get_integer_input("Enter task ID: ")
    task = task_manager.get_task_by_id(task_id)

    if not task:
        print_error("Task not found.")
        return

    title = input(f"New title [{task.title}]: ").strip() or None
    description = input("New description (leave blank to keep): ").strip() or None
    priority = input("Priority (high/medium/low): ").strip() or None

    task_manager.update_task(
        task_id,
        title=title,
        description=description,
        priority=priority,
    )

    print_success("Task updated successfully!")


# ================= DELETE =================

def delete_task_menu(task_manager: TaskManager):
    print_header("Delete Task")

    task_id = get_integer_input("Enter task ID to delete: ")
    task = task_manager.get_task_by_id(task_id)

    if not task:
        print_error("Task not found.")
        return

    if get_confirmation(f"Are you sure you want to delete '{task.title}'"):
        task_manager.delete_task(task_id)
        print_success("Task deleted successfully!")


# ================= COMPLETE =================

def mark_task_complete_menu(task_manager: TaskManager):
    print_header("Mark Task Complete / Incomplete")

    task_id = get_integer_input("Enter task ID: ")
    task = task_manager.get_task_by_id(task_id)

    if not task:
        print_error("Task not found.")
        return

    action = "complete" if not task.is_completed else "incomplete"

    if get_confirmation(f"Mark task '{task.title}' as {action}?"):
        task_manager.mark_task_complete(task_id, not task.is_completed)
        print_success("Task status updated!")


# ================= SEARCH / FILTER / SORT =================

def search_filter_sort_menu(task_manager: TaskManager):
    while True:
        print_header("Search, Filter, or Sort Tasks")

        console.print("1. Search Tasks")
        console.print("2. Filter Tasks")
        console.print("3. Sort Tasks")
        console.print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            keyword = input("Enter keyword: ").strip()
            results = task_manager.search_tasks(keyword)
            _display_tasks_table(results, f"Search Results for '{keyword}'")

        elif choice == "2":
            status = input("Status (complete/incomplete): ").strip().lower()
            status_val = True if status == "complete" else False if status == "incomplete" else None
            results = task_manager.filter_tasks(status=status_val)
            _display_tasks_table(results, "Filtered Tasks")

        elif choice == "3":
            sort_by = input("Sort by (title/priority/due_date): ").strip()
            results = task_manager.sort_tasks(task_manager.get_all_tasks(), sort_by)
            _display_tasks_table(results, "Sorted Tasks")

        elif choice == "0":
            return

        else:
            print_error("Invalid choice.")


# ================= ADVANCED =================

def advanced_features_menu(task_manager: TaskManager):
    while True:
        print_header("Advanced Task Features")

        console.print("1. View Overdue Reminders")
        console.print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            overdue = task_manager.get_overdue_tasks()

            if not overdue:
                print_success("🎉 No overdue tasks!")
            else:
                print_header("Overdue Tasks", "bold red")
                _display_tasks_table(overdue, "Overdue Tasks")

        elif choice == "0":
            return

        else:
            print_error("Invalid choice.")
