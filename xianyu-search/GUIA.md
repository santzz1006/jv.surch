# Seu buscador local de Xianyu

## O que já foi implementado

Interface com estilos próprios, busca, preço mínimo/máximo em yuan, ordenação, paginação dos resultados coletados, cache de cinco minutos e API Python. O coletor usa Playwright para ler anúncios renderizados em um Chromium local, sem API paga.

**No teste real de 13/11/2026, a consulta “rtx 3060” retornou bloqueio de login nesta sessão.** O coletor detectou a exigência e parou. Não foram obtidos anúncios. Portanto, a busca sem conta ainda NÃO está funcionando; os filtros e a API foram validados separadamente. Login, CAPTCHA, bloqueio regional, alterações no HTML e indisponibilidade podem impedir a coleta. O adaptador DOM precisa ser validado com anúncios reais em uma sessão disponível. O backend de terceiros não faz parte deste projeto.

## 1. Instalar e iniciar no Windows

Abra PowerShell nesta pasta:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
.\.venv\Scripts\python.exe server.py
```

Abra http://127.0.0.1:8081. Nas próximas vezes, execute `iniciar.ps1`. O navegador do coletor fica visível durante a busca e fecha ao terminar. Não execute duas instâncias usando o mesmo perfil. O servidor só escuta neste computador.

As dependências e o Chromium já foram instalados neste computador durante a preparação. Você pode começar diretamente pelo `iniciar.ps1`; os comandos acima servem para reinstalar ou levar o projeto para outro computador.

## 2. Fluxo da API

```text
Campo de busca → GET /api/search → scraper.collect()
             → navegador abre o Xianyu
             → leitura dos anúncios visíveis
             → normalização em JSON → cache → filtros → cartões
```

Exemplo, com o servidor em execução:

```powershell
Invoke-RestMethod 'http://127.0.0.1:8081/api/search?q=rtx%203060&min=100&max=3000&sort=asc&page=1'
```

Parâmetros: `q` (1–120 caracteres), `min`, `max` (yuan), `sort` (`relevance`, `asc`, `desc`), `page` (começa em 1). Retorna `items`, `total`, `collected`, `page`, `hasMore`, `cached`, `query`. Cada item contém `id`, `title`, `image`, `priceCny` e `url`. Preço ausente vira `null`, nunca zero inventado.

Os filtros abrangem somente os anúncios carregados nessa coleta (até 60 links inspecionados). A paginação divide essa lista em grupos de 20; não percorre todas as páginas do Xianyu. Não há tradução automática ou cotação de moedas. Os títulos permanecem como publicados.

## 3. Se pedir login ou CAPTCHA

Na prévia web, use **Abrir sessão do Xianyu**. Entre pessoalmente na janela aberta e, quando terminar, volte à prévia e clique em **Salvar sessão**. Em seguida faça uma nova busca. Salvar só encerra a janela e persiste o perfil: não confirma que o login foi aceito. Enquanto a janela de sessão estiver aberta, a API bloqueia buscas para não disputar o mesmo perfil.

`GET /api/health` informa a saúde da API e o resultado da última consulta à fonte. `POST /api/session/open` abre a janela; `POST /api/session/finish` encerra a sessão manual. Esses endpoints só aceitam chamadas locais. Os filtros operam sobre os anúncios coletados e não acrescentam anúncios ao cache.

O coletor para e retorna uma mensagem, sem tentar contornar a proteção. Para abrir a sessão manual:

```powershell
.\.venv\Scripts\python.exe scraper.py --login
```

Se você tiver uma conta aceita pelo Xianyu, entre pelo fluxo normal no navegador. Resolva pessoalmente qualquer verificação apresentada. Volte ao terminal e pressione Enter para fechar e persistir a sessão. Depois inicie o servidor novamente. Se você não tiver uma conta e o site exigir login, esta abordagem não atende ao objetivo de pesquisar sem conta; não há como prometer resolver isso só com código gratuito.

O perfil é salvo em `.browser-profile/`, fora da pasta pública. Ele contém dados sensíveis da sessão: não compartilhe, não faça upload e não versione. O `.gitignore` já exclui essa pasta.

## 4. Adaptar o coletor quando o HTML mudar

1. Abra uma busca normal no Xianyu e confirme que há anúncios visíveis.
2. Nas ferramentas de desenvolvedor do navegador, inspecione um cartão de anúncio.
3. Localize o link do produto, o título, a imagem e o texto de preço dentro do mesmo cartão.
4. Em `scraper.py`, ajuste `page.locator('a[href*="/item?"]')` e a função `evaluate_all` para a estrutura observada. A implementação inicial presume que o conteúdo do cartão fica dentro do link.
5. Confira manualmente alguns títulos, URLs e preços antes de confiar nos dados. Evite seletores que incluam recomendações, anúncios patrocinados ou elementos fora da grade desejada.
6. Se não houver preço legível, mantenha `null`. Se a estrutura não for reconhecida, devolva erro em vez de produtos falsos.

Não reutilize tokens de outros sites, endpoints protegidos de terceiros ou serviços para contornar CAPTCHA. Este projeto apenas lê o conteúdo que a sessão normal consegue ver.

## 5. Testar e evoluir

```powershell
.\.venv\Scripts\python.exe -m unittest -v
```

Os 20 testes automatizados verificam filtros, paginação, preços ausentes, separador de milhares, deduplicação, validação HTTP, cache e expiração, concorrência, limite de consultas, sessão e rejeição de origens/arquivos privados. O coletor é simulado nos testes HTTP; esses testes não demonstram acesso real ao Xianyu. O fluxo real é verificado separadamente na prévia.

Para publicar, será necessário um servidor que execute Python e Chromium, fila de coleta, limites de uso, proteção da sessão e validação do acesso permitido pela fonte. Este servidor de desenvolvimento não está preparado para exposição pública. Hospedagem e disponibilidade contínua não estão garantidas gratuitamente. Um site pode dispensar o login dos visitantes e ainda depender de uma sessão mantida pelo operador; são coisas diferentes.

Referência do destino: https://www.goofish.com/ . A implementação não usa o serviço pago pesquisado e não faz chamadas a Apify ou JustOneAPI.
