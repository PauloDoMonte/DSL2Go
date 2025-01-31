class DSLParser:
    def __init__(self):
        self.commands = []

    def parse(self, dsl_input):
        lines = dsl_input.strip().split('\n')
        model_definition = False
        model_lines = []
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
            else:
                self._parse_line(stripped_line)

    def _parse_line(self, line):
        if line.startswith('API'):
            self.commands.append(self._parse_api(line))
        elif line.startswith('ROUTE'):
            self.commands.append(self._parse_route(line))
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
        # Example: API "Gestão de Usuários"
        parts = line.split('"')
        return {'type': 'api', 'name': parts[1]}

    def _parse_route(self, line):
        # Example: ROUTE GET /users
        parts = line.split()
        return {'type': 'route', 'method': parts[1], 'path': parts[2]}

    def _parse_model(self, line):
        # Example: MODEL User { ID int Name string Email string }
        parts = line.split('{')
        model_name = parts[0].split()[1]
        fields = parts[1].replace('}', '').strip().split()
        fields = [{'name': fields[i], 'type': fields[i+1]} for i in range(0, len(fields), 2)]
        self.commands.append({'type': 'model', 'name': model_name, 'fields': fields})

    def _parse_docker_db_type(self, line):
        # Example: DOCKER_DB_TYPE "PostgreSQL"
        parts = line.split('"')
        return {'type': 'docker_db_type', 'value': parts[1]}

    def _parse_docker_db_name(self, line):
        # Example: DOCKER_DB_NAME "mydb"
        parts = line.split('"')
        return {'type': 'docker_db_name', 'value': parts[1]}

    def _parse_docker_db_host(self, line):
        # Example: DOCKER_DB_HOST "localhost"
        parts = line.split('"')
        return {'type': 'docker_db_host', 'value': parts[1]}

    def _parse_docker_cache_type(self, line):
        # Example: DOCKER_CACHE_TYPE "Redis"
        parts = line.split('"')
        return {'type': 'docker_cache_type', 'value': parts[1]}

    def _parse_docker_cache_name(self, line):
        # Example: DOCKER_CACHE_NAME "mycache"
        parts = line.split('"')
        return {'type': 'docker_cache_name', 'value': parts[1]}

    def _parse_docker_cache_host(self, line):
        # Example: DOCKER_CACHE_HOST "localhost"
        parts = line.split('"')
        return {'type': 'docker_cache_host', 'value': parts[1]}