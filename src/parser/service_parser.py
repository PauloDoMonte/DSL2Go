def parse_service(line):
    parts = line.split('{')
    service_name = parts[0].split()[1]
    methods = parts[1].replace('}', '').strip().split('\n')
    methods = [method.strip() for method in methods if method.strip()]
    return {'type': 'service', 'name': service_name, 'methods': methods}