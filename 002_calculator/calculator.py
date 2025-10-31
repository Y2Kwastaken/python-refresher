from typing import Callable
from enum import Enum

class Operator:
    """Operator for mathmatical operations
    
    This class allows for the priority assignment and operation of mathmatical functions
    """
    def __init__(self, priority: int, symbol: str, operate: Callable[[float, float], float]) -> None:
        self.priority = priority
        self.symbol = symbol
        self.operate = operate
        pass
    
    
    def has_priority(self, other: 'Operator') -> bool:
        """Determines whether or not this operation has priority over the given operator

        Args:
            other (Operator): the operator to copmare against

        Returns:
            bool: true if this operator has priority, false if the priority is ambiguous or inverted
        """
        return self.priority >  other.priority

OPERATORS = {
    '*': Operator(1, "*", lambda f, s: f * s),
    '/': Operator(1, "/", lambda f, s: f / s),
    '+': Operator(2, "+", lambda f, s: f + s),
    '-': Operator(2, "-", lambda f, s: f - s)
}

class TokenType(Enum):
    NUMBER = 1
    OPERATOR = 2
    INVALID = 3

class Token:
    def __init__(self, segment: str, type: TokenType):
        self.segment = segment
        self.type = type
        return
    
    def __str__(self) -> str:
        return "Token[{}|{}]".format(self.segment, self.type)

class ElementNode:
    def __init__(self, token: Token, operator: Operator | None, left: 'ElementNode | None', right: 'ElementNode | None'):
        self.token = token
        self.operator = operator
        self.left = left
        self.right = right
        return
    
    def operation_node(self) -> bool:
        return self.operator != None
    
    def __str__(self) -> str:
        return "Node({}) -> {} | {}".format(self.token.segment, self.left, self.right)
    
def new_root() -> ElementNode:
    return ElementNode(Token("", TokenType.INVALID), None, None, None)

def tokenize(input: str) -> list[Token]:
    """Tokenizes an input string into a list of tokens. Note this method does not strictly stop parsing
    the existance of TokenType.INVALID my persist. These can be validated later

    Args:
        input (str): the string to tokenize

    Returns:
        list[Token]: the tokens parsed
    """
    input += "\0" # insert null terminator for beloved proper string ending
    tokens: list[Token] = []
    segment: list[str] = []
    for char in input:
        if char == " " or char == "\0":
            conjoined = "".join(segment)
            if conjoined.isdigit():
                tokens.append(Token(conjoined, TokenType.NUMBER))
            elif conjoined in OPERATORS.keys():
                tokens.append(Token(conjoined, TokenType.OPERATOR))
            else:
                tokens.append(Token(conjoined, TokenType.INVALID))
            segment.clear()
        else:
            segment.append(char)
    return tokens

def validate_tokens(tokens: list[Token], strict: bool) -> bool:
    """validates all tokens in a list of tokens by ensuring they are sensically ordering and discarding 
    or failing on invalid tokens

    Args:
        tokens (list[Token]): the list of tokens to validate
        strict (bool): whether or not to fail on an invalid token
    """
    last: Token | None = None
    for token in tokens:
        if token.type == TokenType.INVALID and strict:
            print("Invalid Token {}".format(token.segment))
            return False
        elif token.type == TokenType.INVALID:
            continue
        elif last != None and token.type == last.type:
            print("Invalid Tokens {} followed by {}, which is not valid".format(last.segment, token.segment))
            return False
        last = token
        
    if last != None and last.type == TokenType.OPERATOR:
        print("Invalid Ending Token {}".format(last))
        return False

    return True

def find_highest_operator(tokens: list[Token]) -> tuple[ElementNode, int]:
    """Find the operator with the highest precedence.
       For operators with the same precedence, pick the rightmost one to preserve left-to-right order.
    """
    highest_op = None
    highest_index = -1

    for i, token in enumerate(tokens):
        if token.type != TokenType.OPERATOR:
            continue
        op = OPERATORS[token.segment]
        if highest_op is None or op.has_priority(highest_op) or (op.priority == highest_op.priority and i > highest_index):
            highest_op = op
            highest_index = i

    if highest_op is None:
        raise Exception("No operators present")

    return ElementNode(tokens[highest_index], highest_op, None, None), highest_index

def make_tree(tokens: list[Token]) -> ElementNode:
    """Recursively builds an expression tree respecting operator precedence."""
    if len(tokens) == 1:
        token = tokens[0]
        if token.type != TokenType.NUMBER:
            raise Exception(f"Invalid single token: {token.segment}")
        return ElementNode(token, None, None, None)

    # find the operator with highest precedence
    node, index = find_highest_operator(tokens)

    left_tokens = tokens[:index]
    right_tokens = tokens[index + 1:]

    if not left_tokens or not right_tokens:
        raise Exception(f"Malformed expression around operator '{node.token.segment}'")

    node.left = make_tree(left_tokens)
    node.right = make_tree(right_tokens)

    return node

def execute_tree(node: ElementNode) -> float:
    """Recursively evaluates an expression tree and returns the result."""
    if not node.operation_node():
        try:
            return float(node.token.segment)
        except ValueError:
            raise Exception(f"Invalid number token: {node.token.segment}")

    if node.left is None or node.right is None:
        raise Exception(f"Incomplete operation node for operator {node.operator.symbol}") # type: ignore

    left_val = execute_tree(node.left)
    right_val = execute_tree(node.right)

    result = node.operator.operate(left_val, right_val)  # type: ignore
    return result


def user_loop() -> None:
    while True:
        usr_in: str = input("")
        tokens: list[Token] = tokenize(usr_in)
        if not validate_tokens(tokens, True):
            continue
        tree: ElementNode | None = make_tree(tokens)
        print(execute_tree(tree))
    return

if __name__ == "__main__":
    print("Simple Calculator App Activated")
    user_loop()