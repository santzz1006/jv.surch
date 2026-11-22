# Goofish Br 1.2 — busca, sincronização e alertas na Cloudflare

A pesquisa dos 4.720 anúncios empacotados na extensão funciona sem login e sem Cloudflare. Para novas consultas ao vivo, sincronização entre dispositivos, coleções compartilhadas e alertas, publique a API abaixo. Não há integração com IA nesta versão.

## O que precisa existir para busca ao vivo



## Publicar sua API gratuita

1. Crie uma conta em https://dash.cloudflare.com/sign-up e mantenha o plano Workers Free.
2. Extraia o projeto da API e abra um terminal nessa pasta. Use Node.js 22 ou mais recente; os testes foram feitos no Node 24.
3. Execute:

```powershell
npm ci
npx wrangler login
npx wrangler d1 create goofish-br
```

4. Substitua SUBSTITUA_PELO_ID_DO_D1 em wrangler.jsonc pelo database_id retornado. Mantenha o binding DB.
5. Publique:

```powershell
npx wrangler d1 migrations apply goofish-br --remote
npm run deploy
```

6. Gere uma chave aleatória com pelo menos 32 caracteres no seu gerenciador de senhas. Grave-a como segredo:

```powershell
npx wrangler secret put API_TOKEN
```

7. No painel Nuvem da extensão, informe o endereço https://goofish-br-api.SUA-CONTA.workers.dev e essa chave. Ela é do seu projeto, não o token administrativo da Cloudflare. Não publique a chave no site ou GitHub.

A API representa um espaço pessoal. Use a mesma URL/chave somente nos seus dispositivos. Não distribua essa chave aos visitantes: isso daria acesso à mesma coleção. Um serviço público com contas separadas exige autenticação e isolamento por usuário adicionais.

Não foi criada uma conta nem ativado plano pago nesta entrega. O código e a migração foram testados localmente; a implantação real depende de sua conta. Franquias gratuitas têm limites: confira https://developers.cloudflare.com/workers/platform/limits/ e https://developers.cloudflare.com/d1/platform/limits/ .

## Conectar sua fonte de busca

No painel do Worker, configure a variável:

```text
SEARCH_SOURCE_URL=https://SEU-COLETOR
```

Se o coletor exigir chave, use:

```powershell
npx wrangler secret put SEARCH_SOURCE_TOKEN
```

O Worker consulta GET /search?q=TERMO&page=1&limit=48&min=0&max=1000 nessa base. min e max são opcionais e expressos em yuan. A chave, se configurada, vai no cabeçalho Authorization: Bearer. A resposta deve ser:

```json
{
  "items": [{
    "id": "ID-NUMERICO-REAL",
    "title": "Título em português, se disponível",
    "titleOriginal": "Título original",
    "description": "Descrição observada",
    "priceCny": 100,
    "images": ["https://FOTO-REAL"],
    "seller": "Nome público",
    "sellerCredit": "Reputação observada",
    "categories": ["eletronicos"],
    "area": "Localização informada"
  }],
  "hasMore": true
}
```

Esse é um contrato para um serviço que você controla, não a URL de uma API que já esteja ativa. Se usar provedor comercial, a conta e as condições dele são separadas. Não há chave de provedor incluída. Para manter custo zero, não contrate nem habilite cobrança sem avaliar a franquia e seus limites.

## Alertas de preço e venda

Cadastre anúncios no painel Alertas. O cron consulta até dez anúncios a cada seis horas, priorizando os menos recentemente consultados. Limite de cem acompanhamentos. Mudanças de preço, preço desejado e venda confirmada geram eventos. Erros preservam o último preço/estado conhecido. Fora de estoque ou bloqueio não são tratados como venda.

Por padrão, a consulta tenta dados estruturados públicos da página Goofish. Um teste real retornou HTML sem esses dados; não há confirmação de que esse caminho seja suficiente. Quando precisar de coletor autenticado, configure:

```text
PRODUCT_SOURCE_URL=https://SEU-COLETOR
```

```powershell
npx wrangler secret put PRODUCT_SOURCE_TOKEN
```

A API solicita GET /products/ID. Resposta:

```json
{
  "id": "ID-NUMERICO-REAL",
  "title": "Título",
  "priceCny": 100,
  "images": [],
  "availability": "available",
  "observedAt": "DATA-ISO-8601-DA-COLETA"
}
```

Estados: available, sold ou unknown. Use sold somente com confirmação da origem. Dados sem data, com mais de 24 horas ou de outro ID são recusados. Erro de login deve ser erro HTTP, nunca um anúncio fictício.

O coletor autenticado não está incluído no pacote. Publicar o Worker não transfere sua sessão Chrome. A arquitetura de um navegador remoto está em IMPLEMENTACAO-CLOUDFLARE.md, no repositório principal; exige implantação e validação próprias.

Ative notificações no Chrome para receber os eventos. A coleta agendada fica na Cloudflare com o PC desligado, mas as notificações visuais precisam do Chrome funcionando. Histórico: 500 eventos no servidor, cem recentes no painel. Consultas manuais têm intervalo mínimo de quinze minutos.

## Sincronizar e compartilhar

Confira primeiro a coleção remota. Enviar a coleção deste Chrome grava anúncios, lojas, propostas, encomendas e cotação no D1. Usar a coleção da nuvem substitui a local: faça backup antes. Revisões desatualizadas geram 409 para evitar sobrescrita silenciosa.


## Limites funcionais


## Verificar e atualizar

```powershell
npm test
npx wrangler deploy --dry-run
```

Atualize o servidor com npm ci e npm run deploy. Para a extensão, substitua os arquivos na mesma pasta e clique Recarregar em chrome://extensions.

401 significa chave inválida; 409, conflito de revisão; 503, configuração ou fonte indisponível. /health confirma que o Worker responde, mas não prova que a fonte Goofish esteja funcionando.

Apagar dados remotos exclui coleção, acompanhamentos, eventos e compartilhamentos. Desinstalar a extensão não apaga o D1. Backups devem ser apagados separadamente.

Referências: https://developers.cloudflare.com/d1/get-started/ e https://developers.cloudflare.com/workers/configuration/cron-triggers/ .
