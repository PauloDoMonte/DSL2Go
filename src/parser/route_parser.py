def parse_route(line):
    parts = line.split()
    return {'type': 'route', 'method': parts[1], 'path': parts[2]}