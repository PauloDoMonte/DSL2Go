"""
Módulo responsável por transpilar o DSL parseado para a estrutura de um projeto Go.
"""

import os
from transpiler.file_operations import copy_template_structure, get_template_content
from transpiler.model_operations import create_model_files
from transpiler.route_operations import get_routes_content
from transpiler.repository_operations import create_repository_files
from transpiler.controller_operations import create_controller_files
from transpiler.service_operations import create_service_files
from transpiler.middleware_operations import create_middleware_files

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
        copy_template_structure(output_dir)
        self.create_main_file(output_dir)
        self.create_router_file(output_dir)
        self.create_model_files(output_dir)
        self.create_repository_files(output_dir)
        self.create_controller_files(output_dir)
        self.create_service_files(output_dir)
        self.create_middleware_files(output_dir)
        self.create_docker_file(output_dir)

    def create_main_file(self, output_dir):
        """
        Cria o arquivo main.go no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        main_content = get_template_content('main.go')
        with open(os.path.join(output_dir, 'main.go'), 'w', encoding='utf-8') as f:
            f.write(main_content)

    def create_router_file(self, output_dir):
        """
        Cria o arquivo router.go no diretório de saída dentro da pasta routes.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        routes_content = get_routes_content(self.parsed_dsl)
        routes_dir = os.path.join(output_dir, 'routes')
        os.makedirs(routes_dir, exist_ok=True)
        with open(os.path.join(routes_dir, 'router.go'), 'w', encoding='utf-8') as f:
            f.write(routes_content)

    def create_model_files(self, output_dir):
        """
        Cria arquivos de modelo no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        create_model_files(self.parsed_dsl, output_dir)

    def create_repository_files(self, output_dir):
        """
        Cria arquivos de repositório no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        create_repository_files(self.parsed_dsl, output_dir)

    def create_controller_files(self, output_dir):
        """
        Cria arquivos de controlador no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        create_controller_files(self.parsed_dsl, output_dir)

    def create_service_files(self, output_dir):
        """
        Cria arquivos de serviço no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        create_service_files(self.parsed_dsl, output_dir)

    def create_middleware_files(self, output_dir):
        """
        Cria arquivos de middleware no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        create_middleware_files(self.parsed_dsl, output_dir)

    def create_docker_file(self, output_dir):
        """
        Cria o arquivo Dockerfile no diretório de saída.
        
        :param output_dir: O diretório onde a estrutura do projeto será gerada.
        """
        docker_content = get_template_content('Dockerfile')
        with open(os.path.join(output_dir, 'Dockerfile'), 'w', encoding='utf-8') as f:
            f.write(docker_content)