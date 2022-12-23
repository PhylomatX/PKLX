from pplx.parser import parse_statement


if __name__ == '__main__':
    statements = [
        'Abraham = Hans im Glück HAT GERN ( ( grünen Apfel MAG Birne) IST EIN leckeres Obst )',
    ]
    relations = [
        'HAT GERN',
        'IST EIN',
        'MAG',
    ]
    for statement in statements:
        import ipdb
        ipdb.set_trace()
        parsed_statement = parse_statement(relations, statement)
        print(parsed_statement)
