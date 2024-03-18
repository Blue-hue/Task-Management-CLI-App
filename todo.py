import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todos, delete_todo, insert_todo, complete_todo, update_todo

console = Console()

app = typer.Typer()

app_config = {
    "name": "taskcli",
    "add_completion": False,
    "options_metavar": False,
    "help": "taskcli is a CLI tool to manage tasks with command line",
}

# Apply the configuration settings to the application
for key, value in app_config.items():
    setattr(app, key, value)

@app.command(short_help='Add an item')
def add(task: str, category: str = typer.Argument('Misc')):
    """
    Add a task to the todo list.

    Arguments:\n
    - task: The task to add.\n
    - category: The category of the task.

    Example usage:\n
        python todo.py add "Complete assignment" "School"
    """
    typer.echo(f"adding {task}, category: {category}")
    todo = Todo(task, category)
    insert_todo(todo)
    show()

@app.command(short_help='Delete a task from the todo list')
def delete(position: int):
    """
    Delete a task from the todo list.

    Arguments:\n
    - position: The position of the task to delete (1-based index).

    Example usage:\n
        python todo.py delete 1
    """
    typer.echo(f"Deleting task at position {position}")
    # Indices in UI begin at 1, but in the database at 0
    delete_todo(position - 1)
    show()


@app.command(short_help='Update a task in the todo list')
def update(
    position: int,
    task: str = typer.Option(None, help="The updated task description"),
    category: str = typer.Option(None, help="The updated category of the task"),
):
    """
    Update a task in the todo list.

    Arguments:\n
    - position: The position of the task to update (1-based index).\n
    - task: The updated task description (optional).\n
    - category: The updated category of the task (optional).\n

    Example usage:\n
        python todo.py update 1 --task "Updated task description" --category "Work"
    """
    typer.echo(f"Updated task at position {position}")
    update_todo(position - 1, task, category)
    show()

@app.command(short_help='Mark a task as complete')
def complete(position: int):
    """
    Mark a task as complete in the todo list.

    Arguments:\n
    - position: The position of the task to mark as complete (1-based index).

    Example usage:\n
        python todo.py complete 1
    """
    typer.echo(f"Completing task at position {position}")
    complete_todo(position - 1)
    show()

@app.command(short_help='Display the to-do list')
def show():
    tasks = get_all_todos()
    console.print("[bold magenta]My To-Do List[/bold magenta]!", "💻")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style="dim", width=6)
    table.add_column("Task description", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'YouTube': 'red', 'Sports': 'cyan', 'Study': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'

    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(idx), task.task, f'[{c}]{task.category}[/{c}]', is_done_str)
    console.print(table)

if __name__ == "__main__":
    app()