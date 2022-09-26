"""
    This is a module that will parse execution like
    PRINT("HELLO WORLD")
    MEM  ("HELLOW")
"""
from typing import Union
from dataclasses import dataclass
from enum import Enum, auto

# from logs import print_info, print_debug
class TokenType(Enum):
    """
        TokenType
    """
    RIGHT_PAREN = auto()
    LEFT_PAREN = auto()
    WORD = auto()
    LIST = auto()
    STRING_LITERAL = auto()


def get_string_token(text, index):
    """
        Returns a WORD token
    """
    string = ""
    while index < len(text) and text[index].isalnum():
        string += text[index]
        index += 1
        # print("character is ' '", character == " ")
    # print(string)
    return index-1, string

def get_string_literal_token(text, index):
    """
        When the get_next_token encounters double quotes
        this function will return anything before other
        double quotes
    """
    string = ""
    while index < len(text) and text[index] != "\"":
        string += text[index]
        index += 1
        # print("character is ' '", character == " ")
    # print(string)
    return index+1, string
def get_list_token(text, index):
    """
        When get_next_token encounters a square brackets([)
        this function will return all of the tokens as a whole
        token
    """
    tokens = list()
    while index < len(text) and text[index] != "]":
        index, token = get_next_token(text, index)
        # print_debug("Token list", tokens)
        # print_debug("Token is", token)
        tokens.append(token)
    return index+1, tokens
def get_next_token(text, index):
    """
        Returns the next token
    """
    token = None
    while index < len(text):
        if text[index].isalnum():
            index, string = get_string_token(text, index)
            index += 1
            return index, (TokenType.WORD, string)
        if text[index] == "(":
            index += 1
            return index, (TokenType.LEFT_PAREN, None)
        if text[index] == ")":
            index += 1
            return index, (TokenType.RIGHT_PAREN, None)
        if text[index] == "[":
            index += 1
            index, parsed_list = get_list_token(text, index)
            return index, (TokenType.LIST, parsed_list)
        if text[index] == "\"":
            index += 1
            index, string = get_string_literal_token(text, index)
            return index, (TokenType.STRING_LITERAL, string)
        if text[index] in ("\n", " ", ","):
            index += 1
            continue
        if text[index] == "]":
            # print("heya")
            return index, token
        raise Exception(f"Unreachable \"{text[index]}\"")
    return index, token

def get_token_list(text: str) -> list:
    """
        Gets a text and returns a list of tokens
    """
    index = 0
    tokens = list()
    while index < len(text):
        index, token = get_next_token(text, index)
        tokens.append(token)
    return tokens


def get_lex_execution(text: str) -> tuple:
    """
        Returns the list of execution tokens
    """
    tokens = list()
    tokens = get_token_list(text)
    return tuple(tokens)

class ExecutionType(Enum):
    """
        Type of the executions
        MEM: Memorization
        WORK: Work for
        PRINT: Print to screen
    """
    MEM = auto()
    WORK = auto()
    PRINT = auto()
@dataclass
class Execution:
    """
        A container for Execution object
        MEM: MEM LPAREN LIST RPAREN
        WORK: WORK LPAREN STRING RPAREN
        PRINT: PRINT LPAREN STRING RPAREN
    """
    execute: ExecutionType
    value: Union[str, list]

def check_paren(tokens: tuple, word: ExecutionType) -> tuple:
    """
        Checks if token list has parens if needed
    """
    paren_start, *tokens = tokens
    if len(tokens) < 1:
        raise SyntaxError("There's not enough tokens to parse in check_parentheses")
    *tokens, paren_end = tokens
    if (paren_start[0] != TokenType.LEFT_PAREN or
            paren_end[0] != TokenType.RIGHT_PAREN):
        raise SyntaxError(f"{word} need parens")
    return tokens

def get_parse_execution(text: str) -> Execution:
    """
        Returns the parsed line
    """
    assert bool(text), "Text must be checked before get_parse_execution"
    tokens = get_lex_execution(text)
    execution_token = None
    if len(tokens) != 1:
        execution_token, *tokens = tokens
    else:
        execution_token = tokens[0]
        print_debug(execution_token)
    # print_debug(tokens)
    assert len(tokens) != 0, "Text must be contain at least 1 token\
            before passed get_parse_execution"
    execution_token, value = execution_token
    value = value.upper()
    if execution_token != TokenType.WORD:
        raise SyntaxError("Execution should start with a WORD")
    assert len(ExecutionType) == 3, "You forgot to parse a new execution"
    # PARSING OF WORDS
    if value == "MEM":
        name_of_the_execution = ExecutionType.MEM
        tokens = check_paren(tokens, name_of_the_execution)
        if len(tokens) != 1:
            raise SyntaxError(f"Too many arguments for {name_of_the_execution}:Arguments({tokens})")
        list_token, list_value = tokens[0]
        if list_token != TokenType.LIST:
            raise SyntaxError(f"{name_of_the_execution} only accepts\
                    a {TokenType.LIST} you passed {list_token}")
        listed_token_value = [lv[1].strip() for lv in list_value]
        return Execution(name_of_the_execution, listed_token_value)

    if value == "PRINT":
        name_of_the_execution = ExecutionType.PRINT
        tokens = check_paren(tokens, name_of_the_execution)
        if len(tokens) != 1:
            raise SyntaxError(f"Too many arguments for {name_of_the_execution}:Arguments({tokens})")
        print_token, print_value = tokens[0]
        if print_token != TokenType.STRING_LITERAL:
            raise SyntaxError(f"{name_of_the_execution} only accepts \
                    a {TokenType.STRING_LITERAL} you passed {list_token}")
        string_value = print_value
        return Execution(name_of_the_execution, string_value)
    if value == "WORK":
        name_of_the_execution = ExecutionType.WORK
        tokens = check_paren(tokens, name_of_the_execution)
        if len(tokens) != 1:
            raise SyntaxError(f"Too many arguments for {name_of_the_execution}:Arguments({tokens})")
        print_token, print_value = tokens[0]
        if print_token != TokenType.STRING_LITERAL:
            raise SyntaxError(f"{name_of_the_execution} only accepts \
                    a {TokenType.STRING_LITERAL} you passed {list_token}")
        string_value = print_value
        return Execution(name_of_the_execution, string_value)
    raise SyntaxError(f"This is a unknow WORD: {value}")




if __name__ == "__main__":
    pass
