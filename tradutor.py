import json
from googletrans import Translator

# Coloque o nome do seu arquivo JSON aqui
nome_arquivo = 'por.all_3FFFFFFFFFFFFFFF.string.json'

translator = Translator()

def traduzir_string(texto):
    # Por enquanto, vamos fazer uma tradução simples
    try:
        traducao = translator.translate(texto, dest='pt').text
        return traducao
    except Exception as e:
        print(f"Erro ao traduzir '{texto}': {e}")
        return texto  # Retorna o texto original em caso de erro

try:
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'StringMap' in data:
        string_map = data['StringMap']
        print("Arquivo JSON carregado e 'StringMap' encontrado!")

        for key, value in string_map.items():
            if 'String' in value:
                texto_original = value['String']
                # Vamos traduzir apenas se o texto parecer estar em inglês (uma abordagem simples por enquanto)
                if any(char.isalpha() for char in texto_original): # Verifica se há pelo menos uma letra no texto
                    texto_traduzido = traduzir_string(texto_original)
                    value['String'] = texto_traduzido
                    print(f"ID: {key}, Original: {texto_original[:50]}..., Traduzido: {texto_traduzido[:50]}...") # Imprime os primeiros 50 caracteres para não poluir muito o terminal
                else:
                    print(f"ID: {key}, Texto parece não ter letras para traduzir: {texto_original}")

    else:
        print("Chave 'StringMap' não encontrada no arquivo JSON.")

    # Salvar o arquivo JSON traduzido (você pode mudar o nome se quiser)
    nome_arquivo_traduzido = 'seu_arquivo_traduzido.json'
    with open(nome_arquivo_traduzido, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\nArquivo traduzido salvo como '{nome_arquivo_traduzido}'")

except FileNotFoundError:
    print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
except json.JSONDecodeError:
    print(f"Erro: Falha ao decodificar o arquivo JSON. Verifique se o formato está correto.")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")