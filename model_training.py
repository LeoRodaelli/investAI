import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados do arquivo CSV
print("Carregando dados do arquivo CSV...")
df = pd.read_csv('AAPL.csv')

# Converter a coluna de datas para números inteiros representando o número de dias desde a primeira data
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = (df['Date'] - df['Date'].min()).dt.days

# Assumir que a coluna 'Close' contém os dados de fechamento
X = df.drop(columns=['Close'])
y = df['Close']

# Dividir os dados em conjuntos de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo de regressão linear
print("Treinando modelo de regressão linear...")
model = LinearRegression()
model.fit(X_train, y_train)

# Fazer previsões para o dia seguinte
ultima_data = X_test.iloc[-1]
proximo_dia = ultima_data + 1
previsao_proximo_dia = model.predict([proximo_dia])

print("Previsão para o próximo dia:", previsao_proximo_dia)

# Interpretar a previsão para o próximo dia
ultimo_valor_real = y_test.values[-1]

if previsao_proximo_dia > ultimo_valor_real:
    print("Tendência de queda para o próximo dia")
elif previsao_proximo_dia < ultimo_valor_real:
    print("Tendência de alta para o próximo dia")
else:
    print("Sem mudança significativa para o próximo dia")
