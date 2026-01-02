import sys
from cli.menu import display_main_menu, get_user_choice, add_task_menu, view_task_list_menu, update_task_menu, delete_task_menu, mark_task_complete_menu, search_filter_sort_menu, advanced_features_menu
from logic.task_manager import TaskManager
from cli.utils import console

def main():
    task_manager = TaskManager()

    while True:
        display_main_menu()
        choice = get_user_choice()

        if choice == '1':
            add_task_menu(task_manager)
        elif choice == '2':
            view_task_list_menu(task_manager)
        elif choice == '3':
            update_task_menu(task_manager)
        elif choice == '4':
            delete_task_menu(task_manager)
        elif choice == '5':
            mark_task_complete_menu(task_manager)
        elif choice == '6':
            search_filter_sort_menu(task_manager)
        elif choice == '7':
            advanced_features_menu(task_manager)
        elif choice == '0':
            console.print("\n[bold green]Exiting Todo application. Goodbye![/bold green]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")

if __name__ == "__main__":
    main()