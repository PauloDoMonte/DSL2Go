import os

def create_controller_files(parsed_dsl, output_dir):
    """
    Cria arquivos de controlador no diretório de saída com base no DSL parseado.
    
    :param parsed_dsl: O DSL que foi parseado.
    :param output_dir: O diretório onde os arquivos de controlador serão gerados.
    """
    controllers = [cmd for cmd in parsed_dsl if cmd['type'] == 'controller']
    controllers_dir = os.path.join(output_dir, 'controllers')
    os.makedirs(controllers_dir, exist_ok=True)
    
    for controller in controllers:
        controller_content = generate_controller_code(controller)
        controller_filename = os.path.join(controllers_dir, f'{controller["name"].lower()}.go')
        with open(controller_filename, 'w', encoding='utf-8') as f:
            f.write(controller_content)

def generate_controller_code(controller):
    """
    Gera o código Go para um controlador.
    
    :param controller: O controlador a ser gerado.
    :return: O código Go do controlador.
    """
    methods_code = '\n'.join([generate_controller_method_code(method, controller["name"]) for method in controller['methods']])
    return f'''package controllers

import (
    "net/http"
    "encoding/json"
    "strconv"
    "github.com/gorilla/mux"
    "context"
    "your_project/services"
    "your_project/models"
)

type {controller["name"]} struct {{
    service services.{controller["name"]}Service
}}

{methods_code}
'''

def generate_controller_method_code(method, controller_name):
    """
    Gera o código Go para um método de controlador.
    
    :param method: O método a ser gerado.
    :param controller_name: O nome do controlador.
    :return: O código Go do método.
    """
    parts = method.split()
    action = parts[0]
    model = parts[1]
    if action == 'GetAll':
        return f'''func (c *{controller_name}) GetAll{model}(w http.ResponseWriter, r *http.Request) {{
    {model.lower()}s := c.service.GetAll{model}()
    json.NewEncoder(w).Encode({model.lower()}s)
}}'''
    elif action == 'GetByID':
        return f'''func (c *{controller_name}) GetByID(w http.ResponseWriter, r *http.Request) {{
    params := mux.Vars(r)
    id, _ := strconv.Atoi(params["id"])
    {model.lower()} := c.service.GetByID(id)
    json.NewEncoder(w).Encode({model.lower()})
}}'''
    elif action == 'Create':
        return f'''func (c *{controller_name}) Create{model}(w http.ResponseWriter, r *http.Request) {{
    var {model.lower()} {model}
    _ = json.NewDecoder(r.Body).Decode(&{model.lower()})
    created{model} := c.service.Create{model}({model.lower()})
    json.NewEncoder(w).Encode(created{model})
}}'''
    elif action == 'Delete':
        return f'''func (c *{controller_name}) Delete(w http.ResponseWriter, r *http.Request) {{
    params := mux.Vars(r)
    id, _ := strconv.Atoi(params["id"])
    c.service.Delete(id)
    w.WriteHeader(http.StatusNoContent)
}}'''
    else:
        raise ValueError(f"Unknown action: {action}")