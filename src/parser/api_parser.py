def parse_api(line):
    parts = line.split('"')
    return {'type': 'api', 'name': parts[1]}