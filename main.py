from lexer.Lexer import Lexer
from parsing.Parser import Parser

def main():
    input_string = '''
        function gcd(a, b) {
            if (b = 0) {
                return a;
            }
            else {
                return gcd(b, a % b);
            }
        }
    '''

    lexer = Lexer()
    tokens = lexer.tokenize(input_string)

    parser = Parser()
    ast = parser.parse(tokens)
    ast.visualize()

if __name__ == "__main__":
    main()

