import os
import openai
from dotenv import load_dotenv

load_dotenv()

MARITACA_MODEL = 'sabiazinho-4'
# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv("MARITACA_API_KEY"),
    base_url="https://chat.maritaca.ai/api")

def openai_enviar_prompt_extrair_conteudo_pub(texto, max_retries=3):
    system_prompt = """
Você é um assistente jurídico especializado em análise de publicações processuais.
Sua expertise está em identificar rapidamente o tipo de ato processual comunicado em publicações judiciais.
Você tem anos de experiência lendo diários oficiais e intimações, sendo capaz de reconhecer instantaneamente padrões textuais que indicam diferentes tipos de atos processuais.

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
PUBLICAÇÃO A CLASSIFICAR:
    """
    prompt = system_prompt + texto
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MARITACA_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": texto}
                ],
                max_tokens=10,
                temperature=0
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_EXTRAÇÃO"


def openai_enviar_prompt_especificar_pub_outros(texto, max_retries=3):
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
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MARITACA_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": texto}
                ],
                max_tokens=15,
                temperature=0
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_ESPECIFICAÇÃO"


def openai_enviar_prompt_especificar_conteudo_pub_defesa(texto, max_retries=3):
    system_prompt = """
Você é um processualista especializado em peças defensivas e recursais. Sua expertise está em identificar precisamente o tipo de manifestação processual para a qual uma parte está sendo intimada. Você tem profundo conhecimento dos diferentes tipos de defesas e recursos, especialmente embargos de declaração, recursos inominados e impugnações à contestação.
TAREFA DE CLASSIFICAÇÃO DE DEFESA
Analise a publicação judicial abaixo e identifique o tipo específico de defesa ou contrarrazões para o qual a parte está sendo intimada.
CATEGORIAS:

CONTRARRAZOES_EDCL: Intimações para apresentar contrarrazões a embargos de declaração (EDcl, ED, embargos declaratórios)
IMPUGCONT: Intimações para apresentar impugnação à contestação
CONTRARRAZOES_RI: Intimações para apresentar contrarrazões a recurso inominado (RI)
DEFESA_OUTROS: Qualquer outro tipo de defesa, contrarrazões ou manifestação defensiva não listada acima

REGRAS DE CLASSIFICAÇÃO:

Identifique EXATAMENTE o tipo de peça mencionada na intimação
Se a publicação mencionar MÚLTIPLOS tipos de defesa: classifique como DEFESA_OUTROS
Se houver AMBIGUIDADE sobre o tipo de defesa: classifique como DEFESA_OUTROS
Se não for uma das três categorias específicas: classifique como DEFESA_OUTROS

FORMATO DE RESPOSTA:

Responda APENAS com uma das quatro expressões: CONTRARRAZOES_EDCL, IMPUGCONT, CONTRARRAZOES_RI ou DEFESA_OUTROS
NÃO forneça explicações
NÃO use pontuação
NÃO adicione texto antes ou depois da classificação

PUBLICAÇÃO:
"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MARITACA_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": texto}
                ],
                max_tokens=15,
                temperature=0
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_ESPECIFICAÇÃO"


def openai_extrair_data_audiencia(texto, max_retries=3):
    system_prompt = """
Você é um assistente especializado em extração de informações temporais de documentos judiciais. Sua função é identificar com precisão datas e horários em publicações processuais, sendo capaz de distinguir entre diferentes referências temporais e focar especificamente na data e horário da audiência designada.
TAREFA DE EXTRAÇÃO DE DATA E HORÁRIO
Analise a publicação judicial abaixo e extraia a data e horário da audiência de conciliação designada.
REGRAS DE EXTRAÇÃO:

Se houver UMA única data/horário de audiência claramente identificável:

Responda no formato: DD-MM-YYYY HH-MM
Exemplo: 15-03-2024 14-30


Se houver MÚLTIPLAS datas de audiência mencionadas (remarcações, datas alternativas, etc.):

Responda apenas: MULTIPLAS_DATAS


Se NÃO for possível identificar uma data clara de audiência:

Responda apenas: DATA_NAO_ENCONTRADA



FORMATO OBRIGATÓRIO:

Data: DD-MM-YYYY (use zeros à esquerda quando necessário)
Horário: HH-MM (formato 24 horas, use zeros à esquerda)
Separe data e horário com UM espaço
Use hífen (-) como separador

ATENÇÃO:

Ignore datas que não sejam da audiência (prazo processual, data da publicação, etc.)
Foque APENAS na data e horário da audiência de conciliação
NÃO forneça explicações adicionais
NÃO use pontuação além dos hífens

PUBLICAÇÃO:
"""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=MARITACA_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": texto}
                ],
                max_tokens=15,
                temperature=0
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                print(f"Falha ao tentar extrair conteúdo da pub após {max_retries} tentativas.")
                return "ERRO_EXTRAÇÃO_DATA_AUD"