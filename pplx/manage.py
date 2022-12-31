import argparse
from visx.backend import main as view
from pplx.parser import load, extract_from_statements
from settings import FOLDER_PATH

parser = argparse.ArgumentParser(description='Train a network.')
parser.add_argument('--view', action='store_true', help='View the network')
parser.add_argument('--collect', type=str, help='Collect knowledge about a specific variable')
parser.add_argument('--file', type=str, help='Save the output into a file')

args = parser.parse_args()

if args.collect is not None:
    relations, statements = load(FOLDER_PATH)
    extracted_statements = extract_from_statements(statements, args.collect)
    if args.file is not None:
        statement_text = '\n'.join(map(str, extracted_statements))
        with open(args.file, 'w') as f:
            f.write(statement_text)
    else:
        for statement in extracted_statements:
            print(statement)
if args.view:
    view()