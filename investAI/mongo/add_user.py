
from pymongo import MongoClient

def adicionar_usuario(nome, email, celular, cpf, senha):
    """
    Função para adicionar um novo usuário ao banco de dados MongoDB.

    Argumentos:
        nome (str): Nome do usuário.
        email (str): Email do usuário.
        celular (str): Celular do usuário.
        cpf (str): CPF do usuário.
        senha (str): Senha do usuário.

    Retorno:
        None.
    """

    # Importar a função de conexão do arquivo raw.py
    from raw import conectar_mongodb

    # Conectar ao cliente MongoDB
    client = conectar_mongodb()

    # Acessar o banco de dados e a coleção
    db = client["Invest"]
    collection = db["Usuarios"]

    # Criar o documento do usuário
    document = {
        "nome": nome,
        "email": email,
        "celular": celular,
        "cpf": cpf,
        "senha": senha,
    }

    # Inserir o documento na coleção
    collection.insert_one(document)

    # Mensagem de sucesso
    print(f"Usuário '{nome}' adicionado com sucesso!")

# Exemplo de uso
adicionar_usuario("Matheus", "matheus@email.com", "11999999999", "12345678900", "senha123")