# EVO Society 5.5 — análise técnica e equivalência Goofish Br 1.2

Inventário completo do pacote distribuído: 429 arquivos. Lista e hashes em EVO-INVENTARIO.csv. Originais em references/evo-original/. A análise é estática do cliente e das interfaces públicas; o código do servidor não veio no download.

## Busca sem login: o que foi encontrado

- background.js:9324–9355: evoXyBuscar lê evoTokenConta e chama POST https://addon.evosociety.com.br/api/xianyu-buscar com Authorization Bearer. Comentário do cliente identifica UnitBytes e custo de API.
- content.js:16400 em diante: visitante consulta buscar_catalogo_xianyu; usuário PRO combina busca ao vivo e acervo. A busca gratuita do cliente é um catálogo, não uma consulta direta ilimitada ao Goofish.
- Teste sem sessão em /api/xianyu-buscar: HTTP 401, corpo "sem sessão". Nenhum token foi reutilizado.
- Teste normal no H3X /api/search: HTTP 401. Não foi contornada a verificação.
- goofish-anuncio.js: alterna APIs de detalhe desktop/móvel e usa proxy remoto como fallback. Detalhe de anúncio não é API de pesquisa de catálogo.
- O fornecedor documenta cobrança por resultado: https://github.com/unitbytes/Goofish-Xianyu-Scraper-API .

## O que funciona na implementação própria

- Catálogo empacotado com 4.720 anúncios, sem conta chinesa e sem servidor local para pesquisar.
- Filtros de categoria, palavra/modelo, preço, cor e condição citadas no texto; ordenação e paginação.
- Galeria, informações disponíveis do vendedor, original preservado, preços em yuan e reais estimados.
- Favoritos, pastas, lojas, backup/importação e captura explícita do anúncio aberto.
- Conversor de links e rotas de agentes sem afiliados. Hubbuy aceitou a URL de teste (HTTP 200); CSSBuy retornou 403 ao cliente automatizado. Isso não confirma disponibilidade de compra.
- Sincronização privada, compartilhamento, colaboração, notificações e alertas com backend próprio preparado para Cloudflare.
- Fonte arredondada Junegull e três banners na página de download. Recursos dependentes de IA retirados.

## Dependências que impedem equivalência integral

- Busca ao vivo e dados atualizados: precisam de fonte acessível/coletor próprio. O adaptador está implementado, sem fonte ativa nesta entrega.
- Chat com vendedor: exige serviço autenticado e sessão; não foi implementado nem foram lidas mensagens privadas.
- Álbuns QC/pedidos/rastreio automático: dependem das contas e APIs dos agentes/transportadoras; só organização manual de links e códigos está implementada.
- Banco de fornecedores, contas e assinaturas EVO: dados e serviços remotos não estão no pacote. Não foram copiados ou contornados.
- Contas públicas independentes: backend atual é espaço pessoal com chave; não é serviço multiusuário público.
- Tradução online da EVO usa serviço externo. A versão própria preserva traduções já salvas e não chama o serviço deles.

## Mensagens cliente/servidor encontradas no pacote

### background.js

`analisarAnuncioIA`, `buscaVisual`, `buscarPorImagem`, `conferirPlano`, `estaturaPuxar`, `estaturaSalvar`, `estaturaSincronizar`, `evo17Captcha`, `evo17Resultado`, `evo17Sincronizar`, `evoAbrirFotoNovaAba`, `evoAnalisarQc`, `evoAtividade`, `evoAutorizarSalvos`, `evoBatchAlbuns`, `evoCantosAbrir`, `evoCapaYupoo`, `evoChatAssinarVideo`, `evoChatDigitar`, `evoChatOnline`, `evoChatPrevia`, `evoChatSom`, `evoChatStatus`, `evoChatSubirImagem`, `evoChatVisto`, `evoFotoDoProduto`, `evoHbInvoice`, `evoImagemBytes`, `evoNegCheckout`, `evoNegEnviar`, `evoNegImagens`, `evoNotifSincronizar`, `evoPedirAmizade`, `evoRastreio17Agora`, `evoRastreio17Permitir`, `evoRastreio17Status`, `evoRastreioAtualizar`, `evoRpc`, `evoSalvosPermitido`, `evoTermoBuscaIA`, `evoTraduzirParaChines`, `evoVariantesDoProduto`, `evoXyAcervo`, `evoXyBuscar`, `evoXyCabecalho`, `evoXyClassificar`, `evoXyDetalhe`, `evoXyLerLoja`, `fetchProductInfo`, `fetchProductPrice`, `fetchQcAlbums`, `forcarUpdateCotação`, `lerTabelaMedidas`, `melhoresBatchs`, `qcCacheMorto`, `reportarAgente`, `resolveUrl`, `sincronizarConta`, `uufindsProduto`, `weidianIdDoOffer`

### content.js

`atualizarPrecos`, `evo_seller_data_found`, `mudarAutoTraducao`, `mudarBloqueador`, `mudarLingua`

## Arquivos de integração relevantes

manifest.json: permissões, mundos de execução e recursos públicos. background.js: despacho, autenticação e chamadas remotas. content.js: telas injetadas, filtros e leitura do DOM. popup.js: conta, planos e configuração. conversor.js: reconhecimento de plataformas e formatos dos agentes. goofish-anuncio.js: detalhe móvel/desktop e fallback remoto. pastas.js: organização de coleção. Nenhuma chave ou token é reproduzido neste relatório.
