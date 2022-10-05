"""
    This is a module that will parse execution like
    PRINT("HELLO WORLD")
    MEM  ("HELLOW")
"""
from typing import Tuple, List
from typing import Union
from dataclasses import dataclass
from enum import Enum, auto
from logs import print_debug, print_error, print_done

class TokenType(Enum):
    """
        TokenType
    """
    RIGHT_PAREN = auto()
    LEFT_PAREN = auto()
    WORD = auto()
    LIST = auto()
    STRING_LITERAL = auto()
    SEP = auto()


def get_string_token(text, index):
    """
        Returns a WORD token
    """
    string = ""
    while index < len(text) and text[index].isalnum():
        string += text[index]
        index += 1
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
            return index, token
        if text[index] == ";":
            index += 1
            return index, (TokenType.SEP, None)
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
    CONTAINER = auto()
    PLACE = auto()
    IF = auto()

@dataclass
class Execution:
    """
        A container for Execution object
        MEM: MEM LPAREN LIST RPAREN
        WORK: WORK LPAREN STRING RPAREN
        PRINT: PRINT LPAREN STRING RPAREN
    """
    execute: ExecutionType
    value: Union[str, list, tuple]
    # position: Tuple

def check_paren(tokens: Tuple, word: ExecutionType) -> Tuple:
    """
        Checks if token list has parens if needed
    """
    old_tokens = tokens[:]
    paren_start, *tokens = tokens
    if len(tokens) < 1:
        raise SyntaxError("There's not enough tokens to parse in check_parentheses")
    *tokens, paren_end = tokens
    if (paren_start[0] != TokenType.LEFT_PAREN or
            paren_end[0] != TokenType.RIGHT_PAREN):
        print(*old_tokens, sep="\n")
        raise SyntaxError(f"{word} need parens, tokens: ")
    return tokens

def get_parse_execution(text: str) -> Execution:
    """
        Returns the parsed line
    """
    assert bool(text), "Text must be checked before get_parse_execution"
    tokens = get_lex_execution(text)
    return get_parse_execution_by_token(tokens)

def get_parse_execution_by_token(tokens: List[TokenType]):
    execution_token = None
    if len(tokens) != 1:
        execution_token, *tokens = tokens
    else:
        execution_token = tokens[0]
    assert len(tokens) != 0, "Text must be contain at least 1 token\
            before passed get_parse_execution"
    execution_token, value = execution_token
    value = value.upper()
    if execution_token != TokenType.WORD:
        raise SyntaxError("Execution should start with a WORD")
    assert len(ExecutionType) == 6, "You forgot to parse a new execution"
    # PARSING OF WORDS
    if value == "MEM":
        name_of_the_execution = ExecutionType.MEM
        tokens = check_paren(tokens, name_of_the_execution)
        if len(tokens) != 2:
            raise SyntaxError(f"Too less arguments for {name_of_the_execution}:arguments({tokens})")
        string_literal_token, string_literal_value = tokens[0]
        if string_literal_token != TokenType.STRING_LITERAL:
            raise SyntaxError(f"{name_of_the_execution} only accepts\
                    a {TokenType.STRING_LITERAL} you passed {string_literal_token}")
        list_token, list_value = tokens[1]
        if list_token != TokenType.LIST:
            raise SyntaxError(f"{name_of_the_execution} only accepts\
                    a {TokenType.LIST} you passed {list_token}")
        listed_token_value = [lv[1].strip() for lv in list_value]
        return Execution(name_of_the_execution, (string_literal_value, listed_token_value))

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
    if value == "CONTAINER":
        name_of_the_execution = ExecutionType.CONTAINER
        tokens = check_paren(tokens, name_of_the_execution)
        list_of_executes = seperate_by_token(tokens)
        list_of_executions = list()
        for executable in list_of_executes:
            container_execution = get_parse_execution_by_token(executable)
            list_of_executions.append(container_execution)

        return Execution(name_of_the_execution, list_of_executions)
    if value == "PLACE":
        name_of_the_execution = ExecutionType.PLACE
        tokens = check_paren(tokens, name_of_the_execution)
        if len(tokens) != 2:
            raise SyntaxError(f"{name_of_the_execution} takes two arguments")
        place_token, place_value = tokens[0]
        print_done(place_token)
        if place_token != TokenType.STRING_LITERAL:
            raise SyntaxError(f"{name_of_the_execution} takes string literal as its first argument")
        answer_token, answer_value = tokens[1]
        if answer_token != TokenType.STRING_LITERAL:
            raise SyntaxError(f"{name_of_the_execution} takes string literal as its second argument")
        return Execution(name_of_the_execution, (place_value, answer_value))
    if value == "IF":
        name_of_the_execution = ExecutionType.IF
        tokens = check_paren(tokens, name_of_the_execution)
        sep_tokens = seperate_by_token(tokens)
        if len(sep_tokens) != 2:
            raise SyntaxError(f"IF needs at least 2 arguments to you've given {len(sep_tokens)}")
        first_part, second_part = sep_tokens
        if len(first_part) != 1:
            if first_part[0][0] == TokenType.WORD:
                first_part = get_parse_execution_by_token(first_part)
            else:
                raise SyntaxError(f"Wrong token for IF {first_part}")
        else:
            first_part = first_part[0]
        print_debug(*first_part, sep="\n")
        print_debug(*second_part, sep="\n")
        if second_part[0][0] != TokenType.WORD:
            raise SyntaxError("Second part of IF should be an execution")
        second_part_as_execution = get_parse_execution_by_token(second_part)

        print_error(*tokens, sep="\n")
        return Execution(name_of_the_execution, (first_part, second_part_as_execution))

    raise SyntaxError(f"This is a unknown WORD: {value}")

def seperate_by_token(tokens):
    list_of_executions = list()
    temp_list = list()
    for token in tokens:
        if token[0] != TokenType.SEP:
            temp_list.append(token)
        else:
            list_of_executions.append(list(temp_list))
            temp_list = []
    list_of_executions.append(temp_list)
    return list_of_executions


if __name__ == "__main__":
    pass
