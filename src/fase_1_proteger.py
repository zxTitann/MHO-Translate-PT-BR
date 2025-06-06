import json
import re
import os

# --- CONFIGURAÇÃO DE ARQUIVOS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_ORIGINAL = os.path.join(BASE_DIR, '..', 'data', 'arquivos_originais_json', 'por.all_3FFFFFFFFFFFFFFF.string.json')
DIRETORIO_SAIDA = os.path.join(BASE_DIR, '..', 'data', 'arquivo_traduzido_com_api')
DIRETORIO_FASE_1 = os.path.join(DIRETORIO_SAIDA, 'FASE_1')
ARQUIVO_FASE_1 = os.path.join(DIRETORIO_FASE_1, 'por.all_3FFFFFFFFFFFFFFF_FASE_1-X.string.json')
ARQUIVO_PLACEHOLDERS = os.path.join(DIRETORIO_FASE_1, 'Vxplaceholders_map.json')

# --- REGRAS DE PROTEÇÃO (A ORDEM IMPORTA) ---

REGEX_GROUP_1_DELIMITED = [
    {"name": "url", "pattern": r"https?://[^\s/$.?#].[^\s]*"},
    {"name": "filepath", "pattern": r"\b[a-zA-Z0-9_]+\.(bk2|txt|json|xml|exe)\b"},
    {"name": "dollar_variable", "pattern": r"\$[a-zA-Z0-9_.]+\$?"},
    {"name": "html_tag", "pattern": r"<[/]?[a-zA-Z0-9\s\"\'=\-:/.]+>"},
    {"name": "hashtag_pattern", "pattern": r"#[^#\s]+#"},
]
REGEX_GROUP_2_PROPERTIES = [
    {"name": "dot_property", "pattern": r"\b[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)+\b"},
]
REGEX_GROUP_3_MISC = [
    {"name": "level_rank", "pattern": r"\b(Lvl|Level|Rank)\s*(\d+)\b"},
]
EXACT_STRINGS_TO_PROTECT = sorted([
    "Cooldown", "cooldown", "duration", "Magik", "Red", "Green", "Fisk Tower", "Psi-Knife", "Emblema Excelsiors",
    "condition0", "proceffect0", "missileCollidePower",
    "S.H.I.E.L.D.", "S.H.I.E.L.D", "A.I.M.", "A.I.M", "M.O.D.O.K.", "M.O.D.O.K", "S.W.O.R.D.", "S.W.O.R.D",
    "H.A.M.M.E.R.", "H.A.M.M.E.R", "H.E.R.B.I.E.", "H.E.R.B.I.E", "A.R.M.O.R.", "A.R.M.O.R",
    "A.R.M.A.D.U.R.A.", "A.R.M.A.D.U.R.A", "O.M.D.", "O.M.D", "G.S.T.", "G.S.T", "F.L.G.", "F.L.G",
    "M.A.P.", "M.A.P", "I.V.A.", "I.V.A", "I.M.A.", "I.M.A", "E.U.", "E.U", "U.S.", "U.S",
    "a.k.a.", "a.k.a", "Pt.2", "Pt.3", "Pt.4", "S.T.A.S.H"
], key=len, reverse=True)

# --- FUNÇÕES ---

def carregar_json_do_txt(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"SUCESSO: Arquivo JSON carregado de: {caminho_arquivo}")
        return data
    except Exception as e:
        print(f"ERRO CRÍTICO AO CARREGAR O JSON: {caminho_arquivo} | Erro: {e}")
    return None

def criar_placeholder_seguro(match, placeholders_map, placeholder_counter):
    matched_text = match.group(0)
    if "__PROTECTED_" in matched_text:
        return matched_text
    placeholder = f"__PROTECTED_{placeholder_counter[0]}__"
    placeholders_map[placeholder] = matched_text
    placeholder_counter[0] += 1
    return placeholder

def aplicar_protecao_regex(texto, placeholders_map, placeholder_counter, regex_patterns):
    for pattern_info in regex_patterns:
        texto = re.sub(pattern_info["pattern"], lambda m: criar_placeholder_seguro(m, placeholders_map, placeholder_counter), texto)
    return texto

# --- FUNÇÃO CORRIGIDA ---
def aplicar_protecao_exata(texto, placeholders_map, placeholder_counter):
    for termo in EXACT_STRINGS_TO_PROTECT:
        try:
            # Lógica de fronteira de palavra inteligente
            prefixo = r'\b' if termo[0].isalnum() else ''
            sufixo = r'\b' if termo[-1].isalnum() else ''
            pattern = prefixo + re.escape(termo) + sufixo
            texto = re.sub(pattern, lambda m: criar_placeholder_seguro(m, placeholders_map, placeholder_counter), texto, flags=re.IGNORECASE)
        except re.error as e:
            print(f"Erro de Regex no termo exato '{termo}': {e}")
            continue
    return texto

# --- FLUXO PRINCIPAL DO SCRIPT ---
if __name__ == "__main__":
    if not os.path.exists(DIRETORIO_FASE_1):
        os.makedirs(DIRETORIO_FASE_1)
        
    data = carregar_json_do_txt(ARQUIVO_ORIGINAL)

    if data:
        string_map_data = data.get('StringMap')
        if not string_map_data or not isinstance(string_map_data, dict):
            print("ERRO: Chave 'StringMap' não encontrada ou não é um dicionário no arquivo JSON.")
        else:
            master_placeholders_map = {}
            total_entradas = len(string_map_data)
            print(f"\nIniciando Fase 1: Protegendo {total_entradas} entradas...")
            
            for i, (key, value_object) in enumerate(string_map_data.items()):
                print(f"Processando item {i+1}/{total_entradas}...", end='\r')

                original_text = ""
                if isinstance(value_object, dict) and "String" in value_object:
                    original_text = value_object.get("String", "")
                
                if not isinstance(original_text, str) or not original_text.strip():
                    continue

                placeholders_map_local = {}
                placeholder_counter = [0]
                texto_processado = original_text

                texto_processado = aplicar_protecao_regex(texto_processado, placeholders_map_local, placeholder_counter, REGEX_GROUP_1_DELIMITED)
                texto_processado = aplicar_protecao_regex(texto_processado, placeholders_map_local, placeholder_counter, REGEX_GROUP_2_PROPERTIES)
                texto_processado = aplicar_protecao_regex(texto_processado, placeholders_map_local, placeholder_counter, REGEX_GROUP_3_MISC)
                texto_processado = aplicar_protecao_exata(texto_processado, placeholders_map_local, placeholder_counter)
                
                if placeholders_map_local:
                    value_object["String"] = texto_processado
                    # Corrigindo a estrutura do mapa de placeholders para a desejada
                    master_placeholders_map[key] = {v: k for k, v in placeholders_map_local.items()}

            print(f"\nProcessamento concluído. {len(master_placeholders_map)} chaves foram modificadas.")
            
            data['StringMap'] = string_map_data
            with open(ARQUIVO_FASE_1, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            with open(ARQUIVO_PLACEHOLDERS, 'w', encoding='utf-8') as f:
                json.dump(master_placeholders_map, f, indent=4, ensure_ascii=False)

            print("-" * 30)
            print(f"SUCESSO: Arquivo da Fase 1 (protegido) salvo em: {ARQUIVO_FASE_1}")
            print(f"SUCESSO: Mapa de placeholders salvo em: {ARQUIVO_PLACEHOLDERS}")
            print("Fase 1 (Proteção) concluída com sucesso!")