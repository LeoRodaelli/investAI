import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import yfinance as yf

# Função para lidar com a subtração de dias com base na versão do Python
def subtract_days(dt, days):
    if hasattr(dt, 'subtract'):  # Verifica se o método 'subtract' existe
        return dt.subtract(timedelta(days=days))
    else:
        return dt - timedelta(days=days)

# Função para salvar histórico no MongoDB
def salvar_historico(df, ticker, collection):
    for i in range(len(df)):
        data = df.index[i].strftime('%Y-%m-%d')
        if collection.count_documents({"data": data, "ticker": ticker}) == 0:
            documento = {
                "ticker": ticker,
                "data": data,
                "fechamento": df.iloc[i]["Close"]
            }
            collection.insert_one(documento)
            print("Novo documento inserido:", documento)
        else:
            print("Documento já existe para data", data, "e ticker", ticker)

# Conectar ao MongoDB
def conectar_mongodb():
    # Substitua "<username>" e "<password>" pelas suas credenciais
    connection_string = "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest"
    client = pymongo.MongoClient(connection_string)
    return client

# Lista de tickers
tickers = ["AAPL", "BTC-USD"]

# Conectar ao MongoDB
client = conectar_mongodb()
db = client.Invest  # Nome do banco de dados
collection = db.historico  # Nome da coleção

# Definir a data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt - timedelta(days=1)

# Definir data de início: 3 anos atrás
inicio = subtract_days(fim, 2)

for ticker in tickers:
    # Carregar dados
    df = yf.Ticker(ticker).history(interval='1d', start=inicio, end=fim)

    # Calcular WMA
    df['WMA'] = df['Close'].rolling(window=14).mean()

    # Salvar histórico no MongoDB
    salvar_historico(df, ticker, collection)
