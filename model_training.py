import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import statsmodels.api as sm
from busca_historico import obter_fechamentos_historicos

def treinar_modelo(ticker, fechamentos_historicos):
    # Converter a lista de fechamentos históricos em um DataFrame
    df = pd.DataFrame(fechamentos_historicos, columns=['Close'])
    
    # Converter a lista de fechamentos históricos em um DataFrame
    df = pd.DataFrame(fechamentos_historicos, columns=['Close'])

    # Preencher valores ausentes com a média dos valores existentes
    df.fillna(df.mean(), inplace=True)

    # Suponha que a última coluna contenha os dados de fechamento
    X = df[['Close']]  # Usando apenas a coluna 'Close' para prever
    y = df.iloc[:, -1]

    # Dividir os dados em conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Normalizar os dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Criar e treinar o modelo de regressão linear
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Fazer previsão para o próximo dia
    previsao_proximo_dia = model.predict(X_test_scaled[[-1]])

    # Interpretar a previsão para o próximo dia
    ultimo_valor_real = y_test.values[-1]

    if previsao_proximo_dia > ultimo_valor_real:
        print("Tendência de queda para o próximo dia")
    elif previsao_proximo_dia < ultimo_valor_real:
        print("Tendência de alta para o próximo dia")
    else:
        print("Sem mudança significativa para o próximo dia")

    #print("Previsão para o próximo dia:", previsao_proximo_dia)

    # Plotagem do gráfico
    plt.figure(figsize=(10, 6))

    # Plotar os dados reais
    plt.plot(X_test, y_test, label='Valores reais', color='black')

    # Plotar a previsão para o próximo dia
    plt.plot(X_test.iloc[-1], previsao_proximo_dia, 'ro', label='Previsão próximo dia')

    # Título e rótulos dos eixos
    plt.xlabel('Data')
    plt.ylabel('Valor de Fechamento')

    # Adicionar legenda
    plt.legend()

    # Exibir o gráfico
    plt.show()

    # Decomposição da série temporal
    decomposicao = sm.tsa.seasonal_decompose(df['Close'], model='additive')
    decomposicao.plot()
    plt.show()

    # Autocorrelação
    sm.graphics.tsa.plot_acf(df['Close'], lags=30)
    plt.show()

    # Autocorrelação Parcial
    sm.graphics.tsa.plot_pacf(df['Close'], lags=30)
    plt.show()

    # Análise de resíduos
    residuos = y_test - model.predict(X_test_scaled)
    plt.figure(figsize=(10, 6))
    plt.plot(residuos)
    plt.title('Resíduos do Modelo')
    plt.xlabel('Amostras')
    plt.ylabel('Resíduos')
    plt.show()

def main():
    # Solicitar ao usuário o ticker desejado
    ticker = input("Digite o ticker desejado (exemplo: MGLU3.SA): ")

    # Chamar a função para treinar o modelo
    treinar_modelo(ticker)

if __name__ == "__main__":
    main()
