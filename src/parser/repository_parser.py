def parse_repository(line):
    parts = line.split('{')
    repo_name = parts[0].split()[1]
    methods = parts[1].replace('}', '').strip().split('\n')
    methods = [method.strip() for method in methods if method.strip()]
    return {'type': 'repository', 'name': repo_name, 'methods': methods}