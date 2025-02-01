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
                    self._parse_model(' '.join(model_lines))
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
                    self._parse_line('\n'.join(multi_line_buffer))
                    multi_line_command = False
                    multi_line_buffer = []
            else:
                self._parse_line(stripped_line)
        
        print("Parsed commands:", self.commands)
    def _parse_line(self, line):
        if line.startswith('API'):
            self.commands.append(self._parse_api(line))
        elif line.startswith('ROUTE'):
            self.commands.append(self._parse_route(line))
        elif line.startswith('REPOSITORY'):
            self.commands.append(self._parse_repository(line))
        elif line.startswith('CONTROLLER'):
            self.commands.append(self._parse_controller(line))
        elif line.startswith('SERVICE'):
            self.commands.append(self._parse_service(line))
        elif line.startswith('MIDDLEWARE'):
            self.commands.append(self._parse_middleware(line))
        elif line.startswith('DOCKER_DB_TYPE'):
            self.commands.append(self._parse_docker_db_type(line))
        elif line.startswith('DOCKER_DB_NAME'):
            self.commands.append(self._parse_docker_db_name(line))
        elif line.startswith('DOCKER_DB_HOST'):
            self.commands.append(self._parse_docker_db_host(line))
        elif line.startswith('DOCKER_CACHE_TYPE'):
            self.commands.append(self._parse_docker_cache_type(line))
        elif line.startswith('DOCKER_CACHE_NAME'):
            self.commands.append(self._parse_docker_cache_name(line))
        elif line.startswith('DOCKER_CACHE_HOST'):
            self.commands.append(self._parse_docker_cache_host(line))
        else:
            raise ValueError(f"Unknown command: {line}")

    def _parse_api(self, line):
        parts = line.split('"')
        return {'type': 'api', 'name': parts[1]}

    def _parse_route(self, line):
        parts = line.split()
        return {'type': 'route', 'method': parts[1], 'path': parts[2]}

    def _parse_model(self, line):
        parts = line.split('{')
        model_name = parts[0].split()[1]
        fields = parts[1].replace('}', '').strip().split()
        fields = [{'name': fields[i], 'type': fields[i+1]} for i in range(0, len(fields), 2)]
        return {'type': 'model', 'name': model_name, 'fields': fields}

    def _parse_repository(self, line):
        parts = line.split('{')
        repo_name = parts[0].split()[1]
        methods = parts[1].replace('}', '').strip().split('\n')
        methods = [method.strip() for method in methods if method.strip()]
        return {'type': 'repository', 'name': repo_name, 'methods': methods}

    def _parse_controller(self, line):
        parts = line.split('{')
        controller_name = parts[0].split()[1]
        methods = parts[1].replace('}', '').strip().split('\n')
        methods = [method.strip() for method in methods if method.strip()]
        return {'type': 'controller', 'name': controller_name, 'methods': methods}

    def _parse_service(self, line):
        parts = line.split('{')
        service_name = parts[0].split()[1]
        methods = parts[1].replace('}', '').strip().split('\n')
        methods = [method.strip() for method in methods if method.strip()]
        return {'type': 'service', 'name': service_name, 'methods': methods}

    def _parse_middleware(self, line):
        parts = line.split('{')
        middleware_name = parts[0].split()[1]
        methods = parts[1].replace('}', '').strip().split('\n')
        methods = [method.strip() for method in methods if method.strip()]
        return {'type': 'middleware', 'name': middleware_name, 'methods': methods}
    
    def _parse_docker_db_type(self, line):
        parts = line.split('"')
        return {'type': 'docker_db_type', 'value': parts[1]}

    def _parse_docker_db_name(self, line):
        parts = line.split('"')
        return {'type': 'docker_db_name', 'value': parts[1]}

    def _parse_docker_db_host(self, line):
        parts = line.split('"')
        return {'type': 'docker_db_host', 'value': parts[1]}

    def _parse_docker_cache_type(self, line):
        parts = line.split('"')
        return {'type': 'docker_cache_type', 'value': parts[1]}

    def _parse_docker_cache_name(self, line):
        parts = line.split('"')
        return {'type': 'docker_cache_name', 'value': parts[1]}

    def _parse_docker_cache_host(self, line):
        parts = line.split('"')
        return {'type': 'docker_cache_host', 'value': parts[1]}