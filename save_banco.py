import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import yfinance as yf
from raw import conectar_mongodb

# Definir a função para lidar com a subtração de dias com base na versão do Python
def subtract_days(dt, days):
    if hasattr(dt, 'subtract'):  # Verifica se o método 'subtract' existe
        return dt.subtract(timedelta(days=days))
    else:
        return dt - timedelta(days=days)

# Função para salvar histórico no MongoDB
def salvar_historico(df, ticker):

    # Conectar ao MongoDB usando a string de conexão das variáveis de ambiente
   # Conectar ao cliente MongoDB
    client = conectar_mongodb()

    # Acessar banco de dados e coleção
    db = client["Invest"]
    collection = db["historico"]

    # Criar dicionários para cada dia
    data_dict = []
    for i in range(len(df)):
        # Verificar se o documento já existe no banco de dados
        if collection.count_documents({"data": df.index[i].strftime('%Y-%m-%d'), "ticker": ticker}) == 0:
            data_dict.append({
                "data": df.index[i].strftime('%Y-%m-%d'),
                "ticker": ticker,
                "Close": df['Close'].iloc[i],
                "WMA": df['WMA'].iloc[i]
            })

    # Inserir dicionários na coleção
    if data_dict:
        collection.insert_many(data_dict)
        print(f"{len(data_dict)} documentos inseridos no banco de dados.")
    else:
        print("Nenhum novo documento inserido no banco de dados.")

    # Verificar se a conexão foi estabelecida com sucesso
    if "Invest" in client.list_database_names():
        print("Conexão bem-sucedida com o banco de dados 'Invest'.")
    else:
        print("Erro ao conectar ao banco de dados 'Invest'.")

# Definir as variáveis
ticker = 'AAPL'  # Ajustar o ticker desejado para ser pego pelo Site
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt - timedelta(days=1)

# Definir data de início: 3 anos atrás
inicio = subtract_days(fim, 3*365)

# Carregar dados
df = yf.Ticker(ticker).history(interval='1d', start=inicio, end=fim)

# Calcular WMA
df['WMA'] = df['Close'].rolling(window=14).mean()

# Salvar histórico no MongoDB
salvar_historico(df, ticker)
