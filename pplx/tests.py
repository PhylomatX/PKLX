from pplx.parser import parse_statement, load
from pplx.settings import FOLDER_PATH

if __name__ == '__main__':
    relations, statements = load(FOLDER_PATH)
    for statement in statements:
        anchor, graph = statement.to_graph()
        print(statement)
