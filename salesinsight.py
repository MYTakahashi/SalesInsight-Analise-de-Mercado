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

#Função para inspeção inicial dos dados.

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


 # Função para limpeza dos dados.

def limpar_dados(df):

    n_inicial = len(df)
    relatorio =  {}

    #Limpeza de espaços em branco em texto

    colunas_texto = df.select_dtypes(include=["object", "string"]).columns
    for col in colunas_texto:
        df[col] = df[col].str.strip()

    #Conversão e limpeza de datas

    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    n_datas_invalidas = df["data_venda"].isnull().sum()
    df = df.dropna(subset=["data_venda"])
    relatorio["datas_invalidas_removidas"] = n_datas_invalidas

    #Remover linhas com quantidade ou preço nulos

    n_antes = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes - len(df)

    # Garantir tipos numéricos corretos

    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    n_final = len(df)
    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = n_final
    relatorio["registros_removidos_total"] = n_inicial - n_final


     # Relatório de limpeza
    print("\n" + "=" * 40 + " RELATÓRIO DE LIMPEZA " + "=" * 40)
    for chave, valor in relatorio.items():
        print(f"  {chave}: {valor}")

    return df, relatorio

#Função para criar colunas derivadas.

def criar_colunas_derivadas(df):

    #Receita total por linha de venda
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]

    # Extração de componentes de data
    df["mes"] = df["data_venda"].dt.month
    df["mes_nome"] = df["data_venda"].dt.strftime("%B") 
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda q: f"Q{q}")
    df["ano"] = df["data_venda"].dt.year

     # Classificação da receita por item
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000
    ]
    classificacoes = ["Baixo Valor", "Médio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, classificacoes, default="Não Classificado")

    print("\n" + "=" * 40 + " COLUNAS DERIVADAS CRIADAS " + "=" * 40)
    print(df[["data_venda", "receita_total", "mes", "mes_nome", "trimestre", "ano", "faixa_receita_item"]].head())

    return df

# Função para calcular métricas.

def calcular_metricas(df):

    metricas = {}

    #Receita por mês
    por_mes = df.groupby("mes").agg(
    receita_total=("receita_total", "sum"),
    quantidade=("quantidade", "sum"),
    n_vendas=("id_venda", "count")
    ).reset_index().sort_values("mes")
    metricas["por_mes"] = por_mes

    # Top 5 produtos por receita
    top_produtos = df.groupby("produto")["receita_total"].sum()\
                     .sort_values(ascending=False).head(5).reset_index()
    metricas["top_produtos"] = top_produtos

    
    # Receita por categoria
    por_categoria = df.groupby("categoria")["receita_total"].sum().reset_index()
    metricas["por_categoria"] = por_categoria

    # Receita por região
    por_regiao = df.groupby("regiao").agg(
        receita_total=("receita_total", "sum"),
        media_ticket=("receita_total", "mean")
    ).reset_index().sort_values("receita_total", ascending=False)
    metricas["por_regiao"] = por_regiao

    # Exibição
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.to_string(index=False))

    return metricas

# Função principal para execução do projeto
def main():
    df_bruto = gerar_dataset_vendas()

    inspecionar_dados(df_bruto)

    df_bruto.to_csv("vendas.csv", index=False)

    df_limpo = df_bruto.copy()

    df_limpo, relatorio = limpar_dados(df_limpo)

    df_limpo = criar_colunas_derivadas(df_limpo)

    metricas = calcular_metricas(df_limpo)

    df_limpo.to_csv("vendas_limpo.csv", index=False)

if __name__ == "__main__":
    main()

