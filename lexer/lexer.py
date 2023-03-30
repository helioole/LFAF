from lexer.tokens import Tokens
import re


class Lexer:
    def __init__(self):
        self.token_patterns = [Tokens(name, pattern) for name, pattern in Tokens.token_patterns.items()]

    def tokenize(self, inputs):
        global token_value
        tokens = []
        leftb = 'LEFT_BRACE', '{'
        rightb = 'RIGHT_BRACE', '}'
        leftp = 'LEFT_PAREN', '('
        rightp = 'RIGHT_PAREN', ')'

        lbrace_count = 0
        rbrace_count = 0
        lparen_count = 0
        rparen_count = 0

        while inputs:
            match = None
            for token in self.token_patterns:
                match = re.match(token.pattern, inputs)
                if match:
                    token_value = (token.name, match.group(0))
                    if token_value[0] != "WHITESPACE":
                        tokens.append(token_value)
                    inputs = inputs[len(token_value[1]):]
                    break

            if not match:
                raise SyntaxError(f'Invalid syntax: {token_value}')

            lbrace_count = tokens.count(leftb)
            rbrace_count = tokens.count(rightb)
            lparen_count = tokens.count(leftp)
            rparen_count = tokens.count(rightp)

        if ((leftb in tokens) or (rightb in tokens)) \
                and ((tokens.index(leftb) > tokens.index(rightb))
                     or (lbrace_count != rbrace_count)):
            raise SyntaxError(f'Invalid syntax: {token_value}')

        elif ((leftp in tokens) or (rightp in tokens)) \
                and ((tokens.index(leftp) > tokens.index(rightp))
                     or (lparen_count != rparen_count)):
            raise SyntaxError(f'Invalid syntax: {token_value}')

        return tokens
