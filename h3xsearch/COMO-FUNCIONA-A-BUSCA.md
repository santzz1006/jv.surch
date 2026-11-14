# Como funciona a procura de produtos

Análise estática do arquivo original `site/assets/index-SN2rHd-V.js` e da configuração pública `site/api/config`. O fluxo de resultados não foi validado ponta a ponta porque depende da sessão e da verificação humana do site.

## Não é um filtro de catálogo local

O frontend React envia a consulta ao backend e renderiza `items` na ordem recebida. Não foi encontrado filtro local de preço, categoria ou ordenação de produtos no bundle analisado. As operações `filter` e `sort` presentes nessa parte do código tratam principalmente de tags e números da paginação.

## Sequência das requisições

1. `GET /api/config` obtém nome do site, links da comunidade e cadastro, chave pública do Turnstile e `perPage: 20`.
2. O frontend solicita a verificação Cloudflare Turnstile usando essa chave pública.
3. `POST /api/session`, com JSON `{ "turnstileToken": "<resultado da verificação>" }`, solicita uma sessão. O código espera receber `token` e `expiresAt`. Nenhum token de sessão foi salvo nesta cópia.
4. `GET /api/search?q=rtx+3060&page=1&lang=pt` envia a busca com o cabeçalho `X-Session: <token>`. Quando a tradução está ativada, acrescenta `translate=1`.
5. A tela renderiza os produtos retornados e a paginação. O algoritmo interno de consulta, classificação e tradução roda no servidor e não é revelado pelo bundle.

Todos esses caminhos são relativos à origem. Servir a cópia em localhost faz as chamadas apontarem para localhost; o servidor estático não implementa a API. Apontar somente as URLs para o domínio original também não recria o backend nem resolve os controles de sessão e origem.

## Parâmetros e comportamento da interface

| Controle | Comportamento observado no código |
| --- | --- |
| Texto | Campo com limite de 120 caracteres; a consulta lida da URL passa por `trim()` |
| URL da página | `q`, `page` e `tr=1` |
| URL da API | `q`, `page`, `lang` e, opcionalmente, `translate=1` |
| Página | Limitada de 1 a 50 no frontend; próxima página depende de `hasMore` |
| Idioma | Português, inglês ou chinês; tradução de busca é desativada para interface chinesa |
| Tradução | Preferência guardada no localStorage em `h3x.translate`; termos/modelos podem ser enviados literalmente |
| Sugestões | Botões de sugestões iniciam busca com tradução habilitada, exceto em chinês |
| Nova busca/tradução | Reinicia a paginação na primeira página |
| Navegação | Atualiza o histórico e lê mudanças com `popstate` |

## Formato de dados consumido

O frontend acessa os campos abaixo. Esta é uma descrição inferida dos acessos no código, não uma resposta de produtos capturada nem um contrato completo da API.

- Resposta: `items`, `page`, `hasMore`, `query.translated`, `rate`, `translationPending`.
- Produto: `id`, `title`, `titleTranslated`, `image`, `priceBrl`, `priceCny`, `area`, `wantCount`, `tags`, `buyUrl`.
- Mostra o título traduzido quando não vazio; caso contrário, usa o original.
- Os preços em reais e yuan já chegam nos campos da resposta; o componente formata os valores.
- Exibe no máximo duas tags não vazias e abre `buyUrl` na Hubbuy.
- Os 20 cartões de carregamento são placeholders, não prova de uma lista de produtos baixada.

## Sessão, atualização e falhas

- A sessão é renovada aproximadamente um minuto antes de expirar. Se não houver mais de cinco segundos de validade, uma nova sessão é solicitada.
- Em `UNAUTHORIZED`, o cliente tenta renovar a sessão e repetir a busca uma vez.
- Se `translationPending` vier verdadeiro, repete a consulta uma vez após 2,5 segundos.
- `AbortController` cancela consultas antigas quando os parâmetros mudam.
- `RATE_LIMITED` bloqueia temporariamente o envio conforme `retryAfter`; na ausência do valor usa 30 segundos.
- Também trata `INVALID_QUERY`, `BUSY`, `UPSTREAM`, problemas de rede e falhas da verificação.

## O que falta para uma implementação independente

É necessário implementar um backend próprio com uma fonte autorizada de anúncios, busca, paginação, tradução e conversão de moeda. Esses serviços não foram obtidos ao baixar os arquivos públicos. Não existe nesta captura um JSON completo de produtos que possa substituir o backend original.
