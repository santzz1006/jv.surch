# Diagnóstico de acesso público — 13/11/2026

Foram feitas requisições normais, sem cookies e sem tokens de login, aos caminhos observados no JavaScript público do site de referência.

| Requisição | Resultado |
| --- | --- |
| GET `/api/config` | HTTP 200, configuração pública e chave pública Turnstile; não contém produtos nem credencial privada |
| GET `/api/search?q=rtx%203060&page=1&lang=pt` | HTTP 401, `UNAUTHORIZED`, sessão inválida ou expirada |
| POST `/api/session` com `{}` | HTTP 401, verificação humana não confirmada |
| GET `https://www.goofish.com/search?q=rtx%203060` | HTTP 200, HTML sem links de produtos; não equivale a uma busca bem-sucedida |

O frontend de referência pede uma sessão após a verificação humana e envia o token no cabeçalho `X-Session`. Isso explica como o visitante acessa o servidor intermediário, mas não revela a fonte, as credenciais, a infraestrutura ou o método usado pelo backend para obter anúncios. Não é possível afirmar que ele coleta dados anonimamente no Xianyu.

Não foi encontrada uma integração anônima funcional nos endpoints públicos observados. O coletor local continua sem conseguir obter anúncios sem login. Nenhum endpoint protegido de terceiros foi incorporado à aplicação, e nenhuma verificação foi contornada.

## Visual

O projeto agora usa a identidade **Garimpo**, estilos próprios, paleta verde-petróleo e fundo claro. O CSS original de referência foi substituído. As referências de marca, comunidade e afiliados foram removidas do projeto ativo. A captura original permanece na pasta separada em que foi baixada anteriormente, para preservar o material solicitado naquela etapa.
