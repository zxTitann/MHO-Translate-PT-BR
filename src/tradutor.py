import json
from googletrans import Translator
import time

def carregar_lista(Nao_traduzir):
    with open(Nao_traduzir, 'r', encoding='utf-8') as arquivo:
        return [linha.strip() for linha in arquivo]

#Listas de exceção    
termos_nao_traduzir = carregar_lista('data/lista_de_excecao/nao_traduzir.txt')
termos_capitalizacao_original = carregar_lista("data/lista_de_excecao/nao_alterar_capitalizacao.txt")

#Arquivos originais para traduzir
nome_arquivo_entrada = 'data/arquivos_originais_json/por.all_3FFFFFFFFFFFFFFF.string.json'

translator = Translator()

def aplicar_capitalizacao_original_preservada(texto_traduzido_ou_original, mapa_termos_originais_preservar):
    """
    Usa o mapa de termos originais para restaurar a capitalização exata original
    desses termos no texto traduzido ou original.
    """
    texto_final = texto_traduzido_ou_original # Começa com o texto processado pela API

    # Itera pelo dicionário de termos originais que devemos preservar a capitalização
    # A chave é a versão lowercase do termo, o valor é a versão EXATA original
    for termo_lower, termo_original_exato in mapa_termos_originais_preservar.items():
        # Precisamos encontrar onde a versão lowercase do termo original (a chave do dicionário)
        # aparece no texto final (que pode ser traduzido e bagunçado).
        texto_final_lower = texto_final.lower() # Busca case-insensitive
        indice_busca = 0

        while True:
            # Tenta encontrar a próxima ocorrência do termo (ignorando capitalização)
            indice_encontrado = texto_final_lower.find(termo_lower, indice_busca)

            if indice_encontrado == -1:
                break # Termo não encontrado ou sem mais ocorrências

            # Se encontrou, pega o fim da ocorrência na versão lowercase
            fim_encontrado_lower = indice_encontrado + len(termo_lower)

            # Substituímos a parte encontrada no texto_final (que tem a capitalização bagunçada)
            # pela versão EXATA ORIGINAL que está guardada no nosso dicionário!
            texto_final = (texto_final[:indice_encontrado] + # Pega a parte ANTES
                           termo_original_exato + # <-- Substitui pela capitalização EXATA ORIGINAL guardada!
                           texto_final[fim_encontrado_lower:]) # Pega a parte DEPOIS

            # Atualiza para continuar buscando: recalcula o lower e ajusta o índice
            texto_final_lower = texto_final.lower() # O texto_final mudou, recalcula o lower
            indice_busca = indice_encontrado + len(termo_original_exato) # Busca continua após a substituição (usando o tamanho do termo original EXATO)


    return texto_final # Retorna o texto com a capitalização original dos termos preservada!


def corrigir_capitalizacao(texto_processado, lista_termos_originais):
    #Corrige a capitalização de termos conhecidos no texto processado
    #substituindo-os pela sua versão original da lista.

    texto_corrigido = texto_processado

    for termo_original in lista_termos_originais:
        # Precisamos encontrar onde esse termo (em qualquer capitalização) aparece no texto.
        # Uma forma é procurar pela versão em lowercase do termo na versão em lowercase do texto.
        termo_original_lower = termo_original.lower()
        texto_corrigido_lower = texto_corrigido.lower()
        indice_busca = 0 # Começa a buscar desde o início

        # Loop para encontrar e substituir TODAS as ocorrências do termo
        while True:
            # Tenta encontrar a próxima ocorrência do termo (ignorando capitalização)
            indice_encontrado = texto_corrigido_lower.find(termo_original_lower, indice_busca)

            if indice_encontrado == -1:
                # Termo não encontrado (ou não há mais ocorrências), sai do loop
                break

            # Se encontrou, calculamos o fim da ocorrência no texto original e no texto corrigido
            fim_encontrado = indice_encontrado + len(termo_original_lower)

            # Agora, substituímos a parte encontrada no texto_corrigido (mantendo a capitalização original do texto *encontrado*)
            # pela versão ORIGINAL do termo da nossa lista (restaurando a capitalização correta)
            # Isso é um pouco delicado pra garantir que não estraga o texto ao redor
            # Uma forma mais segura é reconstruir a string: parte antes + termo original + parte depois

            texto_corrigido =   (texto_corrigido[:indice_encontrado] +
                                termo_original + # <-- Substitui pela capitalização CORRETA da lista!
                                texto_corrigido[fim_encontrado:])

            # Atualiza o texto_corrigido_lower e o indice_busca para continuar procurando DEPOIS da substituição
            # Precisamos recalcular o lower do texto_corrigido pois ele mudou
            texto_corrigido_lower = texto_corrigido.lower()
            indice_busca = indice_encontrado + len(termo_original) # Continua buscando após o termo substituído

    return texto_corrigido # Retorna o texto com a capitalização corrigida


def traduzir_string(texto, max_tentativas=5, delay_segundos=1): # <-- Adicione parâmetros para tentativas e delay
    """
    Tenta traduzir uma string usando googletrans, com lógica de retentativa em caso de erro.
    """
    texto_para_traduzir = texto.strip() # Remover espaços em branco extras do início/fim
    if not texto_para_traduzir: # Se a string estiver vazia ou só com espaços
        return texto # Retorna o original vazio/com espaços se não há texto real

    for tentativa in range(max_tentativas): # <-- Loop para retentar
        try:
            # Tenta traduzir. A API da googletrans é meio instável, pode falhar.
            resultado_traducao_obj = translator.translate(texto_para_traduzir, dest='pt')

            if resultado_traducao_obj is not None and resultado_traducao_obj.text is not None:
                 texto_traduzido = resultado_traducao_obj.text.strip() # Remover espaços extras na tradução também
                 if texto_traduzido: # Verificar se a tradução não ficou vazia depois de remover espaços
                     return texto_traduzido # <-- Tradução OK, retorna o resultado
                 else:
                      # A API retornou um objeto, mas o texto traduzido está vazio/só espaços.
                      print(f"API retornou texto vazio para '{texto_para_traduzir}'. Tentativa {tentativa + 1}/{max_tentativas}. Retentando...")
                      # Continua para a próxima tentativa
            else:
                 # A API retornou None, ou o .text é None
                 print(f"API retornou None para '{texto_para_traduzir}'. Tentativa {tentativa + 1}/{max_tentativas}. Retentando...")
                 # Continua para a próxima tentativa

        except Exception as e:
            # Ocorreu um erro (conexão, etc.)
            print(f"Erro ao traduzir '{texto_para_traduzir}' (Tentativa {tentativa + 1}/{max_tentativas}): {e}")
            if tentativa < max_tentativas - 1: # Se ainda há tentativas restantes...
                print(f"Aguardando {delay_segundos} segundos antes de retentar...")
                time.sleep(delay_segundos) # <-- Espera um pouco antes de tentar de novo
            # Continua para a próxima tentativa do loop for

    # Se o loop de tentativas terminou sem sucesso
    print(f"Falha na tradução após {max_tentativas} tentativas para '{texto_para_traduzir}'. Retornando texto original.")
    return texto # <-- Retorna o texto original se falhou em todas as tentativas

try:
    with open(nome_arquivo_entrada, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'StringMap' in data:
        string_map = data['StringMap']
        print("Arquivo JSON carregado e 'StringMap' encontrado!")

    for key, value in string_map.items():
            if 'String' in value: # <-- Primeiro check: Este item tem a chave 'String'?
                texto_original = value['String'] # <-- Pega o texto original (este está no lugar certo)

                termos_originais_para_preservar = {}

                for termo_base in termos_capitalizacao_original: # <-- Pega os termos originais para preservar
                    termo_base_lower = termo_base.lower() # Termo base em lowercase
                    texto_original_lower = texto_original.lower() # Texto original em lowercase
                    indice_busca = 0 # Começa a buscar desde o início

                    while True:
                        indice_encontrado = texto_original_lower.find(termo_base_lower, indice_busca) # Tenta encontrar a próxima ocorrência
                        if indice_encontrado == -1: # Termo nao encontrado (ou nao ha mais ocorrencias), sai do loop
                            break
                        
                        fim_encontrado = indice_encontrado + len(termo_base_lower) # Calcula o fim da ocorrência no texto original
                        ocorrencia_exata_original = texto_original[indice_encontrado : fim_encontrado] # Pega a ocorrência exata no texto original
                        # Armazena no dicionário: a versão lowercase como chave, a versão EXATA original como valor
                        # Se já existir (por exemplo, se "missilecollidepower" e "missileCollidePower"
                        # em lowercase são iguais), a gente só armazena a primeira encontrada,
                        # ou a última, dependendo de como queremos lidar com MÚLTIPLAS variações no ORIGINAL.
                        # Para simplificar AGORA, vamos só garantir que a versão lowercase
                        # aponta para a capitalização EXATA que encontramos PRIMEIRO no original.
                        if termo_base_lower not in termos_originais_para_preservar:
                            termos_originais_para_preservar[termo_base_lower] = ocorrencia_exata_original

                            indice_busca = fim_encontrado # Pula para o fim da ocorrência encontrada
                    
                    


                # === BLOCO DE EXCLUSÃO COMENTADO (OK PARA O TESTE) ===
                # Esta é a lógica original para excluir textos que contêm termos da lista nao_traduzir.txt.
                # Mantemos ele comentado por enquanto para testar as correções de formatacao/capitalizacao.
                # manter_original = False
                # for termo in termos_nao_traduzir:
                #     if termo in texto_original: # <-- Esta é a linha do filtro agressivo
                #         manter_original = True
                #         break # Se encontramos um termo, podemos parar de verificar para esta linha
                # === FIM DO BLOCO COMENTADO ===

                # === NOVO BLOCO SIMPLIFICADO PARA O TESTE ===
                # ESTE bloco SUBSTITUI o if manter_original: e o elif/else original
                # Ele está no MESMO NÍVEL de indentação que o bloco de exclusão COMENTADO estava
                # E ESTÁ DENTRO DO if 'String' in value: E DENTRO DO LOOP FOR!

                if any(char.isalpha() for char in texto_original): # Se o texto original (que tem a chave 'String') tiver letras...
                    texto_traduzido = traduzir_string(texto_original) # <-- CHAMA A FUNÇÃO DE TRADUÇÃO BLINDADA!
                    texto_traduzido_corrigido = corrigir_capitalizacao(texto_traduzido, termos_capitalizacao_original)

                    texto_final_com_capitalizacao_preservada = aplicar_capitalizacao_original_preservada(texto_traduzido_corrigido, termos_originais_para_preservar)

                    time.sleep(0.3) #Pequena pausa para nao sobrecarregar a API

                    value['String'] = texto_final_com_capitalizacao_preservada # Atualiza o valor no dicionário 'data' com a tradução (ou original se a API falhou/retornou None)
                    # Imprime a mensagem de Original e Traduzido (se a função não retornou erro ou None)
                    print(f"ID: {key}, Original: {texto_original[:70]}..., Traduzido: {texto_final_com_capitalizacao_preservada[:50]}...")
                else: # Se não tiver letras (como "..." ou "$%$%" ou só números), pula a tradução para este item
                    print(f"ID: {key}, Texto parece nao conter letras para traduzir: {texto_original}")
                # === FIM DO NOVO BLOCO ===

            # Se 'String' não estiver em value, este item é pulado (lógica original do script continua funcionando)


    # Salvar o arquivo JSON traduzido (você pode mudar o nome se quiser)
    nome_arquivo_traduzido = 'data/arquivo_traduzido_com_api/seu_arquivo_traduzido_Vx.json'
    with open(nome_arquivo_traduzido, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nArquivo traduzido salvo como '{nome_arquivo_traduzido}'")

except FileNotFoundError:
    print(f"Erro: Arquivo '{nome_arquivo_entrada}' não encontrado.")
except json.JSONDecodeError:
    print(f"Erro: Falha ao decodificar o arquivo JSON. Verifique se o formato está correto.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")