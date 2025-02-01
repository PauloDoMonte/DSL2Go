import os
import sys

# Adiciona o diretório 'src' ao sys.path para garantir que os módulos possam ser importados corretamente
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.parser import DSLParser
from src.transpiler_ import Transpiler
from utils.helpers import read_file

def main():
    """
    Função principal que lê o arquivo DSL, faz o parse do conteúdo e gera a estrutura do projeto Go.
    """
    if len(sys.argv) != 2:
        print("Uso: python main.py <caminho_para_arquivo_dsl>")
        sys.exit(1)

    dsl_file_path = sys.argv[1]
    if not os.path.isfile(dsl_file_path):
        print(f"Erro: Arquivo '{dsl_file_path}' não encontrado.")
        sys.exit(1)

    # Ler o arquivo DSL
    dsl_content = read_file(dsl_file_path)

    # Fazer o parse do conteúdo DSL
    parser = DSLParser()
    parser.parse(dsl_content)
    parsed_dsl = parser.commands

    # Verificar se o parsed_dsl foi populado corretamente
    if not parsed_dsl:
        print("Erro: O DSL não foi parseado corretamente.")
        sys.exit(1)

    # Gerar a estrutura do projeto Go
    output_dir = os.path.splitext(dsl_file_path)[0] + "_go_project"
    transpiler = Transpiler(parsed_dsl)
    transpiler.generate_project_structure(output_dir)

    print(f"Projeto Go gerado em: {output_dir}")

if __name__ == "__main__":
    main()