# Import libraries
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

# Import libraries for data and WMA calculation
import yfinance as yf
from pandas import DataFrame

connection_string = "<CONNECTION_STRING>"
client = MongoClient(connection_string)

# Acessar banco de dados e coleção
db = client["Invest"]
collection = db["historico"]

# Define the function to handle date subtraction based on Python version
def subtract_days(dt, days):
    if hasattr(dt, 'subtract'):  # Check if 'subtract' method exists
        return dt.subtract(timedelta(days=days))
    else:
        return dt - timedelta(days=days)

# Define variables
ticker = 'MGLU3.SA'  # Adjust the ticker desired
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt - timedelta(days=1)

# Define inicio data: 3 anos atras
inicio = subtract_days(fim, 3*365)

# Load data
df = yf.Ticker(ticker).history(interval='1d', start='2020-01-01', end='2023-03-08')

# Calculate WMA
WMA = df['Close'].rolling(window=14).mean()
print(WMA)
def salvar_historico(df, ticker):

    # Load environment variables from .env
    load_dotenv()

    # conexao com o banco
    connection_string = os.getenv("CONNECTION_STRING")
    client = pymongo.MongoClient(connection_string)

    # acesso database e collection
    db = client["Invest"]
    collection = db["historico"]

    # Cria dictionaries de cada dia
    data_dict = []
    for i in range(len(df)):
        data_dict.append({
            "data": df.index[i].strftime('%Y-%m-%d'),
            "ticker": ticker,
            "fechamento": df['Close'].iloc[i],
            "WMA": WMA[i]
        })

    # Insert dictionaries into the collection
    collection.insert_many(data_dict)

# Save historical data to MongoDB
def salvar_historico(df, ticker):

    # Load environment variables from .env
    load_dotenv()

    # Connect to MongoDB using connection string from environment
    connection_string = os.getenv("CONNECTION_STRING")
    client = pymongo.MongoClient(connection_string)  # Use MongoClient after import
print(salvar_historico)