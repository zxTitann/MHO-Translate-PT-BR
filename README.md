# MHO-Translate-PT-BR-Ferramenta de Tradução Automatizada para Marvel Heroes Omega

## Visão Geral

O *MHO-Translate-PT-BR* é uma solução avançada de localização desenvolvida em Python para aprimorar significativamente a experiência em português brasileiro do jogo *Marvel Heroes Omega*. Este projeto vai além de uma simples tradução, implementando um sistema inteligente que preserva a integridade técnica dos arquivos do jogo enquanto melhora a qualidade linguística.

## Problemas na Tradução Original do Jogo

- **Tradução incompleta/inconsistente**:

  - Mistura de idiomas em diálogos e descrições

  - Textos originais em inglês mantidos em elementos críticos

  - Falta de padronização em termos do universo Marvel

  - **Tradução incompleta**:  
  Muitos textos não foram traduzidos totalmente, contendo diversos trechos com ingles e portugues misturados em uma unica caixa de dialogo, alem de descrições de itens, nomes de itens, habilidades e outras partes importantes.

## Problemas na Implementação do Script de Tradução

O script possui duas categorias de problemas:

- **Problemas de Formatação Geral**:  
  Inconsistências encontradas atualmente no script de tradução como:
  - Espaços extras indevidos.
  - Quebras de linha afetadas.

- **Problemas de Tradução Indesejada**:
  - Termos cruciais para o jogo (nomes de habilidades, status, itens, referências internas de código como `$param1$`, `#emphasis#`, `condition0`) foram:
  - Traduzidos indevidamente.
  - Tiveram sua formatação alterada (como espaçamentos extras e/ou excluidos).
  - Perderam a capitalização original, o que pode impactar o reconhecimento pelo codigo do jogo.

- **Problemas de Capitalização**:  
  Termos que dependem de capitalização específica para reconhecimento pelo jogo tiveram essa formatação alterada.

## Solução Proposta

Para abordar esses desafios, o script:

1. Utiliza a API do Google Translate (via biblioteca `googletrans`) como base para tradução inicial
2. Implementa lógicas customizadas para:
   - Identificar e corrigir automaticamente os problemas específicos
   - Preservar referências internas e formatação original
   - Manter a capitalização correta de termos técnicos

## Objetivo Final

Gerar arquivos de texto traduzidos para PT-BR que sejam:
✅ Compreensíveis  
✅ Precisos  
✅ Consistentes  
✅ Preservem a integridade das referências internas  
✅ Mantenham a formatação original essencial  

*Resultado:* Uma tradução que funcione corretamente no jogo sem causar quebras ou exibir informações de forma incorreta.