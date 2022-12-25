import os
import re
from typing import List, Tuple
from .objects import PPLX
import networkx as nx


def load(folder_path: str) -> Tuple[List[str], List[str]]:
    files = os.listdir(folder_path)
    for file in files:
        if file == '.ontology':
            with open(os.path.join(folder_path, file), 'r') as f:
                relations = f.readlines()
        else:
            with open(os.path.join(folder_path, file), 'r') as f:
                statements = f.readlines()
    return relations, statements


def parse_relations(relations: List[str]) -> List[str]:
    return [relation.split('-/')[0].strip() for relation in relations]


def lexer(relations: List[str], statement: str) -> List[str]:
    split_tokens = [token for token in re.split(r'(\W)', statement) if token.strip()]
    
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

    return tokens


def parse_statements(relations: List[str], statements: List[str]) -> List[PPLX]:
    parsed_statements = []
    for statement in statements:
        parsed_statements.append(parse_statement(relations, statement))
    return parsed_statements


def parse_statement(relations: List[str], statement: str) -> PPLX:
    tokens = lexer(relations, statement)
    parsed_statement = PPLX().parse(tokens)
    return parsed_statement


def pplx_to_graph(pplx: List[PPLX]) -> nx.DiGraph:
    pass
