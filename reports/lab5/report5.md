# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Racovcena Irina

___

## Theory Notations
### Parsing
Parsing is used to process and interpret code written in a specific programming language. 
A parser takes the code as input and verifies its syntax, ensuring that it conforms to the rules of 
the language's grammar. If the code is syntactically correct, the parser generates a parse tree or an 
abstract syntax tree (AST), which represents the code's structure and can be used for subsequent analysis or execution.

### Abstract Syntax Tree
AST stands for Abstract Syntax Tree. It is a hierarchical representation of the syntactic 
structure of source code or a programming language expression. An AST is typically generated during 
the parsing phase of a compiler or interpreter.

The purpose of an AST is to capture the essential structure of the code while 
abstracting away irrelevant details. It represents the code's logical structure in a way 
that is easier to analyze and manipulate than the raw source code. Each node in the AST represents 
a specific construct in the code, such as a function declaration, a loop, an assignment statement, or an expression.

The AST retains the hierarchical relationships between the nodes, reflecting the nesting and 
ordering of the code constructs. For example, in a programming language like Python, an AST 
for the code snippet `x = 5 + 3` would have a root node representing the assignment statement, 
with child nodes representing the variable `x`, the addition operator, and the operands `5` and `3`.

## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation
Firstly, I created a separate class for TokenType which includes all the tokens from the 3rd laboratory work and looks like this:
```python
class TokenType:
    MODULUS = "MODULUS"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    COMMA = "COMMA"
    ASSIGN_EQUAL = "ASSIGN_EQUAL"
    SEMICOLON = "SEMICOLON"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    GREATER = "GREATER"
    LESS = "LESS"
    NOT_EQUAL = "NOT_EQUAL"
    IF = "IF"
    ELSE = "ELSE"
    FOR = "FOR"
    RETURN = "RETURN"
    BREAK = "BREAK"
    VAR = "VAR"
    FUNCTION = "FUNCTION"
    ID = "ID"
    NUMBER = "NUMBER"
    STRING = "STRING"
    WHITESPACE = "WHITESPACE"
    COMMENT = "COMMENT"
```
Then, moving to AST we have a class that is responsible for all the implementations regarding it. It is build simply containing 
a constructor with `value` and a list for `children`. 

The method `add_child()` is used to add a child node to 
the current node. It takes a child parameter, 
representing the child node to be added, and appends it to the children list of the current node.

`visualize()` method represents the AST structure. It takes optional parameters `indent_level` and `is_last_child`, 
which determine the indentation level of the node and whether it is the last child of its parent. 
The method prints the value of the current node with appropriate indentation and connector characters to indicate the node's position in the tree.

`get_indentation()` returns a string containing whitespace characters that represent the indentation for a given `indent_level`. 
It calculates the number of spaces based on the `indent_level` parameter and a constant `spaces_per_indent`:

```python
class ASTNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def visualize(self, indent_level=0, is_last_child=True):
        indent = self.get_indentation(indent_level)
        connector = "└── " if is_last_child else "├── "

        print(indent + connector + self.value)

        if self.children:
            for i, child in enumerate(self.children):
                is_last = i == len(self.children) - 1
                child.visualize(indent_level + 1, is_last)

    def get_indentation(self, indent_level):
        spaces_per_indent = 4
        spaces = indent_level * spaces_per_indent
        return " " * spaces
```

The constructor method of the `Parser`initializes the tokens list as an empty list and sets the `current_token_index` to 0.

The `parse()` method is the entry point for parsing. It takes a list of tokens as input and initiates the parsing process. 
It sets the tokens attribute of the parser to the provided tokens list and resets the `current_token_index` to 0.
It then calls the `parse_program()` method to parse the entire program and returns the resulting AST.

This `parse_program()` method parses a program, which consists of multiple statements. It creates a new ASTNode object with the label `Program` to represent 
the root node of the program's AST. It iterates over the tokens until it reaches the end of the token 
list and calls the appropriate `parse_*` method based on the type of statement encountered. It adds the resulting statement node as a child of the program node. 
Finally, it returns the program node representing the entire AST.

The `parse_statement()` method parses a single statement. It checks the type of the 
current token and determines which specific statement parsing method to call based on 
the token's type. It sequentially checks for different token types (such as VAR, FUNCTION, IF, FOR, RETURN, BREAK), 
and if a match is found, it calls the corresponding parse_* method. If none of the specific statement types match, 
it assumes the statement to be an expression statement and calls the `parse_expression_statement()` method:

```python
class Parser:
    def __init__(self):
        self.tokens = []
        self.current_token_index = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        return self.parse_program()

    def parse_program(self):
        program_node = ASTNode("Program")
        while not self.is_end_of_tokens():
            statement = self.parse_statement()
            program_node.add_child(statement)
        return program_node

    def parse_statement(self):
        if self.match(TokenType.VAR):
            return self.parse_variable_declaration_statement()
        if self.match(TokenType.FUNCTION):
            return self.parse_function_declaration_statement()
        if self.match(TokenType.IF):
            return self.parse_if_statement()
        if self.match(TokenType.FOR):
            return self.parse_for_statement()
        if self.match(TokenType.RETURN):
            return self.parse_return_statement()
        if self.match(TokenType.BREAK):
            return self.parse_break_statement()
        return self.parse_expression_statement()
```

The next methods work similarly and are returned if they match with the statement in the input code:

```python
    def parse_variable_declaration_statement(self):
        variable_declaration_node = ASTNode("VariableDeclaration")
        self.consume(TokenType.VAR)
        identifier_token = self.consume(TokenType.ID)
        identifier_node = ASTNode(identifier_token[1])
        variable_declaration_node.add_child(identifier_node)
        if self.match(TokenType.ASSIGN_EQUAL):
            self.consume(TokenType.ASSIGN_EQUAL)
            expression = self.parse_expression()
            variable_declaration_node.add_child(expression)
        self.consume(TokenType.SEMICOLON)
        return variable_declaration_node

    def parse_function_declaration_statement(self):
        function_declaration_node = ASTNode("FunctionDeclaration")
        self.consume(TokenType.FUNCTION)
        identifier_token = self.consume(TokenType.ID)
        identifier_node = ASTNode(identifier_token[1])
        function_declaration_node.add_child(identifier_node)
        self.consume(TokenType.LPAREN)
        parameters = self.parse_function_parameters()
        function_declaration_node.children.extend(parameters)
        self.consume(TokenType.RPAREN)
        function_body = self.parse_block()
        function_declaration_node.add_child(function_body)
        return function_declaration_node
        
        ...
```

More helper methods:

```python
    def parse_block(self):
        self.consume(TokenType.LBRACE)
        block_node = ASTNode("Block")
        while not self.match(TokenType.RBRACE):
            statement = self.parse_statement()
            block_node.add_child(statement)
        self.consume(TokenType.RBRACE)
        return block_node

    def match(self, *token_types):
        if self.is_end_of_tokens():
            return False
        return self.current_token()[0] in token_types

    def consume(self, *token_types):
        if self.is_end_of_tokens():
            raise Exception("Unexpected end of input")
        token = self.current_token()
        if token[0] not in token_types:
            raise Exception(f"Unexpected token: {token[0]}, expected: {token_types}")
        self.current_token_index += 1
        return token

    def current_token(self):
        return self.tokens[self.current_token_index]

    def is_end_of_tokens(self):
        return self.current_token_index >= len(self.tokens)
```
`parse_block()` is responsible for parsing a block of code enclosed in curly braces ({}). 
It begins by consuming the opening brace token ({) using the consume() method. Then, it creates an 
ASTNode object with the label "Block" to represent the block of code. It enters a loop that continues 
until it encounters the closing brace token (}). Within the loop, it calls the `parse_statement()` method 
to parse each statement in the block and adds the resulting statement node as a child of the block node. 
After parsing all the statements, it consumes the closing brace token using `consume()` and returns the block node.

`match()` checks if the current token matches any of the specified token types.

`consume()` consumes the current token and moves the `current_token_index` forward by one. It takes multiple token types as arguments and checks 
if the current token's type is in the specified types. If it matches, it returns the consumed token. 
Otherwise, it raises an exception with an appropriate error message.

`current_token()` returns the current token based on the `current_token_index`. It retrieves the token from the tokens list at the specified index.

`is_end_of_tokens()` checks if the parser has reached the end of the token list by comparing the `current_token_index` with the length of the tokens list. 
It returns True if the index is greater than or equal to the length, indicating that there are no more tokens to parse.

## Conclusion
In this laboratory work I developed practical skills in working with ASTs and parsers which insluded
designing a parser which should be able to recognize the structure of the code and construct an AST,
building AST nodes and establishing relationships between nodes, 
visualizing the AST to analyze or transform the code, implementing error handling and reporting for syntax errors.


## Results

The input:
```commandline
        function gcd(a, b) {
            if (b = 0) {
                return a;
            }
            else {
                return gcd(b, a % b);
            }
        }
```

The output:
```commandline
└── Program
    └── FunctionDeclaration
        ├── gcd
        ├── a
        ├── b
        └── Block
            └── IfElseStatement
                ├── AssignmentExpression
                    ├── b
                    └── 0
                ├── Block
                    └── ReturnStatement
                        └── a
                └── Block
                    └── ReturnStatement
                        └── FunctionCall
                            ├── gcd
                            ├── b
                            └── %
                                ├── a
                                └── b
```
