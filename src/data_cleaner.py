import pandas as pd
import numpy as np
import re
from pathlib import Path

#funçao para o caminho
def caminho_para_dataset():
  """
  Calcula e retorna os caminhos para as pastas de dados raw e processed.
  Assume que o script está sendo executado a partir da pasta 'notebooks'.
  """
  BASE_DIR = Path.cwd().parent
  RAW_DATA_DIR = BASE_DIR / 'data' / 'raw'
  PROCESSED_DATA_DIR = BASE_DIR / 'data' / 'processed'

  return RAW_DATA_DIR, PROCESSED_DATA_DIR


def converter_faixa_salarial(faixa):
  """
  Converte uma faixa salarial em texto para um valor numérico (média da faixa).
  Função genérica para ser usada em todos os datasets anuais.
  """
  if pd.isna(faixa):
    return np.nan
  
  s = str(faixa).lower().replace('r$', '').replace('.', '').replace('/mês', '').strip()
  numeros = re.findall(r'[0-9]+', s)
  numeros = [int(n) for n in numeros]

  if len(numeros) == 2:
    return np.mean(numeros)
  elif len(numeros) ==1:
    return float(numeros[0])
  else: 
    return np.nan
  

def agrupar_cargo(cargo):
  #Recebe um cargo (string) e o classifica em um grupo principal.
  if pd.isna(cargo):
    return 'Não se aplica/Outra área' # Padrão para nulos
  
  cargo = cargo.lower()

  if 'analista de dados' in cargo or 'data analyst' in cargo:
    return 'Analista de Dados'
  if 'cientista de dados' in cargo or 'data scientist' in cargo:
    return 'Cientista de Dados'
  if 'engenheiro de dados' in cargo or 'data engineer' in cargo or 'arquiteto de dados' in cargo or 'data architect' in cargo or 'dba' in cargo or 'administrador de banco de dados' in cargo:
    return 'Engenheiro de Dados'
  if 'analista de bi' in cargo or 'bi analyst' in cargo:
    return 'Analista de BI'
  if 'analytics engineer' in cargo:
    return 'Engenheiro de Analytics'
  if 'machine learning' in cargo or 'ml engineer' in cargo:
    return 'Engenheiro de ML'
  if 'business analyst' in cargo or 'analista de negócios' in cargo:
    return 'Analista de Negócios'
  if 'product manager' in cargo or 'dpm' in cargo:
    return 'Gestão de Produto de Dados'
  else:
    return 'Outros'
  

def converter_experiencia(experiencia_texto):
  """
  Recebe um texto de experiência e o converte para um valor numérico.
  Pode precisar de ajustes se as categorias forem diferentes.
  """
  if pd.isna(experiencia_texto):
        return np.nan
  
  mapa_experiencia = {
    'Não tenho experiência na área de dados': 0,
    'Menos de 1 ano': 0.5,
    'de 1 a 2 anos': 1.5,
    'de 3 a 4 anos': 3.5,
    'de 4 a 6 anos': 5.0, #linha adicionada para o dataset 2023
    'de 5 a 6 anos': 5.5,
    'de 7 a 10 anos': 8.5,
    'Mais de 10 anos': 12.0
    }
  
  return mapa_experiencia.get(experiencia_texto, np.nan)