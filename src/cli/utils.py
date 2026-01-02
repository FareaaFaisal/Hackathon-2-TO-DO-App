from rich.console import Console

console = Console()

CHECK_BOX_EMPTY = "☐"
CHECK_BOX_FILLED = "☑"

SUCCESS = "bold green"
ERROR = "bold red"
WARNING = "bold yellow"
INFO = "bold blue"


def get_valid_input(prompt, validator=None, error_message="Invalid input."):
    while True:
        value = input(prompt).strip()
        if validator is None or validator(value):
            return value
        print_error(error_message)


def get_integer_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                raise ValueError
            if max_value is not None and value > max_value:
                raise ValueError
            return value
        except ValueError:
            print_error("Please enter a valid number.")


def get_confirmation(message):
    while True:
        choice = input(f"{message} (yes/no): ").lower()
        if choice in ("yes", "no"):
            return choice == "yes"
        print_warning("Please answer 'yes' or 'no'.")


def print_header(title, style="bold white"):
    console.rule(f"[{style}]{title}[/{style}]")


def print_success(message):
    console.print(f"[{SUCCESS}]{message}[/{SUCCESS}]")


def print_error(message):
    console.print(f"[{ERROR}]{message}[/{ERROR}]")


def print_warning(message):
    console.print(f"[{WARNING}]{message}[/{WARNING}]")
