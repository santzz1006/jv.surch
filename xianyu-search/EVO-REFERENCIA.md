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

Código: `extension-shop/`. Pacote público: `public/downloads/goofish-br-extensao-1.0.0.zip`. Guia público: `public/extensao.html`.

| Recurso | Versão Goofish Br 1.0.0 |
|---|---|
| Busca | Catálogo Goofish Br ou abertura da busca original |
| CNY para BRL | Cotação manual e rótulos opcionais na aba |
| Anúncios salvos | Captura explícita dos dados visíveis; até 1.000 itens |
| Pastas, filtro e ordenação | Disponíveis localmente |
| Fornecedores | Cadastro pessoal de links; até 500 lojas |
| Envio para agente | Cópia de texto e link; envio manual pelo usuário |
| Variação de preço | Compara ao capturar novamente, sem monitoramento automático |
| Fotos e descrição | Preserva os dados disponíveis; sem tradução automática |
| IA, QC, rastreio, agentes afiliados, alertas automáticos | Não implementados nesta versão |
| Conta e sincronização remota | Não implementadas; armazenamento local |
| Coleta autenticada para API | Continua sendo responsabilidade da extensão local anterior |

Esta é uma extensão independente, não uma cópia integral funcional da EVO. Implementar os recursos remotos restantes exige serviços próprios e validação das integrações. Nenhuma credencial da EVO é necessária para usar a versão entregue.

## Validação

`node --test test_extension_shop.cjs test_shop.cjs test_extension.cjs`

Os testes exercitam captura em DOM de teste, proteção de URLs, preços, persistência, pastas, cópia, pesquisa, mudanças de preço e ausência de serviços de terceiros no pacote. A instalação e o funcionamento com anúncios reais na sessão do usuário não foram validados nesta entrega.

Documentação de permissões usada: https://developer.chrome.com/docs/extensions/develop/concepts/activeTab
