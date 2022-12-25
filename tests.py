from pplx.parser import parse_statement


if __name__ == '__main__':
    statements = [
        'Abraham = ( GLÜCKLICHER Hans im Glück ) WEISS ( ( grüner Apfel UND Birne) IST EIN leckeres Obst )',
    ]
    relations = [
        'WEISS',
        'IST EIN',
        'UND',
        'GLÜCKLICHER'
    ]
    for statement in statements:
        parsed_statement = parse_statement(relations, statement)
        print(parsed_statement)
