import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf

# Função para lidar com a subtração de dias com base na versão do Python
def subtract_days(dt, days):
    if hasattr(dt, 'subtract'):  # Verifica se o método 'subtract' existe
        return dt.subtract(timedelta(days=days))
    else:
        return dt - timedelta(days=days)

# Função para atualizar o arquivo CSV
def atualizar_csv(ticker, df_novo):
    # Caminho do arquivo CSV
    file_path = f"{ticker}.csv"
    
    try:
        # Carregar dados existentes do CSV
        df_existente = pd.read_csv(file_path)
        df_existente['Date'] = pd.to_datetime(df_existente['Date'])
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame vazio
        df_existente = pd.DataFrame()

    # Concatenar dados existentes com novos dados
    df_atualizado = pd.concat([df_existente, df_novo])
    df_atualizado.drop_duplicates(subset='Date', keep='last', inplace=True)
    
    # Ordenar por data
    df_atualizado.sort_values(by='Date', inplace=True)

    # Calcular WMA
    df_atualizado['WMA'] = df_atualizado['Close'].rolling(window=14).mean()

    # Salvar de volta no CSV
    df_atualizado.to_csv(file_path, index=False)
    print(f"CSV atualizado para {ticker}")

# Lista de tickers
tickers = ["MGLU3.SA", "AAPL"]

# Definir a data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt - timedelta(days=1)

# Definir data de início: 3 anos atrás
inicio = subtract_days(fim, 7)

for ticker in tickers:
    # Carregar dados
    df = yf.Ticker(ticker).history(interval='1d', start=inicio, end=fim)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Atualizar CSV
    atualizar_csv(ticker, df)
