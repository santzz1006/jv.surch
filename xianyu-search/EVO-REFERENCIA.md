# Referência EVO Society e versão Goofish Br

## Download

Solicitado: https://addon.evosociety.com.br/invite?download

O JavaScript público da página aponta para a Chrome Web Store, extensão `ehccdfjhomilgnfbkaobioolcchaoogd`. O pacote foi baixado do serviço oficial de distribuição do Chrome, sem instalar ou executar código da EVO.

- Versão informada no manifesto: **5.5**.
- Pacote CRX3: **14.332.527 bytes**.
- Conteúdo extraído: **429 arquivos e uma entrada de diretório**.
- SHA-256 CRX: `f7cac5c9b23dc49db37b77fe8a342f3a9779e0db52cd99b5f6fc5901cf9ff661`.
- Originais: `references/evo-original/package.crx`, `package.zip` e `files/`.
- O original fica disponível localmente; está excluído do Git e do site público.

## O que o pacote contém

Manifesto, scripts de interface e integração, popup, estilos, fontes, ícones, banners, imagens de fornecedores e outros recursos distribuídos com a extensão. Foram inspecionados o manifesto e trechos dos scripts para identificar as dependências.

O pacote cliente referencia serviços de autenticação, armazenamento remoto, consulta de anúncios, planos, integrações com agentes e recursos de IA. O código e os dados privados desses servidores não estão no download. Não foram copiadas contas, chaves de sessão, bases privadas, códigos de afiliados nem feitas consultas autenticadas aos servidores da EVO.

## Implementação própria

Código: `extension-shop/`. Pacote atual: `public/downloads/goofish-br-extensao-1.1.0.zip`. Backend: `cloudflare/`. Guia público: `public/extensao.html` e `public/cloudflare.html`.

| Recurso | Versão Goofish Br 1.1.0 |
|---|---|
| Busca | Catálogo Goofish Br ou abertura da busca original |
| CNY para BRL | Cotação manual ou consulta diária opcional; rótulos na aba |
| Anúncios salvos | Captura explícita dos dados visíveis; até 1.000 itens |
| Pastas, filtro e ordenação | Disponíveis localmente |
| Fornecedores | Cadastro pessoal de links; até 500 lojas |
| Envio para agente | Cópia de texto e link; envio manual pelo usuário |
| Variação de preço | Captura manual ou cron remoto preparado; requer fonte acessível |
| IA e tradução | Código pronto para Workers AI; conta e ativação pendentes |
| QC | Análise de fotos enviadas pelo usuário; referência opcional; sem importação de pedidos |
| Busca por imagem | IA gera termos para pesquisa; não é índice visual do marketplace |
| Mensagem ao vendedor | Rascunho traduzido, sem envio ou chat integrado |
| Rastreio | Códigos, notas e links manuais; sem consulta automática à transportadora |
| Comparação de agentes | Soma produto/frete das propostas cadastradas; sem cotação automática |
| Sincronização remota | API pessoal com chave e proteção contra conflitos; aguarda Cloudflare |
| Coleções | Links, atualização após sincronizar, colaboração por código e revogação |
| Coleta autenticada para API | Continua sendo responsabilidade da extensão local anterior |

Esta é uma extensão independente, não uma cópia integral funcional da EVO. Implementar os recursos remotos restantes exige serviços próprios e validação das integrações. Nenhuma credencial da EVO é necessária para usar a versão entregue.

## Validação

`node --test test_extension_shop.cjs test_dashboard.cjs test_shop.cjs test_extension.cjs cloudflare/test/worker.test.mjs`

Os testes exercitam DOM, URLs, persistência, cópia, IA simulada, notificações, API com SQLite real, autenticação, limites, sincronização, conflitos, compartilhamento, colaboração e exclusão. O Wrangler empacotou o Worker e aplicou a migração ao D1 local. Não houve implantação na Cloudflare, chamada real de IA ou instalação da nova extensão no navegador do usuário.

Uma consulta HTTP pública ao anúncio real `1085868013932` retornou HTML sem dados estruturados verificáveis para o adaptador. O adaptador recusou o conteúdo, preservando a distinção entre falha de coleta e produto vendido. Isso confirma a necessidade de validar uma fonte acessível/coletor para alertas reais; não demonstra que a sessão autenticada esteja indisponível.

Documentação de permissões usada: https://developer.chrome.com/docs/extensions/develop/concepts/activeTab
