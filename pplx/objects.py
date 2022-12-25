import networkx as nx


class ParsingException(Exception):
    pass


class PPLX():

    def parse(self, tokens):
        try:
            return Statement().parse(tokens)
        except ParsingException:
            pass
        try:
            return Knowledge().parse(tokens)
        except ParsingException:
            pass
        raise ParsingException(f"Could not parse PPLX: {tokens}")


class Statement(PPLX):
    
    def __init__(self, name=None, knowledge=None):
        self.name = name
        self.knowledge = knowledge

    def parse(self, tokens):
        try:
            assert tokens[1] == '='
            self.name = Name().parse(tokens[0])
            self.knowledge = Knowledge().parse(tokens[2:])
        except (AssertionError, ParsingException):
            raise ParsingException(f"Could not parse Statement: {tokens}")
        return self

    def to_graph(self):
        anchor, graph = self.knowledge.to_graph()
        graph.nodes[anchor]['variable'] = self.name
        return anchor, graph

    def __repr__(self):
        return f"{self.name} = {self.knowledge}"


class Knowledge(PPLX):
    
    def parse(self, tokens):
        try:
            return Binary().parse(tokens)
        except ParsingException:
            pass
        try:
            return Unary().parse(tokens)
        except ParsingException:
            pass
        raise ParsingException(f"Could not parse Knowledge: {tokens}")


class Binary(Knowledge):
    
    def __init__(self, left_expression=None, binary_operator=None, right_expression=None):
        self.left_expression = left_expression
        self.binary_operator = binary_operator
        self.right_expression = right_expression

    def parse(self, tokens):
        try:
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
        except ParsingException:
            raise ParsingException(f"Could not parse Binary: {tokens}")
        return self

    def to_graph(self):
        left_expression_anchor, left_expression_graph = self.left_expression.to_graph()
        right_expression_anchor, right_expression_graph = self.right_expression.to_graph()
        binary_operator_anchor, binary_operator_graph = self.binary_operator.to_graph()
        graph = nx.compose(left_expression_graph, right_expression_graph)
        graph = nx.compose(graph, binary_operator_graph)
        graph.add_edge(left_expression_anchor, binary_operator_anchor)
        graph.add_edge(binary_operator_anchor, right_expression_anchor)
        return binary_operator_anchor, graph

    def __repr__(self):
        return f"{self.left_expression} {self.binary_operator} {self.right_expression}"


class Unary(Knowledge):
        
    def __init__(self, unary_operator=None, right_expression=None):
        self.unary_operator = unary_operator
        self.right_expression = right_expression

    def parse(self, tokens):
        try:
            self.unary_operator = Unop().parse(tokens[0])
            self.right_expression = Expression().parse(tokens[1:])
        except ParsingException:
            raise ParsingException(f"Could not parse Unary: {tokens}")
        return self

    def to_graph(self):
        right_expression_anchor, right_expression_graph = self.right_expression.to_graph()
        unary_operator_anchor, unary_operator_graph = self.unary_operator.to_graph()
        graph = nx.compose(right_expression_graph, unary_operator_graph)
        graph.add_edge(unary_operator_anchor, right_expression_anchor)
        return unary_operator_anchor, graph

    def __repr__(self):
        return f"{self.unary_operator} {self.right_expression}"


class Expression():
    
    def parse(self, tokens):
        try:
            if len(tokens) == 1:
                return Name().parse(tokens[0])
            else:
                return NestedExpression().parse(tokens)
        except ParsingException:
            raise ParsingException(f"Could not parse Expression: {tokens}")


class NestedExpression(Expression):

    def __init__(self, knowledge=None):
        self.knowledge = knowledge

    def parse(self, tokens):
        if tokens[0] == '(' and tokens[-1] == ')':
            self.knowledge = Knowledge().parse(tokens[1:-1])
        else:
            raise ParsingException(f"Could not parse NestedExpression: {tokens}")
        return self

    def to_graph(self):
        return self.knowledge.to_graph()

    def __repr__(self):
        return f"( {self.knowledge} )"


class Name(Expression):
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise ParsingException(f"Could not parse Name: {token}")
        return self

    def to_graph(self):
        graph = nx.DiGraph()
        graph.add_node(self.name, node_type='variable')
        return self.name, graph
    
    def __repr__(self):
        return f"{self.name}"


class Binop():
    
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise ParsingException(f"Could not parse Binop: {token}")
        return self

    def to_graph(self):
        graph = nx.DiGraph()
        graph.add_node(self.name, node_type='binary')
        return self.name, graph

    def __repr__(self):
        return f"{self.name}"


class Unop():
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token):
        if type(token) == str and token[0].isalpha():
            self.name = token
        else:
            raise ParsingException(f"Could not parse Unop: {token}")
        return self

    def to_graph(self):
        graph = nx.DiGraph()
        graph.add_node(self.name, node_type='unary')
        return self.name, graph

    def __repr__(self):
        return f"{self.name}"
