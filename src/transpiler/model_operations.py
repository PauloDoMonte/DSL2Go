import os

def create_model_files(parsed_dsl, output_dir):
    """
    Cria arquivos de modelo no diretório de saída com base no DSL parseado.
    
    :param parsed_dsl: O DSL que foi parseado.
    :param output_dir: O diretório onde os arquivos de modelo serão gerados.
    """
    models = [cmd for cmd in parsed_dsl if cmd['type'] == 'model']
    models_dir = os.path.join(output_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    for model in models:
        model_content = generate_model_code(model)
        model_filename = os.path.join(models_dir, f'{model["name"].lower()}.go')
        with open(model_filename, 'w', encoding='utf-8') as f:
            f.write(model_content)

def generate_model_code(model):
    """
    Gera o código Go para um modelo.
    
    :param model: O modelo a ser gerado.
    :return: O código Go do modelo.
    """
    fields_code = '\n    '.join([f'{field["name"]} {field["type"]}' for field in model['fields']])
    return f'''package models

import (
    "gorm.io/gorm"
)

type {model["name"]} struct {{
    gorm.Model
    {fields_code}
}}
'''