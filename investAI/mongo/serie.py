import datetime
from datetime import timedelta

import numpy as np
import pandas as pd
import yfinance as yf
from pandas.tseries.offsets import BDay
from ta import momentum, trend  # Importação da biblioteca ta
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.exponential_smoothing import ExponentialSmoothing
from datetime import datetime

# Definir data de hoje
hoje = datetime.today().strftime('%Y-%m-%d')

# Converter hoje para formato Datetime
hoje_dt = datetime.strptime(hoje, '%Y-%m-%d')

# Definir data final: 1 dia antes do atual
fim = hoje_dt - timedelta(days=1)

# Definir data inicial: 3 anos antes do final
inicio = fim - timedelta(days=3*365)  # Subtrair 3 anos (em dias) do fim

# Carregar dados históricos da ação MGLU3 (3 anos)
ticket = yf.Ticker('MGLU3.SA')
df = ticket.history(interval='1d', start=inicio, end=fim)

# Selecionar apenas a coluna 'Close'
df = df[['Close']]

# Visualizar as primeiras e últimas linhas
df.head()
df.tail()
print(df)
# Definir pesos para a WMA
pesos = list(range(1, 11))[::-1]

# Criar lista para armazenar valores da WMA
WMA = []

# Calcular a WMA para cada dia
for i in range(len(df)):
    if i < len(pesos):
        WMA.append(np.dot(df['Close'].iloc[i:i+len(pesos)], pesos) / sum(pesos))
    else:
        WMA.append(np.dot(df['Close'].iloc[i-len(pesos):i+1], pesos) / sum(pesos))

# Adicionar a coluna da WMA ao DataFrame
df['WMA'] = WMA

# Visualizar o preço de fechamento e a WMA
plt.plot(df['Close'], label='Preço de Fechamento')
plt.plot(df['WMA'], label='WMA')
plt.legend()
plt.show()
