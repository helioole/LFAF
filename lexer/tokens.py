
class Tokens:
    patterns = {
        'FUNCTION': r'function',
        'NUMBER': r'\d+(\.\d+)?',
        'STRING': r'"[^"]*"',
        'LEFT_PAREN': r'\(',
        'RIGHT_PAREN': r'\)',
        'LEFT_BRACE': r'\{',
        'RIGHT_BRACE': r'\}',
        'COMMA': r',',
        'ASSIGN': r'=',
        'END': r';',
        'PLUS': r'\+',
        'MINUS': r'\-',
        'MULTIPLY': r'\*',
        'DIVIDE': r'\/',
        'MODULUS': r'\%',
        'GREATER': r'>',
        'GREATER_EQUAL': r'>=',
        'EQUAL': r'==',
        'LESS': r'<',
        'LESS_EQUAL': r'<=',
        'NOT_EQUAL': r'!=',
        'IF': r'if',
        'ELSE': r'else',
        'WHILE': r'while',
        'FOR': r'for',
        'RETURN': r'return',
        'BREAK': r'break',
        'CONTINUE': r'continue',
        'VARIABLE_DECLARATION': r'var',
        'WHITESPACE': r'\s+',
        'NAME': r'[a-zA-Z_]\w*',
        'NAME1': r'[a-z]\w*' + r'()',
        'COMMENT': r'//.*'
    }

    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern

