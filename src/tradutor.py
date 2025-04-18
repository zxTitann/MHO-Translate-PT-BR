import json
from googletrans import Translator

def carregar_lista(Nao_traduzir):
    with open(Nao_traduzir, 'r', encoding='utf-8') as arquivo:
        return [linha.strip() for linha in arquivo]

#Listas de exceção    
termos_nao_traduzir = carregar_lista('data/lista_de_excecao/nao_traduzir.txt')
termos_capitalizacao_original = carregar_lista("data/lista_de_excecao/nao_alterar_capitalizacao.txt")

#Arquivos originais para traduzir
nome_arquivo_entrada = 'data/arquivos_originais_json/por.all_3FFFFFFFFFFFFFFF.string.json'

translator = Translator()

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

            texto_corrigido = (texto_corrigido[:indice_encontrado] +
                               termo_original + # <-- Substitui pela capitalização CORRETA da lista!
                               texto_corrigido[fim_encontrado:])

            # Atualiza o texto_corrigido_lower e o indice_busca para continuar procurando DEPOIS da substituição
            # Precisamos recalcular o lower do texto_corrigido pois ele mudou
            texto_corrigido_lower = texto_corrigido.lower()
            indice_busca = indice_encontrado + len(termo_original) # Continua buscando após o termo substituído

    return texto_corrigido # Retorna o texto com a capitalização corrigida


def traduzir_string(texto):
    # Por enquanto, vamos fazer uma tradução simples
    try:
        resultado_traducao_obj = translator.translate(texto, dest='pt')
        
        if resultado_traducao_obj is not None:
            texto_traduzido = resultado_traducao_obj.text
            #eu nao vou adicionar o todo porque quero lhe mostrar as listas com problemas de capitalização, espacamento e afins para voce ver comigo se esse todo nao vai nos dar problemas.
            return texto_traduzido
        
        else:
            print(f"API retornou None para '{texto}'. Retornando texto original.")
            return texto
        
    except Exception as e:
        print(f"Erro ao traduzir '{texto}': {e}")
        return texto  # Retorna o texto original em caso de erro

try:
    with open(nome_arquivo_entrada, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'StringMap' in data:
        string_map = data['StringMap']
        print("Arquivo JSON carregado e 'StringMap' encontrado!")

    for key, value in string_map.items():
            if 'String' in value: # <-- Primeiro check: Este item tem a chave 'String'?
                texto_original = value['String'] # <-- Pega o texto original (este está no lugar certo)

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

                    value['String'] = texto_traduzido_corrigido # Atualiza o valor no dicionário 'data' com a tradução (ou original se a API falhou/retornou None)
                    # Imprime a mensagem de Original e Traduzido (se a função não retornou erro ou None)
                    print(f"ID: {key}, Original: {texto_original[:50]}..., Traduzido: {texto_traduzido_corrigido[:50]}...")
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