"""
    The module that will parse all file
"""
import re
from dataclasses import dataclass
from typing import List, Tuple
from os.path import join, dirname, realpath
from parse_task import parse_task_from_text, TaskContainer
from parse_task_execution import Execution, get_parse_execution

SCRIPT_PATH = dirname(realpath(__file__))
FOLDER = "" # "tasks"
EXT = ".ns"

# print(SCRIPT_PATH)
@dataclass
class Task:
    """
        A container for a whole Task
    """
    task_container: TaskContainer
    execute_container: List[Execution]

def read_file(filename: str) -> str:
    """
        Opens and reads filename and returns the containing
    """
    file_path = join(SCRIPT_PATH, FOLDER, filename+EXT)
    file_container = None
    with open(file_path, "r") as file:
        file_container = file.read()
    if not file_container:
        raise SyntaxError("The file is empty")
    return file_container

def parse_single_execute(execute: str) -> Execution:
    """
        Parses a single line of execute
    """
    parsed_execute = get_parse_execution(execute)
    return parsed_execute
def parse_all_execute(execute: str) -> Tuple[Execution]:
    """
        Gets a execute list like {EXECUTE*} and parses it into
        single Execution's
    """
    execute = execute[1:-1] # Strip the curly brackets
    lines = [e.strip() for e in execute.split("\n") if e.strip()]
    all_executes = list()
    for single_execute in lines:
        parsed_execute = parse_single_execute(single_execute)
        all_executes.append(parsed_execute)
    return tuple(all_executes)

def parse_single_task(task: str) -> TaskContainer:
    """
        Parses one task
    """
    parsed_task = parse_task_from_text(task)
    return parsed_task

def divide_into_task_execute(text: str) -> tuple:
    """
        Divides the whole file into
        TASK{EXECUTE}
        blocks
    """
    # NOTE: You can make this into a generator
    regex = """([^{}]+)({[^{}]+})"""
    prog = re.compile(regex)
    findall = prog.findall(text)
    return tuple(findall)
def parse_all_task_execute(task_execute: Tuple[Tuple[str, str]]) -> Tuple[Task]:
    """
        Gets the
        TASK{EXECUTE}*
        and parses all
        TASK{EXECUTE}
        blocks into
        Task
    """
    all_tasks = list()
    for task, execute in task_execute:
        parsed_task = parse_single_task(task)
        parsed_execute = parse_all_execute(execute)
        all_tasks.append(Task(parsed_task, parsed_execute))
    return tuple(all_tasks)
def parse_the_file(filename: str) -> List[List[Execution]]:
    """
        Main function to parsing of the file
    """
    file_container = read_file(filename)
    task_unparsed_container = divide_into_task_execute(file_container)
    tasks = parse_all_task_execute(task_unparsed_container)
    return tasks

def read_the_file_current(filename: str) -> str:
    """
        Opens and reads filename and returns the containing
    """
    file_container = None
    filename += ".ns"
    with open(filename, "r") as file:
        file_container = file.read()
    if not file_container:
        raise SyntaxError("The file is empty")
    return file_container
def parse_the_file_current(filename: str) -> List[List[Execution]]:
    file_container = read_the_file_current(filename)
    task_unparsed_container = divide_into_task_execute(file_container)
    tasks = parse_all_task_execute(task_unparsed_container)
    return tasks




if __name__ == "__main__":
    print(__file__)
