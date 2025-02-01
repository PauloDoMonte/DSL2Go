from parser.api_parser import parse_api
from parser.route_parser import parse_route
from parser.model_parser import parse_model
from parser.repository_parser import parse_repository
from parser.controller_parser import parse_controller
from parser.service_parser import parse_service
from parser.middleware_parser import parse_middleware
from parser.docker_parser import (
    parse_docker_db_type,
    parse_docker_db_name,
    parse_docker_db_host,
    parse_docker_cache_type,
    parse_docker_cache_name,
    parse_docker_cache_host
)

class DSLParser:
    def __init__(self):
        self.commands = []

    def parse(self, dsl_input):
        lines = dsl_input.strip().split('\n')
        model_definition = False
        model_lines = []
        multi_line_command = False
        multi_line_buffer = []
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith('#'):
                continue
            if model_definition:
                model_lines.append(stripped_line)
                if stripped_line.endswith('}'):
                    self.commands.append(parse_model(' '.join(model_lines)))
                    model_definition = False
                    model_lines = []
            elif stripped_line.startswith('MODEL'):
                model_definition = True
                model_lines.append(stripped_line)
            elif stripped_line.startswith(('REPOSITORY', 'CONTROLLER', 'SERVICE', 'MIDDLEWARE')):
                multi_line_command = True
                multi_line_buffer.append(stripped_line)
            elif multi_line_command:
                multi_line_buffer.append(stripped_line)
                if stripped_line.endswith('}'):
                    self.commands.append(self._parse_line('\n'.join(multi_line_buffer)))
                    multi_line_command = False
                    multi_line_buffer = []
            else:
                self.commands.append(self._parse_line(stripped_line))
        
        print("Parsed commands:", self.commands)

    def _parse_line(self, line):
        if line.startswith('API'):
            return parse_api(line)
        elif line.startswith('ROUTE'):
            return parse_route(line)
        elif line.startswith('REPOSITORY'):
            return parse_repository(line)
        elif line.startswith('CONTROLLER'):
            return parse_controller(line)
        elif line.startswith('SERVICE'):
            return parse_service(line)
        elif line.startswith('MIDDLEWARE'):
            return parse_middleware(line)
        elif line.startswith('DOCKER_DB_TYPE'):
            return parse_docker_db_type(line)
        elif line.startswith('DOCKER_DB_NAME'):
            return parse_docker_db_name(line)
        elif line.startswith('DOCKER_DB_HOST'):
            return parse_docker_db_host(line)
        elif line.startswith('DOCKER_CACHE_TYPE'):
            return parse_docker_cache_type(line)
        elif line.startswith('DOCKER_CACHE_NAME'):
            return parse_docker_cache_name(line)
        elif line.startswith('DOCKER_CACHE_HOST'):
            return parse_docker_cache_host(line)
        else:
            raise ValueError(f"Unknown command: {line}")