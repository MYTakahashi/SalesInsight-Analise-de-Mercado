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


df_bruto = gerar_dataset_vendas()
df_bruto.to_csv("vendas.csv", index=False)

print(df_bruto.head())

# %%
## Função para gerar visualizações a partir do DataFrame e das métricas calculadas
def gerar_visualizacoes(df, metricas, output_dir="outputs/graficos"):
        os.makedirs(output_dir, exist_ok=True)
        # Configurações visuais globais
        sns.set_theme(style="whitegrid", palette="muted")
        plt.rcParams["figure.figsize"] = (12, 6)
        plt.rcParams["axes.titlesize"] = 14
        plt.rcParams["axes.labelsize"] = 12
        # --- Gráfico 1: Receita por Mês (linha) ---
        fig, ax = plt.subplots()
        por_mes = metricas["por_mes"]
        ax.plot(por_mes["mes"], por_mes["receita_total"], marker="o", linewidth=2, color="#2196F3")
        ax.fill_between(por_mes["mes"], por_mes["receita_total"], alpha=0.15, color="#2196F3")
        ax.set_title("Receita Total por Mês (2024)")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Receita Total (R$)")
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"], rotation=45)
        plt.tight_layout()
        caminho = os.path.join(output_dir, "vendas_por_mes.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f" Gráfico exportado: {caminho}")
                # --- Gráfico 2: Top 5 Produtos (barras horizontais) ---
        fig, ax = plt.subplots()
        top = metricas["top_produtos"]
        sns.barplot(data=top, y="produto", x="receita_total", ax=ax, palette="Blues_d")
        ax.set_title("Top 5 Produtos por Receita Total")
        ax.set_xlabel("Receita Total (R$)")
        ax.set_ylabel("Produto")
        for container in ax.containers:
                ax.bar_label(container, fmt="R$ %.0f", padding=5)
        plt.tight_layout()
        caminho = os.path.join(output_dir, "top_produtos.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f" Gráfico exportado: {caminho}")
        # --- Gráfico 3: Distribuição de Receita por Região (boxplot) ---
        fig, ax = plt.subplots()
        sns.boxplot(data=df, x="regiao", y="receita_total", ax=ax, palette="Set2")
        ax.set_title("Distribuição de Receita por Transação – Por Região")
        ax.set_xlabel("Região")
        ax.set_ylabel("Receita por Venda (R$)")
        plt.xticks(rotation=30)
        plt.tight_layout()
        caminho = os.path.join(output_dir, "distribuicao_regioes.png")
        plt.savefig(caminho, dpi=150)
        plt.close()
        print(f" Gráfico exportado: {caminho}")
        print("\n=== VISUALIZAÇÕES GERADAS COM SUCESSO ===")