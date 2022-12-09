class Statement():
    
    def __init__(self, name, knowledge):
        self.name = name
        self.knowledge = knowledge

    def __repr__(self):
        return f"{self.name} = {self.knowledge}"


class Knowledge():
    pass


class Binary(Knowledge):
    
    def __init__(self, left_expression, binary_operator, right_expression):
        self.left_expression = left_expression
        self.binary_operator = binary_operator
        self.right_expression = right_expression

    def __repr__(self):
        return f"{self.left_expression} {self.binary_operator} {self.right_expression}"


class Unary(Knowledge):
        
        def __init__(self, unary_operator, right_expression):
            self.unary_operator = unary_operator
            self.right_expression = right_expression
    
        def __repr__(self):
            return f"{self.unary_operator} {self.right_expression}"


class Expression():
    pass


class Name(Expression):
        
        def __init__(self, name):
            self.name = name
        
        def __repr__(self):
            return f"{self.name}"


class Binop():
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Unop():
        
        def __init__(self, name):
            self.name = name
    
        def __repr__(self):
            return f"{self.name}"
