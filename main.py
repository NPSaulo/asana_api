from funcoes import *
from comunicapje import capturar_pubs
from dados import dados
import asana
from asana.rest import ApiException
from pprint import pprint
from datetime import datetime, timedelta

def main():
    #1 EXTRAINDO TODAS AS PUBS DOS QUATRO ADVOGADOS
    set_id_pubs = set()
    num_pubs = 0
    pubs = []
    for adv in dados['advogados']:
        num_pubs_adv, pubs_adv = capturar_pubs(nome_adv=adv, data_inicio=hoje_str, data_fim=hoje_str, set_id_pubs=set_id_pubs)
        num_pubs += num_pubs_adv
        pubs.extend(pubs_adv)
    #2 PEGANDO OS PROCESSOS DO ESCRITÓRIO
    '''
    Faço essa separação pois há processos em nome dos sócios que não são deste escritório
    '''
    lista_processos = dados['processos'].iloc[:,1].tolist()
    #print(lista_processos)
    cont_pubs = 0
    for pub in pubs:
        print(pub['numeroprocessocommascara'])
        #3 FILTRANDO APENAS AS PUBS DE PROCESSOS DO ESCRITÓRIO
        #print(pub)
        if pub['numeroprocessocommascara'] in lista_processos:
            print(f"Localizada publicação do processo {pub['numeroprocessocommascara']}")
            cont_pubs += 1
            #4 DISTRIBUINDO PARA A EQUIPE
            area_processo = extrair_area_processo(dados, pub)
            #print(area_processo)
            if area_processo == 'SERVIDOR PUBLICO':
                responsavel = dados['membros']['Saulo Niederle']
                nome_tarefa = 'OUTROS'
                criar_tarefa_geral(nome_tarefa, pub, dados, responsavel)
            else:
                conteudo_pub = extrair_conteudo_pub(pub['texto'], cliente='ANTHROPIC')
                print(conteudo_pub)
                if conteudo_pub == 'OUTROS':
                    conteudo_pub = especificar_pub_outros(pub['texto'], cliente='ANTHROPIC')
                    print(conteudo_pub)
                    responsavel = dados['membros']['Alan Almeida']
                    criar_tarefa_geral(conteudo_pub, pub, dados, responsavel)
                elif conteudo_pub == 'AUDIENCIA_CONCILIACAO': #temporariamente desativado
                    #data_hora_audiencia = extrair_data_audiencia(pub['texto'], cliente='ANTHROPIC')
                    #print(data_hora_audiencia)
                    #criar_tarefa_audiencia_conciliacao(dados, pub, data_audiencia) #aqui criar tanto tarefa para aud quanto para impugcont
                    pass
                elif conteudo_pub == 'DEFESA_CONTRARRAZOES':
                    criar_tarefa_defesa(pub, dados)
                else:
                    responsavel = dados['membros']['Alan Almeida']
                    criar_tarefa_geral(conteudo_pub, pub, dados, responsavel)

    print(f"Número de publicações localizadas aqui: {cont_pubs}")

if __name__ == '__main__':    
    main()

    
