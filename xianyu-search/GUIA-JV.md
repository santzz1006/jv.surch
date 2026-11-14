# JV Busca

## Abrir

Execute `iniciar.ps1` nesta pasta e abra http://127.0.0.1:8081.
O catálogo, os favoritos, a navegação por categoria e os filtros não precisam da extensão. As fotos dos vendedores e produtos continuam hospedadas na fonte original e exigem internet.

## Coleta usando sua sessão

O servidor local envia consultas à extensão **JV Busca — conexão local 0.3.1**, instalada no Chrome em que você entrou no Goofish. Ela lê anúncios renderizados, sem exportar cookies, senha, pedidos ou mensagens. A API fica em `127.0.0.1:8081`, acessível somente nesta máquina.

A interface pública não exibe controles administrativos nem referências ao formato dos arquivos. Para iniciar a coleta pelo PowerShell:

```powershell
# Meta de 1.000 anúncios únicos em cada categoria prioritária:
Invoke-RestMethod -Method Post http://127.0.0.1:8081/api/catalog/deep

# Acompanhar progresso, página atual e erros:
(Invoke-RestMethod http://127.0.0.1:8081/api/catalog).collection

# Coletar as demais categorias ainda vazias:
Invoke-RestMethod -Method Post http://127.0.0.1:8081/api/catalog/collect
```

Prioridades atuais: roupas e esportes, depois a retomada de eletrônicos. Computadores atingiu 1.020 anúncios e celulares foi encerrado com 330, conforme solicitado. A meta das demais categorias continua em 1.000 anúncios únicos. Roupas reúne buscas de moda masculina, feminina, tênis, casacos e jeans. Esportes reúne tênis de corrida, roupas esportivas, equipamentos de academia, basquete e badminton. Cada termo tem um progresso independente, preservado na retomada, e os IDs repetidos são eliminados dentro da categoria.

A meta não é uma garantia: cada busca percorre no máximo 50 páginas, se disponíveis. Não se inventam registros para preencher quantidade. A coleta para quando faltam controles de paginação, aparecem verificações ou a conexão falha. O progresso confirmado é preservado.

## Busca sem manter o computador ligado

O plano detalhado de migração está em [IMPLEMENTACAO-CLOUDFLARE.md](IMPLEMENTACAO-CLOUDFLARE.md). Inclui navegador remoto, autenticação, API, cache, banco de dados, limites gratuitos e testes de aceitação. A implantação Cloudflare ainda não foi realizada; a busca adicional atual continua usando a conexão local.

O visitante pesquisa primeiro nos anúncios salvos. Quando não há resultados, a busca pode consultar a sessão conectada; os resultados recebidos são persistidos. Escolher japonês permite enviar texto japonês ao Goofish, sem trocar de marketplace ou prometer tradução automática da consulta.

## Traduções e páginas

As traduções são automáticas e locais, usando Argos Translate de chinês para inglês e depois português. Podem conter erros; o texto original é preservado na ficha do produto. Após novas coletas:

```powershell
.venv/Scripts/python.exe translate_catalog.py
.venv/Scripts/python.exe build_site.py
```

Os modelos já foram instalados nesta máquina. Para outra instalação, use `requirements-translation.txt` e `setup_translation.py`. O script retoma os textos ainda não traduzidos.

## Dados e detalhes

O arquivo interno `public/data/products.json` reúne os anúncios únicos, as categorias e traduções. `catalog/` guarda os resultados por categoria e a última página; `live-results.json` guarda resultados de buscas e `details.json` guarda galerias recebidas. Esses dados são necessários ao funcionamento, embora não apareçam como recursos técnicos na interface.

Na ficha, “Atualizar fotos e detalhes” consulta o anúncio original e salva as imagens disponíveis. Nem todo anúncio fornece várias fotos. Vendas, avaliações e reputação só podem ser exibidas quando fornecidas pela fonte; os dados ausentes não são preenchidos com números fictícios.

## Visual

Nome JV Busca, amarelo/preto, fonte Junegull, mascote fornecido pelo usuário, banners com fotos de anúncios, ícones SVG para setas/corações e animações GSAP com respeito à preferência de reduzir movimento. O botão da comunidade permanece desativado até receber um convite do Discord.

## Testes

```powershell
.venv/Scripts/python.exe -m unittest -q
node --test test_shop.cjs test_extension.cjs
```

Os testes locais verificam API, filtros, armazenamento, deduplicação, retomada de páginas e componentes em DOM simulado. Eles não substituem uma coleta real nem a revisão visual em aparelhos móveis.
