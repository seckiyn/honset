"""
    Testing
"""
from parse_task import lex_task_from_text, parse_task_from_text
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
            print_error("Lex is not complete")
        except SyntaxError:
            print_done("Lex is complete")
        try: # to use wrong tasks on PARSER
            parse_task_from_text(task)
            print_error("Parse is not complete")
        except SyntaxError:
            print_done("Parse is complete")

    true_tasks = ["1 - memo: hello this is a task", ]
    print_debug("True tasks:", true_tasks)
    for task in true_tasks:
        try: # This is the one perfect
            lex_task_from_text(task)
            print_done("Lex is complete")
        except SyntaxError:
            print_error("Lex is not complete")
        try: # to use wrong tasks on PARSER
            parse_task_from_text(task)
            print_done("Parse is complete")
        except SyntaxError:
            print_error("Parse is not complete")

def tests():
    parse_task_tests()
if __name__ == "__main__":
    tests()
