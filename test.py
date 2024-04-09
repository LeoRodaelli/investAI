
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Carregar dados do arquivo CSV
print("Carregando dados do arquivo CSV...")
df = pd.read_csv('AAPL.csv')

# Assumir que a coluna 'Close' contém os dados de fechamento
data = df['Close']

# Explorar os dados (considerar sazonalidade)
print("Exploração dos dados...")
print(data.describe())  # Verificar estatísticas descritivas

# Diferenciação raiz quadrada de segunda ordem
#Realiza uma diferenciação de segunda ordem na série temporal, onde é aplicada a raiz quadrada dos valores e, em seguida, é calculada a diferença entre os valores resultantes.
data_sqrt = np.sqrt(data.astype(float))
data_sqrt_diff = np.diff(data_sqrt)

# Decomposição Sazonal (opcional, mas mantida)
print("Decomposição Sazonal...")

#Realiza a decomposição sazonal da série temporal, identificando tendência, sazonalidade e componentes residuais.
seasonal_result = seasonal_decompose(data, model='additive', period=5)  # Ajustar período se necessário
data_diff = seasonal_result.resid  # Resíduos da decomposição sazonal (diferenciada)
decomposition = seasonal_decompose(data, model='additive', period=5)  # Verificar sazonalidade (dados diários assumidos)
decomposition.plot()
plt.show()

# Teste de Estacionariedade
#Realiza o teste de estacionariedade (ADF) na série temporal e exibe a estatística ADF e o valor p resultante.
print("Teste de Estacionariedade (ADF)...")
result = adfuller(data.dropna())
print('Estatística ADF: %f' % result[0])
print('Valor p: %f' % result[1])

# Diferenciação (se necessário)
#Inicia um loop para aplicar diferenciação na série temporal até que ela se torne estacionária (valor p < 0.05).
d = 0  # Inicializar contador de diferenciação
while result[1] > 0.05:  # Diferenciação enquanto a série não for estacionária
    if d == 0:
        # Verificar se a série contém valores NaN antes da diferenciação
        if data.isna().sum() > 0:
            print("Valores NaN encontrados na série. Removendo antes da diferenciação.")
            data = data.dropna()
        
        # Função personalizada para raiz quadrada (considerando NaN e valores não numéricos)
        data_sqrt = np.sqrt(data.astype(float))  # Diferenciação raiz quadrada de primeira ordem
        
        # **Verificar o tipo de objeto de data_sqrt:**
        print(type(data_sqrt))  # Imprimir o tipo de objeto
        
        # **Converter data_sqrt para um array NumPy se necessário:**
        if not isinstance(data_sqrt, np.ndarray):
            data_sqrt = np.array(data_sqrt)  # Converter para array NumPy
        
        data_sqrt_diff = np.diff(data_sqrt)  # Diferenciação raiz quadrada de primeira ordem
    elif d == 1:
        data_sqrt_diff = np.diff(data_sqrt_diff)  # Diferenciação raiz quadrada de segunda ordem
    else:
        data_sqrt_diff = np.diff(data_sqrt_diff)  # Diferenciação raiz quadrada de terceira
           
    # Teste ADF após diferenciação
    # Teste ADF após diferenciação
    result = adfuller(pd.Series(data_sqrt_diff).dropna()) #transformar em panda dnv
    print('Estatística ADF após diferenciação de ordem %d:' % d, result[0])
    print('Valor p após diferenciação de ordem %d:' % d, result[1])

    d += 1  # Incrementar contador de diferenciação

# ACF e PACF Plots
    #Plota os gráficos de ACF (função de autocorrelação) para identificar a ordem do componente autorregressivo (AR).
print("ACF e PACF Plots...")
plot_acf(data.dropna())
plt.show()


acf_values = acf(data.dropna())  # Calcular a ACF
plt.plot(acf_values)
plt.xlabel("Lag")
plt.ylabel("Autocorrelation")
plt.title("Autocorrelation Function (ACF)")
plt.show()

# Seleção e Avaliação de Modelos ARIMA
#Define as ordens ARIMA candidatas que serão testadas para ajuste ao modelo.
print("Seleção e Avaliação de Modelos...")
ordens_candidatas = [(1, 1, 1), (2, 1, 2), (2, 2, 1)]  # Exemplos de ordens


melhor_modelo = None
melhor_aic = None
melhor_rmse = None
melhor_diferenciacao = None  # Armazenar a ordem de diferenciação do melhor modelo

#Este loop itera sobre d variando de 0 a 1. Isso significa que o programa tentará ajustar modelos ARIMA com diferenciação de 0 e 1. Iniciando um loop para testar diferentes ordens ARIMA com diferentes graus de diferenciação.
for d in range(2):  # Tentar diferenciação de 0 a 1 vez 
   
    #Aqui, a série temporal é diferenciada uma vez (d=0) ou duas vezes (d=1) para torná-la estacionária, dependendo do valor de d no loop.
    data_diff = data.diff()  # Diferenciação inicial (se necessária)

   #Outro loop é iniciado, iterando sobre cada conjunto de parâmetros (p, q, s) em ordens_candidatas, onde ordens_candidatas contém diferentes combinações de ordens ARIMA. 
    for p, q, s in ordens_candidatas:
       
        
       #Aqui, um modelo ARIMA é instanciado usando a classe ARIMA do pacote statsmodels, com a série temporal diferenciada data_diff e os parâmetros (p, d, q) definidos por ordens_candidatas.
        modelo = ARIMA(data_diff, order=(p, q, s))
        
        #O modelo é ajustado aos dados usando o método fit(), que estima os parâmetros do modelo com base na série temporal fornecida.
        modelo_fit = modelo.fit()

        # Aqui, o critério de informação de Akaike (AIC) e o erro médio quadrático (RMSE) são calculados como métricas para avaliar o desempenho do modelo ajustado.
        aic = modelo_fit.aic
        rmse = mean_squared_error(data_diff.iloc[q:], modelo_fit.forecast(steps=len(data_diff) - q))

        #Verifica-se se o AIC do modelo atual é menor do que o AIC do melhor modelo encontrado até agora. Se for o caso, o modelo atual é considerado como o melhor modelo até agora.
        if melhor_modelo is None or aic < melhor_aic:

            #Se o modelo atual for considerado o melhor até agora, os detalhes desse modelo, como o modelo em si, o AIC, o RMSE e as ordens (d, p, q), são armazenados.
            melhor_modelo = modelo_fit
            melhor_aic = aic
            melhor_rmse = rmse
            melhor_diferenciacao = (d, p, q, s)  # Armazenar ordem de diferenciação e modelo ARIMA

    # Verificar se encontrou um modelo válido
    if melhor_modelo is None:
        print("Não foi possível encontrar um modelo ARIMA adequado.")
        break  # Sair do loop se nenhum modelo for válido

    # Previsão utilizando o melhor modelo
    print(f"Melhor modelo ARIMA encontrado: {(melhor_diferenciacao[1:])}")
    previsoes = melhor_modelo.forecast(steps=30)  # Previsão para os próximos 30 períodos

    # Inverter diferenciação para obter previsões no nível original (se houver diferenciação)
    if d > 0:
        if d == 1:
            previsoes = previsoes.cumsum()  # Acumulação para diferenciação de primeira ordem
        elif d == 2:
            previsoes_invertidas = np.zeros(len(previsoes))
            previsoes_invertidas[0] = previsoes[0]
            previsoes_invertidas[1] = previsoes[1] + previsoes_invertidas[0]
            for i in range(2, len(previsoes)):
                previsoes_invertidas[i] = previsoes[i] + previsoes_invertidas[i-1] + previsoes_invertidas[i-2]
            previsoes = previsoes_invertidas
        else:
            # Implementar inversão para diferenciações de ordem superior
            pass
    else:
        previsoes += data.iloc[-1]  # Somar o último valor observado se não houver diferenciação

    # Análise de Resíduos (opcional)
    print("Análise de Resíduos...")
    residuos = melhor_modelo.resid  # Armazenar os resíduos do modelo
    resultado_adf_residuos = adfuller(residuos.dropna())
    print('Estatística ADF dos resíduos:', resultado_adf_residuos[0])
    print('Valor p dos resíduos:', resultado_adf_residuos[1])

    # Verificar se os resíduos são estacionários (valor p < 0.05)
    if resultado_adf_residuos[1] < 0.05:
        print("Os resíduos do modelo ARIMA parecem ser estacionários.")
    else:
        print("Os resíduos do modelo ARIMA podem não ser estacionários. Considere transformações adicionais.")

    # Interpretação e Visualização das Previsões
    print("Interpretação e Visualização das Previsões...")
    # ... plotar previsões junto com os dados originais para comparação ...

   # Análise de Tendência
ultimo_valor_fechamento = data.iloc[-1]
primeira_previsao = previsoes.iloc[0]

if ultimo_valor_fechamento < primeira_previsao:
    print("Tendência de alta: o valor previsto para o próximo período é maior que o fechamento anterior.")
elif ultimo_valor_fechamento > primeira_previsao:
    print("Tendência de queda: o valor previsto para o próximo período é menor que o fechamento anterior.")
else:
    print("Tendência incerta: o valor previsto para o próximo período é igual ao fechamento anterior.")
