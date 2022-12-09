import os
from typing import List, Tuple


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
    return [relation.split()[0] for relation in relations]


def lexer(statements: List[str]) -> List[str]:
    raise NotImplementedError


def parse_statements(statements: List[str]) -> List[str]:
    raise NotImplementedError
