def get_routes_content(parsed_dsl):
    """
    Retorna o conteúdo do arquivo router.go.
    
    :param parsed_dsl: O DSL que foi parseado.
    :return: O conteúdo do arquivo router.go.
    """
    routes = [cmd for cmd in parsed_dsl if cmd['type'] == 'route']
    routes_code = '\n'.join([generate_route_code(route) for route in routes])
    return f'''package routes

import (
    "net/http"
    "github.com/gorilla/mux"
    "your_project/controllers"
)

func NewRouter() *mux.Router {{
    r := mux.NewRouter()
    {routes_code}
    return r
}}
'''

def generate_route_code(route):
    """
    Gera o código Go para uma rota.
    
    :param route: A rota a ser gerada.
    :return: O código Go da rota.
    """
    method = route['method'].lower().capitalize()
    path = route['path']
    handler = f'controllers.{method}Handler'
    return f'r.HandleFunc("{path}", {handler}).Methods("{route["method"]}")'