import pymongo
from pymongo import MongoClient

connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"

client = MongoClient(connection_string)

# Verificar se a conexão foi bem-sucedida
if client:
    print("Conectado ao MongoDB!")
else:
    print("Erro ao conectar ao MongoDB!")

# Acessar o banco de dados "invest"
db = client["Invest"]

# Acessar a coleção "acoes"
collection = db["acoes"]

# Inserir um documento
#document = {"nome": "MGLU3", "data": "2023-11-14", "preco": 21.50}
#collection.insert_one(document)

# Ler todos os documentos
documents = collection.find({})

# Atualizar um documento
collection.update_one({"nome": "MGLU3"}, {"$set": {"preco": 22.00}})

# Excluir um documento
#collection.delete_one({"nome": "MGLU3"})

def conectar_mongodb():
   

    # Substitua "<username>" e "<password>" pelas suas credenciais
    connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"
    client = pymongo.MongoClient(connection_string)

    return client
