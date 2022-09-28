#!/usr/bin/env python3
"""
    Main script of honset
"""
import sys
from logs import print_error, print_info, print_done, print_debug
from parse_task import lex_task_from_text, parse_task_from_text
from parse_task_execution import get_parse_execution
from parse_all import parse_the_file, parse_the_file_current
from handle_parsed_data import handle_data

def usage() -> int:
    print("Usage:" + __file__ + " [OPTIONS] <todo>")
    print(" -h,     --help          " + "    Shows this help")
    print(" -f,     --file <file>   " + "    Uses the file  ")
    return 1
def parse_file(filename) -> int:
    parsed_file = parse_the_file_current(filename)
    handle_data(parsed_file)
    return 1

def args() -> int:
    arguments = sys.argv
    script_name, *arguments = arguments
    if "-f" in arguments or "--file" in arguments:
        file, *filename = arguments
        print(filename)
        if len(filename) != 1:
            sys.exit(1)
        filename = filename[0]
        print(filename)
        return parse_file(filename)
    return usage()


def main() -> int:
    """
        Main function
    """
    handle_data(parse_the_file("games"))
    return args()



if __name__ == "__main__":
    sys.exit(main())
