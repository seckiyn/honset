"""
    Contains the function that lexes and parses the task string
"""
from enum import Enum, auto
from dataclasses import dataclass
from logs import print_debug # print_error, print_info, print_done, print_debug

# TODO: We probably don't need these
"""
class TaskType(Enum):
    \"\"\"
        Enumaration that contains type of tasks
    \"\"\"
    MEMO = auto()
    WORK = auto()
    PRINT = auto()
"""
@dataclass
class TaskContainer:
    """
        A dataclass to contain the a task
        task_index: Importance of the task
        task_name: Name of the task
        task_string: Description of the task
    """
    task_index: int
    task_name: str
    task_string: str
# TODO: We probably don't need these
"""
TaskTypeNames = {
        "memo": TaskType.MEMO,
        "work": TaskType.WORK,
        "print": TaskType.PRINT
        }
"""

def lex_task_from_text(text: str) -> tuple:
    """
        Gets a text in a format
        "TaskType:TASK_DESCRIPTION"
        and returns a tuple containing tokens
    """
    task_index = None
    task_name = None
    task_string = None
    text_splitted_by_score = text.split("-")
    if len(text_splitted_by_score) != 2:
        raise SyntaxError(f"This is not a regularly formatted text for task index: {text}")
    task_index_str, task_name_and_string = text_splitted_by_score
    task_index_str = task_index_str.strip()
    if not task_index_str.isnumeric():
        raise SyntaxError("Task index must be a positive integer")
    task_index = int(task_index_str)
    text_splitted_by_colon = task_name_and_string.split(":")
    if len(text_splitted_by_colon) != 2:
        raise SyntaxError(f"This is not a regularly formatted text for colon: {text}")
    task_name, task_string = text_splitted_by_colon
    task_name = task_name.strip()
    task_string = task_string.strip()
    return (task_index, task_name, task_string)


def parse_task_from_text(text: str) -> TaskContainer:
    """
        Gets a text in a format
        "TaskType:TASK_DESCRIPTION"
        and returns a TaskContainer object

    """
    task_container = None
    task_index, task_name, task_string = lex_task_from_text(text)
    assert isinstance(task_index, int), "Something must be wrong with lex_task_from_text"
    assert isinstance(task_name, str), "Something must be wrong with lex_task_from_text"
    assert isinstance(task_string, str), "Something must be wrong with lex_task_from_text"
    task_container = TaskContainer(task_index, task_name, task_string)
    print_debug(task_container)
    return task_container
