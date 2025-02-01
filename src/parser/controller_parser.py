def parse_controller(line):
    parts = line.split('{')
    controller_name = parts[0].split()[1]
    methods = parts[1].replace('}', '').strip().split('\n')
    methods = [method.strip() for method in methods if method.strip()]
    return {'type': 'controller', 'name': controller_name, 'methods': methods}