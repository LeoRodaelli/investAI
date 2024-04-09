import pandas as pd
from model_training import treinar_modelo
from busca_historico import obter_fechamentos_historicos

def main(ticker):
    try:
        # Obter os fechamentos históricos para o ticker especificado
        fechamentos_historicos = obter_fechamentos_historicos(ticker)

        # Exibir os fechamentos obtidos no prompt
        print("Fechamentos históricos para o ticker", ticker, ":")
        for fechamento in fechamentos_historicos:
            print(fechamento)

        # Chamar a função para treinar o modelo
        treinar_modelo(ticker, fechamentos_historicos)

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    # Solicitar ao usuário o ticker desejado
    ticker = input("Digite o ticker desejado (exemplo: MGLU3.SA): ")

    # Chamar a função principal
    main(ticker)
