def read_file(file_path):
    """
    Lê o conteúdo de um arquivo e retorna como uma string.
    
    :param file_path: Caminho para o arquivo.
    :return: Conteúdo do arquivo como string.
    """
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    """
    Escreve o conteúdo em um arquivo.
    
    :param file_path: Caminho para o arquivo.
    :param content: Conteúdo a ser escrito no arquivo.
    """
    with open(file_path, 'w') as file:
        file.write(content)