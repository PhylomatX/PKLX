import networkx as nx
from typing import Tuple
import uuid


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

    def parse(self, tokens) -> PPLX:
        if type(tokens) != list or len(tokens) == 0:
            raise ParsingException(f"Could not parse Statement: {tokens}")
        try:
            assert tokens[1] == '='
            self.name = Name().parse(tokens[0])
            self.knowledge = Knowledge().parse(tokens[2:])
            return self
        except (AssertionError, ParsingException):
            raise ParsingException(f"Could not parse Statement: {tokens}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        anchor, graph = self.knowledge.to_graph()
        graph.nodes[anchor]['variable'] = self.name.name
        return anchor, graph

    def __repr__(self):
        return f"{self.name} = {self.knowledge}"


class Knowledge(PPLX):
    
    def parse(self, tokens) -> PPLX:
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

    def parse(self, tokens) -> PPLX:
        if type(tokens) != list or len(tokens) == 0:
            raise ParsingException(f"Could not parse Binary: {tokens}")
        try:
            if tokens[0] == '(':
                # Find the matching closing parenthesis
                open_parentheses = 0
                for i, token in enumerate(tokens):
                    if token == '(':
                        open_parentheses += 1
                    if token == ')':
                        open_parentheses -= 1
                        if open_parentheses == 0:
                            break
                self.left_expression = NestedExpression().parse(tokens[0:i+1])
                self.binary_operator = Binop().parse(tokens[i+1])
                self.right_expression = Expression().parse(tokens[i+2:])
            else:
                self.left_expression = Expression().parse([tokens[0]])
                self.binary_operator = Binop().parse(tokens[1])
                self.right_expression = Expression().parse(tokens[2:])
            return self
        except ParsingException:
            raise ParsingException(f"Could not parse Binary: {tokens}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        left_expression_anchor, left_expression_graph = self.left_expression.to_graph()
        right_expression_anchor, right_expression_graph = self.right_expression.to_graph()
        binary_operator_anchor, binary_operator_graph = self.binary_operator.to_graph()
        graph = nx.union_all([left_expression_graph, right_expression_graph, binary_operator_graph])
        graph.add_edge(left_expression_anchor, binary_operator_anchor)
        graph.add_edge(binary_operator_anchor, right_expression_anchor)
        return binary_operator_anchor, graph

    def __repr__(self):
        return f"{self.left_expression} {self.binary_operator} {self.right_expression}"


class Unary(Knowledge):
        
    def __init__(self, unary_operator=None, right_expression=None):
        self.unary_operator = unary_operator
        self.right_expression = right_expression

    def parse(self, tokens) -> PPLX:
        if type(tokens) != list or len(tokens) == 0:
            raise ParsingException(f"Could not parse Unary: {tokens}")
        try:
            self.unary_operator = Unop().parse(tokens[0])
            self.right_expression = Expression().parse(tokens[1:])
            return self
        except ParsingException:
            raise ParsingException(f"Could not parse Unary: {tokens}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        right_expression_anchor, right_expression_graph = self.right_expression.to_graph()
        unary_operator_anchor, unary_operator_graph = self.unary_operator.to_graph()
        graph = nx.union(right_expression_graph, unary_operator_graph)
        graph.add_edge(unary_operator_anchor, right_expression_anchor)
        return unary_operator_anchor, graph

    def __repr__(self):
        return f"{self.unary_operator} {self.right_expression}"


class Expression():
    
    def parse(self, tokens) -> PPLX:
        if type(tokens) != list or len(tokens) == 0:
            raise ParsingException(f"Could not parse Expression: {tokens}")
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

    def parse(self, tokens) -> PPLX:
        if type(tokens) != list or len(tokens) == 0:
            raise ParsingException(f"Could not parse NestedExpression: {tokens}")
        try:
            assert tokens[0] == '(' and tokens[-1] == ')'
            self.knowledge = Knowledge().parse(tokens[1:-1])
            return self
        except (AssertionError, ParsingException):
            raise ParsingException(f"Could not parse NestedExpression: {tokens}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        return self.knowledge.to_graph()

    def __repr__(self):
        return f"( {self.knowledge} )"


class Name(Expression):
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token) -> PPLX:
        if type(token) == str and token[0].isalpha():
            self.name = token
            return self
        else:
            raise ParsingException(f"Could not parse Name: {token}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        graph = nx.DiGraph()
        node = str(uuid.uuid4()) + ' ' + self.name
        graph.add_node(node, node_type='variable')
        return node, graph
    
    def __repr__(self):
        return f"{self.name}"


class Binop():
    
    def __init__(self, name=None):
        self.name = name

    def parse(self, token) -> PPLX:
        if type(token) == str and token[0].isalpha():
            self.name = token
            return self
        else:
            raise ParsingException(f"Could not parse Binop: {token}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        graph = nx.DiGraph()
        node = str(uuid.uuid4()) + ' ' + self.name
        graph.add_node(node, node_type='binary')
        return node, graph

    def __repr__(self):
        return f"{self.name}"


class Unop():
        
    def __init__(self, name=None):
        self.name = name

    def parse(self, token) -> PPLX:
        if type(token) == str and token[0].isalpha():
            self.name = token
            return self
        else:
            raise ParsingException(f"Could not parse Unop: {token}")

    def to_graph(self) -> Tuple[str, nx.DiGraph]:
        graph = nx.DiGraph()
        node = str(uuid.uuid4()) + ' ' + self.name
        graph.add_node(node, node_type='unary')
        return node, graph

    def __repr__(self):
        return f"{self.name}"
