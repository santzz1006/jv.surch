# Publicar Goofish Br na Chrome Web Store

A EVO usa uma página da Chrome Web Store. Para oferecer a mesma instalação pelo botão “Usar no Chrome”, a Goofish Br precisa de sua própria publicação. Não existe uma página aprovada da Goofish Br na loja nesta entrega.

## Preparado neste projeto

- ZIP instalável: `public/downloads/goofish-br-extensao-1.3.0.zip`, com manifesto na raiz.
- Manifest V3, código JavaScript empacotado localmente, ícones 16/48/128 e permissões opcionais para nuvem, cotação e notificações.
- Aviso de privacidade público: `https://santzz1006.github.io/jv.surch/xianyu-search/public/privacidade-extensao.html`.
- Guia de instalação e limitações: `public/extensao.html`.
- Testes da extensão/API e pacote do servidor Cloudflare.

## O que ainda depende da sua conta e da revisão

1. Cadastre uma conta de desenvolvedor no painel oficial: https://chrome.google.com/webstore/devconsole . O Google exige taxa única de cadastro; confira o valor exibido no painel antes de pagar. Nenhuma taxa foi paga nesta entrega.
2. Revise os direitos de uso da marca e do mascote antes da submissão. A extensão é um projeto independente, não a extensão oficial do Goofish nem da EVO.
3. Crie um item e envie o ZIP. Preencha nome, descrição, categoria, idioma, contato e privacidade.
4. Faça capturas reais da extensão instalada para a ficha da loja. Elas não foram produzidas nesta entrega. Siga os tamanhos e demais requisitos mostrados no painel.
5. Complete as declarações de dados e de permissões, compatíveis com o aviso público. Recursos online precisam estar configurados e disponíveis para validação. Explique como o revisor acessa e testa esses recursos sem divulgar sua chave pessoal publicamente.
6. Envie para revisão. Publicação e aprovação não foram executadas nem garantidas.
7. Depois da aprovação, use o link real retornado pelo Google no botão de instalação do site. Não use o ID da EVO.

## Texto sugerido para a ficha

**Nome:** Goofish Br — Seus achados

**Resumo:** Organize anúncios do Goofish, veja preços em reais e prepare seus achados para conversar com seu agente.

**Descrição:** Salve anúncios visíveis, organize em pastas, registre lojas, compare propostas informadas pelos agentes e copie informações com o link original. A extensão oferece conversão manual e consulta opcional de cotação. No painel completo, uma API Cloudflare configurada pelo usuário habilita busca ao vivo com fonte própria, sincronização e compartilhamento. Alertas de preço dependem de uma fonte acessível. A extensão não realiza compras, não envia mensagens e não garante acesso sem login ao Goofish. Projeto independente, sem vínculo oficial com Goofish/Xianyu ou EVO Society.

## Finalidade e permissões

Finalidade única proposta: organizar a descoberta e avaliação de anúncios para importação.

| Permissão | Uso real |
|---|---|
| activeTab e scripting | Ler o anúncio ou acrescentar rótulos de preço após ação explícita na aba Goofish |
| storage | Preferências, coleção local e conexão opcional à API |
| alarms | Consultar eventos da API a cada trinta minutos quando ativado |
| notifications, opcional | Avisar mudanças confirmadas nos anúncios acompanhados |
| domínio workers.dev, opcional | Conectar somente a API escolhida pelo usuário |
| open.er-api.com, opcional | Consultar cotação quando o usuário solicitar |

O pacote não lê cookies, histórico, senhas, mensagens ou pedidos. O painel envia termos à fonte de busca ao vivo quando solicitado e coleção à nuvem quando sincronizada. Não há código remoto executável, anúncios ou afiliados embutidos. Essas informações devem ser conferidas no formulário real; não marque declarações incompatíveis com a versão enviada.

## Fontes oficiais

- Cadastro e taxa: https://developer.chrome.com/docs/webstore/register
- Publicação e revisão: https://developer.chrome.com/docs/webstore/publish
- Instalação externa no Windows/macOS: https://developer.chrome.com/docs/extensions/how-to/distribute/install-extensions

## Atualização 1.3.0
Resultados e detalhes no popup, catálogo de 46.011 anúncios e atalho opcional no Goofish. Declarar os hosts goofish.com/www.goofish.com e o content script de interface; não captura automaticamente anúncios nem cookies. Preparar novas imagens da interface antes da submissão.
