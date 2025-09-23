Claro! Aqui está a lista de perguntas e a seção de recomendações de análise formatada em Markdown.

# Análise do Mercado de Dados (2021-2024)

## Lista de Questões para Investigação

### Demografia e Experiência

1. Qual a distribuição de idade dos profissionais de dados (2021–2024)? Houve envelhecimento/juventude crescente?
2. Qual a taxa de transição de carreira (quantos entraram na área vindo de outras áreas)?
3. Tempo médio de busca por emprego em 2021–2024 (quem está procurando emprego — demora para conseguir)?

### Remuneração e Equidade

4. Evolução do salário médio entre 2021 e 2024 (por ano e por cargo)?
5. Existe diferença salarial por gênero (gender pay gap) no conjunto de respondentes?
6. Que faixas salariais são mais comuns por cargo (junior / pleno / sênior)?
7. Há diferenças regionais (por estado) em salário e nível de senioridade?

### Ferramentas e Tecnologias

8. Quais são as ferramentas mais usadas (Python, R, SQL, Power BI, Tableau, etc.) e como mudaram ao longo dos anos?
9. Como evoluiu a experiência com cloud (AWS/GCP/Azure) entre 2021 e 2024?
10. Existe correlação entre ferramentas de BI utilizadas e cargos (ex.: analistas usam mais Power BI)?
11. Quais as principais linguagens preferidas (Python vs R vs outras) e sua evolução?
12. Qual a proporção de pessoas usando AutoML / ferramentas low-code?
13. Como está a adoção de MLOps / produção de modelos ao longo dos anos?

### Formação e Habilidades

14. Qual a proporção de profissionais que estudam continuamente (cursos, bootcamps, estudos autodidatas)?
15. Quais níveis de formação (graduação, pós, mestrado, bootcamp) dominam a área e sua relação com salário?
16. Quais são as skills mais demandadas/possuídas (ML, estatística, engenharia de dados, Cloud)?
17. Top skills / tópicos em ascensão (ML/Cloud/ETL/BI) — tendências.

### Modelo de Trabalho e Satisfação

18. Qual a proporção de trabalho remoto / híbrido / presencial ao longo dos anos?
19. Qual o nível de satisfação com o trabalho e variação por ano?
20. Quais as principais dificuldades relatadas (reskilling, falta de oportunidade, viés, contratação)?
21. Há diferenças por gênero/raça/identidade no relato de experiências negativas (discriminação, processos seletivos)?

---

## Análises Recomendadas e Visualizações

### Escolha Recomendada 1: Evolução Salarial

- **Título:** Evolução do salário médio por ano e por cargo.
- **Visual:** Gráfico de linhas com filtro interativo por cargo e estado.
- **Métricas Principais:**
  - Salário médio e mediana.
  - Número de respondentes por ponto (para dar contexto ao tamanho da amostra).

### Escolha Recomendada 2: Popularidade de Ferramentas

- **Título:** Ferramentas mais utilizadas (Top N) por ano.
- **Visual:** Gráfico de barras agrupadas (grouped bar) por ferramenta e ano (ou barras empilhadas para mostrar a composição total).
- **Métrica:** Percentual de respondentes que usam cada ferramenta.

### Escolha Recomendada 3: Impacto da Formação

- **Título:** Distribuição por nível de formação e impacto no salário.
- **Visual:** Boxplot de salário por `education_level`.
- **Métrica:** Mediana e Intervalo Interquartil (IQR) para comparar a distribuição salarial.

### Escolha Recomendada 4: Gender Pay Gap

- **Título:** Diferença salarial por gênero (gender pay gap).
- **Visual:** Gráfico de barras (para média) lado a lado com boxplots (para distribuição). Pode incluir um KPI de diferença percentual.
- **Métrica:** Salário médio e distribuição (mediana, quartis) por gênero.

### Escolha Recomendada 5: Modelo de Trabalho

- **Título:** Proporção trabalho remoto/híbrido/presencial por ano.
- **Visual:** Gráfico de área empilhada (stacked area chart) ou série de gráficos de rosca (donut) por ano.
- **Métrica:** Percentual de respondentes em cada modalidade.

### Escolha Recomendada 6: Indicador de Mercado

- **Título:** Tempo médio para conseguir emprego.
- **Visual:** Histograma da distribuição do tempo de busca + KPI (média/mediana por ano).
- **Métrica:** Tempo médio/mediano de busca por vaga, indicando a saúde do mercado.

### Escolha Recomendada 7: Tendências de Habilidades

- **Título:** Top skills em ascensão (ML, Cloud, ETL, BI).
- **Visual:** Gráfico de linhas mostrando a variação do percentual de menção para cada skill ao longo dos anos.
- **Métrica:** Percentual de respondentes que citam cada skill/área por ano.
