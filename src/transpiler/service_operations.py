import os

def create_service_files(parsed_dsl, output_dir):
    """
    Cria arquivos de serviço no diretório de saída com base no DSL parseado.
    
    :param parsed_dsl: O DSL que foi parseado.
    :param output_dir: O diretório onde os arquivos de serviço serão gerados.
    """
    services = [cmd for cmd in parsed_dsl if cmd['type'] == 'service']
    services_dir = os.path.join(output_dir, 'services')
    os.makedirs(services_dir, exist_ok=True)
    
    for service in services:
        service_content = generate_service_code(service)
        service_filename = os.path.join(services_dir, f'{service["name"].lower()}.go')
        with open(service_filename, 'w', encoding='utf-8') as f:
            f.write(service_content)

def generate_service_code(service):
    """
    Gera o código Go para um serviço.
    
    :param service: O serviço a ser gerado.
    :return: O código Go do serviço.
    """
    methods_code = '\n'.join([generate_service_method_code(method, service["name"]) for method in service['methods']])
    return f'''package services

import (
    "context"
    "your_project/repositories"
    "your_project/models"
)

type {service["name"]} struct {{
    repo repositories.{service["name"]}Repository
}}

{methods_code}
'''

def generate_service_method_code(method, service_name):
    """
    Gera o código Go para um método de serviço.
    
    :param method: O método a ser gerado.
    :param service_name: O nome do serviço.
    :return: O código Go do método.
    """
    parts = method.split()
    action = parts[0]
    model = parts[1]
    if action == 'GetAll':
        return f'''func (s *{service_name}) GetAll{model}() []{model} {{
    return s.repo.FindAll{model}()
}}'''
    elif action == 'GetByID':
        return f'''func (s *{service_name}) GetByID(id int) {model} {{
    return s.repo.FindByID(id)
}}'''
    elif action == 'Create':
        return f'''func (s *{service_name}) Create{model}({model.lower()} {model}) {model} {{
    return s.repo.Save{model}({model.lower()})
}}'''
    elif action == 'Delete':
        return f'''func (s *{service_name}) Delete(id int) {{
    s.repo.Delete(id)
}}'''
    else:
        raise ValueError(f"Unknown action: {action}")