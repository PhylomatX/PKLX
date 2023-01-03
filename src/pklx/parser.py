import os
import re
from typing import List, Tuple
from .objects import PKLX, Statement
import networkx as nx
from .settings import SETTINGS


def load(folder_path: str) -> Tuple[List[str], List[str]]:
    statements = []
    relations = []
    file_names = [os.path.join(folder, file) for folder, _, files in os.walk(folder_path) for file in files]
    for file_name in file_names:
        if os.path.split(file_name)[-1] == '.ontology':
            with open(os.path.join(folder_path, file_name), 'r') as file:
                relations = file.readlines()
            relations = parse_relations(relations)
        else:
            with open(os.path.join(folder_path, file_name), 'r') as file:
                lines = file.readlines()
            for line in lines:
                # separate statements from text by using the delimiter
                splitted_line = line.split(SETTINGS['DELIMITER'])
                if len(splitted_line) % 2 == 0:
                    raise Exception(f'Invalid syntax in file: {file_name}, line: {line}')
                else:
                    statements.extend(splitted_line[1::2])
    statements = parse_statements(relations, statements)
    return relations, statements


def parse_relations(relations: List[str]) -> List[str]:
    return [relation.split(SETTINGS['DELIMITER'])[0].strip().replace('\n', '') for relation in relations]


def lexer(relations: List[str], statement: str) -> List[str]:
    split_tokens = [token for token in re.split(r'(\W)', statement) if token.strip()]
    relations = relations.copy()
    # longer relations should be matched first
    relations.sort(key=len, reverse=True)
    # merge as many consecutive tokens into a relation as possible
    relation_merged_tokens = []
    i = 0
    while i < len(split_tokens):
        found = False
        for phrase in relations:
            if " ".join(split_tokens[i:i+len(phrase.split())]) == phrase:
                relation_merged_tokens.append(phrase)
                i += len(phrase.split())
                found = True
                break
        if not found:
            relation_merged_tokens.append(split_tokens[i])
            i += 1

    # merge consecutive alphanumeric tokens that are not relations into one token
    tokens = []
    current_string = ""
    for s in relation_merged_tokens:
        if s.isalnum() and s not in relations:
            current_string += " " + s
        else:
            if current_string:
                tokens.append(current_string.strip())
                current_string = ""
            tokens.append(s)
    if current_string:
        tokens.append(current_string.strip())

    # remove optional markdown syntax
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == '[' and tokens[i+1] == '[':
            del tokens[i:i+2]
            continue
        if tokens[i] == ']' and tokens[i+1] == ']':
            del tokens[i:i+2]
            continue
        i += 1

    return tokens


def parse_statements(relations: List[str], statements: List[str]) -> List[PKLX]:
    parsed_statements = []
    for statement in statements:
        parsed_statements.append(parse_statement(relations, statement))
    return parsed_statements


def parse_statement(relations: List[str], statement: str) -> PKLX:
    tokens = lexer(relations, statement)
    parsed_statement = PKLX().parse(tokens, relations)
    return parsed_statement


def statements_to_graph(statements: List[PKLX]) -> nx.DiGraph:
    graph = nx.compose_all([statement.to_graph()[1] for statement in statements])
    for node in list(graph.nodes):
        try:
            variable = graph.nodes[node]['variable']
            nx.contracted_nodes(graph, node, variable, copy=False)
        except KeyError:
            pass
    return graph


def extract_from_statements(statements: List[PKLX], variable: str, done: List[str] = None) -> List[PKLX]:
    extracted_statements = []
    statement_variables = []
    if done is None:
        done = []
    if variable in done:
        return []
    for statement in statements:
        if statement.contains(variable):
            extracted_statements.append(statement)
            if type(statement) == Statement:
                statement_variables.extend(statement.variable.name)
    done.append(variable)
    for statement_variable in statement_variables:
        if statement_variable not in done:
            extracted_statements.extend(extract_from_statements(statements, statement_variable, done))
    extracted_statements = list(set(extracted_statements))
    return extracted_statements
