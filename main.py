# Código principal para rodar o programa
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
import re
import random
from salesinsight import gerar_dataset_vendas,inspecionar_dados,AnalisadorComProjecao, limpar_strings_com_regex, calcular_estatisticas_numpy, exportar_resultados
import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter(action='ignore', category=FutureWarning)

# Função principal que aciona as outras funções desenvolvidas no salesinsight.py
def main():
    """
    Função principal: executa o pipeline completo do SalesInsight PY.
    """
    print("\n" + "="*60)
    print(" SALESINSIGHT PY – Pipeline de Análise de Dados de Vendas")
    print("="*60)
    # Etapa 0: Gerar dataset (se necessário)
    if not os.path.exists("vendas.csv"):
        print("\n[INFO] Gerando dataset sintético...")
        df_gerado = gerar_dataset_vendas(n_registros=200)
        df_gerado.to_csv("vendas.csv", index=False)
    # Etapa 1 a 6: Pipeline via classe com herança
    analisador = AnalisadorComProjecao("vendas.csv", meses_projecao=3)

    analisador.carregar()
    inspecionar_dados(analisador.df_bruto)

    analisador\
    .limpar()\
    .transformar()\
    .analisar()\
    .projetar_tendencia()\
    .visualizar()\
    .exportar_relatorio()


    # Etapa extra: limpeza com regex
    analisador.df_limpo = limpar_strings_com_regex(analisador.df_limpo)
    # Etapa extra: exportação JSON
    stats = calcular_estatisticas_numpy(analisador.df_limpo)
    exportar_resultados(analisador.metricas, analisador.clientes, stats)
    # Resumo final
    analisador.resumo()
    analisador.exibir_projecao_detalhada()
    print("\n[CONCLUÍDO] Pipeline finalizado com sucesso!")

    
if __name__ == "__main__":
    main()