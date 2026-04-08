import pandas as pd

def otimizar_rota(arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    # Ordena por Corredor e depois por Prateleira
    rota_otimizada = df.sort_values(by=['corredor', 'prateleira'])
    return rota_otimizada

if __name__ == "__main__":
    print('--- Rota de Picking Otimizada ---')
    print(otimizar_rota('pedidos.csv'))
