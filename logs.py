"""
    A module to use logging and printing
"""
from pprint import pprint
from colorama import Fore, init
init(autoreset=True)
def print_error(*args, **kwargs):
    """
        Print wrapper to write errors
    """
    print(Fore.RED + "[ERROR]: ", *args, **kwargs)

def print_info(*args, **kwargs):
    """
        Print wrapper to write info
    """
    print(Fore.BLUE + "[INFO]: ", *args, **kwargs)

def print_done(*args, **kwargs):
    """
        Print wrapper to write completes
    """
    print(Fore.GREEN + "[DONE]", *args, **kwargs)

def print_debug(*args, **kwargs):
    """
        Print wrapper to write debugs
    """
    print(Fore.YELLOW + "[DEBUG]", *args, **kwargs)

def pretty_print(*args, **kwargs):
    """
        A wrapper for pretty print
    """
    pprint(*args, **kwargs)
