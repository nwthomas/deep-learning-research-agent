"""Module: state.py

Description:
    This module contains state management for deep agents with TODO tracking and virtual file systems, including:
    - Task planning and progress tracking through TODO lists
    - Context offloading through a virtual file system stored in state
    - Efficient state merging with reducer functions

Author: Nathan Thomas
"""

from typing import Annotated, Literal, TypedDict

from langgraph.prebuilt.chat_agent_executor import AgentState


class Todo(TypedDict):
    """A structured task item for tracking progress through complex workflows.

    Attributes:
        content (str): Short, specific description of the task
        status (Literal["pending", "in_progress", "completed"]): Current state - pending, in_progress, or completed
    """

    content: str
    status: Literal["pending", "in_progress", "completed"]


def file_reducer(left: dict[str, str] | None, right: dict[str, str] | None) -> dict[str, str] | None:
    """Merge two file dictionaries, with right side taking precedence.

    Used as a reducer function for the files field in agent state,
    allowing incremental updates to the virtual file system.

    Args:
        left (dict[str, str] | None): Left side dictionary (existing files)
        right (dict[str, str] | None): Right side dictionary (new/updated files)

    Returns:
        dict[str, str] | None: Merged dictionary with right values overriding left values
    """

    if left is None:
        return right
    elif right is None:
        return left
    else:
        return {**left, **right}


def todo_reducer(left: list[Todo] | None, right: list[Todo] | None) -> list[Todo] | None:
    """Merge two todo lists, with right side taking precedence.

    Used as a reducer function for the todos field in agent state,
    allowing concurrent updates to the TODO list from multiple agents.

    Args:
        left (list[Todo] | None): Left side list (existing todos)
        right (list[Todo] | None): Right side list (new/updated todos)

    Returns:
        list[Todo] | None: Right side todos list, taking full precedence over left
    """

    if right is None:
        return left
    return right


class DeepAgentState(AgentState):
    """Extended agent state that includes task tracking and virtual file system.

    Inherits from LangGraph's AgentState and adds:
    - todos (Annotated[list[Todo], todo_reducer]): List of Todo items for task planning and progress tracking
    - files (Annotated[dict[str, str], file_reducer]): Virtual file system stored as dict mapping filenames to content
    """

    todos: Annotated[list[Todo], todo_reducer]
    files: Annotated[dict[str, str], file_reducer]
