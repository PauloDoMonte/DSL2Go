import os

def create_middleware_files(parsed_dsl, output_dir):
    """
    Cria arquivos de middleware no diretório de saída com base no DSL parseado.
    
    :param parsed_dsl: O DSL que foi parseado.
    :param output_dir: O diretório onde os arquivos de middleware serão gerados.
    """
    middlewares = [cmd for cmd in parsed_dsl if cmd['type'] == 'middleware']
    middlewares_dir = os.path.join(output_dir, 'middlewares')
    os.makedirs(middlewares_dir, exist_ok=True)
    
    for middleware in middlewares:
        middleware_content = generate_middleware_code(middleware)
        middleware_filename = os.path.join(middlewares_dir, f'{middleware["name"].lower()}.go')
        with open(middleware_filename, 'w', encoding='utf-8') as f:
            f.write(middleware_content)

def generate_middleware_code(middleware):
    """
    Gera o código Go para um middleware.
    
    :param middleware: O middleware a ser gerado.
    :return: O código Go do middleware.
    """
    methods_code = '\n    '.join(middleware['methods'])
    return f'''package middlewares

import (
    "net/http"
)

type {middleware["name"]} struct {{
    // Adicione dependências aqui
}}

{methods_code}
'''