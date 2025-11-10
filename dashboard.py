import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
from pathlib import Path

st.set_page_config(
  page_title="Dashboard State of Data Brasil",
  page_icon="📊",
  layout="wide"
)

# fonte das KPI's
st.markdown("""
<style>
[data-testid="stMetricLabel"] p {
  font-size: 18px !important;
}

[data-testid="stMetricValue"] {
  font-size: 36px !important;
  font-weight: 600 !important;
}
[data-testid="stMetricDelta"] {
  font-size: 22px !important;
  font-weight: 500 !important;
}
</style>
""" , unsafe_allow_html=True)

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

st.sidebar.markdown("Projeto de Análise de Dados desenvolvido por:")
st.sidebar.markdown("Os Batutinhas - Facimp Wyden")



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








# ==============================================================================
# SEÇÃO 1: ANÁLISE DE REMUNERAÇÃO
# ==============================================================================
st.header("📈 Análise de Remuneração")
st.markdown("Vamos detalhar como os salários evoluíram e como eles se comparam entre diferentes grupos.")

# --- Gráfico 1.1: Evolução por Senioridade (COM PLOTLY E ANOTAÇÕES) ---
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
  
  # --- 2. Cálculo da Mudança Percentual e Absoluta ---
  df_melted_senioridade.sort_values(by=['nivel_hierarquico', 'ano'], inplace=True)
  df_melted_senioridade['variacao_pct'] = df_melted_senioridade.groupby('nivel_hierarquico')['salario_medio'].pct_change()
  df_melted_senioridade['variacao_absoluta'] = df_melted_senioridade.groupby('nivel_hierarquico')['salario_medio'].diff()
  
  # Ordenar pela salário de 2024 (decrescente)
  salario_2024_senioridade = df_melted_senioridade[df_melted_senioridade['ano'] == 2024].set_index('nivel_hierarquico')['salario_medio']
  ordem_decrescente_senioridade = salario_2024_senioridade.sort_values(ascending=False).index.tolist()

  # --- 3. Criação do Gráfico Plotly ---
  fig_senioridade = px.line(
    df_melted_senioridade,
    x='ano',
    y='salario_medio',
    color='nivel_hierarquico',
    category_orders={'nivel_hierarquico': ordem_decrescente_senioridade},
    markers=True,
    symbol='nivel_hierarquico',
    title='Evolução do Salário Médio por Senioridade (2021-2024)',
    labels={
      'ano': 'Ano',
      'salario_medio': '',
      'nivel_hierarquico': 'Nível de Senioridade'
    }
  )
  
  # --- 4. 🆕 ADICIONAR ANOTAÇÕES AUTOMÁTICAS ---
  # Primeiro ano: valor bruto, anos seguintes: delta
  for _, row in df_melted_senioridade.iterrows():
    if row['ano'] == 2021:
      # Primeiro ano: mostrar valor bruto
      texto = f"R$ {row['salario_medio']:,.0f}"
      cor = '#202020'  # Cinza escuro
      offset_y = 20
      tamanho_fonte = 14
    elif pd.notna(row['variacao_pct']) and row['variacao_pct'] != 0:
      # Anos seguintes: mostrar variação percentual
      variacao = row['variacao_pct']
      cor = 'green' if variacao > 0 else 'red'
      simbolo = '▲' if variacao > 0 else '▼'
      texto = f"{simbolo} {abs(variacao):.1%}"
      offset_y = 20 if variacao > 0 else -20
      tamanho_fonte = 14
    else:
      continue
    
    fig_senioridade.add_annotation(
      x=row['ano'],
      y=row['salario_medio'],
      text=texto,
      showarrow=False,
      yshift=offset_y,
      font=dict(
          color=cor,
          size=tamanho_fonte,
          weight='bold'
      ),
      bgcolor='white',
      bordercolor=cor,
      borderwidth=1,
      borderpad=2
    )
  
  # --- 5. Customização do Hover (Valores Brutos) ---
  fig_senioridade.update_traces(
    hovertemplate="<br>".join([
      "<b>%{fullData.name}</b>",
      "Ano: %{x}",
      "Salário Médio: <b>R$ %{y:,.2f}</b>",
      "<extra></extra>"
    ]),
    marker=dict(size=11),
    line=dict(width=3.5)
  )
  
  # --- 6. Customização do Layout ---
  fig_senioridade.update_layout(
    height=600,
    showlegend=True,
    legend=dict(
      title='Senioridade',
      orientation='v',
      yanchor='top',
      y=1,
      xanchor='left',
      x=1.05
    ),
    xaxis=dict(
      tickmode='array',
      tickvals=[2021, 2022, 2023, 2024],
      ticktext=['2021', '2022', '2023', '2024'],
      gridcolor='lightgray',
      gridwidth=1,
      title_font=dict(size=20, color='black', weight='bold'),  # Título mais forte
      tickfont=dict(size=20, color='black', weight='bold'),    # Números mais fortes
      linecolor='black',                                       # Linha do eixo
      linewidth=1                                              # Espessura da linha
    ),
    yaxis=dict(
      tickprefix='R$ ',
      gridcolor='lightgray',
      gridwidth=1,
      tickformat=',.0f',
      tickfont=dict(size=20, color='black', weight='bold'),    # Números mais fortes
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black')
  )
  
  # --- 7. Exibição no Streamlit ---
  st.plotly_chart(fig_senioridade, use_container_width=True)
  
  # --- 8. Storytelling ---
  st.markdown("""
  **📊 Insights da Análise:**
  - **📈 Crescimento Consistente:** Todos os níveis de senioridade apresentaram aumento salarial de 2021 para 2024
  - **🚀 Salto Sênior:** Senior foi o que mais cresceu em valores absolutos, ultrapassando R$ 14.500 em 2024
  - **🔄 Vale do Pleno:** Leve queda em 2023 antes da recuperação em 2024, indicando possível estabilização
  - **💰 Diferença Hierárquica:** Gap salarial entre Pleno e Sênior é maior que entre Júnior e Pleno
  """)
  
  # --- 9. Expander com Tabela ---
  with st.expander("📋 Ver dados da tabela (Salário Médio por Senioridade)"):
    tabela_para_exibir = df_evol_salario_senioridade.set_index('ano').style.format("R$ {:,.2f}")
    st.dataframe(tabela_para_exibir, use_container_width=True)

else:
  st.warning("Arquivo '04_analise_evolucao_salario_senioridade.csv' não carregado.")

st.divider()








#segundo gráfico
st.header("🏢 Tendências do Mercado de Trabalho")
st.markdown("Como a forma de trabalhar e as tecnologias mais populares evoluíram.")

if df_modelo_trabalho_pct is not None:
    # --- 1. Preparação dos Dados ---
    if 'ano' in df_modelo_trabalho_pct.columns:
        df_modelo_plot = df_modelo_trabalho_pct.copy()
    else:
        df_modelo_plot = df_modelo_trabalho_pct.reset_index()

    # Formatar para porcentagem decimal (0.0 a 1.0)
    colunas_modelo = [col for col in df_modelo_plot.columns if col != 'ano']
    df_modelo_plot[colunas_modelo] = df_modelo_plot[colunas_modelo] / 100.0
    
    # --- 2. Preparação para Plotly (Melt) ---
    df_melted_modelos = df_modelo_plot.melt(
        id_vars='ano',
        var_name='modelo_trabalho',
        value_name='percentual'
    )
    
    # --- 3. GRÁFICO PLOTLY (ÁREA EMPILHADA COM HOVER) ---
    # 🆕 REMOVIDO O MULTISELECT - TODOS OS MODELOS SÃO MOSTRADOS
    
    # 🆕 ORDEM FIXA DO GRÁFICO (de cima para baixo - como aparece visualmente)
    ordem_fixa = [
        'Não informado',     # Topo (primeiro na legenda)
        'Presencial',        # Abaixo do Não informado
        'Híbrido Fixo',      # Abaixo do Presencial
        'Híbrido Flexível',  # Abaixo do Híbrido Fixo
        'Remoto'             # Base (último na legenda)
    ]
    
    # Cores intuitivas (mantendo as originais)
    cores = {
        'Remoto': '#1f77b4',           # Azul
        'Híbrido Flexível': '#2ca02c', # Verde
        'Híbrido Fixo': '#ff7f0e',     # Laranja
        'Presencial': "#ce2a2a",       # Vermelho
        'Não informado': '#7f7f7f'     # Cinza
    }

    # Criar gráfico de área empilhada
    fig_modelos = px.area(
        df_melted_modelos,  # 🆕 Usa todos os dados, sem filtro
        x='ano',
        y='percentual',
        color='modelo_trabalho',
        category_orders={'modelo_trabalho': ordem_fixa},  # 🆕 Ordem fixa
        color_discrete_map=cores,
        title='Evolução da Distribuição dos Modelos de Trabalho (2021-2024)',
        labels={
            'ano': 'Ano',
            'percentual': '',
            'modelo_trabalho': 'Modelo de Trabalho'
        }
    )
    
    # 🆕 ADICIONAR MARKERS VISÍVEIS E REDUZIR TRANSPARÊNCIA
    fig_modelos.update_traces(
        mode='lines+markers',  # 🆕 Adiciona marcadores às linhas
        marker=dict(size=11),   # 🆕 Tamanho dos marcadores
        line=dict(width=3.5),    # 🆕 Espessura das linhas
    )
    
    # --- 4. Customização do Hover ---
    fig_modelos.update_traces(
        hovertemplate="<br>".join([
            "<b>%{fullData.name}</b>",
            "Ano: %{x}",
            "Percentual: <b>%{y:.1%}</b>",
            "<extra></extra>"
        ])
    )
    
    # --- 5. Customização do Layout ---
    fig_modelos.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            title='Modelo de Trabalho',
            orientation='v',
            yanchor='top',
            y=1,
            xanchor='left',
            x=1.05,
            # 🆕 LEGENDA NA ORDEM INVERSA (para combinar com o gráfico)
            traceorder='reversed'  # Inverte a ordem da legenda
        ),
        xaxis=dict(
            tickmode='array',
            tickvals=[2021, 2022, 2023, 2024],
            ticktext=['2021', '2022', '2023', '2024'],
            title_font=dict(size=20, color='black', weight='bold'),
            tickfont=dict(size=20, color='black', weight='bold'),
            linecolor='black',
            linewidth=2
        ),
        yaxis=dict(
            tickformat='.0%',
            gridcolor='lightgray',
            gridwidth=1,
            tickfont=dict(size=20, color='black', weight='bold'),
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='black')
    )
    
    # Exibir gráfico Plotly
    st.plotly_chart(fig_modelos, use_container_width=True)
    
    # --- 6. Storytelling ---
    st.markdown("""
    **📈 Insights Principais:**
    - **📉 Queda do Remoto**: Redução de 50.5% (2021) para 42.6% (2024)
    - **📈 Crescimento Híbrido**: Modelos híbridos saltaram de 26.5% para 35.4%
    - **🎯 Híbrido Flexível**: Manteve-se como segundo modelo mais popular
    - **🏢 Presencial Estável**: Manteve-se around 13-15%
    - **🎭 Mudança Cultural**: Transição clara do remoto para modelos híbridos
    - **📊 Crescimento Híbrido**: Os modelos híbridos (Fixo + Flexível) somados cresceram de 26.5% (2021) para 35.4% (2024).
    
    **💡 Dica**: Clique nos itens da legenda para mostrar/ocultar categorias específicas.
    """)
    
    # --- 7. Tabela Interativa ---
    with st.expander("📊 Ver dados detalhados"):
        tabela_modelos = df_melted_modelos.pivot(
            index='ano', 
            columns='modelo_trabalho', 
            values='percentual'
        )
        
        st.dataframe(tabela_modelos.style.format("{:.2%}"), use_container_width=True)

else:
    st.warning("Arquivo '18_analise_evolucao_modelo_trabalho_pct.csv' não carregado.")

st.divider()