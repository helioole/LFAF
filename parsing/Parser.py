from parsing.AST import ASTNode
from parsing.type import TokenType


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

    def parse_function_parameters(self):
        parameters = []
        while self.match(TokenType.ID):
            identifier_token = self.consume(TokenType.ID)
            identifier_node = ASTNode(identifier_token[1])
            parameters.append(identifier_node)
            if not self.match(TokenType.RPAREN):
                self.consume(TokenType.COMMA)
        return parameters

    def parse_if_statement(self):
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.parse_expression()
        self.consume(TokenType.RPAREN)
        if_block = self.parse_block()
        if self.match(TokenType.ELSE):
            self.consume(TokenType.ELSE)
            else_block = self.parse_block()
            if_else_node = ASTNode("IfElseStatement")
            if_else_node.add_child(condition)
            if_else_node.add_child(if_block)
            if_else_node.add_child(else_block)
            return if_else_node
        else:
            if_node = ASTNode("IfStatement")
            if_node.add_child(condition)
            if_node.add_child(if_block)
            return if_node

    def parse_for_statement(self):
        self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        initialization = self.parse_expression_statement()
        self.consume(TokenType.SEMICOLON)
        condition = self.parse_expression()
        self.consume(TokenType.SEMICOLON)
        increment = self.parse_expression()
        self.consume(TokenType.RPAREN)
        body = self.parse_block()
        for_node = ASTNode("ForStatement")
        for_node.add_child(initialization)
        for_node.add_child(condition)
        for_node.add_child(increment)
        for_node.add_child(body)
        return for_node

    def parse_return_statement(self):
        return_node = ASTNode("ReturnStatement")
        self.consume(TokenType.RETURN)
        if not self.match(TokenType.SEMICOLON):
            expression = self.parse_expression()
            return_node.add_child(expression)
        self.consume(TokenType.SEMICOLON)
        return return_node

    def parse_break_statement(self):
        self.consume(TokenType.BREAK)
        self.consume(TokenType.SEMICOLON)
        return ASTNode("BreakStatement")

    def parse_expression_statement(self):
        if self.match(TokenType.VAR):
            return self.parse_variable_declaration()
        return self.parse_expression()

    def parse_variable_declaration(self):
        self.consume(TokenType.VAR)
        identifier = self.consume(TokenType.ID)[1]
        self.consume(TokenType.ASSIGN_EQUAL)
        initializer = self.parse_expression()
        self.consume(TokenType.SEMICOLON)

        variableDeclarationNode = ASTNode("VariableDeclaration")
        variableDeclarationNode.add_child(ASTNode(identifier))
        variableDeclarationNode.add_child(initializer)

        return variableDeclarationNode

    def parse_expression(self):
        return self.parse_assignment_expression()

    def parse_assignment_expression(self):
        left = self.parse_equality_expression()
        if self.match(TokenType.ASSIGN_EQUAL):
            self.consume(TokenType.ASSIGN_EQUAL)
            right = self.parse_assignment_expression()
            assignment_node = ASTNode("AssignmentExpression")
            assignment_node.add_child(left)
            assignment_node.add_child(right)
            return assignment_node
        return left

    def parse_equality_expression(self):
        left = self.parse_relational_expression()
        while self.match(TokenType.NOT_EQUAL):
            operator_token = self.consume(TokenType.NOT_EQUAL)
            right = self.parse_relational_expression()
            equality_node = ASTNode(operator_token[1])
            equality_node.add_child(left)
            equality_node.add_child(right)
            left = equality_node
        return left

    def parse_relational_expression(self):
        left = self.parse_additive_expression()
        while self.match(TokenType.GREATER) or self.match(TokenType.LESS):
            operator_token = self.consume(TokenType.GREATER, TokenType.LESS)
            right = self.parse_additive_expression()
            relational_node = ASTNode(operator_token[1])
            relational_node.add_child(left)
            relational_node.add_child(right)
            left = relational_node
        return left

    def parse_additive_expression(self):
        left = self.parse_multiplicative_expression()
        while self.match(TokenType.PLUS) or self.match(TokenType.MINUS):
            operator_token = self.consume(TokenType.PLUS, TokenType.MINUS)
            right = self.parse_multiplicative_expression()
            additive_node = ASTNode(operator_token[1])
            additive_node.add_child(left)
            additive_node.add_child(right)
            left = additive_node
        return left

    def parse_multiplicative_expression(self):
        left = self.parse_primary_expression()
        while (self.match(TokenType.MULTIPLY) or self.match(TokenType.DIVIDE) or self.match(TokenType.MODULUS)):
            operator_token = self.consume(
                TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULUS
            )
            right = self.parse_primary_expression()
            multiplicative_node = ASTNode(operator_token[1])
            multiplicative_node.add_child(left)
            multiplicative_node.add_child(right)
            left = multiplicative_node
        return left

    def parse_primary_expression(self):
        if self.match(TokenType.NUMBER) or self.match(TokenType.STRING):
            token = self.consume(TokenType.NUMBER, TokenType.STRING)
            return ASTNode(token[1])
        if self.match(TokenType.ID):
            identifier_token = self.consume(TokenType.ID)
            identifier_node = ASTNode(identifier_token[1])
            if self.match(TokenType.LPAREN):
                self.consume(TokenType.LPAREN)
                arguments = self.parse_function_arguments()
                self.consume(TokenType.RPAREN)
                function_call_node = ASTNode("FunctionCall")
                function_call_node.add_child(identifier_node)
                function_call_node.children.extend(arguments)
                return function_call_node
            return identifier_node
        if self.match(TokenType.LPAREN):
            self.consume(TokenType.LPAREN)
            expression = self.parse_expression()
            self.consume(TokenType.RPAREN)
            return expression
        raise Exception("Invalid expression")

    def parse_function_arguments(self):
        arguments = []
        while not self.match(TokenType.RPAREN):
            argument = self.parse_expression()
            arguments.append(argument)
            if not self.match(TokenType.RPAREN):
                self.consume(TokenType.COMMA)
        return arguments

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
