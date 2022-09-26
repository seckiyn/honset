"""
    Testing
"""
from parse_task_execution import get_lex_execution, get_parse_execution
from parse_task import lex_task_from_text, parse_task_from_text
from parse_all import parse_the_file
from logs import print_error, print_info, print_done, print_debug

def parse_task_tests() -> int:
    """
        Test the functions
    """
    print_info("Starting to test")
    wrong_tasks = ["1-2-3-", "1 - memo: hello: world:", "hellow"]
    print_debug("Wrong tasks:", wrong_tasks)
    # Test lex_task_from_text
    for task in wrong_tasks:
        try: # to use wrong tasks on LEXER
            lex_task_from_text(task)
            print_error("parse_task_tests", "Lex is not complete")
        except SyntaxError:
            print_done("parse_task_tests", "Lex is complete")
        try: # to use wrong tasks on PARSER
            parse_task_from_text(task)
            print_error("parse_task_tests", "Parse is not complete")
        except SyntaxError:
            print_done("parse_task_tests", "Parse is complete")

    true_tasks = ["1 - memo: hello this is a task", ]
    print_debug("parse_task_tests", "True tasks:", true_tasks)
    for task in true_tasks:
        try: # This is the one perfect
            lex_task_from_text(task)
            print_done("parse_task_tests", "Lex is complete")
        except SyntaxError:
            print_error("parse_task_tests", "Lex is not complete")
        try: # to use wrong tasks on PARSER
            parse_task_from_text(task)
            print_done("parse_task_tests", "Parse is complete")
        except SyntaxError:
            print_error("parse_task_tests", "Parse is not complete")

def lex_execution_tests() -> int:
    """
        Test functions from parse_task_execution
    """
    to_lex = [
    """
        PRINT (Lots of work)
        MEM (["This", "that"])
        WORK ("This is what you work")
    """,
    "MEM([\"HELLO\"])"
    ]
    for lex in to_lex:
        lexed = get_lex_execution(lex)
        if lexed:
            print_done("parse_lex_execution_tests:", hash(lex))
        else:
            print_error("Something is wrong")

def parse_execution_tests() -> int:
    tests = [
            "WORK(\"[YOU, SHOULD, MEMORIZE, THIS]\")"
            ]
    for test in tests:
        parsed = get_parse_execution(test)
        if parsed:
            print_done("parse_execution_tests", test)
        else:
            print_error("parse_execution_tests", test)
    return 1
def parse_file_tests() -> int:
    parsed = parse_the_file("test")
    if parsed: print_done("parse_file_tests: test.ns")
    else:
        print_error("parse_file_tests: test.ns")
    return int(bool(parsed))
def tests():
    parse_task_tests()
    lex_execution_tests()
    parse_execution_tests()
    parse_file_tests()
if __name__ == "__main__":
    tests()
