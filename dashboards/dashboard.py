import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
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

# --- Gráfico 1.1: Evolução por Senioridade (COM ANOTAÇÕES DE EVOLUÇÃO) ---

if df_evol_salario_senioridade is not None:
  # --- 1. Preparação dos Dados para Plotagem ---
  if 'ano' not in df_evol_salario_senioridade.columns:
    df_evol_salario_senioridade_plot = df_evol_salario_senioridade.reset_index()
  else:
    df_evol_salario_senioridade_plot = df_evol_salario_senioridade.copy()

  df_melted_senioridade = df_evol_salario_senioridade_plot.melt(
    id_vars='ano', 
    value_vars=['Júnior', 'Pleno', 'Sênior'],
    var_name='nivel_hierarquico',
    value_name='salario_medio'
  )
  
  # --- Cálculo da Mudança Percentual ---
  df_melted_senioridade.sort_values(by=['nivel_hierarquico', 'ano'], inplace=True)
  df_melted_senioridade['variacao_pct'] = df_melted_senioridade.groupby('nivel_hierarquico')['salario_medio'].pct_change()

  
  # --- 2. Criação do Gráfico (Seaborn + Matplotlib) ---
  fig_senioridade, ax_senioridade = plt.subplots(figsize=(10, 4.5)) # Aumentei um pouco a altura para as anotações

  #ordem das legendas
  salario_2024_senioridade = df_melted_senioridade[df_melted_senioridade['ano'] == 2024].set_index('nivel_hierarquico')['salario_medio']
  
  ordem_decrescente_senioridade = salario_2024_senioridade.sort_values(ascending=False).index.tolist()

  sns.lineplot(
    data=df_melted_senioridade,
    x='ano',
    y='salario_medio',
    hue='nivel_hierarquico',
    style='nivel_hierarquico',
    markers=True,
    markersize=10,
    linewidth=2.5,
    dashes=False,
    ax=ax_senioridade,
    hue_order=ordem_decrescente_senioridade
  )

  # colocar aumento percentual em cada marker
  for _, row in df_melted_senioridade.iterrows():
      
    # --- Parte 1: Anotar o Valor Bruto (para o primeiro ano, 2021) ---
    if row['ano'] == 2021:
      cor = "#202020" # Cinza escuro, cor neutra
      texto = f"R$ {row['salario_medio']:,.0f}" # Formato: "R$ 3.876"
      deslocamento_vertical = 15 # Coloca um pouco abaixo do ponto
      fontsize = 8
      fontweight = '500'
    
    # --- Parte 2: Anotar a Variação Percentual (para os outros anos) ---
    elif pd.notna(row['variacao_pct']) and row['variacao_pct'] != 0:
      variacao = row['variacao_pct']
      cor = 'green' if variacao > 0 else 'red'
      seta = '↑' if variacao > 0 else '↓'
      texto = f"{seta} {variacao:+.2%}" # Formato: "+5.2%" ou "-1.8%"
      fontsize = 9
      fontweight = '500'
  
    # --- Parte 3: Pular (se for NaN e não for 2021) ---
    else:
      continue

    # Adiciona a anotação ao gráfico
    ax_senioridade.annotate(
      texto, 
      (row['ano'], row['salario_medio']), #posição dos marcadores
      textcoords="offset points", 
      xytext=(0, 10), #deslocamento dos marcadores
      ha='center', #onde vao ficar
      fontsize=fontsize,
      color=cor,
      fontweight=fontweight
    )
  # --- Fim do Loop de Anotação ---

  # --- 3. Customização (Princípios de Visualização) ---
  ax_senioridade.set_title('Evolução do Salário MÉDIO por Senioridade (2021-2024)', fontsize=16, pad=20)
  ax_senioridade.set_xlabel('Ano', fontsize=12)
  ax_senioridade.set_ylabel("") # Rótulo do eixo Y re-adicionado
  ax_senioridade.grid(axis='y', linestyle='--', alpha=0.4)
  sns.despine(ax=ax_senioridade, left=True, bottom=True)
  
  try:
    from matplotlib.ticker import FuncFormatter
    ax_senioridade.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'R$ {x:,.0f}'))
  except ImportError:
    st.warning("Matplotlib ticker não encontrado.")

  ax_senioridade.set_xticks([2021, 2022, 2023, 2024])
  ax_senioridade.legend(title='Senioridade', bbox_to_anchor=(1.05, 1), loc='upper left')
  plt.tight_layout()

  # --- 4. Exibição no Streamlit ---  
  st.pyplot(fig_senioridade, use_container_width=True)
  plt.close(fig_senioridade) 

  # --- 5. Storytelling ---
  st.markdown("""
  **Insights da Análise:**
  * **Crescimento Consistente:** Todos os níveis de senioridade apresentaram um aumento no salário médio de 2021 para 2024.
  * **Salto Sênior:** O salário médio para Sênior foi o que mais cresceu em termos absolutos, ultrapassando R$ 14.500 em 2024.
  * **"Vale do Pleno":** Curiosamente, o salário médio para o nível Pleno teve uma leve queda em 2023 antes de se recuperar em 2024, indicando uma possível estabilização ou mudança no perfil dos respondentes desse nível.
  """)

  # --- 6. Expander com a Tabela (Sua solução perfeita para o "hover") ---
  with st.expander("Ver dados da tabela (Salário Médio por Senioridade)"):
    tabela_para_exibir = df_evol_salario_senioridade.set_index('ano').style.format("R$ {:,.2f}")
    st.dataframe(tabela_para_exibir, use_container_width=True)

else:
  st.warning("Arquivo '04_analise_evolucao_salario_senioridade.csv' não carregado. O gráfico não pode ser gerado.")

st.divider()













# ==============================================================================
st.subheader("Evolução do Salário Médio por Cargo")

if df_evol_salario_cargo is not None:
  # --- 1. Preparação dos Dados (Melt) ---
  if 'ano' in df_evol_salario_cargo.columns:
    df_evol_salario_cargo_plot = df_evol_salario_cargo.copy()

  df_melted_cargo = df_evol_salario_cargo_plot.melt(
    id_vars='ano',
    var_name='grupo_cargo',
    value_name='salario_medio'
  )
  
  df_melted_cargo['ano'] = df_melted_cargo['ano'].astype(int)
  
  # --- 2. Interatividade ---
  cargos_excluidos = ['Não se aplica/Outra área', 'Outros']
  lista_cargos = sorted(df_melted_cargo['grupo_cargo'].unique())
  cargos_default = [
    'Analista de Dados', 
    'Cientista de Dados', 
    'Engenheiro de Dados', 
    'Analista de BI'
  ]
  
  st.markdown("**Selecione os cargos para comparar:**")
  
  cargos_selecionados = st.multiselect(
      label="Cargos", 
      options=[c for c in lista_cargos if c not in cargos_excluidos],
      default=cargos_default,
      label_visibility="collapsed"
  )
  
  # --- 3. Filtragem dos Dados ---
  if cargos_selecionados:
    df_plotar_cargos = df_melted_cargo[df_melted_cargo['grupo_cargo'].isin(cargos_selecionados)]
    
    # --- 🆕 NOVO: Ordenar cargos por salário em 2024 (decrescente) ---
    # Pega os salários de 2024 para cada cargo
    salarios_2024 = df_plotar_cargos[df_plotar_cargos['ano'] == 2024].set_index('grupo_cargo')['salario_medio']
    
    # Ordena os cargos do MAIOR para o MENOR salário
    ordem_decrescente = salarios_2024.sort_values(ascending=False).index.tolist()
    
    # --- 4. Criação do Gráfico ---
    fig_cargo, ax_cargo = plt.subplots(figsize=(10, 4.5))
    
    sns.lineplot(
      data=df_plotar_cargos,
      x='ano',
      y='salario_medio',
      hue='grupo_cargo',
      style='grupo_cargo',
      markers=True,
      markersize=8,
      linewidth=2,
      ax=ax_cargo,
      dashes=False,
      hue_order=ordem_decrescente  # 🆕 Aplica a ordem decrescente
    )
    
    # --- 5. Customização ---
    ax_cargo.set_title(f'({len(cargos_selecionados)} cargos selecionados)', fontsize=12, pad=20)
    ax_cargo.set_xlabel('Ano', fontsize=12)
    ax_cargo.set_ylabel("")
    ax_cargo.grid(axis='y', linestyle='--', alpha=0.4)
    sns.despine(ax=ax_cargo, left=True, bottom=True)
    
    try:
      from matplotlib.ticker import FuncFormatter
      ax_cargo.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'R$ {x:,.0f}'))
    except ImportError:
      st.warning("Matplotlib ticker não encontrado.")

    ax_cargo.set_xticks([2021, 2022, 2023, 2024])
    
    # 🆕 Legenda já ordenada automaticamente pelo hue_order
    ax_cargo.legend(
      title='Cargo',
      bbox_to_anchor=(1.05, 1), 
      loc='upper left'
      )
    
    plt.tight_layout()
    
    # --- 6. Exibição ---
    st.pyplot(fig_cargo, use_container_width=True)
    plt.close(fig_cargo)

    # --- 7. Tabela de Dados (Expander) ---
    with st.expander("Ver dados da tabela (Salário Médio por Cargo)"):
      # Filtra a tabela original para mostrar apenas os cargos selecionados
      tabela_cargos_filtrada = df_evol_salario_cargo[cargos_selecionados].style.format("R$ {:,.2f}")
      st.dataframe(tabela_cargos_filtrada, use_container_width=True)

  else:
    st.warning("Por favor, selecione pelo menos um cargo para exibir o gráfico.")

else:
  st.warning("Arquivo '04_analise_evolucao_salario_cargo.csv' não carregado.")

st.divider()








# ==============================================================================
# SEÇÃO 2: TENDÊNCIAS DO MERCADO DE TRABALHO
# ==============================================================================
st.header("🏢 Tendências do Mercado de Trabalho")
st.markdown("Como a forma de trabalhar e as tecnologias mais populares evoluíram.")

st.subheader("Evolução dos Modelos de Trabalho (2021-2024)")

if df_modelo_trabalho_pct is not None:
    # --- 1. Preparação dos Dados ---
    if 'ano' in df_modelo_trabalho_pct.columns:
        df_modelo_plot = df_modelo_trabalho_pct.copy()
    else:
        df_modelo_plot = df_modelo_trabalho_pct.reset_index()

    # Formatar para porcentagem decimal (0.0 a 1.0)
    colunas_modelo = [col for col in df_modelo_plot.columns if col != 'ano']
    df_modelo_plot[colunas_modelo] = df_modelo_plot[colunas_modelo] / 100.0
    
    df_modelo_plot = df_modelo_plot.set_index('ano')

    # 🆕 ETAPA DE PREPARAÇÃO CORRIGIDA: Não removemos mais 'Não informado'
    df_plotar_modelos = df_modelo_plot.copy()
    
    # 🆕 ORDEM DA PILHA MANUAL: Definimos a ordem exata da pilha, de baixo para cima
    # Isso nos dá controle total e corrige o problema da legenda.
    ordem_stack = [
        'Remoto', 
        'Híbrido Flexível', 
        'Híbrido Fixo', 
        'Presencial',
        'Não informado' # Colocamos por último, para que apareça no topo
    ]
    
    # Garantir que usamos apenas colunas que existem no DataFrame
    ordem_stack = [col for col in ordem_stack if col in df_plotar_modelos.columns]
    
    # Pega os dados de cada coluna para o stackplot
    dados_stack = [df_plotar_modelos[col] for col in ordem_stack]
    labels_stack = [col.replace('_', ' ') for col in ordem_stack]
    
    # Cores intuitivas (deve incluir 'Não informado' agora)
    cores = {
        'Remoto': '#1f77b4',           # Azul
        'Híbrido Flexível': '#2ca02c', # Verde
        'Híbrido Fixo': '#ff7f0e',     # Laranja
        'Presencial': "#ce2a2a",       # Vermelho
        'Não informado': '#7f7f7f'    # Cinza
    }
    
    # Garante que só pegamos cores para as colunas que existem
    cores_stack = [cores[col] for col in ordem_stack]
    
    # --- 2. Criação do Gráfico (Matplotlib Stackplot) ---
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plotar área empilhada
    ax.stackplot(
        df_plotar_modelos.index,
        *dados_stack,
        labels=labels_stack,
        colors=cores_stack, # 🆕 Usa a lista de cores ordenada
        alpha=0.8
    )
    
    # ==============================================================
    # ADIÇÃO DOS MARCADORES (Agora funciona para todas as camadas)
    # ==============================================================
    
    # 1. Calcular a soma cumulativa dos dados
    df_cumulativo = df_plotar_modelos[ordem_stack].cumsum(axis=1) # 🆕 Usa a ordem manual
    
    # 2. Loop através de cada categoria (camada)
    for col in ordem_stack: # 🆕 Usa a ordem manual
        cor = cores[col] 
        
        ax.plot(
            df_cumulativo.index,
            df_cumulativo[col],
            marker='o',
            linestyle='none',
            markersize=5,
            markerfacecolor=cor,
            markeredgecolor='white',
            markeredgewidth=1.5
        )
    # ==============================================================
    # FIM DA ADIÇÃO DOS MARCADORES
    # ==============================================================

    # --- 3. Customização (Usabilidade) ---
    ax.set_title('Evolução da Distribuição dos Modelos de Trabalho (2021-2024)', fontsize=16, pad=20)
    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Proporção de Profissionais', fontsize=12)
    
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.set_xticks([2021, 2022, 2023, 2024])
    ax.set_ylim(0, 1) 
    
    # Legenda (com a sua inversão correta)
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles=handles[::-1], # 🆕 A sua inversão agora funciona perfeitamente
        labels=labels[::-1],   
        title='Modelo de Trabalho',
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        frameon=True
    )
    sns.despine(ax=ax)
    plt.tight_layout()
    
    # --- 4. Exibição ---
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
    
    # --- 5. Storytelling ---
    # (Seu markdown de insights continua perfeito)
    st.markdown(f"""
    **📈 Insights Principais:**
    **📉 Queda do Remoto**: Redução de 50.5% (2021) para 42.6% (2024)
  - **📈 Crescimento Híbrido**: Modelos híbridos saltaram de 26.5% para 35.4%
  - **🎯 Híbrido Flexível**: Manteve-se como segundo modelo mais popular
  - **🏢 Presencial Estável**: Manteve-se around 13-15%
  - **🎭 Mudança Cultural**: Transição clara do remoto para modelos híbridos.
  - **Crescimento Híbrido**: Os modelos híbridos (Fixo + Flexível) somados cresceram de 26.5% (2021) para 35.4% (2024).
    """)
    
    # --- 6. Tabela Interativa ---
    with st.expander("📊 Ver dados detalhados"):
        st.dataframe(
            df_modelo_trabalho_pct.set_index('ano').style.format("{:.2f}%"),
            use_container_width=True
        )

else:
    st.warning("Arquivo '18_analise_evolucao_modelo_trabalho_pct.csv' não carregado.")

st.divider()