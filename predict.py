import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
from pymongo import MongoClient
from pandas.tseries.offsets import BDay

def subtract_days(dt, days):
    """
    Subtrai um número de dias de uma data fornecida.
    
    Parâmetros:
    - dt: datetime
        A data original.
    - days: int
        O número de dias a serem subtraídos.
    
    Retorna:
    - datetime
        A nova data com os dias subtraídos.
    """
    return dt - timedelta(days=days)

def atualizar_csv(ticker, df_novo):
    """
    Atualiza um arquivo CSV com novos dados de um DataFrame fornecido.
    
    Parâmetros:
    - ticker: str
        O ticker da ação ou ativo.
    - df_novo: DataFrame
        O DataFrame contendo os novos dados a serem adicionados.
    """
    file_path = f"{ticker}.csv"
    try:
        df_existente = pd.read_csv(file_path)
        df_existente['Date'] = pd.to_datetime(df_existente['Date'])
    except FileNotFoundError:
        df_existente = pd.DataFrame()

    # Converte as datas para timezone-naive
    df_existente['Date'] = df_existente['Date'].dt.tz_localize(None)
    df_novo['Date'] = df_novo['Date'].dt.tz_localize(None)

    # Concatenar e remover duplicatas
    df_atualizado = pd.concat([df_existente, df_novo])
    df_atualizado.drop_duplicates(subset='Date', keep='last', inplace=True)
    df_atualizado.sort_values(by='Date', inplace=True)

    # Calcula a média móvel ponderada (WMA)
    df_atualizado['WMA'] = df_atualizado['Close'].rolling(window=14).mean()

    # Salva o DataFrame atualizado de volta no arquivo CSV
    df_atualizado.to_csv(file_path, index=False)
    print(f"CSV atualizado para {ticker}")

def conectar_mongodb():
    """
    Conecta ao MongoDB e retorna o objeto de banco de dados.
    
    Retorna:
    - db: Database
        O objeto de banco de dados MongoDB.
    """
    client = MongoClient(
        "mongodb+srv://matheusp4:b4YEq95UskHGaC3k@invest.aju5sat.mongodb.net/?retryWrites=true&w=majority&appName=Invest",
        tlsAllowInvalidCertificates=True
    )
    return client['Invest']

def salvar_previsao(db, model_name, ticker, prediction, trend, overall_trend, next_date):
    """
    Salva a previsão no MongoDB e remove dados de datas anteriores.
    
    Parâmetros:
    - db: Database
        O objeto de banco de dados MongoDB.
    - model_name: str
        O nome do modelo utilizado para a previsão.
    - ticker: str
        O ticker da ação ou ativo.
    - prediction: float
        O valor previsto de fechamento.
    - trend: str
        A tendência prevista (Alta ou Queda).
    - overall_trend: str
        A tendência geral baseada em múltiplas previsões.
    - next_date: datetime
        A data da previsão.
    """
    collection = db['predictions']
    # Remove previsões de datas anteriores para o mesmo ticker e modelo
    collection.delete_many({'model': model_name, 'ticker': ticker})
    prediction_data = {
        'model': model_name,
        'ticker': ticker,
        'prediction': prediction,
        'trend': trend,
        'overall_trend': overall_trend,
        'prediction_date': next_date.strftime('%Y-%m-%d')
    }
    collection.insert_one(prediction_data)
    print(f"Previsão salva no MongoDB para {ticker} usando {model_name}.")

def load_and_preprocess_data(file_path):
    """
    Carrega e pré-processa os dados do arquivo CSV.
    
    Parâmetros:
    - file_path: str
        O caminho do arquivo CSV.
    
    Retorna:
    - data: DataFrame
        O DataFrame pré-processado.
    - last_date: datetime
        A última data disponível nos dados.
    - last_close: float
        O último valor de fechamento disponível nos dados.
    """
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by='Date', inplace=True)
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data['Weekday'] = data['Date'].dt.weekday
    data['MA7'] = data['Close'].rolling(window=7, min_periods=1).mean().shift(1)
    data['Dividends'] = 0
    data['Stock Splits'] = 0
    data['WMA'] = data['Close'].rolling(window=14).mean()
    last_date = data['Date'].iloc[-1]
    last_close = data['Close'].iloc[-1]
    data = data.drop(columns=['Date', 'Adj Close']).dropna(subset=['MA7'], how='all')
    return data, last_date, last_close

def predict_next_day(file_path):
    """
    Faz a previsão para o próximo dia útil e salva no MongoDB.
    
    Parâmetros:
    - file_path: str
        O caminho do arquivo CSV contendo os dados históricos.
    """
    db = conectar_mongodb()
    file_name = file_path.split('.')[0]
    data, last_date, last_close = load_and_preprocess_data(file_path)
    
    loaded_scaler = joblib.load(f'scaler_{file_name}.joblib')
    
    next_date = last_date + BDay(1)
    next_data = {
        'Open': [data['Open'].iloc[-1]],
        'High': [data['High'].iloc[-1]],
        'Low': [data['Low'].iloc[-1]],
        'Volume': [data['Volume'].iloc[-1]],
        'Year': [next_date.year],
        'Month': [next_date.month],
        'Day': [next_date.day],
        'Weekday': [next_date.weekday()],
        'MA7': [data['MA7'].iloc[-1]],
        'Dividends': [0],
        'Stock Splits': [0],
        'WMA': [data['WMA'].iloc[-1]]
    }
    next_data_df = pd.DataFrame(next_data)
    feature_names = loaded_scaler.feature_names_in_
    next_data_df = next_data_df[feature_names]
    next_data_scaled = loaded_scaler.transform(next_data_df)
    next_data_scaled_df = pd.DataFrame(next_data_scaled, columns=next_data_df.columns)

    predictions = {}
    trends = []

    models = ['RandomForest', 'GradientBoosting']
    for model_name in models:
        loaded_model = joblib.load(f'best_{model_name}_{file_name}.joblib')
        next_day_prediction = loaded_model.predict(next_data_scaled_df)[0]
        trend = "Alta" if next_day_prediction > last_close else "Queda"
        predictions[model_name] = (next_day_prediction, trend)
        trends.append(trend)
        print(f"Previsão de fechamento para {next_date.strftime('%Y-%m-%d')} usando {model_name} ({file_path}): ${next_day_prediction:.2f} ({trend})")

    overall_trend = "Previsão Indeterminada"
    if trends.count("Alta") == 2:
        overall_trend = "Grandes chances de ALTA"
    elif trends.count("Queda") == 2:
        overall_trend = "Grandes chances de QUEDA"

    for model_name, (next_day_prediction, trend) in predictions.items():
        salvar_previsao(db, model_name, file_name, next_day_prediction, trend, overall_trend, next_date)

# Lista de tickers das ações ou ativos a serem analisados
tickers = ['MGLU3.SA', 'AAPL', 'TSLA', 'AMZO34.SA', 'BTC-USD', 'DISB34.SA', 'GOGL34.SA', 'ROXO34.SA', 'ITSA4.SA', 'BHIA3.SA']

# Definir a data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt

# Ajuste para garantir que pegamos dados até o dia atual
inicio = subtract_days(fim, 10)

# Atualizar os arquivos CSV com os dados mais recentes
for ticker in tickers:
    df = yf.Ticker(ticker).history(interval='1d', start=inicio, end=fim)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    atualizar_csv(ticker, df)

# Realizar a previsão para o próximo dia útil para cada arquivo CSV
files = [f"{ticker}.csv" for ticker in tickers]
for file_path in files:
    predict_next_day(file_path)
