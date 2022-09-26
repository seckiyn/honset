"""
    Main script of honset
"""
from logs import print_error, print_info, print_done, print_debug
from parse_task import lex_task_from_text, parse_task_from_text
from parse_task_execution import get_parse_execution




def main() -> int:
    """
        Main function
    """
    execution = get_parse_execution("Mem([World])")
    print(execution.value)
    return 1



if __name__ == "__main__":
    main()
