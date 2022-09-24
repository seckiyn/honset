"""
    Main script of honset
"""
from logs import print_error, print_info, print_done, print_debug
from parse_task import lex_task_from_text, parse_task_from_text




def main() -> int:
    """
        Main function
    """
    tests()
    return 1



if __name__ == "__main__":
    main()
