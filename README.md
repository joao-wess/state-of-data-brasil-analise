# 📊 Projeto: Análise State of Data

Este repositório contém a análise exploratória, tratamento e visualização dos datasets **State of Data (2021–2024)**.  
Nosso objetivo é aplicar boas práticas de análise de dados usando Python, seguindo a metodologia **CRISP-DM** para estruturar o trabalho de ponta a ponta.

---

## 🚀 Preparando o Ambiente

Antes de começar, todos devem configurar o ambiente da mesma forma.  
Estamos utilizando **Python 3.12.3**.

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/analise_state_of_data.git
cd analise_state_of_data
```

### 2. Criar e ativar ambiente virtual

- Criar o ambiente

```bash
python -m venv .venv
```

- Ativar o ambiente:
- Linux/MacOS

```bash
source .venv/bin/activate
```

- Windows (PowerShell)

```bash
.venv\Scripts\Activate
```

### 3. Instalar as dependências

pip install -r requirements.txt

## esse comando faz com que você tenha todas as dependências e rode sem problemas o projeto

### 4. Rodando o Dashboard Interativo

Com o ambiente ativado e as dependências instaladas, você pode iniciar o dashboard interativo.

O `dashboard.py` na raiz do projeto é o arquivo principal que executa o aplicativo Streamlit.

````bash
streamlit run dashboard.py

## 🗂 Estrutura do Projeto
```bash
analise_state_of_data/
├── data/
│ ├── raw/
│ │ ├── State_of_data_2021.csv
│ │ ├── State_of_data_2022.csv
│ │ ├── State_of_data_2023.csv
│ │ └── State_of_data_2024.csv
│ └── processed/
├── notebooks/
├── src/
│ └── utils/
├── dashboards/
├── .gitignore
└── README.md
````

### Explicação das pastas:

- **`data/raw/`**  
  Onde ficam os datasets originais, **sem nenhuma modificação**. Sempre preservamos a versão bruta para referência.

- **`data/processed/`**  
  Aqui serão salvos os datasets **limpos e tratados**, prontos para análise ou visualização.

- **`notebooks/`**  
  Espaço para exploração inicial com **Jupyter Notebooks**.  
  Cada integrante pode ter seu próprio notebook ou criar notebooks separados por etapas, exemplo:

  - `01_exploracao_inicial.ipynb`
  - `02_limpeza_2021.ipynb`
  - `03_merge_final.ipynb`

- **`src/`**  
  Pasta destinada ao **código fonte**.  
  Se criarmos funções reutilizáveis (ex.: padronizar colunas de salários, remover nulos, etc.), elas ficarão aqui.

- **`src/utils/`**  
  Nossa "caixa de ferramentas". Guardaremos funções auxiliares que podem ser reaproveitadas em vários notebooks.

- **`dashboards/`**  
  Local onde está salvo o dashboard inicial e legado - antes da implementação do streamlit com o pages.

- **`pages/`**
  Local onde ficam as páginas do streamlit com as outras análises

- **`dashboard.py`**
  Arquivo principal do streamlit para visualização da análise/

- **`README.md`**  
  Este arquivo. Serve como guia inicial do projeto: objetivo, instalação e instruções de uso.

- **`.gitignore`**  
  Lista arquivos/pastas que não devem ser versionados pelo Git (ex.: ambiente virtual, cache, arquivos temporários, datasets muito grandes).
