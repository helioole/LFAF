from parsing.type import TokenType
class Tokens:
    token_patterns = {
        TokenType.LPAREN: r'\(',
        TokenType.RPAREN: r'\)',
        TokenType.LBRACE: r'\{',
        TokenType.RBRACE: r'\}',
        TokenType.COMMA: r',',
        TokenType.ASSIGN_EQUAL: r'=',
        TokenType.SEMICOLON: r';',
        TokenType.PLUS: r'\+',
        TokenType.MINUS: r'\-',
        TokenType.MULTIPLY: r'\*',
        TokenType.DIVIDE: r'\/',
        TokenType.MODULUS: r'\%',
        TokenType.GREATER: r'>',
        TokenType.LESS: r'<',
        TokenType.NOT_EQUAL: r'!=',
        TokenType.IF: r'if',
        TokenType.ELSE: r'else',
        TokenType.FOR: r'for',
        TokenType.RETURN: r'return',
        TokenType.BREAK: r'break',
        TokenType.VAR: r'var',
        TokenType.FUNCTION: r'function',
        TokenType.ID: r'[a-zA-Z_]\w*',
        TokenType.NUMBER: r'\d+(\.\d+)?',
        TokenType.STRING: r'"[^"]*"',
        TokenType.WHITESPACE: r'\s+',
        TokenType.COMMENT: r'\/\/.*'
    }

    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern
