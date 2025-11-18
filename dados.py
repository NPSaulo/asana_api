from dotenv import load_dotenv
from datetime import datetime
import pandas as pd 
import os
import json

load_dotenv()

'''
Aqui é um script para ler a planilha local de processos e retornar num dicionário, junto com outras informações do escritório.

Por exemplo:

"responsabilidades": {
    "ALAN ALMEIDA SANTOS": {
      "areas_direito": [
        "consumidor"
      ],
      "tarefas": [
        "tratar de alvarás",
        "analisar decisões de tutela antecipada",
        "analisar sentenças",
        "lidar com qualquer publicação de sua área que não for responsabilidade de outro"
      ]
    },
    "SAULO NIEDERLE PEREIRA": {
      "areas_direito": [
        "servidor publico"
      ],
      "tarefas": [
        "lidar com toda e qualquer publicação"
      ]
    }
  }
'''

def formatar_numeroprocesso(numeroprocesso):
    # Formato: XXXXXXX-XX.XXXX.X.XX.XXXX
    return f"{numeroprocesso[:7]}-{numeroprocesso[7:9]}.{numeroprocesso[9:13]}.{numeroprocesso[13]}.{numeroprocesso[14:16]}.{numeroprocesso[16:]}"

colunas = ['data_protocolo', 'numero_cnj', 'natureza', 'cliente']
processos = pd.read_excel(os.getenv('PATH_PROCESSOS'), dtype={0: str}, usecols=colunas)
processos = processos.rename(columns={'numero_cnj':'numeroprocesso'})
print(processos.info())

with open('dados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

dados['processos'] = processos
dados['key'] = os.getenv('ASANA_KEY')