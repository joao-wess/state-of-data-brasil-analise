# dashboards_pages/2_💻_Tendências_de_Tecnologias.py
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# --- 1. CONFIGURAÇÃO E CARREGAMENTO ---
st.set_page_config(page_title="Tendências de Tecnologias", layout="wide")
st.title("💻 Tendências de Tecnologias")
st.markdown("A popularidade das principais linguagens, ferramentas de BI e plataformas de Cloud.")

BASE_PATH = Path.cwd()
DASHBOARD_DATA_DIR = BASE_PATH / 'notebook' / 'dashboard_data'

@st.cache_data 
def load_data(file_path):
  try:
    return pd.read_csv(file_path)
  except FileNotFoundError:
    st.error(f"Erro: Arquivo não encontrado em {file_path}")
    return None

# (Copie e cole TODAS as suas linhas de load_data aqui novamente)
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





# --- 2. CONTEÚDO DA PÁGINA ---
# --- Gráfico 3.1: Popularidade das Linguagens de Programação --
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
    'usa_linguagem_java',
    'usa_linguagem_r',
    'usa_linguagem_matlab',
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
# Gráfico 3.2: Popularidade das Ferramentas de BI (VERSÃO HORIZONTAL CORRIGIDA)
# ==============================================================================
st.subheader("Popularidade das Ferramentas de BI (% de Uso)")

if df_pop_bi_pct is not None:
    # --- 1. Preparação e Tratamento de Anomalias ---
    if 'ano' not in df_pop_bi_pct.columns:
        df_bi_plot = df_pop_bi_pct.reset_index()
    else:
        df_bi_plot = df_pop_bi_pct.copy()

    df_bi_plot_filtrado = df_bi_plot[df_bi_plot['ano'] != 2022].copy()
    st.info("📊 **Nota**: Os dados de 2022 para esta análise não são comparáveis e, portanto, não são exibidos.")

    # --- 2. Preparação para Plotagem (Melt) ---
    df_melted_bi = df_bi_plot_filtrado.melt(
        id_vars='ano',
        var_name='ferramenta_bi',
        value_name='popularidade_pct'
    )
    
    # --- 3. Interatividade (Filtro Multiselect) ---
    lista_bi = sorted(df_melted_bi['ferramenta_bi'].unique())
    bi_excluidos = ['Nenhuma', 'Excel Gsheets', 'Codigo Python R', 'Ferramenta Propria', 'Sap', 'Alteryx', 'Superset', 'Amazon Quicksight', 'Qlik']
    
    pop_bi_2024_sorted = df_bi_plot_filtrado.set_index('ano').loc[2024].drop(bi_excluidos, errors='ignore').sort_values(ascending=False)
    bi_default = ['Powerbi', 'Tableau', 'Looker Studio']    

    st.markdown("**Selecione as ferramentas de BI para comparar:**")
    bi_selecionadas = st.multiselect(
        label="Ferramentas de BI",
        options=[ferramenta for ferramenta in lista_bi if ferramenta not in bi_excluidos],
        default=bi_default,
        label_visibility="collapsed"
    )

    # --- 4. Filtragem e Plotagem (Gráfico de Barras HORIZONTAL) ---
    if bi_selecionadas:
        df_plotar_bi = df_melted_bi[df_melted_bi['ferramenta_bi'].isin(bi_selecionadas)]
        df_plotar_bi = df_plotar_bi[df_plotar_bi['ano'].isin([2021, 2023, 2024])]
        
        # Ano como string para a cor
        df_plotar_bi['ano_str'] = df_plotar_bi['ano'].astype(str)

        # 💡 GRÁFICO INVERTIDO: Y é a categoria, X é o valor
        fig_bi = px.bar(
            df_plotar_bi,
            y='ferramenta_bi',       # 💡 Y = Categoria (Ferramenta)
            x='popularidade_pct',    # 💡 X = Valor (%)
            color='ano_str',         # Cor agrupa por Ano
            barmode='group',
            text='popularidade_pct', # Adiciona o texto
            title=f'Popularidade das Ferramentas de BI Selecionadas',
            labels={
                'ferramenta_bi': '', # Eixo Y não precisa de título
                'popularidade_pct': '% de Uso',
                'ano_str': 'Ano'
            },
            category_orders={'ano_str': ['2021', '2023', '2024']}
        )
        
        # --- 5. Customização (Foco na ordenação do Eixo Y) ---
        fig_bi.update_layout(
            height=600,
            showlegend=True,
            legend_title_text='Ano',
            # 💡 ORDENA O EIXO Y (ferramentas) pela popularidade total (decrescente, maior no topo)
            yaxis=dict(
                categoryorder='total ascending', 
                tickfont=dict(size=14, color='black') # 💡 Fonte do Eixo Y
            ), 
            xaxis=dict(
                ticksuffix='%', 
                gridcolor='lightgray',
                tickfont=dict(size=14, color='black', weight='bold') # 💡 Fonte do Eixo X
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='black'),
            bargap=0.15,
            bargroupgap=0.1,
            legend=dict(
                orientation='h', 
                yanchor='bottom',
                y=-0.3, 
                xanchor='center',
                x=0.5
            )
        )
        
        # --- 6. Melhorar o hover E o texto da barra 💡 ---
        fig_bi.update_traces(
            texttemplate='%{x:.1f}%', # 💡 Usa %{x} pois o valor está no eixo X
            textposition='outside',
            textfont_size=12, # 💡 Tamanho da fonte do texto
            hovertemplate="<br>".join([
                "<b>%{y}</b>", # 💡 Y é o nome da ferramenta
                "Ano: %{fullData.name}", # 💡 fullData.name é o Ano
                "Popularidade: <b>%{x:.2f}%</b>",
                "<extra></extra>"
            ]),
            marker=dict(line=dict(width=1, color='white'))
        )

        # --- 7. Exibição ---
        # 💡💡💡 A GRANDE CORREÇÃO (O Erro que você encontrou) 💡💡💡
        st.plotly_chart(fig_bi, use_container_width=True) # <-- CORRIGIDO para plotly_chart
        
        # --- 8. Storytelling (sem mudanças) ---
        st.markdown("""
        **📈 Insights Principais:**
        - **🏆 Power BI Lidera**: Mantém-se como a ferramenta mais popular em todos os anos
        - **📊 Tableau Consistente**: Segunda posição com crescimento estável
        - **🚀 Looker Studio em Alta**: Crescimento significativo de 2021 para 2023
        - **🔄 Metabase Estável**: Manteve participação consistente no mercado
        - **💡 Dica**: Clique nos itens da legenda para focar em ferramentas específicas
        """)
        
        # --- 9. Tabela de Dados (Expander) ---
        with st.expander("📋 Ver dados da tabela (% de Popularidade de Ferramentas de BI)"):
            tabela_bi_filtrada = df_plotar_bi.pivot(
                index='ano', 
                columns='ferramenta_bi', 
                values='popularidade_pct'
            )[bi_selecionadas]
            
            # Ordenar colunas da tabela
            media_para_ordenar_tabela = tabela_bi_filtrada.mean().sort_values(ascending=False).index
            tabela_bi_filtrada = tabela_bi_filtrada[media_para_ordenar_tabela]
            
            st.dataframe(tabela_bi_filtrada.style.format("{:.2f}%", na_rep="N/A"), use_container_width=True)

    else:
        st.warning("Por favor, selecione pelo menos uma ferramenta de BI para exibir o gráfico.")

else:
    st.warning("Arquivo '08_analise_popularidade_bi_pct.csv' não carregado.")

st.divider()








# --- Gráfico 2.3: Popularidade de Plataformas Cloud ---
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
            height=600,
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