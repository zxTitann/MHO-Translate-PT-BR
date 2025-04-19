# MHO-Translate-PT-BR

## Descrição e Propósito

Este projeto consiste em um script desenvolvido em Python para automatizar e aprimorar o processo de tradução dos arquivos de texto do jogo *Marvel Heroes Omega (MHO)* para o Português Brasileiro (PT-BR).

## Problemas na Tradução Original

O principal motivo para a criação deste projeto reside nos problemas e inconsistências encontrados na tradução original do jogo:

- **Tradução Literal ou Sem Sentido**:  
  Muitos textos foram traduzidos de forma muito literal ou perderam o sentido no contexto do jogo.

- **Termos Técnicos e Referências Internas**:  
  Termos cruciais para o jogo (nomes de habilidades, status, itens, referências de código como `$param1$`, `#emphasis#`, `condition0`) foram:
  - Traduzidos indevidamente
  - Tiveram sua formatação alterada (como espaços extras)
  - Perderam a capitalização original, o que pode impactar o reconhecimento pelo jogo

- **Problemas de Formatação Geral**:  
  Inconsistências como:
  - Espaços extras indevidos
  - Quebras de linha afetadas
  - Outros problemas que prejudicam a leitura e apresentação

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
