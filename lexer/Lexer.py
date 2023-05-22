import re

from lexer.tokens import Tokens
from parsing.type import TokenType

class Lexer:
    def __init__(self):
        self.token_patterns = [Tokens(name, pattern) for name, pattern in Tokens.token_patterns.items()]

    def tokenize(self, inputs):
        tokens = []
        while inputs:
            match = None
            for token in self.token_patterns:
                match = re.match(token.pattern, inputs)
                if match:
                    token_value = (token.name, match.group(0))
                    if token_value[0] != TokenType.WHITESPACE and token_value[0] != TokenType.COMMENT:
                        tokens.append(token_value)
                    inputs = inputs[len(token_value[1]):]
                    break

            if not match:
                raise SyntaxError(f'Invalid syntax: {inputs}')

        return tokens
