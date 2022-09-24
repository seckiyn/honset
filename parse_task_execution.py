"""
    This is a module that will parse execution like
    PRINT("HELLO WORLD")
    MEM  ("HELLOW")
"""
from logs import print_info, print_debug
from enum import Enum, auto

class TokenType(Enum):
    """
        TokenType
    """
    RIGHT_PAREN = auto()
    LEFT_PAREN = auto()
    STRING = auto()
    LIST = auto()
    STRING_LITERAL = auto()


def get_string_token(text, index):
    """
        Returns a WORD token
    """
    string = ""
    while text[index].isalnum() and index < len(text):
        string += text[index]
        index += 1
        # print("character is ' '", character == " ")
    print(string)
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
    print(string)
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
        print_debug("Token list", tokens)
        print_debug("Token is", token)
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
            return index, (TokenType.STRING, string)
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
        else:
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


def lex_execution(text: str) -> tuple:
    tokens = list()
    tokens = get_token_list(text)
    print_info(*tokens, sep="\n")
    return tuple()





def tests():
    to_lex = ["""
        PRINT (Lots of work)
        MEM (["This", "that"])
        WORK ("This is what you work")
    """,
    """
    MEM(["HELLO"])

    """]
    for lex in to_lex:
        lex_execution(lex)


    while True:
        print(lex_execution(input("What to lex:")))

if __name__ == "__main__":
    print("hello world")
    tests()
