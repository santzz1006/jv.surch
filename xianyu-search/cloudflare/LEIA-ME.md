# Goofish Br: ativar IA, sincronização e alertas na Cloudflare

O código está preparado e foi testado localmente. Você ainda precisa criar sua conta e publicar a API. Nenhuma conta foi criada nem serviço pago ativado nesta entrega.

## O que está pronto no código

- Workers AI: análise de anúncio, tradução para português, tradução de busca para chinês, dúvidas, rascunho para vendedor, descrição de foto para pesquisa e inspeção visual de QC.
- D1: coleção privada, revisão para impedir sobrescrita por outro computador, anúncios acompanhados e histórico de mudanças.
- Coleções compartilhadas: uma pasta por link, cópia fixa ou atualização após sincronizar, código separado para colaboração e revogação.
- Cron: consulta a cada seis horas, até dez anúncios por execução, bloqueio de consultas sobrepostas e intervalo de quinze minutos para solicitações manuais.
- Alertas: aumento/queda de preço, preço desejado atingido e venda confirmada pela fonte. Falha de consulta não vira aviso de venda.
- Extensão: recebe os alertas enquanto o Chrome funciona e mostra o histórico acumulado quando você voltar.

## Limitações reais

Publicar esta API não transfere a sessão do Goofish do seu Chrome. O acesso público a um anúncio só funciona quando o Goofish entrega dados estruturados verificáveis. Se a origem exigir login ou só renderizar dados via JavaScript, configure um coletor próprio compatível com o contrato abaixo. O código não chama os servidores da EVO.

A extensão não inclui o banco privado de fornecedores ou QC dos agentes. Você cadastra lojas e envia fotos para analisar. Comparação de agentes usa propostas inseridas por você. Rastreio guarda códigos, notas e links; não consulta transportadoras automaticamente. Mensagens são rascunhos, sem envio automático. A busca por foto gera termos com IA e abre uma pesquisa; não é um índice visual de todo o Goofish.

## 1. Criar conta gratuita

Abra https://dash.cloudflare.com/sign-up e crie sua conta. Use **Workers Free**. Não ative Workers Paid para este projeto gratuito.

Workers AI oferece 10.000 neurônios por dia no plano Free. Modelo e tamanho das consultas determinam o consumo; não é ilimitado. Ao esgotar a cota, novas chamadas podem falhar. O projeto também limita a IA a 40 solicitações por dia. Isso é uma proteção adicional, não uma garantia de consumo. Confira o painel de uso.

Fonte: https://developers.cloudflare.com/workers-ai/platform/pricing/

## 2. Preparar e publicar

Abra um terminal em `xianyu-search/cloudflare`. Use Node.js 22 ou mais recente; os testes foram executados no Node 24.

```powershell
npm ci
npx wrangler login
npx wrangler d1 create goofish-br
```

O login abre o navegador oficial. Não envie senha ou token no chat. Copie o `database_id` retornado e substitua `SUBSTITUA_PELO_ID_DO_D1` em `wrangler.jsonc`. O binding deve continuar `DB`.

```powershell
npx wrangler d1 migrations apply goofish-br --remote
npm run deploy
```

Guarde o endereço `https://goofish-br-api.SUA-CONTA.workers.dev` retornado. Sem o segredo da próxima etapa, as rotas privadas permanecem indisponíveis.

## 3. Chave privada e conexão

Gere uma chave aleatória com pelo menos 32 caracteres em seu gerenciador de senhas, preferencialmente 64 caracteres hexadecimais. Guarde-a em um local privado.

```powershell
npx wrangler secret put API_TOKEN
```

Cole a chave no prompt. Ela é uma chave do seu projeto, **não o token de administração da Cloudflare**. Não a coloque no GitHub, no site ou em `wrangler.jsonc`.

Na extensão → **Abrir painel** → **Nuvem e privacidade**, informe a URL `workers.dev` e a chave. Clique em **Conectar API** e aceite acesso somente ao domínio informado.

Esta implementação é um espaço pessoal protegido por chave. Para outro computador seu, use a mesma URL/chave. Não distribua a chave para visitantes: todos acessariam a mesma coleção. Um serviço público com contas independentes exige autenticação e isolamento por usuário antes de abrir cadastros.

## 4. Ativar IA e imagens

O binding `AI` e os modelos estão em `wrangler.jsonc`. Escolha **Assistente IA**, selecione um anúncio ou cole um texto e clique em **Analisar**.

Para imagens, `@cf/meta/llama-3.2-11b-vision-instruct` exige revisão e aceite da licença e da política da Meta. A documentação orienta uma primeira chamada ao modelo com `{"prompt":"agree"}`. Faça isso na sua conta, pelo painel/API Cloudflare, após revisar os termos. O projeto não aceita a licença automaticamente.

Instruções oficiais: https://developers.cloudflare.com/workers-ai/models/llama-3.2-11b-vision-instruct/

O painel aceita uma foto de QC e uma referência opcional. Reduz as fotos e envia à sua API/Workers AI. Não envie etiquetas com dados pessoais. A resposta é auxiliar, pode errar e não certifica autenticidade ou qualidade. A IA não compra nem envia mensagens.

## 5. Sincronização e compartilhamento

1. Salve anúncios pelo popup da extensão.
2. Em Nuvem, **Conferir coleção da nuvem** mostra a revisão atual.
3. **Enviar coleção deste Chrome** grava os dados no D1.
4. Em outro computador, confira a nuvem e escolha **Usar coleção da nuvem neste Chrome**. Faça backup antes: essa ação substitui a coleção local.
5. Em Coleções, selecione uma pasta e crie um link. A opção contínua acompanha futuras sincronizações da pasta.
6. Compartilhe o código de colaboração apenas com quem pode acrescentar produtos. Ele não é a chave da API. **Revogar** invalida link e código.

A sincronização é manual. Conflitos retornam erro 409 em vez de sobrescrever alterações de outro computador. Exporte backup e baixe a revisão atual antes de reconciliar.

## 6. Alertas e origem dos preços

Selecione anúncios salvos e um preço desejado opcional. Limite: 100 anúncios por espaço. Cada execução consulta até dez, priorizando os menos recentemente consultados. Nem todos passam em cada lote se houver mais de dez.

**Consultar preços agora** valida a origem. Login, CAPTCHA, timeout ou página sem dados estruturados produzem consulta indisponível, preservando o último preço. “Fora de estoque” não basta para afirmar venda.

O cron continua com seu PC desligado. As notificações visuais precisam do Chrome funcionando e de permissão. O histórico guarda até 500 eventos; o painel mostra os cem recentes.

Não foi confirmada uma consulta bem-sucedida pelo ambiente Cloudflare nesta entrega. Sem fonte de preços acessível, a lógica de alertas está pronta, mas não detecta mudanças reais.

### Coletor próprio quando a origem exigir login

Configure a URL da API que você controla no painel Cloudflare → Worker → Settings → Variables:

```text
PRODUCT_SOURCE_URL=https://SEU-COLETOR
```

Se exigir chave:

```powershell
npx wrangler secret put PRODUCT_SOURCE_TOKEN
```

O Worker solicita `GET /products/ID`, com `Authorization: Bearer ...` quando configurado. Resposta esperada, somente com dados observados:

```json
{
  "id": "123456789",
  "title": "Título original",
  "description": "Descrição observada",
  "priceCny": 100,
  "images": ["https://ENDERECO-REAL-DA-FOTO"],
  "seller": "Nome público",
  "availability": "available",
  "observedAt": "DATA-ISO-8601-DA-COLETA"
}
```

Estados: `available`, `sold` ou `unknown`. Use `sold` só quando a origem confirmar. Erros de login devem ser erro HTTP. Dados de outro ID, sem data ou com mais de 24 horas são recusados.

O coletor com sessão remota é separado: este pacote não implementa um navegador Goofish remoto. A arquitetura está em `../IMPLEMENTACAO-CLOUDFLARE.md`. Workers não recebe automaticamente o login do Chrome; valide a sessão remota e os limites gratuitos antes de depender dela.

## 7. Verificação, atualização e exclusão

```powershell
npm test
npx wrangler deploy --dry-run
```

Atualizar servidor: `npm ci` e `npm run deploy`. Atualizar extensão: substitua os arquivos na mesma pasta e clique **Recarregar** em `chrome://extensions`.

401: chave incorreta. 409: revisão antiga. 429: limite diário. 503: binding, licença, cota ou fonte indisponível. `/health` confirma o Worker, não garante que IA e Goofish respondam.

Apague dados remotos no painel Nuvem, ou exclua Worker e D1 na Cloudflare. Desinstalar não apaga o banco remoto. Backups baixados precisam ser excluídos separadamente.

## Documentação oficial

- https://developers.cloudflare.com/d1/get-started/
- https://developers.cloudflare.com/workers-ai/configuration/bindings/
- https://developers.cloudflare.com/workers/configuration/cron-triggers/
- https://developer.chrome.com/docs/extensions/reference/api/permissions
- https://developer.chrome.com/docs/extensions/reference/api/alarms
