import argparse
from .visx.backend import main as main_view
from pklx.parser import load, extract_from_statements
from .settings import SETTINGS
from .settings import set_settings as internal_set_settings


def view():
    main_view()


def collect(variable, file):
    relations, statements = load(SETTINGS['FOLDER_PATH'])
    extracted_statements = extract_from_statements(statements, variable)
    if file is not None:
        statement_text = '\n'.join(map(str, extracted_statements))
        with open(file, 'w') as f:
            f.write(statement_text)
    else:
        for statement in extracted_statements:
            print(statement)


def set_settings(key, value):
    internal_set_settings(key, value)


def cmd_view():
    main_view()


def cmd_collect():
    parser = argparse.ArgumentParser(description='Collect knowledge about a specific variable')
    parser.add_argument('variable', type=str, help='The variable to collect knowledge about')
    parser.add_argument('--file', type=str, help='Save the output into a file')
    args = parser.parse_args()
    collect(args.variable, args.file)


def cmd_set_settings():
    parser = argparse.ArgumentParser(description='Set settings')
    parser.add_argument('key', type=str, help='The key of the setting')
    parser.add_argument('value', type=str, help='The value of the setting')
    args = parser.parse_args()
    internal_set_settings(args.key, args.value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a network.')
    parser.add_argument('--view', action='store_true', help='View the network')
    parser.add_argument('--collect', type=str, help='Collect knowledge about a specific variable')
    parser.add_argument('--file', type=str, help='Save the output into a file')
    parser.add_argument('--settings', nargs='+', type=str, help='Specify settings by passing a list of key-value pairs. Example: --settings FOLDER_PATH /home/user/ DELIMITER /')

    args = parser.parse_args()

    if args.collect is not None:
        relations, statements = load(SETTINGS['FOLDER_PATH'])
        extracted_statements = extract_from_statements(statements, args.collect)
        if args.file is not None:
            statement_text = '\n'.join(map(str, extracted_statements))
            with open(args.file, 'w') as f:
                f.write(statement_text)
        else:
            for statement in extracted_statements:
                print(statement)
    if args.view:
        main_view()
    if args.settings is not None:
        for i in range(0, len(args.settings), 2):
            key = args.settings[i]
            value = args.settings[i + 1]
            set_settings(key, value)
