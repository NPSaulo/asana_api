import json, requests, random
from datetime import datetime



LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"  # Ajuste conforme endereço do seu servidor LMStudio


def construir_prompt_conteudo_pub(texto):
    system_prompt = """
Você é um assistente jurídico especializado em análise de publicações processuais. 
Sua expertise está em identificar rapidamente o tipo de ato processual comunicado em publicações judiciais. 
Você tem anos de experiência lendo diários oficiais e intimações, sendo capaz de reconhecer instantaneamente padrões textuais que indicam diferentes tipos de atos processuais.

TAREFA DE CLASSIFICAÇÃO DE PUBLICAÇÕES JUDICIAIS
Você deve classificar a publicação judicial fornecida em EXATAMENTE uma das três categorias abaixo:

PROMPT 1 - CLASSIFICAÇÃO INICIAL (ATUALIZADO)
Você é um assistente jurídico especializado em análise de publicações processuais. Sua expertise está em identificar rapidamente o tipo de ato processual comunicado em publicações judiciais. Você tem anos de experiência lendo diários oficiais e intimações, sendo capaz de reconhecer instantaneamente padrões textuais que indicam diferentes tipos de atos processuais.
TAREFA DE CLASSIFICAÇÃO DE PUBLICAÇÕES JUDICIAIS
Você deve classificar a publicação judicial fornecida em EXATAMENTE uma das categorias abaixo:
CATEGORIAS:

AUDIENCIA_CONCILIACAO: Publicações que tratam de marcação, designação ou convocação para audiência de conciliação
DEFESA_CONTRARRAZOES: Publicações que intimam para apresentação de defesa (contestação, resposta, impugnação) ou contrarrazões (resposta a recurso)
SENTENCA: Publicações que comunicam a prolação de sentença (decisão que encerra a fase de conhecimento do processo, com ou sem julgamento de mérito)
TUTELA_LIMINAR: Publicações sobre decisões de tutela antecipada, tutela de urgência, tutela cautelar, liminar ou qualquer medida urgente
HOMOLOGACAO_ACORDO: Publicações sobre homologação de acordo, transação, conciliação ou qualquer forma de composição entre as partes
OUTROS: Qualquer publicação que não se enquadre nas categorias anteriores

REGRAS OBRIGATÓRIAS:

Responda APENAS com uma das palavras: AUDIENCIA_CONCILIACAO, DEFESA_CONTRARRAZOES, SENTENCA, TUTELA_LIMINAR, HOMOLOGACAO_ACORDO ou OUTROS
NÃO forneça explicações
NÃO use pontuação
NÃO adicione texto antes ou depois da classificação

EXEMPLOS:
Entrada: "Ficam as partes intimadas para comparecerem à audiência de conciliação designada para o dia 15/03/2024 às 14h"
Saída: AUDIENCIA_CONCILIACAO
Entrada: "Intime-se o réu para apresentar contestação no prazo de 15 dias"
Saída: DEFESA_CONTRARRAZOES
Entrada: "Dê-se vista ao Ministério Público"
Saída: OUTROS
PUBLICAÇÃO A CLASSIFICAR:"""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": texto}
    ]


def llmstudio_enviar_prompt_extrair_conteudo_pub(texto, max_retries=3):
    prompt = construir_prompt_conteudo_pub(texto)
    # Parâmetros para a requisição ao LMStudio
    payload = {
        "messages": prompt,
        "temperature": 0,
        "max_tokens": 10,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }
    # Tenta fazer a requisição com retry em caso de falha
    for attempt in range(max_retries):
        try:
            response = requests.post(
                LMSTUDIO_API_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=30  # Timeout em segundos
            )

            response.raise_for_status()  # Levanta exceção para erros HTTP

            result = response.json()
            resposta_modelo = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip().upper()
            return resposta_modelo

        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_EXTRAÇÃO"

def construir_prompt_especificar_pub(texto):
    system_prompt = """
Você é um assistente jurídico especializado em análise de publicações processuais. 
Sua expertise está em identificar rapidamente o tipo de ato processual comunicado em publicações judiciais. 
Você tem anos de experiência lendo diários oficiais e intimações, sendo capaz de reconhecer instantaneamente padrões textuais que indicam diferentes tipos de atos processuais.

TAREFA DE CRIAÇÃO DE CATEGORIA PARA PUBLICAÇÃO JUDICIAL
Analise a publicação judicial abaixo e crie uma categoria que capture sua essência principal.
FORMATO DA CATEGORIA:

Use 1 a 3 palavras que resumam a ação/conteúdo principal
Separe palavras com underscore (_)
Use APENAS letras MAIÚSCULAS
Seja extremamente conciso e direto

EXEMPLOS DE CATEGORIAS:

TUTELA_ANTECIPADA
EMENDA_INICIAL
SENTENCA
CITACAO
VISTA_MP
JULGAMENTO_RECURSO
CUSTAS
ALVARA
PERICIA_DESIGNADA
JUNTADA_DOCUMENTOS
SUSPENSAO_PROCESSO
HOMOLOGACAO_ACORDO

REGRAS:

Responda APENAS com a categoria criada
NÃO forneça explicações
NÃO use pontuação
Foque na ação ou determinação principal da publicação

PUBLICAÇÃO:"""
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": texto}
    ]


def llmstudio_enviar_prompt_especificar_pub(texto, max_retries=3):
    prompt = construir_prompt_especificar_pub(texto)
    # Parâmetros para a requisição ao LMStudio
    payload = {
        "messages": prompt,
        "temperature": 0,
        "max_tokens": 15,
        "stream": False
    }

    headers = {
        "Content-Type": "application/json"
    }
    # Tenta fazer a requisição com retry em caso de falha
    for attempt in range(max_retries):
        try:
            response = requests.post(
                LMSTUDIO_API_URL,
                headers=headers,
                data=json.dumps(payload),
                timeout=30  # Timeout em segundos
            )

            response.raise_for_status()  # Levanta exceção para erros HTTP

            result = response.json()
            resposta_modelo = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip().upper()
            return resposta_modelo

        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_ESPECIFICAÇÃO"