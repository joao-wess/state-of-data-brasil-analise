import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
  page_title="Dashboard State of Data Brasil",
  page_icon="📊",
  layout="wide"
)

BASE_PATH = Path.cwd()
DASHBOARD_DATA_DIR = BASE_PATH / 'notebook' / 'dashboard_data'

#carregar em cache para o streamlit ficar mais rápido
@st.cache_data 
def load_data(file_path):
  try:
    return pd.read_csv(file_path)
  except FileNotFoundError:
    st.error(f"Erro: Arquivo não encontrado em {file_path}")
    return None
  
# --- Título Principal ---
st.title("📊 Análise do Mercado de Dados no Brasil (2021-2024)")
st.markdown("Este dashboard apresenta insights sobre salários, tecnologias e tendências do mercado de dados brasileiro, com base na pesquisa State of Data.")

#Carregar os dataset
df_evol_salario_cargo = load_data(DASHBOARD_DATA_DIR / '04_analise_evolucao_salario_cargo.csv')
df_evol_salario_senioridade = load_data(DASHBOARD_DATA_DIR / '04_analise_evolucao_salario_senioridade.csv')

df_salario_genero_senioridade_stats = load_data(DASHBOARD_DATA_DIR / '05_analise_salario_por_genero_senioridade_stats.csv')
df_pay_gap_nivel = load_data(DASHBOARD_DATA_DIR / '05_analise_pay_gap_percentual_por_nivel.csv')

df_salario_regiao_stats = load_data(DASHBOARD_DATA_DIR / '07_analise_salario_por_regiao_stats.csv') # Principal para pergunta 7
df_salario_regiao_senioridade_stats = load_data(DASHBOARD_DATA_DIR / '07_analise_salario_por_regiao_senioridade.csv')

df_pop_linguagens_pct = load_data(DASHBOARD_DATA_DIR / '08_analise_popularidade_linguagens_pct.csv')
df_pop_bi_pct = load_data(DASHBOARD_DATA_DIR / '08_analise_popularidade_bi_pct.csv')

df_pop_cloud_pct = load_data(DASHBOARD_DATA_DIR / '09_analise_popularidade_cloud_pct.csv')

df_salario_ensino_stats = load_data(DASHBOARD_DATA_DIR / '15_analise_salario_por_nivel_ensino_stats.csv') # Principal para pergunta 15
df_salario_ensino_senioridade_stats = load_data(DASHBOARD_DATA_DIR / '15_analise_salario_por_ensino_senioridade_stats.csv') # Detalhado

df_modelo_trabalho_pct = load_data(DASHBOARD_DATA_DIR / '18_analise_evolucao_modelo_trabalho_pct.csv')

# Carregamento dos KPI's
df_kpi_salario_geral = load_data(DASHBOARD_DATA_DIR / 'kpi_salario_geral_mediana_ano.csv')


# KPI's
# --- KPIs Principais (Resumo Rápido do Cenário Atual - 2024) ---
st.header("✨ KPIs Principais (2024)")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3) # Cria 3 colunas para os KPIs

# KPI 1: Salário Mediano Geral 2024 e Comparação com 2023
if df_kpi_salario_geral is not None:
  try:
    # Garante que 'ano' seja o índice para facilitar a busca com .loc
    df_kpi_salario_geral_idx = df_kpi_salario_geral.set_index('ano')

    salario_mediano_2024 = df_kpi_salario_geral_idx.loc[2024, 'salario_mediano_geral']
    salario_mediano_2023 = df_kpi_salario_geral_idx.loc[2022, 'salario_mediano_geral']
    delta_salario_mediano = salario_mediano_2024 - salario_mediano_2023

    kpi_col1.metric("Salário Mediano Geral 2024", f"R$ {salario_mediano_2024:,.2f}", f"{delta_salario_mediano:,.2f} vs 2022")
  except KeyError:
    kpi_col1.error("Ano 2024 ou 2022 não encontrado nos dados do KPI.")
  except Exception as e:
    kpi_col1.error(f"Erro KPI Salário Mediano: {e}")