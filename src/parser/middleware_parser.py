def parse_middleware(line):
    parts = line.split('{')
    middleware_name = parts[0].split()[1]
    methods = parts[1].replace('}', '').strip().split('\n')
    methods = [method.strip() for method in methods if method.strip()]
    return {'type': 'middleware', 'name': middleware_name, 'methods': methods}