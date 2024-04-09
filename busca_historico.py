import pandas as pd
import yfinance as yf
from raw import conectar_mongodb

def obter_fechamentos_historicos(ticker):
    # Conectar ao banco de dados
    client = conectar_mongodb()
    db = client.Invest  # Nome do banco de dados
    collection = db.historico  # Nome da coleção

    # Consultar o banco de dados para obter os dados históricos para o ticker especificado
    cursor = collection.find({"ticker": ticker})

    # Extrair os fechamentos dos dados do cursor e retornar
    fechamentos_historicos = [dado['Close'] for dado in cursor]
    return fechamentos_historicos

def main(ticker):
    # Obter os fechamentos históricos para o ticker especificado
    fechamentos_historicos = obter_fechamentos_historicos(ticker)

    # Exibir os fechamentos obtidos no prompt
    print("Fechamentos históricos para o ticker", ticker, ":")
    for fechamento in fechamentos_historicos:
        print(fechamento)

if __name__ == "__main__":
    # Solicitar ao usuário o ticker desejado
    ticker = input("Digite o ticker desejado (exemplo: MGLU3.SA): ")

    # Chamar a função principal
    main(ticker)
