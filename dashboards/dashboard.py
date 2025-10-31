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
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4) # Cria 3 colunas para os KPIs

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


# KPI 2: % de Trabalho Remoto em 2024 vs 2023
if df_modelo_trabalho_pct is not None:
  try:
    df_modelo_trabalho_pct_idx = df_modelo_trabalho_pct.set_index('ano')

    remoto_2024 = df_modelo_trabalho_pct_idx.loc[2024, 'Remoto']

    #calcular a diferença com o de 2023
    if 2023 in df_modelo_trabalho_pct_idx.index:
      remoto_2023 = df_modelo_trabalho_pct_idx.loc[2023, 'Remoto']
      delta_remoto = remoto_2024 - remoto_2023
      delta_texto = f"{delta_remoto:.1f}% vs 2023"

    kpi_col2.metric("% Trabalho Remoto (2024)", f"{remoto_2024:.1f}%", delta=delta_texto)

  except KeyError:
    kpi_col2.error(f"Coluna 'Remoto' ou Ano não encontrado ({e}). Verifique o CSV.")
  except Exception as e:
    kpi_col2.error(f"Erro KPI Remoto: {e}")


# KPI 3: 
if df_pop_linguagens_pct is not None:
  try:
    df_pop_linguagens_pct_idx = df_pop_linguagens_pct.set_index('ano')

    linguagens_2024 = df_pop_linguagens_pct_idx.loc[2024]

    top_linguagem_2024 = linguagens_2024.idxmax()
    percent_top_linguagem_2024 = linguagens_2024.max()
    
    #limpeza do nome
    nome_limpo = top_linguagem_2024.replace('usa_linguagem_', '').replace('_', ' ').upper()
    if nome_limpo == 'C C++ C#':
      nome_limpo = 'C/C++/C#'

    #delta
    if 2023 in df_pop_linguagens_pct_idx.index:
      percent_top_linguagem_2023 = df_pop_linguagens_pct_idx.loc[2023, top_linguagem_2024]
      delta_linguagem = percent_top_linguagem_2024 - percent_top_linguagem_2023
      delta_texto = f'{delta_linguagem:.2f}% p.p vs 2023' #p.p significa pontos percentuais

    #exibir
    kpi_col3.metric(
      label='Linguagem mais popular(%)', 
      value=f'{nome_limpo} - ({percent_top_linguagem_2024}%)', 
      delta=delta_texto
    )

  except KeyError as e:
    kpi_col3.error(f"Ano ou coluna não encontrado ({e}). Verifique o CSV de linguagens.")
  except Exception as e:
    kpi_col3.error(f"Erro KPI Linguagem: {e}")


# --- KPI 4: Top Ferramenta de BI (2024) ---
if df_pop_bi_pct is not None:
  try:
    df_pop_bi_pct_idx = df_pop_bi_pct.set_index('ano')

    bi_2024 = df_pop_bi_pct_idx.loc[2024]

    top_bi_2024 = bi_2024.idxmax()
    percent_top_bi_2024 = bi_2024.max()

    #calcular o delta
    if 2023 in df_pop_bi_pct_idx.index:
      percent_top_bi_2023 = df_pop_bi_pct_idx.loc[2023, top_bi_2024]
      delta_bi = percent_top_bi_2024 - percent_top_bi_2023
      delta_bi_texto = f"{delta_bi:.2f}% p.p vs 2023"

  #exibir
    kpi_col4.metric(
      label='Top Ferramenta BI (Uso %)',
      value=f"{top_bi_2024} - {percent_top_bi_2024}%",
      delta=delta_bi_texto
    )

  except KeyError as e:
    kpi_col4.error(f"Ano ou coluna não encontrado ({e}). Verifique o CSV de BI.")
  except Exception as e:
    kpi_col4.error(f"Erro KPI BI: {e}")


st.divider() #linha para divisão dos kpis e gráficos



# Início dos gráficos
# ==============================================================================
# SEÇÃO 1: ANÁLISE DE REMUNERAÇÃO
# ==============================================================================
st.header("📈 Análise de Remuneração")
st.markdown("Vamos detalhar como os salários evoluíram e como eles se comparam entre diferentes grupos.")

# --- Gráfico 1.1: Evolução por Senioridade ---
st.subheader("Evolução do Salário Médio por Nível de Senioridade")

if df_evol_salario_senioridade is not None:

  if 'ano' in df_evol_salario_senioridade.columns:
    df_evol_salario_senioridade_plot = df_evol_salario_senioridade.copy()

  # "Derreter" o DataFrame e deixar em formato longo
  df_melted_senioridade = df_evol_salario_senioridade_plot.melt(
    id_vars='ano', 
    value_vars=['Júnior', 'Pleno', 'Sênior'], # Colunas que queremos transformar em linhas
    var_name='nivel_hierarquico',  # Nome da nova coluna para as categorias (Júnior, Pleno...)
    value_name='salario_medio'     # Nome da nova coluna para os valores (R$ 3876.49, etc.)
  )
  
  # --- 2. Criação do Gráfico (Seaborn + Matplotlib) ---
  # Criar a "tela" (Figure) e a "área de desenho" (Axes)
  fig_senioridade, ax_senioridade = plt.subplots(figsize=(10, 4)) # Tamanho 10x5 polegadas

  # Plotar o gráfico de linhas
  sns.lineplot(
    data=df_melted_senioridade, #qual dado vamos usar
    x='ano', #eixo x
    y='salario_medio', #eixo y
    hue='nivel_hierarquico', # Cria uma linha de cor diferente para cada nível
    style='nivel_hierarquico', # (Opcional) Usa estilos de linha diferentes
    markers=True, # Adiciona marcadores (bolinhas) nos pontos de dados
    markersize=8, #tamanho do marcador
    linewidth=2.5, #espessura da linha
    dashes=False, #todas serão linhas contínuas
    ax=ax_senioridade # Diz ao Seaborn para desenhar nesta "área"
  )

  # for nivel in df_melted_senioridade['nivel_hierarquico'].unique():
  #   dados_nivel = df_melted_senioridade[df_melted_senioridade['nivel_hierarquico'] == nivel]
    
  #   for _, row in dados_nivel.iterrows():
  #       ax_senioridade.annotate(
  #           f'R$ {row["salario_medio"]:,.0f}'.replace(',', '.'),  # Formatação BR
  #           (row['ano'], row['salario_medio']),
  #           textcoords="offset points",
  #           xytext=(0,10),
  #           ha='center',
  #           fontsize=9,
  #           alpha=0.8,
  #           bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8)  # Fundo branco
  #       )

  # --- 3. Customização (Princípios de Visualização) ---
  # Título claro e informativo
  ax_senioridade.set_title('Evolução do Salário MÉDIO por Senioridade (2021-2024)', fontsize=16, pad=20)
  
  # Rótulos dos eixos claros
  ax_senioridade.set_xlabel('Ano', fontsize=12)
  ax_senioridade.set_ylabel('', fontsize=12)
  
  # Adicionar uma grade no axes sutil
  ax_senioridade.grid(axis='y', linestyle='--', alpha=0.4)
  
  # Remover "espinhas" (bordas) desnecessárias do gráfico
  sns.despine(ax=ax_senioridade, left=True, bottom=True)
  
  # Formatar o eixo Y para parecer com dinheiro
  # Isso transforma 12000 em "R$ 12.000"
  try:
      # Tenta usar um formatador mais avançado se 'matplotlib.ticker' estiver disponível
      from matplotlib.ticker import FuncFormatter
      ax_senioridade.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'R$ {x:,.0f}'))
  except ImportError:
      # Se falhar, usa um fallback simples
      st.warning("Matplotlib ticker não encontrado, formatando eixo Y de forma simples.")
      
  # Ajustar ticks do eixo X para mostrar todos os anos
  ax_senioridade.set_xticks([2021, 2022, 2023, 2024])
  
  # Mover a legenda para fora do gráfico para não poluir
  ax_senioridade.legend(title='Senioridade', bbox_to_anchor=(1.05, 1), loc='upper left')

  # Ajusta o layout para garantir que nada (como a legenda) seja cortado
  plt.tight_layout()

  # --- 4. Exibição no Streamlit ---  
  # use_container_width=True é o comando chave para fazer o gráfico
  st.pyplot(fig_senioridade, use_container_width=True)
  plt.close(fig_senioridade) # Limpa a figura da memória (MUITO IMPORTANTE)

  # --- 5. Storytelling (Opcional, mas recomendado) ---
  st.markdown("""
  **Insights da Análise:**
  * **Crescimento Consistente:** Todos os níveis de senioridade apresentaram um aumento no salário médio de 2021 para 2024.
  * **Salto Sênior:** O salário médio para Sênior foi o que mais cresceu em termos absolutos, ultrapassando R$ 14.500 em 2024.
  * **"Vale do Pleno":** Curiosamente, o salário médio para o nível Pleno teve uma leve queda em 2023 antes de se recuperar em 2024, indicando uma possível estabilização ou mudança no perfil dos respondentes desse nível.
  """)

# mostra a tabela de dados
  with st.expander("Ver dados da tabela (Salário Médio por Senioridade)"):
      # Prepara a tabela para exibição, formatando os números
      tabela_para_exibir = df_evol_salario_senioridade.set_index('ano').style.format("R$ {:,.2f}")
      st.dataframe(tabela_para_exibir, use_container_width=True)

else:
  st.warning("Arquivo '04_analise_evolucao_salario_senioridade.csv' não carregado. O gráfico não pode ser gerado.")

st.divider()