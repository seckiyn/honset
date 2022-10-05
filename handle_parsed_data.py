from parse_all import Task, parse_the_file
from parse_task_execution import Execution, ExecutionType
from logs import *
from typing import Tuple


# HANDLING FUNCITONS
def handle_execution_print(value):
    print(value)

def handle_execution_work(value):
    print(value)

def handle_execution_mem(value):
    """
        Handle the occurance of TokenType.MEM
    """
    print("Can you recite this?")
    print(value[0])
    to_memorize = value[1]
    to_memorize = [i.lower() for i in to_memorize]
    while to_memorize:
        answer = input("Answer: ").lower().strip()
        if answer in to_memorize:
            to_memorize.remove(answer)
        else:
            print("This is wrong!")
    print("Congrulations")

def handle_execution_container(value):
    for execute in value:
        handle_execution(execute)

def handle_execution_place(value):
    """
        Value is a tuple of two string
    """
    place, answer = value
    answer = answer.lower()
    print(place)
    inp = None
    while inp != answer:
        inp = input("Answer: ").lower()

    print(f"Well done it was '{answer}'")

def handle_execution_if(value):
    first_part, second_part = value
    print_error(first_part, sep="\n")
    value = first_part[1]
    if value:
        handle_execution(second_part)
        return True # 
    else:
        return False

def handle_execution(execution: Execution):
    assert len(ExecutionType) == 6, "You forgot to handle and \
execution on handle_parsed_data:handle_execution"
    to_execute = execution.execute
    value = execution.value
    if to_execute == ExecutionType.PRINT:
        handle_execution_print(value)
        # print_info("YEY A PRINT")
    if to_execute == ExecutionType.WORK:
        handle_execution_work(value)
    if to_execute == ExecutionType.MEM:
        handle_execution_mem(value)
    if to_execute == ExecutionType.CONTAINER:
        handle_execution_container(value)
    if to_execute == ExecutionType.PLACE:
        handle_execution_place(value)
    if to_execute == ExecutionType.IF:
        response = handle_execution_if(value)
        return response


def handle_task(task: Task) -> int:
    task_name = task.task_container.task_name
    execute = task.execute_container
    response = None
    pointer = 0
    while pointer < len(execute):
        execution = execute[pointer]
        response = handle_execution(execution)
        print_debug(response)

        if response:
            pointer += 1

        pointer += 1
    return response
def handle_data(data: Tuple[Task]) -> int:
    """
        Gets the data as Tuple[Task] and sorts the data
        and executes tasks in order
    """
    tasks = sorted(data, \
            key=lambda x: x.task_container.task_index)
    pointer = 0
    response = None
    while pointer < len(tasks):
        task = tasks[pointer]
        response = handle_task(task)
        print_debug(response)
        pointer += 1
    return response


def main():
    pass

if __name__ == "__main__":
    # print("Hello, world")
    handle_data(parse_the_file("test"))
