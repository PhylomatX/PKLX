from pklx.parser import load, extract_from_statements
from pklx.settings import SETTINGS

if __name__ == '__main__':
    relations, statements = load(SETTINGS['FOLDER_PATH'])
    extracted_statements = extract_from_statements(statements, 'B')
    for statement in extracted_statements:
        print(statement)
