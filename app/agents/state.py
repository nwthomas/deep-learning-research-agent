from typing import cast

from pydantic import BaseModel, Field
from pydantic_ai import RunContext, Tool


class File(BaseModel):
    """File for the supervisor agent."""

    name: str
    contents: str
    summary: str


class TodoItem(BaseModel):
    """Todo item for the supervisor agent."""

    completed: bool = Field(default=False)
    name: str
    summary: str


class State(BaseModel):
    """State for the supervisor agent."""

    files: dict[str, File] = Field(default_factory=dict)
    todos: dict[str, TodoItem] = Field(default_factory=dict)


@Tool
def add_file(ctx: RunContext[State], name: str, contents: str, summary: str) -> None:
    """Add a file to the state.

    Args:
        name: The name of the file
        contents: The contents of the file
        summary: The summary of the file
    """

    ctx.deps.files[name] = File(
        name=name,
        contents=contents,
        summary=summary,
    )


@Tool
def get_file_names(ctx: RunContext[State]) -> list[str]:
    """Get a list of the names of the files stored in state

    Returns:
        List[str]: The names of the files
    """

    return list(ctx.deps.files.keys())


@Tool
def get_file(ctx: RunContext[State], name: str) -> File | None:
    """Get a file from the state.

    Args:
        name: The name of the file

    Returns:
        File | None: The file or None if the file does not exist
    """

    return cast(File | None, ctx.deps.files.get(name))


@Tool
def add_todo(ctx: RunContext[State], name: str, summary: str) -> None:
    """Add a todo item to the state.

    Args:
        name: The name of the todo item
        summary: The summary of the todo item
    """

    ctx.deps.todos[name] = TodoItem(name=name, summary=summary)


@Tool
def get_todo_names(ctx: RunContext[State]) -> list[str]:
    """Get a list of the names of the todo items stored in state

    Returns:
        List[str]: The names of the todo items
    """

    return list(ctx.deps.todos.keys())


@Tool
def get_todos(ctx: RunContext[State]) -> list[TodoItem]:
    """Get a list of the todo items stored in state

    Returns:
        List[TodoItem]: The todo items
    """

    return list(ctx.deps.todos.values())


@Tool
def get_todo(ctx: RunContext[State], name: str) -> TodoItem | None:
    """Get a todo item from the state.

    Args:
        name: The name of the todo item

    Returns:
        TodoItem | None: The todo item or None if the todo item does not exist
    """

    return cast(TodoItem | None, ctx.deps.todos.get(name))


@Tool
def complete_todo(ctx: RunContext[State], name: str) -> None:
    """Complete a todo item in the state.

    Args:
        name: The name of the todo item
    """

    if todo_item := ctx.deps.todos.get(name):
        todo_item.completed = True
    else:
        raise ValueError(f"Todo item {name} not found")
