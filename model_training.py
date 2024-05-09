import pandas as pd
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib

def load_and_preprocess_data(file_path):
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

def train_model(data, file_path):
    X = data.drop('Close', axis=1)
    y = data['Close']
    
    # Armazenar nomes das colunas para uso pós-escalonamento
    feature_names = X.columns
    
    scaler = StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    
    # Converter array numpy de volta para DataFrame, preservando nomes das colunas
    X_scaled = pd.DataFrame(X_scaled, columns=feature_names)

    models = {
        'RandomForest': RandomForestRegressor(random_state=42),
        'GradientBoosting': GradientBoostingRegressor(random_state=42)
    }
    param_grid = {
       'n_estimators': [100],
        'max_depth': [10],
        'min_samples_split': [2],
        'min_samples_leaf': [2]
    }
    tscv = TimeSeriesSplit(n_splits=5)

    results = []
    for name, model in models.items():
        grid_search = GridSearchCV(model, param_grid, cv=tscv, scoring='neg_mean_squared_error', verbose=5, n_jobs=-1)
        grid_search.fit(X_scaled, y)
        best_model = grid_search.best_estimator_

        # O GridSearchCV retrains o modelo com todo o conjunto de dados usando os melhores parâmetros encontrados.
        # aguarda retorno do professor para modificar
        # Salva cada modelo treinado com um nome específico para cada arquivo e modelo
        best_model.fit(X_scaled, y)  # O melhor modelo é retreinado explicitamente no conjunto completo
        joblib.dump(best_model, f'best_{name}_{file_path.split(".")[0]}.joblib')

        # Avaliação do modelo
        predictions = best_model.predict(X_scaled)

        # Previsão para o último dia disponível
        last_day_prediction = best_model.predict(X_scaled.iloc[[-1]])
        results.append(f"Best parameters for {name}: {grid_search.best_params_}")
        results.append(f"Previsão de fechamento para o último dia usando {name}: ${last_day_prediction[0]:.2f}")

    joblib.dump(scaler, f'scaler_{file_path.split(".")[0]}.joblib')
    return results

files = ['MGLU3.SA.csv', 'AAPL.csv']
all_results = []
for file_path in files:
    data = load_and_preprocess_data(file_path)
    results = train_model(data, file_path)
    all_results.extend(results)

# Imprime todos os resultados no final
for result in all_results:
    print(result)
