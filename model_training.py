import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

# Função para subtrair um número de dias de uma data fornecida
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

# Função para atualizar o arquivo CSV com novos dados
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
        # Tenta carregar dados existentes do CSV
        df_existente = pd.read_csv(file_path)
        df_existente['Date'] = pd.to_datetime(df_existente['Date'])
    except FileNotFoundError:
        # Se o arquivo não existir, criar um novo DataFrame vazio
        df_existente = pd.DataFrame()

    # Garante que a coluna 'Date' esteja presente
    if 'Date' not in df_existente.columns:
        df_existente['Date'] = pd.NaT

    # Converte as datas para timezone-naive
    df_existente['Date'] = df_existente['Date'].dt.tz_localize(None)
    df_novo['Date'] = df_novo['Date'].dt.tz_localize(None)

    # Concatenar e remover duplicatas
    df_atualizado = pd.concat([df_existente, df_novo])
    df_atualizado.drop_duplicates(subset='Date', keep='last', inplace=True)
    df_atualizado.sort_values(by='Date', inplace=True)

    # Calcula a média móvel ponderada (WMA) de 14 dias
    df_atualizado['WMA'] = df_atualizado['Close'].rolling(window=14).mean()

    # Salva o DataFrame atualizado de volta no arquivo CSV
    df_atualizado.to_csv(file_path, index=False)
    print(f"CSV atualizado para {ticker}")

# Função para carregar e preprocessar os dados
def load_and_preprocess_data(file_path):
    """
    Carrega e pré-processa os dados do arquivo CSV.
    
    Parâmetros:
    - file_path: str
        O caminho do arquivo CSV.
    
    Retorna:
    - data: DataFrame
        O DataFrame pré-processado.
    """
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data.sort_values(by='Date', inplace=True)
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data['Weekday'] = data['Date'].dt.weekday
    data['MA7'] = data['Close'].rolling(window=7).mean().shift(1)
    data = data.drop(columns=['Date', 'Adj Close']).dropna()
    return data

# Função para calcular e mostrar as métricas
def calcular_metricas(y_true, y_pred, modelo, ticker):
    """
    Calcula e exibe as métricas de avaliação do modelo.
    
    Parâmetros:
    - y_true: array-like
        Valores reais.
    - y_pred: array-like
        Valores previstos.
    - modelo: str
        Nome do modelo.
    - ticker: str
        O ticker da ação ou ativo.
    """
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    print(f'Métricas para {modelo} - {ticker}:')
    print(f'MSE: {mse}')  # Mean Squared Error (Erro Quadrático Médio)
    print(f'MAE: {mae}')  # Mean Absolute Error (Erro Absoluto Médio)
    print(f'R²: {r2}')  # R-Squared (Coeficiente de Determinação)
    print('-----------------------------------')

# Função para treinar o modelo
def train_model(data, file_path):
    """
    Treina o modelo com os dados fornecidos e salva o modelo treinado.
    
    Parâmetros:
    - data: DataFrame
        Os dados de entrada para treinamento.
    - file_path: str
        O caminho do arquivo CSV contendo os dados.
    
    Retorna:
    - results: list
        Lista de strings com os melhores parâmetros e previsões para o último dia.
    """
    # Separar os dados em recursos (X) e alvo (y)
    X = data.drop('Close', axis=1)
    y = data['Close']
    
    # Armazenar nomes das colunas para uso pós-escalonamento
    feature_names = X.columns.tolist()
    
    # Padronização dos dados
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    
    # Converter array numpy de volta para DataFrame, preservando nomes das colunas
    X_scaled = pd.DataFrame(X_scaled, columns=feature_names)

    # Modelos a serem utilizados
    models = {
        'RandomForest': RandomForestRegressor(random_state=42),
        'GradientBoosting': GradientBoostingRegressor(random_state=42)
    }
    # Grade de parâmetros para o GridSearchCV
    param_grid = {
       'n_estimators': [100, 200, 250],  # Número de árvores no ensemble
        'max_depth': [2, 4],  # Profundidade máxima da árvore
        'min_samples_split': [2, 4, 6],  # Número mínimo de amostras necessárias para dividir um nó
        'min_samples_leaf': [1, 2, 3]  # Número mínimo de amostras necessárias em um nó folha
    }
    # Ajustar n_splits para ser menor do que o número de amostras
    n_splits = min(5, len(X) - 1)  # Número de divisões para validação cruzada

    tscv = TimeSeriesSplit(n_splits=n_splits)

    results = []
    for name, model in models.items():
        # Realiza a busca em grade com validação cruzada
        grid_search = GridSearchCV(model, param_grid, cv=tscv, scoring='neg_mean_squared_error', verbose=5, n_jobs=-1)
        grid_search.fit(X_scaled, y)
        best_model = grid_search.best_estimator_

        # O GridSearchCV retreina o modelo com todo o conjunto de dados usando os melhores parâmetros encontrados.
        best_model.fit(X_scaled, y)  # O melhor modelo é retreinado explicitamente no conjunto completo
        joblib.dump(best_model, f'best_{name}_{file_path.split(".")[0]}.joblib')

        # Avaliação do modelo
        predictions = best_model.predict(X_scaled)
        calcular_metricas(y, predictions, name, file_path.split(".")[0])

        # Previsão para o último dia disponível
        last_day_prediction = best_model.predict(X_scaled.iloc[[-1]])
        results.append(f"Best parameters for {name}: {grid_search.best_params_}")
        results.append(f"Previsão de fechamento para o último dia usando {name}: ${last_day_prediction[0]:.2f}")

    joblib.dump(scaler, f'scaler_{file_path.split(".")[0]}.joblib')
    return results

# Lista de tickers das ações ou ativos a serem analisados
tickers = ['MGLU3.SA.csv', 'AAPL.csv', 'TSLA', 'AMZO34.SA', 'BTC-USD', 'DISB34.SA', 'GOGL34.SA', 'ROXO34.SA', 'ITSA4.SA', 'BHIA3.SA']

# Definir a data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')
fim = hoje_dt - timedelta(days=1)

# Definir data de início: 7 dias atrás
inicio = subtract_days(fim, 7)

for ticker in tickers:
    # Carregar dados
    df = yf.Ticker(ticker).history(interval='1d', start=inicio, end=fim)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Atualizar CSV
    atualizar_csv(ticker, df)

# Treinar o modelo após atualizar os dados
files = ['MGLU3.SA.csv', 'AAPL.csv', 'TSLA.csv', 'AMZO34.SA.csv', 'BTC-USD.csv', 'DISB34.SA.csv', 'GOGL34.SA.csv', 'ROXO34.SA.csv', 'ITSA4.SA.csv', 'BHIA3.SA.csv']
all_results = []
for file_path in files:
    data = load_and_preprocess_data(file_path)
    results = train_model(data, file_path)
    all_results.extend(results)

# Imprime todos os resultados no final
for result in all_results:
    print(result)
