# Verificação — JV Busca — 14/11/2026

## Testes concluídos

- 35 testes Python passaram: API, filtros, cache, validação, proteção dos arquivos privados, erros, persistência, deduplicação, categorias e detalhes.
- 10 testes da extensão passaram: preços decimais, preço em milhares chineses, ausência de preço, verificação, paginação com troca de IDs, recusa de página repetida, salto além das dez páginas visíveis e proteção de retomada.
- 7 testes do frontend em DOM simulado passaram: destaques, 29 páginas de categoria, marca JV, ausência de controles JSON, ícones SVG, fotos nos banners, favoritos, filtros, galeria e anúncio ausente.
- 34 rotas HTTP de páginas e recursos responderam 200 na verificação anterior desta sessão.

## Evidência com o Goofish real

A conexão 0.3.1 foi confirmada pela API. A coleta de celulares salvou 330 anúncios únicos e foi encerrada nessa quantidade por solicitação do usuário. A coleta seguinte está direcionada a computadores, eletrônicos, roupas e esportes, nessa ordem.

O avanço além da página 10 funcionou com anúncios reais de Computadores. Cada página é deduplicada por ID e persistida antes do avanço. Um produto também teve três fotografias únicas salvas na ficha; isso não significa que todas as galerias foram coletadas.

As contagens evoluem durante a coleta. Consulte `/api/catalog` para a contagem por categoria e o estado atual, e `public/data/products.json` para os anúncios disponíveis no site.

## Limites da validação

Os testes do frontend usam DOM simulado. Não foi concluída uma nova revisão visual em um celular real. Os testes da extensão simulam controles de página; o avanço real foi confirmado separadamente pela coleta.

A implantação Cloudflare descrita em `IMPLEMENTACAO-CLOUDFLARE.md` ainda não foi executada. Não há evidência de que o Goofish aceite a sessão em Browser Run até que a prova de acesso descrita no documento seja realizada.

## Reproduzir

```powershell
.venv/Scripts/python.exe -m unittest -q
node --test test_extension.cjs test_shop.cjs
```
