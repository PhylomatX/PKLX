from pplx.parser import load, extract_from_statements
from pplx.settings import FOLDER_PATH

if __name__ == '__main__':
    relations, statements = load(FOLDER_PATH)
    extracted_statements = extract_from_statements(statements, 'B')
    for statement in extracted_statements:
        print(statement)
