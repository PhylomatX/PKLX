class PPLX():

    def parse(self, tokens):
        try:
            return Statement().parse(tokens)
        except:
            pass
        try:
            return Knowledge().parse(tokens)
        except:
            pass
        raise Exception(f"Could not parse PPLX: {tokens}")


class Statement(PPLX):
    
    def __init__(self, name=None, knowledge=None):
        self.name = name
        self.knowledge = knowledge

    def parse(self, tokens):
        try:
            assert tokens[1] == '='
        except:
            raise Exception(f"Could not parse Statement: {tokens}")
        self.name = Name().parse(tokens[0])
        self.knowledge = Knowledge().parse(tokens[2:])
        return self

    def __repr__(self):
        return f"{self.name} = {self.knowledge}"


class Knowledge(PPLX):
    
    def parse(self, tokens):
        try:
            return Binary().parse(tokens)
        except:
            pass
        try:
            return Unary().parse(tokens)
        except:
            pass
        raise Exception(f"Could not parse Knowledge: {tokens}")


class Binary(Knowledge):
    
    def __init__(self, left_expression=None, binary_operator=None, right_expression=None):
        self.left_expression = left_expression
        self.binary_operator = binary_operator
        self.right_expression = right_expression

    def parse(self, tokens):
        if tokens[0] == '(':
            # Find the matching closing parenthesis
            for i, token in enumerate(tokens):
                if token == ')':
                    break
            self.left_expression = NestedExpression().parse(tokens[0:i+1])
            self.binary_operator = Binop().parse(tokens[i+1])
            self.right_expression = Expression().parse(tokens[i+2:])
        else:
            self.left_expression = Expression().parse([tokens[0]])
            self.binary_operator = Binop().parse(tokens[1])
            self.right_expression = Expression().parse(tokens[2:])
        return self

    def __repr__(self):
        return f"{self.left_expression} {self.binary_operator} {self.right_expression}"


class Unary(Knowledge):
        
    def __init__(self, unary_operator=None, right_expression=None):
        self.unary_operator = unary_operator
        self.right_expression = right_expression

    def parse(self, tokens):
        self.unary_operator = Unop().parse(tokens[0])
        self.right_expression = Expression().parse(tokens[1:])
        return self

    def __repr__(self):
        return f"{self.unary_operator} {self.right_expression}"


class Expression():
    
    def parse(self, tokens):
        if len(tokens) == 1:
            return Name().parse(tokens[0])
        elif tokens[0] == '(' and tokens[-1] == ')':
            return NestedExpression().parse(tokens)
        else:
            raise Exception(f"Could not parse Expression: {tokens}")


class NestedExpression(Expression):

    def __init__(self, knowledge=None):
        self.knowledge = knowledge

    def parse(self, tokens):
        if tokens[0] == '(' and tokens[-1] == ')':
            self.knowledge = Knowledge().parse(tokens[1:-1])
        else:
            raise Exception(f"Could not parse NestedExpression: {tokens}")
        return self

    def __repr__(self):
        return f"( {self.knowledge} )"


class Name(Expression):
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise Exception(f"Could not parse Name: {token}")
        return self
    
    def __repr__(self):
        return f"{self.name}"


class Binop():
    
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise Exception(f"Could not parse Binop: {token}")
        return self

    def __repr__(self):
        return f"{self.name}"


class Unop():
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise Exception(f"Could not parse Unop: {token}")
        return self

    def __repr__(self):
        return f"{self.name}"

