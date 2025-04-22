import json
import re
import os # Vamos precisar de os para manipular caminhos

# --- NOSSAS REGRAS DE PROTEÇÃO (A PLANTA!) ---

# 1. Strings Exatas para Proteger (Prioridade 1)
# Lista de strings literais que NUNCA devem ser traduzidas.
# Você vai popular e refinar esta lista com suas anotações de nao_traduzir.txt e outras que encontrar.
EXACT_STRINGS_TO_PROTECT = [
    "Cooldown",
    "Magik",
    "Red", # Exemplo da sua string complexa, se for um termo não traduzível
    "Green", # Exemplo da sua string complexa
    "Fisk Tower", # Exemplo da sua string complexa
    "Psi-Knife",
    "Emblema Excelsiors",
    "condition0",
    "proceffect0",
    "#waypointheader#", # Já pego pelo regex, mas pode estar aqui para garantia ou clareza
    "#/waypointheader#", # Já pego pelo regex
    # ... adicione mais strings exatas da sua lista nao_traduzir.txt e anotações
]

# 2. REGEX de Proteção Refinados (Prioridade 2 - Aplicar após as Strings Exatas)
# Lista de dicionários, onde cada dicionário tem um nome e o padrão regex refinado.
# A ORDEM nesta lista PODE importar (do mais específico/complexo para o mais geral),
# especialmente se os padrões puderem se sobrepor.
REGEX_PATTERNS_TO_PROTECT = [
    # Endereços de E-mail (Nosso novo REGEX!)
    {"name": "email", "pattern": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"},
    # internal_links ([[...]]) - REGEX OK
    {"name": "internal_link", "pattern": r"\[\[([^\]]+)\]\]"},
    # html_tags (<tag>...</tag>, <tag/>) - REGEX REFINADO
    {"name": "html_tag", "pattern": r"<[/]?[a-zA-Z]+[^>]*>"},
    # hashtag_patterns (tudo entre # e #, incluindo #/...#) - REGEX REFINADO
    {"name": "hashtag_pattern", "pattern": r"#[^#]+#"},
    # dollar_variables ({{$...}}) - REGEX REFINADO com escape
    {"name": "dollar_variable", "pattern": r"\{\{\$([A-Za-z0-9_]+)\}\}"},
    # $dot.properties$ ($prop.sub.prop$) - REGEX REFINADO (Aplicar ANTES de dot_properties)
    {"name": "dollar_dot_property", "pattern": r"\$[a-zA-Z0-9_\.]+\$"},
    # dot_properties (prop.sub.prop) - REGEX REFINADO (Aplicar DEPOIS de $dot.properties$)
    {"name": "dot_property", "pattern": r"[a-zA-Z0-9_\.]+"},
    # level_rank (Lvl #, Rank #) - REGEX OK
    {"name": "level_rank", "pattern": r"(L|Lvl|Level|Rank)\s*(\d+)"},
    # tokens (@token) - REGEX OK (Aplicar por último nos padrões com @, DEPOIS do email)
    {"name": "token", "pattern": r"@([A-Za-z0-9_]+)"},
    # ... adicione outros regex de proteção que identificar

    # NOTA: O padrão de comandos '/' puro (r"/([a-zA-Z]+)") foi deixado de fora por enquanto,
    # pois parece que '/' aparece mais em contextos de tags (#/...) ou outros padrões que já estamos pegando.
    # A gente pode revisitar se encontrar casos de "/comando" puros não protegidos.
]

# --- FUNÇÃO PARA CARREGAR O JSON ---

def carregar_json_do_txt(caminho_arquivo):
    """
    Lê um arquivo de texto que contém conteúdo JSON e carrega como um dicionário Python.
    """
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Arquivo JSON carregado com sucesso de: {caminho_arquivo}")
        return data
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado em '{caminho_arquivo}'")
        return None
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar JSON. Verifique o formato do arquivo '{caminho_arquivo}'.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar o arquivo: {e}")
        return None

# --- FUNÇÃO PARA APLICAR A PROTEÇÃO (FASE 1) ---

def aplicar_protecao(texto_original, strings_exatas, regex_patterns):
    """
    Aplica regras de proteção (strings exatas e regex) a uma string.
    Substitui padrões protegidos por placeholders únicos e retorna o texto modificado
    e um mapa de placeholders para o conteúdo original.
    """
    texto_processado = texto_original # Começa com o texto original
    placeholders_map = {} # Dicionário para guardar {placeholder: texto_original_protegido}
    placeholder_counter = 0 # Contador para gerar placeholders únicos

    # Prioridade 1: Proteger Strings Exatas
    # Importante: Substituir strings exatas mais LONGAS primeiro para não pegar partes de strings mais curtas.
    strings_exatas_ordenadas = sorted(strings_exatas, key=len, reverse=True)

    for string_exata in strings_exatas_ordenadas:
        # Precisamos ter cuidado para substituir SÓ a string exata e não quebrar o regex depois.
        # Uma forma é usar re.escape() para tratar a string exata como um padrão literal,
        # e usar word boundaries \b para garantir que casamos palavras inteiras se aplicável.
        # No entanto, alguns dos nossos "strings exatas" (como /emphasis#) NÃO são palavras inteiras.
        # Uma abordagem mais segura é usar uma função de substituição com re.sub que verifica
        # se o match encontrado é EXATAMENTE a string exata.
        # Para simplificar AGORA, vamos tentar uma substituição simples de string, mas
        # ciente que isso pode ter limitações (ex: "Word" em "AnotherWord").
        # Uma abordagem mais robusta para strings exatas que NÃO são palavras inteiras
        # seria usar re.finditer para encontrar todas as ocorrências e substituir indexando.
        # Vamos simplificar com substituição simples por enquanto, e refinar se der problema.

        # Usar re.escape para tratar a string exata como padrão literal
        padrao_string_exata = re.escape(string_exata)
        # Opcional: adicionar \b para strings exatas que são palavras, mas difícil de automatizar
        # Vamos usar o re.escape simples por enquanto

        # re.sub com uma função de substituição para garantir que só casamos a string exata
        # Esta é uma forma mais segura do que a substituição de string simples ou re.sub direto
        def substituir_string_exata(match):
            # match.group(0) é a string completa casada pelo padrão (que é a string_exata escapada)
            # Geramos o placeholder
            nonlocal placeholder_counter # Permite modificar a variável do escopo exterior
            placeholder = f"__PROTECTED_{placeholder_counter}__"
            placeholders_map[placeholder] = match.group(0) # Guarda a string original
            placeholder_counter += 1
            return placeholder

        # O re.sub com a função vai encontrar todas as ocorrências do padrao_string_exata
        # e rodar substituir_string_exata para cada uma.
        texto_processado = re.sub(padrao_string_exata, substituir_string_exata, texto_processado)


    # Prioridade 2: Proteger Padrões REGEX (nosso texto JÁ tem placeholders para strings exatas)
    # Iterar sobre a lista de padrões REGEX na ordem definida.
    for pattern_info in regex_patterns:
        regex_name = pattern_info["name"]
        regex_pattern = pattern_info["pattern"]

        # Usar re.finditer para encontrar TODAS as ocorrências do padrão REGEX
        # re.finditer é bom porque nos dá os spans (início e fim) de cada match
        # Vamos encontrar os matches e substituí-los.
        # É importante substituir do fim para o início para não invalidar os spans dos próximos matches,
        # OU construir a nova string de forma diferente.
        # Uma forma mais simples para garantir que não sobrepõe ou quebra placeholders já criados
        # é usar re.sub com uma função que checa o que está sendo substituído.

        # Usamos re.sub com uma função de substituição para gerar placeholders
        def substituir_regex_match(match):
            # match.group(0) é a string completa casada pelo padrão regex
            # match.start() e match.end() são as posições no texto_processado ATUAL

            # Geração de placeholder
            nonlocal placeholder_counter
            placeholder = f"__PROTECTED_{placeholder_counter}__"

            # Armazenar no mapa (guardamos a string ORIGINAL que foi casada pelo regex)
            placeholders_map[placeholder] = match.group(0)
            placeholder_counter += 1

            # Retornar o placeholder para substituir o match
            return placeholder

        # Aplicar o regex de substituição.
        # A função substituir_regex_match será chamada para CADA match do regex_pattern
        # no texto_processado atual.
        texto_processado = re.sub(regex_pattern, substituir_regex_match, texto_processado)


    # Retorna o texto com placeholders e o mapa para restaurar depois
    return texto_processado, placeholders_map

# --- CONFIGURAÇÃO DE ARQUIVOS ---

# Caminhos para seus arquivos .txt (com conteúdo JSON)
# Ajuste estes caminhos para onde você salvou os arquivos no seu PC
# Usando caminhos relativos em vez de caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Diretório base do script atual
CAMINHO_ARQUIVO_ORIGINAL_TXT = os.path.join(BASE_DIR, '../data/arquivos_originais_json/por.all_3FFFFFFFFFFFFFFF.string.json')  # Caminho relativo ao arquivo original
CAMINHO_ARQUIVO_PROCESSADO_FASE1 = os.path.join(BASE_DIR, '../data/arquivo_traduzido_com_API/por.all_3FFFFFFFFFFFFFFF_FASE_1.string.json')  # Caminho relativo ao arquivo processado

# --- FLUXO PRINCIPAL DO SCRIPT ---

if __name__ == "__main__":
    # Carregar os dados JSON do arquivo original
    dados_json_original = carregar_json_do_txt(CAMINHO_ARQUIVO_ORIGINAL_TXT)

    if dados_json_original and 'StringMap' in dados_json_original:
        string_map = dados_json_original['StringMap']
        total_entries = len(string_map)
        print(f"Processando {total_entries} entradas para PROTEÇÃO...")

        # Dicionário para armazenar todos os mapas de placeholders por string ID
        # (Pode ser útil depois para debug ou para a fase de tradução)
        # No entanto, para o fluxo direto, o mapa é retornado pela função por string.
        # Vamos aplicar a proteção DIRETAMENTE no dicionário dados_json_original
        # E armazenar os mapas de placeholder EM OUTRO LUGAR se necessário.
        # Por enquanto, a função aplicar_protecao já retorna o mapa por string.
        # Vamos modificar o loop para usar e guardar esse mapa.

        # Armazenar todos os mapas de placeholders por key da string
        all_placeholders_maps = {}

        count = 0
        # Iterar sobre cada entrada no StringMap
        for key, value in string_map.items():
            if 'String' in value and value['String'] is not None:
                texto_original = value['String']

                # Aplicar a proteção
                texto_com_placeholders, placeholders_map_current = aplicar_protecao(
                    texto_original,
                    EXACT_STRINGS_TO_PROTECT,
                    REGEX_PATTERNS_TO_PROTECT
                )

                # Atualizar a string no dicionário original com a versão com placeholders
                dados_json_original['StringMap'][key]['String'] = texto_com_placeholders

                # Armazenar o mapa de placeholders para esta string (pode ser útil depois)
                # all_placeholders_maps[key] = placeholders_map_current # Opcional: guardar todos os mapas

                count += 1
                if count % 1000 == 0: # Imprimir progresso a cada X strings
                    print(f"Proteção aplicada a {count}/{total_entries} strings...")

        print(f"Fase de PROTEÇÃO concluída para {count} strings.")

        # Salvar o resultado da Fase 1 (JSON com placeholders)
        # Garante que o diretório de saída existe
        diretorio_saida = os.path.dirname(CAMINHO_ARQUIVO_PROCESSADO_FASE1)
        if diretorio_saida and not os.path.exists(diretorio_saida):
            os.makedirs(diretorio_saida)

        try:
            with open(CAMINHO_ARQUIVO_PROCESSADO_FASE1, 'w', encoding='utf-8') as f_out:
                json.dump(dados_json_original, f_out, indent=4, ensure_ascii=False)
            print(f"Resultado da Fase 1 (JSON com placeholders) salvo em: {CAMINHO_ARQUIVO_PROCESSADO_FASE1}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo da Fase 1: {e}")


    else:
        print("Não foi possível carregar os dados JSON ou 'StringMap' não encontrado.")