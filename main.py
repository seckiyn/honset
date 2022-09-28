"""
    Main script of honset
"""
import sys
from logs import print_error, print_info, print_done, print_debug
from parse_task import lex_task_from_text, parse_task_from_text
from parse_task_execution import get_parse_execution
from parse_all import parse_the_file

def args() -> int:
    arguments = sys.argv
    if "-p" in arguments:
        return None


def main() -> int:
    """
        Main function
    """
    return args()



if __name__ == "__main__":
    sys.exit(main())
