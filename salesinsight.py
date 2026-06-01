"""
Projeto de Análise de Vendas - Sales Insight    
Código para analisar um dataset de vendas, incluindo geração de dados sintéticos,  
limpeza, transformação, cálculo de métricas e visualizações.

"""

# %%
# Bibliotecas necessárias para o projeto de análise de vendas
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import re
import random

# %%
# Função para gerar um dataset sintético de vendas 
def gerar_dataset_vendas(n_registros=200, seed=42):
    """Gera um dataset sintético de vendas com dados intencionalmente sujos."""
    
    random.seed(seed)
    np.random.seed(seed)

    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse", "Headset"]

    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Periféricos",
        "Mouse": "Periféricos",
        "Headset": "Periféricos"
    }

    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 51)]

    data_inicio = datetime(2024, 1, 1)

    dados = []

    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)

        preco_base = {
            "Notebook": 3500,
            "Smartphone": 2200,
            "Tablet": 1800,
            "Monitor": 1200,
            "Teclado": 250,
            "Mouse": 120,
            "Headset": 350
        }[produto]

        preco = round(preco_base * random.uniform(0.85, 1.15), 2)

        data = data_inicio + timedelta(days=random.randint(0, 364))

        if random.random() < 0.05:
            quantidade = None

        if random.random() < 0.04:
            preco = None

        if random.random() < 0.03:
            produto = " " + produto

        dados.append({
            "id_venda": i + 1,
            "data_venda": data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVÁLIDA",
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categorias.get(produto.strip(), "Outros"),
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })

    return pd.DataFrame(dados)

def inspecionar_dados(df):
    print(f"\n" + "="*40 + " Inspeção Inicial dos Dados " + "="*40)
    df.info()
    print(f"\n" + "=" *40 + " Tamanho do dataset" + "="*40 + f"\n{df.shape}")
    print(f"\n" + "=" *40 + " Listagem de colunas do dataset" + "="*40 + f"\n{list(df.columns)}")
    print(f"\n" + "=" *40 + " Tipos de dados das colunas" + "="*40 + f"\n{df.dtypes}")
    print(f"\n" + "=" *40 + " Estatísticas do dataset" + "="*40 + f"\n{df.describe(include='all')}")
    print(f"\n" + "=" *40 + " Amostra dos dados" + "="*40 + f"\n{df.head()}")
    print(f"\n" + "=" *40 + " Verificação de valores nulos" + "="*40 + f"\n{df.isnull().sum()}")
    print(f"\n" + "="*40 + " Fim da inspeção inicial " + "="*40)
    

def main():
    df_bruto = gerar_dataset_vendas()

    inspecionar_dados(df_bruto)

    df_bruto.to_csv("vendas.csv", index=False)

if __name__ == "__main__":
    main()

