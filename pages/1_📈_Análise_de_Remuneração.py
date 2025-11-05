# dashboards_pages/1_📈_Análise_de_Remuneração.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

# --- 1. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Análise de Remuneração", layout="wide")
st.title("📈 Análise de Remuneração")
st.markdown("Vamos detalhar como os salários evoluíram e como eles se comparam entre diferentes grupos.")

# --- 2. CAMINHOS E FUNÇÃO DE CARREGAMENTO---
BASE_PATH = Path.cwd() #Sobe um nível para a raiz do projeto
DASHBOARD_DATA_DIR = BASE_PATH / 'notebook' / 'dashboard_data'

@st.cache_data 
def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Erro: Arquivo não encontrado em {file_path}")
        return None

# --- 3. CARREGAMENTO DOS DADOS (REPETIR) ---
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











# --- 4. CONTEÚDO DA PÁGINA ---
# --- Gráfico 1.1: Evolução por Cargo (Interativo) ---
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






# --- Gráfico 1.2: Nível de Ensino x Salário (Interativo) ---
st.subheader("O Nível de Ensino Impacta o Salário?")
st.markdown("Use os filtros para explorar o salário mediano por nível de ensino, filtrando por ano e senioridade.")

if df_salario_ensino_senioridade_stats is not None and df_salario_ensino_stats is not None:
    # --- 1. Preparação dos Dados ---
    df_ensino_plot_detalhado = df_salario_ensino_senioridade_stats.copy()
    df_ensino_plot_geral = df_salario_ensino_stats.copy()

    # --- 2. Interatividade (Filtros) ---
    col_filtro_ano, col_filtro_senioridade = st.columns(2)
    
    with col_filtro_ano:
        anos_disponiveis = sorted(df_ensino_plot_geral['ano'].unique(), reverse=True)
        ano_selecionado_ensino = st.selectbox(
            label="Selecione o Ano:",
            options=anos_disponiveis,
            index=0, 
            key='select_ano_ensino'
        )
        
    with col_filtro_senioridade:
        niveis_senioridade = sorted(df_ensino_plot_detalhado['nivel_hierarquico'].unique())
        nivel_selecionado_ensino = st.selectbox(
            label="Selecione a Senioridade:",
            options=['Todos'] + niveis_senioridade, 
            index=0,
            key='select_senioridade_ensino'
        )

    # --- 3. Filtragem dos Dados ---
    if nivel_selecionado_ensino == 'Todos':
        df_para_plotar = df_ensino_plot_geral[df_ensino_plot_geral['ano'] == ano_selecionado_ensino].copy()
        coluna_valor = 'salario_mediana'
        titulo_grafico = f"Salário Mediano Geral por Nível de Ensino ({ano_selecionado_ensino})"
    else:
        df_para_plotar = df_ensino_plot_detalhado[
            (df_ensino_plot_detalhado['ano'] == ano_selecionado_ensino) &
            (df_ensino_plot_detalhado['nivel_hierarquico'] == nivel_selecionado_ensino)
        ].copy()
        coluna_valor = 'salario_mediana'
        titulo_grafico = f"Salário Mediano por Nível de Ensino ({nivel_selecionado_ensino} - {ano_selecionado_ensino})"
        
    # --- 4. Ordenação (Princípio da Organização) ---
    ordem_ensino_cat = [
        'Não tenho graduação formal',
        'Estudante de Graduação',
        'Graduação/Bacharelado',
        'Pós-graduação',
        'Mestrado',
        'Doutorado ou Phd',
        'Prefiro não informar',
        'Não Informado'
    ]
    df_para_plotar['nivel_ensino_cat'] = df_para_plotar['nivel_ensino_cat'].replace('Doutorado', 'Doutorado ou Phd')
    df_para_plotar['nivel_ensino_cat'] = pd.Categorical(
        df_para_plotar['nivel_ensino_cat'],
        categories=[cat for cat in ordem_ensino_cat if cat in df_para_plotar['nivel_ensino_cat'].unique()],
        ordered=True
    )
    df_para_plotar = df_para_plotar.sort_values('nivel_ensino_cat')
    
    # --- 5. Criação do Gráfico (Gráfico de Barras) ---
    if not df_para_plotar.empty:
        fig_ensino = px.bar(
            df_para_plotar,
            x='nivel_ensino_cat',
            y=coluna_valor,
            title=titulo_grafico,
            labels={'nivel_ensino_cat': 'Nível de Ensino', coluna_valor: 'Salário Mediano (R$)'},
            text=coluna_valor,
            custom_data=['contagem'] # 💡 Coluna de contagem adicionada para o hover
        )
        
        # --- 6. Customização (Plotly) ---
        fig_ensino.update_layout(
            height=600, 
            xaxis_title=None,
            yaxis_title='',
            yaxis_ticksuffix=' ',
            yaxis_tickprefix='R$ ',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            xaxis=dict(linecolor='black', linewidth=1, tickfont=dict(size=13.5, color='black')),
            yaxis=dict(
                gridcolor='lightgray',
                tickfont=dict(size=16, color='black'),
            )
        )
        
        # 💡 Hover e Texto da Barra ATUALIZADOS
        fig_ensino.update_traces(
            texttemplate='R$ %{y:,.0f}', 
            textposition='outside',
            hovertemplate="<br>".join([
                "<b>%{x}</b>",
                "Salário Mediano: <b>R$ %{y:,.0f}</b>",
                "Contagem de Respondentes: <b>%{customdata[0]}</b>", # Mostra a contagem
                "<extra></extra>"
            ])
        )
        
        # --- 7. Exibição ---
        st.plotly_chart(fig_ensino, use_container_width=True) # Exibindo o gráfico
        
        # --- 8. 💡 NOVO STORYTELLING 💡 ---
        st.markdown(f"""
        **📈 Insights Principais (Filtros: {ano_selecionado_ensino}, {nivel_selecionado_ensino}):**

        1.  **Para Sênior, a Experiência Nivela o Jogo:**. A mediana salarial é de **R$ 14k** para Graduação, Pós-graduação, Mestrado e Doutorado. Isso sugere fortemente que, no nível Sênior, a **experiência e as entregas superam o peso da formação acadêmica adicional**.

        2.  **O Mestrado é o Grande Diferencial no Nível Pleno:**. O salário mediano salta de **R$ 7k** (Graduação/Pós) para **R$ 10k** (Mestrado/Doutorado). É aqui que o título de Mestre parece ter o maior impacto financeiro, criando um "degrau" salarial.

        3.  **Na Entrada (Júnior). A mediana é de **R$ 5k** para quase todos os níveis (Graduação, Pós, Mestrado e Doutorado). Isso indica que, na porta de entrada, o mercado nivela os salários e a capacidade de "começar" não é tão dependente da sua formação avançada.
        """)
        
        # --- 9. Tabela de Dados (Expander) ---
        with st.expander("📋 Ver dados detalhados da seleção"):
            st.dataframe(df_para_plotar.style.format({'salario_medio': "R$ {:,.2f}", 'salario_mediana': "R$ {:,.2f}"}), use_container_width=True)
    else:
        st.warning(f"Nenhum dado encontrado para os filtros selecionados.")

else:
    st.warning("Arquivos de análise de Nível de Ensino não carregados.")

st.divider()






# --- Gráfico 1.3: Pay Gap por Gênero (Interativo) ---
st.subheader("Comparativo Salarial: Masculino vs. Feminino")
st.markdown("Use os filtros para comparar o salário **médio** lado a lado por gênero, ano e senioridade.")

if df_salario_genero_senioridade_stats is not None:
    # --- 1. Preparação dos Dados ---
    df_genero_plot = df_salario_genero_senioridade_stats.copy()

    # --- 2. Interatividade (Filtros) ---
    col_filtro_ano_gen, col_filtro_senioridade_gen = st.columns(2)
    
    with col_filtro_ano_gen:
        anos_disponiveis_gen = sorted(df_genero_plot['ano'].unique(), reverse=True)
        ano_selecionado_gen = st.selectbox(
            label="Selecione o Ano:",
            options=anos_disponiveis_gen,
            index=0, 
            key='select_ano_genero'
        )
        
    with col_filtro_senioridade_gen:
        niveis_senioridade_gen = sorted(df_genero_plot['nivel_hierarquico'].unique())
        nivel_selecionado_gen = st.selectbox(
            label="Selecione a Senioridade:",
            options=niveis_senioridade_gen, 
            index=len(niveis_senioridade_gen)-1, # Padrão para "Sênior"
            key='select_senioridade_genero'
        )

    # --- 3. Filtragem dos Dados ---
    df_para_plotar_gen = df_genero_plot[
        (df_genero_plot['ano'] == ano_selecionado_gen) &
        (df_genero_plot['nivel_hierarquico'] == nivel_selecionado_gen)
    ].copy()
    
    df_para_plotar_gen = df_para_plotar_gen[df_para_plotar_gen['genero'].isin(['Masculino', 'Feminino'])]
        
    # --- 4. Criação do Gráfico (Gráfico de Barras) ---
    if not df_para_plotar_gen.empty:
        
        fig_genero = px.bar(
            df_para_plotar_gen,
            x='genero',
            y='salario_medio', # Usando a Média
            color='genero', 
            color_discrete_map={'Masculino': '#1f77b4', 'Feminino': '#ff7f0e'},
            title=f"Salário MÉDIO por Gênero ({nivel_selecionado_gen} - {ano_selecionado_gen})",
            labels={'genero': 'Gênero', 'salario_medio': 'Salário Médio (R$)'},
            text='salario_medio', 
            custom_data=['contagem', 'salario_mediana']
        )
        
        # --- 5. Customização (Plotly) ---
        fig_genero.update_layout(
            height=500,
            xaxis_title=None,
            yaxis_title='',
            yaxis_ticksuffix=' ',
            yaxis_tickprefix='R$ ',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            xaxis=dict(linecolor='black', linewidth=1, tickfont=dict(size=16, color='black', weight='bold')),
            yaxis=dict(gridcolor='lightgray', tickfont=dict(size=16, color='black')),
            showlegend=False 
        )
        
        fig_genero.update_traces(
            texttemplate='R$ %{y:,.0f}',
            textposition='outside',
            hovertemplate="<br>".join([
                "<b>%{x}</b>",
                "Salário Médio: <b>R$ %{y:,.0f}</b>",
                "Salário Mediano: <b>R$ %{customdata[1]:,.0f}</b>",
                "Contagem: <b>%{customdata[0]}</b>",
                "<extra></extra>"
            ])
        )
        
        # --- 6. Exibição ---
        st.plotly_chart(fig_genero, use_container_width=True)
        
        # --- 7. 💡 CÁLCULO DO PAY GAP (MÉDIA) COM LÓGICA DINÂMICA 💡 ---
        try:
            # 💡 CORREÇÃO: Usar .values[0] para pegar o valor pela posição, não pelo índice .get(0)
            media_m = df_para_plotar_gen[df_para_plotar_gen['genero'] == 'Masculino']['salario_medio'].values[0]
            media_f = df_para_plotar_gen[df_para_plotar_gen['genero'] == 'Feminino']['salario_medio'].values[0]
            
            if pd.notna(media_m) and pd.notna(media_f) and media_m > 0:
                # Calcula o gap (pode ser positivo ou negativo)
                gap_pct = ((media_m - media_f) / media_m) * 100
                
                # 💡 LÓGICA DINÂMICA PARA A MENSAGEM (como você sugeriu) 💡
                valor_abs_gap = abs(gap_pct)
                
                if gap_pct > 0.5: # Gap positivo (Homens ganham mais)
                    comparacao_texto = f"foi **{valor_abs_gap:.1f}% menor ↓** que a masculina."
                elif gap_pct < -0.5: # Gap negativo (Mulheres ganham mais)
                    comparacao_texto = f"foi **{valor_abs_gap:.1f}% maior ↑** que a masculina."
                else: # Gap próximo de zero
                    comparacao_texto = "foi **praticamente idêntico** ao masculino."
                
                st.info(f"💡 **Pay Gap:** Para **{nivel_selecionado_gen}** em **{ano_selecionado_gen}**, o salário médio feminino {comparacao_texto}")
            
            else:
                st.warning(f"Não foi possível calcular o Pay Gap para '{nivel_selecionado_gen} / {ano_selecionado_gen}' (dados ausentes).")
        
        except IndexError:
            # Este erro acontece se o filtro não retornar 'Masculino' ou 'Feminino'
            st.warning(f"Não foi possível calcular o Pay Gap para '{nivel_selecionado_gen} / {ano_selecionado_gen}' (dados ausentes para um dos gêneros).")
        except Exception as e:
            st.warning(f"Erro inesperado ao calcular o Pay Gap: {e}")

        # --- 8. Tabela de Dados (Expander) ---
        with st.expander("📋 Ver todos os dados de gênero para esta seleção"):
            st.dataframe(df_para_plotar_gen.style.format({'salario_medio': "R$ {:,.2f}", 'salario_mediana': "R$ {:,.2f}"}), use_container_width=True)
    
    else:
        st.warning(f"Nenhum dado encontrado para os filtros selecionados.")

else:
    st.warning("Arquivos de análise de Gênero não carregados.")

st.divider()