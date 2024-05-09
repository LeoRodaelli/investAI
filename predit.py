import pandas as pd
import joblib
from pandas.tseries.offsets import BDay

def load_and_preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by='Date', inplace=True)
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data['Weekday'] = data['Date'].dt.weekday
    data['MA7'] = data['Close'].rolling(window=7, min_periods=1).mean().shift(1)  # Assegure a criação da coluna MA7
    last_date = data['Date'].iloc[-1] # Salva ultima data
    last_close = data['Close'].iloc[-1] # Salva ultimo valor de fechamento
    data = data.drop(columns=['Date', 'Adj Close']).dropna(subset=['MA7'], how='all')  #Para garantir que nao vai ter so Na
    return data, last_date, last_close

def predict_next_day(file_path):
    file_name = file_path.split('.')[0] # Tira o nome do arquivo sem extenão
    data, last_date, last_close = load_and_preprocess_data(file_path) # Pre-carrega e processa os arquivos ja salvo e ajustado
    
    loaded_scaler = joblib.load(f'scaler_{file_name}.joblib') # Carrega o escalonador expessifico pro arquivo
    
    next_date = last_date + BDay(1) # Calculo o proximo dia pela ultima data do arquivo
    next_data = { # Prepara dados para prever ja com a media movel e valor da ultima linha
        'Open': [data['Open'].iloc[-1]],
        'High': [data['High'].iloc[-1]],
        'Low': [data['Low'].iloc[-1]],
        'Volume': [data['Volume'].iloc[-1]],
        'Year': [next_date.year],
        'Month': [next_date.month],
        'Day': [next_date.day],
        'Weekday': [next_date.weekday()],
        'MA7': [data['MA7'].iloc[-1]]  # Garante que exista para nao trava
    }
    next_data_df = pd.DataFrame(next_data)
    next_data_scaled = loaded_scaler.transform(next_data_df) # Escalona os dados com escalonador escolhido
    next_data_scaled_df = pd.DataFrame(next_data_scaled, columns=next_data_df.columns)
    models = ['RandomForest', 'GradientBoosting'] #Lista de modelo a usar
    for model_name in models: # Aplica cada modelo pra fazer previsao do proximo dia
        loaded_model = joblib.load(f'best_{model_name}_{file_name}.joblib')
        next_day_prediction = loaded_model.predict(next_data_scaled_df)
        trend = "Alta" if next_day_prediction[0] > last_close else "Queda"
        print(f"Previsão de fechamento para {next_date.strftime('%Y-%m-%d')} usando {model_name} ({file_path}): ${next_day_prediction[0]:.2f} ({trend})")

files = ['AAPL.csv', 'MGLU3.SA.csv']
for file_path in files:
    predict_next_day(file_path)
