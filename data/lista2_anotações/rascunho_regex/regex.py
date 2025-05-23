# translation_error_report.py

DETECTED_TRANSLATION_ERRORS = {
    # Erros em placeholders #n[]
    "hashtag_placeholders_errors": [
        {
            "original": "#1[Valor de Dinheiro]",
            "translated": "#1[Valor monetário]",
            "issue": "Tradução do conteúdo do placeholder"
        },
        {
            "original": "#2[Valor do Money]",
            "translated": "#2[Valor do dinheiro]",
            "issue": "Tradução do termo técnico Money"
        },
        {
            "original": "#1[Valor de Tempo]",
            "translated": "#1[Valor de tempo]",
            "issue": "Mudança de capitalização no placeholder"
        },
        {
            "original": "#3[Valor Flutuante]",
            "translated": "#3[Valor flutuante]",
            "issue": "Mudança de capitalização"
        },
        {
            "original": "#1[Item Rarity]",
            "translated": "#1[Raridade do item]",
            "issue": "Tradução dentro do placeholder"
        },
        {
            "original": "#2[Player's Rank Value]",
            "translated": "#2[Valor do rank do jogador]",
            "issue": "Tradução do termo técnico Rank"
        }
    ],
    
    # Erros em variáveis $
    "dollar_variable_errors": [
        {
            "original": "{{$ItemBonus}}",
            "translated": "{{$BonusDoItem}}",
            "issue": "Tradução do nome da variável"
        },
        {
            "original": "{{$CreditsRequired}}",
            "translated": "{{$CréditosNecessários}}",
            "issue": "Tradução e acentuação no nome da variável"
        },
        {
            "original": "{{$Credits}}",
            "translated": "{{$Créditos}}",
            "issue": "Acentuação no nome da variável"
        },
        {
            "original": "{{$ItemName}}",
            "translated": "{{$NomeDoItem}}",
            "issue": "Tradução do nome da variável"
        },
        {
            "original": "{{$PlayerName}}",
            "translated": "{{$NomeDoJogador}}",
            "issue": "Tradução do nome da variável"
        }
    ],
    
    # Erros em links internos [[...]]
    "internal_links_errors": [
        {
            "original": "[[Items/Consumable/EventCredits.prototype]]",
            "translated": "[[Itens/Consumíveis/CréditosDoEvento.prototype]]",
            "issue": "Tradução de caminhos e nomes de arquivos"
        },
        {
            "original": "[[Players/$PlayerName$.prototype$PrefServer$]]",
            "translated": "[[Jogadores/$NomeDoJogador$.prototype$ServidorPreferido$]]",
            "issue": "Tradução de variáveis e estrutura interna"
        },
        {
            "original": "[[UI/Dialogs/StoreModal.UITextSocialDialogCreditCardSaveLabel.Text]]",
            "translated": "[[UI/Diálogos/ModalDaLoja.UITextoRótuloSalvarCartãoDeCrédito.Texto]]",
            "issue": "Tradução de identificadores UI e nomes de classes"
        }
    ],
    
    # Erros em tags HTML/XML
    "html_tag_errors": [
        {
            "original": "<color flavor=CombatAttackerName",
            "translated": "<color flavor=NomeDoAtacante",
            "issue": "Tradução do valor do atributo flavor"
        },
        {
            "original": "<text align=center",
            "translated": "<text alinhamento=centro",
            "issue": "Tradução do nome do atributo"
        },
        {
            "original": "<font UISocialDialogBoldFont>",
            "translated": "<font UIDiálogoSocialFonteNegrito>",
            "issue": "Tradução e acentuação do nome da fonte"
        }
    ],
    
    # Erros em propriedades com ponto
    "dot_property_errors": [
        {
            "original": "Players.Name",
            "translated": "Jogadores.Nome",
            "issue": "Tradução do primeiro componente"
        },
        {
            "original": "Inventory.AddItemConfirmation",
            "translated": "Inventário.ConfirmaçãoDeAdicionarItem",
            "issue": "Tradução e acentuação"
        },
        {
            "original": "UI.Navigation.AdvancedWaypointButton",
            "translated": "UI.Navegação.BotãoDePontoDeReferênciaAvançado",
            "issue": "Tradução e acentuação dos componentes"
        }
    ],
    
    # Erros em comandos do jogo
    "command_errors": [
        {
            "original": "/reply player message",
            "translated": "/responder jogador mensagem",
            "issue": "Tradução do comando"
        },
        {
            "original": "/guild",
            "translated": "/guilda",
            "issue": "Tradução do comando"
        },
        {
            "original": "/leave",
            "translated": "/sair",
            "issue": "Tradução do comando"
        }
    ],
    
    # Erros em valores e unidades
    "value_unit_errors": [
        {
            "original": "$1",
            "translated": "R$1",
            "issue": "Conversão de moeda ($ para R$)"
        },
        {
            "original": "L60",
            "translated": "Nv60",
            "issue": "Tradução de abreviação de Level"
        },
        {
            "original": "Lvl 50",
            "translated": "Nível 50",
            "issue": "Tradução de abreviação"
        },
        {
            "original": "Rank 10",
            "translated": "Nível 10",
            "issue": "Tradução incorreta de Rank para Nível"
        }
    ],
    
    # Erros em extensões de arquivo
    "file_extension_errors": [
        {
            "original": "EventCredits.prototype",
            "translated": "CréditosDoEvento.protótipo",
            "issue": "Tradução da extensão .prototype"
        },
        {
            "original": "config.json",
            "translated": "configuração.json",
            "issue": "Tradução do nome do arquivo"
        }
    ],
    
    # Erros em nomes de classes e identificadores
    "class_identifier_errors": [
        {
            "original": "UIDialogTitle",
            "translated": "UITítuloDoDiálogo",
            "issue": "Tradução e acentuação em identificador"
        },
        {
            "original": "ErrorMessage",
            "translated": "MensagemDeErro",
            "issue": "Tradução de identificador"
        },
        {
            "original": "UITextSocialDialogCreditCardOptionDiscountText",
            "translated": "UITextoOpçãoDesconto CartãoDeCrédito",
            "issue": "Quebra da estrutura do identificador"
        }
    ],
    
    # Erros em tokens @
    "token_errors": [
        {
            "original": "@PlayerName",
            "translated": "@NomeDoJogador",
            "issue": "Tradução do token"
        },
        {
            "original": "@UIConfirmationDialogTitle",
            "translated": "@UITítuloDiálogoConfirmação",
            "issue": "Tradução e acentuação do token"
        }
    ],
    
    # Erros de espaçamento em símbolos
    "spacing_errors": [
        {
            "original": "10%",
            "translated": "10 %",
            "issue": "Espaço adicionado antes do símbolo %"
        },
        {
            "original": "{valor}",
            "translated": "{ valor }",
            "issue": "Espaços adicionados dentro das chaves"
        },
        {
            "original": "[Status]",
            "translated": "[ Status ]",
            "issue": "Espaços adicionados dentro dos colchetes"
        }
    ]
}

# Padrões de regex para detectar os erros
TRANSLATION_ERROR_PATTERNS = {
    "hashtag_placeholders": {
        "original_pattern": r"#\d+\[([^\]]+)\]",
        "error_patterns": [
            r"#\d+\[[^\]]*?([áéíóú][^\]]*?)\]",  # Acentos dentro do placeholder
            r"#\d+\[[^\]]*?([A-Z][^\]]*?[a-z]+|[a-z][^\]]*?[A-Z]+[^\]]*?)\]",  # Capitalização alterada
        ]
    },
    
    "dollar_variables": {
        "original_pattern": r"\{\{\$([A-Za-z0-9_]+)\}\}",
        "error_patterns": [
            r"{{\$([A-Za-zÀ-ÿ][A-Za-z0-9À-ÿ_]*)}}",  # Caracteres acentuados
            r"{{\$([^}]*(?:Do|Da|De|Dos|Das)[^}]*)}}",  # Tradução de estrutura
        ]
    },
    
    "internal_links": {
        "original_pattern": r"\[\[([^\]]+)\]\]",
        "error_patterns": [
            r"\[\[(?:[^/\]]*?[áéíóúàèìòùâêîôûãõç]+[^/\]]*?/)+[^\]]+\]\]",  # Acentos no caminho
            r"\[\[([^/\]]*?(?:Itens|Jogadores|Diálogos)[^/\]]*?/)+[^\]]+\]\]",  # Tradução de caminhos
        ]
    },
    
    "html_tags": {
        "original_pattern": r"<[/]?[a-zA-Z]+[^>]*>",
        "error_patterns": [
            r"<([a-zA-Z]+)\s+([a-zA-ZÀ-ÿ]+)=",  # Atributos com acentos
            r"<([a-zA-Z]+)\s+[^>]*(?:alinhamento|sabor|fonte)[^>]*>",  # Atributos traduzidos
        ]
    },
    
    "dot_properties": {
        "original_pattern": r"[a-zA-Z0-9_\.]+",
        "error_patterns": [
            r"([A-Za-zÀ-ÿ]+)\.([A-Za-z]+)",  # Primeiro componente com acentos
            r"([A-Za-z]+)\.([A-Za-zÀ-ÿ]+)",  # Segundo componente com acentos
        ]
    },
    
    "commands": {
        "original_pattern": r"/([a-zA-Z]+)",
        "error_patterns": [
            r"/([a-zA-ZÀ-ÿ]+)",  # Comandos com acentos
            r"/(responder|sair|guilda|ajuda)",  # Comandos traduzidos
        ]
    },
    
    "level_rank": {
        "original_pattern": r"(L|Lvl|Level|Rank)\s*(\d+)",
        "error_patterns": [
            r"(Nv|Nível|Niv)\.?\s*(\d+)",  # Tradução de Level
            r"Rank\s*(\d+)",  # Mantendo Rank (correto)
        ]
    },
    
    "file_extensions": {
        "original_pattern": r"([A-Za-z0-9_\-]+)\.([a-zA-Z]+)",
        "error_patterns": [
            r"([A-Za-z0-9_\-]+)\.(protótipo|configuração|texto)",  # Extensões traduzidas
        ]
    },
    
    "tokens": {
        "original_pattern": r"@([A-Za-z0-9_]+)",
        "error_patterns": [
            r"@([A-Za-zÀ-ÿ][A-Za-z0-9À-ÿ_]*)",  # Tokens com acentos
        ]
    },
    
    "spacing": {
        "original_pattern": r"(\d+%|\{\}|\[\]|\$\d+)",
        "error_patterns": [
            r"\d+\s+%",  # Espaço antes de %
            r"\{\s+[^\}]*\s+\}",  # Espaços dentro de chaves
            r"\[\s+[^\]]*\s+\]",  # Espaços dentro de colchetes
            r"R\$\s*\d+",  # Conversão de moeda
        ]
    }
}

# Função para gerar relatório completo
def generate_error_report():
    report = "# Relatório de Erros de Tradução\n\n"
    total_errors = 0
    
    for category, errors in DETECTED_TRANSLATION_ERRORS.items():
        report += f"## {category.replace('_', ' ').title()}\n"
        report += f"Total de erros: {len(errors)}\n\n"
        total_errors += len(errors)
        
        for error in errors:
            report += f"- Original: `{error['original']}`\n"
            report += f"  Traduzido: `{error['translated']}`\n"
            report += f"  Problema: {error['issue']}\n\n"
    
    report += f"## Resumo\n"
    report += f"Total de erros detectados: {total_errors}\n"
    
    return report

# Função para criar regex de exclusão
def create_exclusion_regex():
    exclusion_patterns = []
    
    for pattern_type, data in TRANSLATION_ERROR_PATTERNS.items():
        exclusion_patterns.append({
            "name": pattern_type,
            "pattern": data["original_pattern"],
            "exclude": True,
            "message": f"Pattern {pattern_type} should not be translated"
        })
    
    # Padrões adicionais específicos
    additional_patterns = [
        r"Marvel Universe",
        r"[A-Z][A-Za-z]+[A-Z][A-Za-z]+",  # CamelCase
        r"UI[A-Za-z]+",
        r"[\w]+\.prototype",
        r"\$[A-Za-z0-9_]+",
        r"@[A-Za-z0-9_]+",
        r"</?[a-zA-Z]+[^>]*>",
        r"#\d+\[[^\]]+\]",
        r"\[\[.*?\]\]",
        r"/[a-zA-Z]+",
    ]
    
    for i, pattern in enumerate(additional_patterns):
        exclusion_patterns.append({
            "name": f"additional_pattern_{i+1}",
            "pattern": pattern,
            "exclude": True,
            "message": f"Additional pattern {i+1} should not be translated"
        })
    
    return exclusion_patterns
