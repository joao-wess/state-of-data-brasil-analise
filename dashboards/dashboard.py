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
  
  # --- 2. 🆕 CÁLCULO DOS DELTAS ---
  df_melted_cargo.sort_values(['grupo_cargo', 'ano'], inplace=True)
  df_melted_cargo['variacao_pct'] = df_melted_cargo.groupby('grupo_cargo')['salario_medio'].pct_change()
  df_melted_cargo['variacao_absoluta'] = df_melted_cargo.groupby('grupo_cargo')['salario_medio'].diff()
  
  # --- 3. Interatividade ---
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
    label="Cargos para comparar",
    options=[c for c in lista_cargos if c not in cargos_excluidos],
    default=cargos_default,
    label_visibility="collapsed"
  )
  
  # --- 4. 🆕 SELETOR DE DELTAS ---
  if cargos_selecionados:
    st.markdown("**Mostrar deltas (variação anual) para:**")
    
    # Opções para mostrar deltas (apenas cargos selecionados)
    opcoes_deltas = ['Selecione Algum'] + cargos_selecionados
    
    cargo_com_delta = st.selectbox(
      label="Selecionar cargo para ver variações",
      options=opcoes_deltas,
      index=0,  # 'Selecione Algum' como padrão
      label_visibility="collapsed"
    )
  
  # --- 5. GRÁFICO PLOTLY (COM HOVER E DELTAS) ---
  if cargos_selecionados:
    df_plotar_cargos = df_melted_cargo[df_melted_cargo['grupo_cargo'].isin(cargos_selecionados)]
    
    # Ordenar pelo salário de 2024 (decrescente)
    salarios_2024 = df_plotar_cargos[df_plotar_cargos['ano'] == 2024].set_index('grupo_cargo')['salario_medio']
    ordem_decrescente = salarios_2024.sort_values(ascending=False).index.tolist()

    # Criar gráfico Plotly
    fig_cargo = px.line(
      df_plotar_cargos,
      x='ano',
      y='salario_medio',
      color='grupo_cargo',
      category_orders={'grupo_cargo': ordem_decrescente},
      markers=True,
      symbol='grupo_cargo',  # 🆕 Símbolos diferentes
      symbol_sequence=['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up'],  # 🆕 Variedade de símbolos
      title=f'Evolução do Salário Médio por Cargo ({len(cargos_selecionados)} cargos selecionados)',
      labels={
        'ano': 'Ano',
        'salario_medio': '',
        'grupo_cargo': 'Cargo'
      }
    )
    
    # --- 6. 🆕 ADICIONAR ANOTAÇÕES DE DELTA ---
    if cargo_com_delta != 'Selecione Algum':
      dados_delta = df_plotar_cargos[df_plotar_cargos['grupo_cargo'] == cargo_com_delta]
      
      for _, row in dados_delta.iterrows():
        # 🆕 PRIMEIRO ANO: MOSTRAR VALOR BRUTO
        if row['ano'] == 2021:
          texto = f"R$ {row['salario_medio']:,.0f}"
          cor = '#202020'  # Cinza escuro
          offset_y = 20
          tamanho_fonte = 15
        
        # 🆕 ANOS SEGUINTES: MOSTRAR VARIAÇÃO PERCENTUAL
        elif pd.notna(row['variacao_pct']) and row['variacao_pct'] != 0:
          # Calcular posição Y para a anotação
          y_pos = row['salario_medio']
          offset_y = 20 if row['variacao_pct'] > 0 else -20
          
          # Cor e símbolo baseado na direção
          cor = 'green' if row['variacao_pct'] > 0 else 'red'
          simbolo = '▲' if row['variacao_pct'] > 0 else '▼'
          
          texto = f"{simbolo} {abs(row['variacao_pct']):.1%}"
          tamanho_fonte = 15
      
        else:
          continue
        
        fig_cargo.add_annotation(
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
          borderpad=1.5
        )
    
    # --- 7. Customização do Hover ---
    fig_cargo.update_traces(
      hovertemplate="<br>".join([
        "<b>%{fullData.name}</b>",
        "Ano: %{x}",
        "Salário Médio: <b>R$ %{y:,.2f}</b>",
        "<extra></extra>"
      ]),
      marker=dict(size=11),
      line=dict(width=3.5)
    )
    
    # --- 8. Customização do Layout ---
    fig_cargo.update_layout(
      height=600,
      showlegend=True,
      legend=dict(
        title='Cargo',
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
        # 🆕 FORTALECER EIXO X
        title_font=dict(size=20, color='black', weight='bold'),
        tickfont=dict(size=20, color='black', weight='bold'),
        linecolor='black',
        linewidth=2
      ),
      yaxis=dict(
        tickprefix='R$ ',
        gridcolor='lightgray',
        gridwidth=1,
        tickformat=',.0f',
        # 🆕 FORTALECER EIXO Y
        tickfont=dict(size=20, color='black', weight='bold'),
      ),
      plot_bgcolor='white',
      paper_bgcolor='white',
      font=dict(color='black')
    )
    
    # --- 9. 🆕 LEGENDA INFORMATIVA ---
    if cargo_com_delta != 'Selecione Algum':
      st.info(f"📈 **Mostrando variações anuais para: {cargo_com_delta}** (▲ aumento, ▼ redução)")
  
    # Exibir gráfico Plotly
    st.plotly_chart(fig_cargo, use_container_width=True)
    
    # --- 10. Tabela de Dados (Expander) ---
    with st.expander("📋 Ver dados da tabela (Salário Médio por Cargo)"):
      tabela_cargos_filtrada = df_plotar_cargos.pivot(
        index='ano', 
        columns='grupo_cargo', 
        values='salario_medio'
      )[cargos_selecionados]
      
      # 🆕 Adicionar coluna de delta se um cargo estiver selecionado
      if cargo_com_delta != 'Selecione Algum':
        dados_delta_tabela = df_plotar_cargos[df_plotar_cargos['grupo_cargo'] == cargo_com_delta][['ano', 'variacao_pct']]
        tabela_cargos_filtrada[f'Delta {cargo_com_delta}'] = dados_delta_tabela.set_index('ano')['variacao_pct']
      
      st.dataframe(tabela_cargos_filtrada.style.format("R$ {:,.2f}"), use_container_width=True)

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







# ==============================================================================
# SEÇÃO 3: TECNOLOGIAS EM ALTA
# ==============================================================================
# --- Gráfico 3.1: Popularidade das Linguagens de Programação --
st.subheader("A popularidade das principais linguagens")

if df_pop_linguagens_pct is not None:
  # --- 1. Preparação e Consolidação dos Dados ---
  
  if 'ano' not in df_pop_linguagens_pct.columns:
    df_lang_plot = df_pop_linguagens_pct.reset_index()
  else:
    df_lang_plot = df_pop_linguagens_pct.copy()

  # Consolidar as colunas "Nenhuma"
  cols_nenhuma_lang = [
    'usa_linguagem_nenhuma', 
    'usa_linguagem_não_utilizo_linguagem_de_programação_no_trabalho', 
    'usa_linguagem_não_utilizo_nenhuma_das_linguagens_listadas'
  ]
  cols_nenhuma_existentes = [col for col in cols_nenhuma_lang if col in df_lang_plot.columns]
  df_lang_plot['Nenhuma'] = df_lang_plot[cols_nenhuma_existentes].sum(axis=1)
  df_lang_plot = df_lang_plot.drop(columns=cols_nenhuma_existentes)
  
  # --- 2. Agrupar a "Longa Cauda" ---
  linguagens_principais = [
    'ano',
    'usa_linguagem_sql',
    'usa_linguagem_python',
    'usa_linguagem_javascript',
    'usa_linguagem_java',
    'Nenhuma'
  ]
  
  cols_outras = [
    col for col in df_lang_plot.columns if col not in linguagens_principais
  ]
  
  df_lang_plot['Outras Linguagens'] = df_lang_plot[cols_outras].sum(axis=1)
  df_lang_final_plot = df_lang_plot[linguagens_principais + ['Outras Linguagens']]

  # --- 3. Preparação para Plotagem (Melt) ---
  df_melted_lang = df_lang_final_plot.melt(
    id_vars='ano',
    var_name='linguagem_coluna',
    value_name='popularidade_pct'
  )
  
  # Limpar os nomes das linguagens para exibição
  df_melted_lang['Linguagem'] = df_melted_lang['linguagem_coluna'].str.replace('usa_linguagem_', '').str.replace('_', ' ').str.title()
  df_melted_lang['Linguagem'] = df_melted_lang['Linguagem'].replace(
    {
    'C C++ C#': 'C/C++/C#',
    'Net': '.NET',
    'Sas Stata':'SAS/Stata',
    'Visual Basic Vba': 'VBA',
    'Sql': 'SQL',
    'Python': 'Python',
    'R': 'R',
    'Nenhuma': 'Nenhuma',
    'Outras Linguagens': 'Outras Linguagens'
  })
  
  # --- 4. 🆕 CÁLCULO DOS DELTAS ---
  df_melted_lang.sort_values(['Linguagem', 'ano'], inplace=True)
  df_melted_lang['delta_pct'] = df_melted_lang.groupby('Linguagem')['popularidade_pct'].diff()
  
  # --- 5. Interatividade ---
  lista_linguagens = sorted(df_melted_lang['Linguagem'].unique())
  linguagens_default = ['SQL', 'Python', 'Outras Linguagens']
  
  st.markdown("**Selecione as linguagens para comparar:**")
  linguagens_selecionadas = st.multiselect(
    label="Linguagens para comparar",
    options=lista_linguagens,
    default=linguagens_default,
    label_visibility="collapsed"
  )

  # --- 6. 🆕 SELETOR DE DELTAS ---
  if linguagens_selecionadas:
    st.markdown("**Mostrar deltas (variação anual) para:**")
    
    # Opções para mostrar deltas (apenas linguagens selecionadas)
    opcoes_deltas = ['Selecione Alguma'] + linguagens_selecionadas
    
    linguagem_com_delta = st.selectbox(
      label="Selecionar linguagem para ver variações",
      options=opcoes_deltas,
      index=0,  # 'Nenhuma' como padrão
      label_visibility="collapsed"
    )
  
  # --- 7. GRÁFICO PLOTLY (COM HOVER E DELTAS) ---
  if linguagens_selecionadas:
    df_plotar_linguagens = df_melted_lang[df_melted_lang['Linguagem'].isin(linguagens_selecionadas)]
    
    # Ordenar pela popularidade de 2024 para legenda
    pop_2024 = df_plotar_linguagens[df_plotar_linguagens['ano'] == 2024]
    ordem_legenda_lang = pop_2024.sort_values(by='popularidade_pct', ascending=False)['Linguagem'].tolist()

    # Criar gráfico Plotly
    fig_lang = px.line(
      df_plotar_linguagens,
      x='ano',
      y='popularidade_pct',
      color='Linguagem',
      category_orders={'Linguagem': ordem_legenda_lang},
      markers=True,
      title=f'Popularidade das Linguagens Selecionadas ({len(linguagens_selecionadas)} categorias)',
      labels={
        'ano': 'Ano',
        'popularidade_pct': '',
        'Linguagem': 'Linguagem de Programação'
      }
    )
    
    # --- 8. 🆕 ADICIONAR ANOTAÇÕES DE DELTA ---
    # --- 8. 🆕 ADICIONAR ANOTAÇÕES DE DELTA ---
    if linguagem_com_delta != 'Selecione Alguma':
      dados_delta = df_plotar_linguagens[df_plotar_linguagens['Linguagem'] == linguagem_com_delta]
      
      for _, row in dados_delta.iterrows():
        # 🆕 PRIMEIRO ANO: MOSTRAR VALOR BRUTO
        if row['ano'] == 2021:
          texto = f"{row['popularidade_pct']:.1f}%"
          cor = '#202020'  # Cinza escuro
          offset_y = 20
          tamanho_fonte = 15
          y_pos = row['popularidade_pct']  # 🆕 DEFINIR y_pos AQUI TAMBÉM
        
        # 🆕 ANOS SEGUINTES: MOSTRAR VARIAÇÃO PERCENTUAL
        elif pd.notna(row['delta_pct']) and row['delta_pct'] != 0:
          # Calcular posição Y para a anotação (acima ou abaixo da linha)
          y_pos = row['popularidade_pct']  # 🆕 DEFINIR y_pos AQUI TAMBÉM
          offset_y = 20 if row['delta_pct'] > 0 else -20
          
          # Cor e símbolo baseado na direção
          cor = 'green' if row['delta_pct'] > 0 else 'red'
          simbolo = '▲' if row['delta_pct'] > 0 else '▼'
          
          texto = f"{simbolo} {abs(row['delta_pct']):.2f}%"
          tamanho_fonte = 15
        
        else:
          continue
        
        fig_lang.add_annotation(
          x=row['ano'],
          y=y_pos,  # 🆕 AGORA y_pos ESTÁ SEMPRE DEFINIDO
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
    
    # --- 9. Customização do Hover ---
    fig_lang.update_traces(
      hovertemplate="<br>".join([
        "<b>%{fullData.name}</b>",
        "Ano: %{x}",
        "Popularidade: <b>%{y:.2f}%</b>",
        "<extra></extra>"
      ]),
      marker=dict(size=11),
      line=dict(width=3.5)
    )
    
    # --- 10. Customização do Layout ---
    fig_lang.update_layout(
      height=600,
      showlegend=True,
      legend=dict(
        title='Linguagem',
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
        title_font=dict(size=20, color='black', weight='bold'),  # Título mais forte
        tickfont=dict(size=20, color='black', weight='bold'),    # Números mais fortes
        linecolor='black',                                       # Linha do eixo
        linewidth=1                                              # Espessura da linha

      ),
      yaxis=dict(
        ticksuffix='%',
        gridcolor='lightgray',
        gridwidth=1,
        tickfont=dict(size=20, color='black', weight='bold'),    # Números mais fortes
      ),
      plot_bgcolor='white',
      paper_bgcolor='white',
      font=dict(color='black')
    )
    
    # --- 11. 🆕 LEGENDA INFORMATIVA ---
    if linguagem_com_delta != 'Selecione Alguma':
      st.info(f"📈 **Mostrando variações anuais para: {linguagem_com_delta}** (▲ aumento, ▼ redução)")
    
    # Exibir gráfico Plotly
    st.plotly_chart(fig_lang, use_container_width=True)
    
    # --- 12. Tabela de Dados (Expander) ---
    with st.expander("Ver dados da tabela (% de Popularidade das Linguagens)"):
      tabela_linguagens_filtrada = df_plotar_linguagens.pivot(
        index='ano', 
        columns='Linguagem', 
        values='popularidade_pct'
      )[linguagens_selecionadas]

      # 🆕 Adicionar coluna de delta se uma linguagem estiver selecionada
      if linguagem_com_delta != 'Selecione Alguma':
        dados_delta_tabela = df_plotar_linguagens[df_plotar_linguagens['Linguagem'] == linguagem_com_delta][['ano', 'delta_pct']]
        tabela_linguagens_filtrada[f'Delta {linguagem_com_delta}'] = dados_delta_tabela.set_index('ano')['delta_pct']

      st.dataframe(tabela_linguagens_filtrada.style.format("{:.2f}%"), use_container_width=True)

  else:
    st.warning("Por favor, selecione pelo menos uma linguagem para exibir o gráfico.")

else:
  st.warning("Arquivo '08_analise_popularidade_linguagens_pct.csv' não carregado.")

st.divider()






# ==============================================================================
# Gráfico 3.2: Popularidade das Ferramentas de BI (com filtro em 2022)
# ==============================================================================
st.subheader("Popularidade das Ferramentas de BI (% de Uso)")

if df_pop_bi_pct is not None:
    # --- 1. Preparação e Tratamento de Anomalias ---
    if 'ano' not in df_pop_bi_pct.columns:
        df_bi_plot = df_pop_bi_pct.reset_index()
    else:
        df_bi_plot = df_pop_bi_pct.copy()

    # --- 💡 FILTRANDO O ANO DE 2022 ---
    df_bi_plot_filtrado = df_bi_plot[df_bi_plot['ano'] != 2022].copy()
    
    # Adicionamos uma nota de transparência para o usuário
    st.info("📊 **Nota**: Os dados de 2022 para esta análise não são comparáveis e, portanto, não são exibidos.")

    # --- 2. Preparação para Plotagem (Melt) ---
    df_melted_bi = df_bi_plot_filtrado.melt(
        id_vars='ano',
        var_name='ferramenta_bi',
        value_name='popularidade_pct'
    )
    
    # --- 3. Interatividade (Filtro Multiselect) ---
    lista_bi = sorted(df_melted_bi['ferramenta_bi'].unique())
    
    # Excluir categorias de "lixo" da seleção
    bi_excluidos = ['Nenhuma', 'Excel Gsheets', 'Codigo Python R', 'Ferramenta Propria']
    
    # 🆕 ORDENAR PELO USO EM 2024 (MAIOR → MENOR)
    pop_bi_2024_sorted = df_bi_plot_filtrado.set_index('ano').loc[2024].drop(bi_excluidos, errors='ignore').sort_values(ascending=False)
    
    bi_default = pop_bi_2024_sorted.head(4).index.tolist() # Sugerir o Top 4
    
    st.markdown("**Selecione as ferramentas de BI para comparar:**")
    bi_selecionadas = st.multiselect(
        label="Ferramentas de BI",
        options=[ferramenta for ferramenta in lista_bi if ferramenta not in bi_excluidos],
        default=bi_default,
        label_visibility="collapsed"
    )

    # --- 4. Filtragem e Plotagem (Gráfico de Barras Agrupadas) ---
    if bi_selecionadas:
        df_plotar_bi = df_melted_bi[df_melted_bi['ferramenta_bi'].isin(bi_selecionadas)]
        
        # 🆕 GARANTIR QUE SÓ TEM OS ANOS 2021, 2023, 2024
        df_plotar_bi = df_plotar_bi[df_plotar_bi['ano'].isin([2021, 2023, 2024])]
        
        # 🆕 CORREÇÃO: ORDENAR FERRAMENTAS POR POPULARIDADE MÉDIA (MAIOR → MENOR)
        # Calcular a média de popularidade de cada ferramenta em todos os anos
        popularidade_media = df_plotar_bi.groupby('ferramenta_bi')['popularidade_pct'].mean().sort_values(ascending=False)
        ordem_ferramentas = popularidade_media.index.tolist()
        
        # 🆕 REORDENAR O DATAFRAME PARA GARANTIR A ORDEM CORRETA
        df_plotar_bi['ferramenta_bi'] = pd.Categorical(
            df_plotar_bi['ferramenta_bi'], 
            categories=ordem_ferramentas, 
            ordered=True
        )
        df_plotar_bi = df_plotar_bi.sort_values(['ferramenta_bi', 'ano'])
        
        # Criar o gráfico de barras agrupadas
        fig_bi = px.bar(
            df_plotar_bi,
            x='ano',                 # Usar ano diretamente
            y='popularidade_pct',    # Eixo Y: Popularidade
            color='ferramenta_bi',   # Cor para cada ferramenta
            barmode='group',         # Modo "agrupado"
            category_orders={
                'ferramenta_bi': ordem_ferramentas,  # 🆕 ORDEM MAIOR → MENOR
                'ano': [2021, 2023, 2024]  # 🆕 ORDEM ESPECÍFICA DOS ANOS
            },
            title=f'Popularidade das Ferramentas de BI Selecionadas ({len(bi_selecionadas)} ferramentas)',
            labels={
                'ano': 'Ano',
                'popularidade_pct': '',
                'ferramenta_bi': 'Ferramenta de BI'
            }
        )
        
        # --- 5. Customização (Seguindo nosso padrão) ---
        fig_bi.update_layout(
            height=600,  # Altura padronizada
            showlegend=True,
            legend=dict(
                title='Ferramenta de BI',
                orientation='v',
                yanchor='top',
                y=1,
                xanchor='left',
                x=1.05,
                traceorder='normal'  # 🆕 GARANTIR ORDEM DA LEGENDA
            ),
            xaxis=dict(
                type='category',  # 🆕 TRATAR EIXO X COMO CATEGORIA (remove espaçamento)
                tickmode='array',
                tickvals=[2021, 2023, 2024],
                ticktext=['2021', '2023', '2024'],
                title_font=dict(size=20, color='black', weight='bold'),
                tickfont=dict(size=20, color='black', weight='bold'),
                linecolor='black',
                linewidth=2,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                ticksuffix='%',
                gridcolor='lightgray',
                gridwidth=1,
                tickfont=dict(size=20, color='black', weight='bold'),
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            # 🆕 REDUZIR ESPAÇAMENTO ENTRE BARRAS
            bargap=0.15,  # Espaço entre grupos de barras
            bargroupgap=0.1  # Espaço entre barras do mesmo grupo
        )
        
        # --- 6. Melhorar o hover ---
        fig_bi.update_traces(
            hovertemplate="<br>".join([
                "<b>%{fullData.name}</b>",
                "Ano: %{x}",
                "Popularidade: <b>%{y:.2f}%</b>",
                "<extra></extra>"
            ]),
            marker=dict(line=dict(width=1, color='white'))  # Borda branca nas barras
        )

        # --- 7. Exibição ---
        st.plotly_chart(fig_bi, use_container_width=True)
        
        # --- 8. Storytelling ---
        st.markdown("""
        **📈 Insights Principais:**
        - **🏆 Power BI Lidera**: Mantém-se como a ferramenta mais popular em todos os anos
        - **📊 Tableau Consistente**: Segunda posição com crescimento estável
        - **🚀 Looker Studio em Alta**: Crescimento significativo de 2021 para 2023
        - **🔄 Metabase Estável**: Manteve participação consistente no mercado
        - **📈 Outras Ferramentas**: Representam uma parcela significativa do mercado
        - **💡 Dica**: Clique nos itens da legenda para focar em ferramentas específicas
        """)
        
        # --- 9. Tabela de Dados (Expander) ---
        with st.expander("📋 Ver dados da tabela (% de Popularidade de Ferramentas de BI)"):
            # 🆕 ORDENAR TABELA PELA MÉDIA TAMBÉM
            tabela_bi_filtrada = df_plotar_bi.pivot(
                index='ano', 
                columns='ferramenta_bi', 
                values='popularidade_pct'
            )[ordem_ferramentas]  # 🆕 USAR A ORDEM DEFINIDA
            
            st.dataframe(tabela_bi_filtrada.style.format("{:.2f}%"), use_container_width=True)

    else:
        st.warning("Por favor, selecione pelo menos uma ferramenta de BI para exibir o gráfico.")

else:
    st.warning("Arquivo '08_analise_popularidade_bi_pct.csv' não carregado.")

st.divider()










# ==============================================================================
# Gráfico 3.3: Popularidade das Plataformas de Cloud (COM DELTAS INTERATIVOS)
# ==============================================================================
st.subheader("Popularidade das Plataformas de Cloud (% de Uso)")

if df_pop_cloud_pct is not None:
    # --- 1. Preparação e Tratamento de Anomalias ---
    if 'ano' not in df_pop_cloud_pct.columns:
        df_cloud_plot = df_pop_cloud_pct.reset_index()
    else:
        df_cloud_plot = df_pop_cloud_pct.copy()

    # --- 💡 FILTRANDO O ANO DE 2023 (Dados Nulos) 💡 ---
    df_cloud_plot_filtrado = df_cloud_plot[df_cloud_plot['ano'] != 2023].copy()
    
    st.info("📊 **Nota**: Os dados de 2023 para esta análise não estão disponíveis no mesmo formato e, portanto, não são exibidos.")

    # --- 2. Preparação para Plotagem (Melt) ---
    df_melted_cloud = df_cloud_plot_filtrado.melt(
        id_vars='ano',
        var_name='plataforma_cloud',
        value_name='popularidade_pct'
    )
    
    # --- 3. 🆕 CÁLCULO DOS DELTAS (Pontos Percentuais) ---
    df_melted_cloud.sort_values(['plataforma_cloud', 'ano'], inplace=True)
    # .diff() calcula a diferença absoluta (ex: 29.72 - 28.80 = 0.92 p.p.)
    df_melted_cloud['delta_pp'] = df_melted_cloud.groupby('plataforma_cloud')['popularidade_pct'].diff()
    
    # --- 4. Interatividade (Filtro Multiselect) ---
    lista_cloud = sorted(df_melted_cloud['plataforma_cloud'].unique())
    cloud_default = ['AWS', 'GCP', 'AZURE', 'ON PREMISE']
    
    st.markdown("**Selecione as plataformas para comparar:**")
    cloud_selecionadas = st.multiselect(
        label="Plataformas Cloud",
        options=lista_cloud,
        default=cloud_default,
        label_visibility="collapsed"
    )
    
    # --- 5. 🆕 SELETOR DE DELTAS ---
    if cloud_selecionadas:
      st.markdown("**Mostrar deltas (variação anual) para:**")
      opcoes_deltas_cloud = ['Selecione Alguma'] + cloud_selecionadas
      
      cloud_com_delta = st.selectbox(
        label="Selecionar plataforma para ver variações",
        options=opcoes_deltas_cloud,
        index=0,  # 'Selecione Alguma' como padrão
        label_visibility="collapsed",
        key='select_cloud_delta' # 🆕 Chave única para este selectbox
      )

    # --- 6. Filtragem e Plotagem (Gráfico de Linhas) ---
    if cloud_selecionadas:
        df_plotar_cloud = df_melted_cloud[df_melted_cloud['plataforma_cloud'].isin(cloud_selecionadas)]
        
        # Ordenar pela popularidade de 2024 para uma legenda mais limpa
        pop_2024 = df_plotar_cloud[df_plotar_cloud['ano'] == 2024]
        ordem_legenda_cloud = pop_2024.sort_values(by='popularidade_pct', ascending=False)['plataforma_cloud'].tolist()

        # Criar gráfico Plotly
        fig_cloud = px.line(
            df_plotar_cloud,
            x='ano',
            y='popularidade_pct',
            color='plataforma_cloud',
            category_orders={'plataforma_cloud': ordem_legenda_cloud},
            markers=True,
            title=f'Popularidade das Plataformas Cloud Selecionadas',
            labels={
                'ano': 'Ano',
                'popularidade_pct': '',
                'plataforma_cloud': 'Plataforma'
            }
        )
        
        # --- 7. 🆕 ADICIONAR ANOTAÇÕES DE DELTA ---
        if cloud_com_delta != 'Selecione Alguma':
          dados_delta_cloud = df_plotar_cloud[df_plotar_cloud['plataforma_cloud'] == cloud_com_delta]
          
          for _, row in dados_delta_cloud.iterrows():
            # PRIMEIRO ANO (2021): MOSTRAR VALOR BRUTO
            if row['ano'] == 2021:
              texto = f"{row['popularidade_pct']:.1f}%"
              cor = '#202020'  # Cinza escuro
              offset_y = 20
              tamanho_fonte = 14
            
            # ANOS SEGUINTES: MOSTRAR VARIAÇÃO EM PONTOS PERCENTUAIS (p.p.)
            elif pd.notna(row['delta_pp']) and row['delta_pp'] != 0:
              offset_y = 20 if row['delta_pp'] > 0 else -20
              cor = 'green' if row['delta_pp'] > 0 else 'red'
              simbolo = '▲' if row['delta_pp'] > 0 else '▼'
              texto = f"{simbolo} {abs(row['delta_pp']):.2f}%." # p.p. = pontos percentuais
              tamanho_fonte = 14
          
            else:
              continue
            
            fig_cloud.add_annotation(
              x=row['ano'],
              y=row['popularidade_pct'],
              text=texto,
              showarrow=False,
              yshift=offset_y,
              font=dict(color=cor, size=tamanho_fonte, weight='bold'),
              bgcolor='white',
              bordercolor=cor,
              borderwidth=1,
              borderpad=1.5
            )
        
        # --- 8. Customização (Plotly) ---
        fig_cloud.update_layout(
            height=500,
            showlegend=True,
            legend=dict(
                title='Plataforma',
                orientation='v',
                yanchor='top',
                y=1,
                xanchor='left',
                x=1.05
            ),
            xaxis=dict(
                tickmode='array',
                tickvals=[2021, 2022, 2024], # Anos que temos dados
                ticktext=['2021', '2022', '2024'],
                title_font=dict(size=18, color='black', weight='bold'),
                tickfont=dict(size=18, color='black', weight='bold'),
                linecolor='black',
                linewidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                ticksuffix='%',
                gridcolor='lightgray',
                gridwidth=1,
                tickfont=dict(size=18, color='black', weight='bold'),
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black')
        )

        # Atualizar traços e hover
        fig_cloud.update_traces(
            marker=dict(size=11),
            line=dict(width=3.5),
            hovertemplate="<br>".join([
                "<b>%{fullData.name}</b>",
                "Ano: %{x}",
                "Popularidade: <b>%{y:.2f}%</b>",
                "<extra></extra>"
            ])
        )
        
        # --- 9. 🆕 LEGENDA INFORMATIVA ---
        if cloud_com_delta != 'Selecione Alguma':
          st.info(f"📈 **Mostrando variações anuais para: {cloud_com_delta}** (▲ aumento, ▼ redução em %.)")
        
        # --- 10. Exibição ---
        st.plotly_chart(fig_cloud, use_container_width=True)
        
        # --- 11. Tabela de Dados (Expander) ---
        with st.expander("📋 Ver dados da tabela (% de Popularidade de Plataformas Cloud)"):
            tabela_cloud_filtrada = df_plotar_cloud.pivot(
                index='ano', 
                columns='plataforma_cloud', 
                values='popularidade_pct'
            )[cloud_selecionadas]
            
            # 🆕 Adicionar coluna de delta se uma plataforma estiver selecionada
            if cloud_com_delta != 'Selecione Alguma':
                dados_delta_tabela = df_plotar_cloud[df_plotar_cloud['plataforma_cloud'] == cloud_com_delta][['ano', 'delta_pp']]
                tabela_cloud_filtrada[f'Delta {cloud_com_delta} (p.p.)'] = dados_delta_tabela.set_index('ano')['delta_pp']
            
            st.dataframe(tabela_cloud_filtrada.style.format("{:.2f}%", na_rep="N/A"), use_container_width=True)

    else:
        st.warning("Por favor, selecione pelo menos uma plataforma para exibir o gráfico.")

else:
    st.warning("Arquivo '09_analise_popularidade_cloud_pct.csv' não carregado.")

st.divider()