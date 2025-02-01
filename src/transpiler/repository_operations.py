import os

def create_repository_files(parsed_dsl, output_dir):
    """
    Cria arquivos de repositório no diretório de saída com base no DSL parseado.
    
    :param parsed_dsl: O DSL que foi parseado.
    :param output_dir: O diretório onde os arquivos de repositório serão gerados.
    """
    repositories = [cmd for cmd in parsed_dsl if cmd['type'] == 'repository']
    repositories_dir = os.path.join(output_dir, 'repositories')
    os.makedirs(repositories_dir, exist_ok=True)
    
    for repository in repositories:
        repository_content = generate_repository_code(repository)
        repository_filename = os.path.join(repositories_dir, f'{repository["name"].lower()}.go')
        with open(repository_filename, 'w', encoding='utf-8') as f:
            f.write(repository_content)

def generate_repository_code(repository):
    """
    Gera o código Go para um repositório.
    
    :param repository: O repositório a ser gerado.
    :return: O código Go do repositório.
    """
    methods_code = '\n'.join([generate_repository_method_code(method, repository["name"]) for method in repository['methods']])
    return f'''package repositories

import (
    "gorm.io/gorm"
    "context"
)

type {repository["name"]} interface {{
    {methods_code}
}}

type {repository["name"]}Impl struct {{
    db *gorm.DB
}}

{methods_code}
'''

def generate_repository_method_code(method, repository_name):
    """
    Gera o código Go para um método de repositório.
    
    :param method: O método a ser gerado.
    :param repository_name: O nome do repositório.
    :return: O código Go do método.
    """
    parts = method.split()
    action = parts[0]
    model = parts[1]
    if action == 'FindAll':
        return f'''func (r *{repository_name}Impl) FindAll{model}() []{model} {{
    var {model.lower()}s []{model}
    r.db.Find(&{model.lower()}s)
    return {model.lower()}s
}}'''
    elif action == 'FindByID':
        return f'''func (r *{repository_name}Impl) FindByID(id int) {model} {{
    var {model.lower()} {model}
    r.db.First(&{model.lower()}, id)
    return {model.lower()}
}}'''
    elif action == 'Save':
        return f'''func (r *{repository_name}Impl) Save{model}({model.lower()} {model}) {model} {{
    r.db.Save(&{model.lower()})
    return {model.lower()}
}}'''
    elif action == 'Delete':
        return f'''func (r *{repository_name}Impl) Delete(id int) {{
    r.db.Delete(&{model}{{}}, id)
}}'''
    else:
        raise ValueError(f"Unknown action: {action}")