"""
Módulo responsável por transpilar o DSL parseado para a estrutura de um projeto Go.
"""

import os
import shutil

class Transpiler:
    """
    Classe responsável por transpilar o DSL parseado para a estrutura de um projeto Go.
    """

    def __init__(self, parsed_dsl):
        """
        Inicializa o Transpiler com o DSL parseado.
        
        :param parsed_dsl: O DSL que foi parseado.
        """
        self.parsed_dsl = parsed_dsl

    def generate_project_structure(self, output_dir):
        """
        Gera a estrutura do projeto Go com base no DSL parseado.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        self.copy_template_structure(output_dir)
        self.create_main_file(output_dir)
        self.create_router_file(output_dir)
        self.create_models_file(output_dir)
        self.create_docker_file(output_dir)

    def copy_template_structure(self, output_dir):
        """
        Copia a estrutura de diretórios e arquivos do template para o diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'go_project_structure')
        shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)

    def create_main_file(self, output_dir):
        """
        Cria o arquivo main.go no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        main_content = self.get_template_content('main.go')
        with open(os.path.join(output_dir, 'main.go'), 'w') as f:
            f.write(main_content)

    def create_router_file(self, output_dir):
        """
        Cria o arquivo router.go no diretório de saída dentro da pasta routes.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        routes_content = self.get_routes_content()
        routes_dir = os.path.join(output_dir, 'routes')
        os.makedirs(routes_dir, exist_ok=True)
        with open(os.path.join(routes_dir, 'router.go'), 'w') as f:
            f.write(routes_content)

    def create_models_file(self, output_dir):
        """
        Cria o arquivo models.go no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        models_content = self.get_models_content()
        with open(os.path.join(output_dir, 'models.go'), 'w') as f:
            f.write(models_content)

    def create_docker_file(self, output_dir):
        """
        Cria o arquivo Dockerfile no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        docker_content = self.get_template_content('Dockerfile')
        with open(os.path.join(output_dir, 'Dockerfile'), 'w') as f:
            f.write(docker_content)

    def get_template_content(self, template_name):
        """
        Retorna o conteúdo de um arquivo de template.
        
        :param template_name: O nome do arquivo de template.
        :return: O conteúdo do arquivo de template.
        """
        template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates', 'go_project_structure', template_name)
        with open(template_path, 'r') as file:
            return file.read()

    def get_routes_content(self):
        """
        Retorna o conteúdo do arquivo router.go.
        
        :return: O conteúdo do arquivo router.go.
        """
        routes = [cmd for cmd in self.parsed_dsl if cmd['type'] == 'route']
        routes_code = '\n'.join([f'r.HandleFunc("{route["path"]}", {route["method"]}Handler).Methods("{route["method"]}")' for route in routes])
        template_content = self.get_template_content('routes/router.go')
        return template_content.replace('// As rotas serão adicionadas aqui pelo transpiler', routes_code)

    def get_models_content(self):
        """
        Retorna o conteúdo do arquivo models.go.
        
        :return: O conteúdo do arquivo models.go.
        """
        models = [cmd for cmd in self.parsed_dsl if cmd['type'] == 'model']
        models_code = '\n\n'.join([self._generate_model_code(model) for model in models])
        template_content = self.get_template_content('models/models.go')
        return template_content.replace('// Os modelos serão adicionados aqui pelo transpiler', models_code)

    def _generate_model_code(self, model):
        """
        Gera o código Go para um modelo.
        
        :param model: O modelo a ser gerado.
        :return: O código Go do modelo.
        """
        fields_code = '\n    '.join([f'{field["name"]} {field["type"]}' for field in model['fields']])
        return f'''type {model["name"]} struct {{
    gorm.Model
    {fields_code}
}}
'''