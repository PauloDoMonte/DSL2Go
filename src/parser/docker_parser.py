def parse_docker_db_type(line):
    parts = line.split('"')
    return {'type': 'docker_db_type', 'value': parts[1]}

def parse_docker_db_name(line):
    parts = line.split('"')
    return {'type': 'docker_db_name', 'value': parts[1]}

def parse_docker_db_host(line):
    parts = line.split('"')
    return {'type': 'docker_db_host', 'value': parts[1]}

def parse_docker_cache_type(line):
    parts = line.split('"')
    return {'type': 'docker_cache_type', 'value': parts[1]}

def parse_docker_cache_name(line):
    parts = line.split('"')
    return {'type': 'docker_cache_name', 'value': parts[1]}

def parse_docker_cache_host(line):
    parts = line.split('"')
    return {'type': 'docker_cache_host', 'value': parts[1]}