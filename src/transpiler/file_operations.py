"""
Módulo responsável por operações de arquivos, como copiar a estrutura de diretórios e ler o conteúdo de templates.
"""

import os
import shutil

def copy_template_structure(output_dir):
    """
    Copia a estrutura de diretórios e arquivos do template para o diretório de saída.
    
    :param output_dir: O diretório onde a estrutura do projeto será gerada.
    """
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'go_project_structure')
    shutil.copytree(template_dir, output_dir, dirs_exist_ok=True)

def get_template_content(template_name):
    """
    Retorna o conteúdo de um arquivo de template.
    
    :param template_name: O nome do arquivo de template.
    :return: O conteúdo do arquivo de template.
    """
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates', 'go_project_structure', template_name)
    with open(template_path, 'r', encoding='utf-8') as file:
        return file.read()