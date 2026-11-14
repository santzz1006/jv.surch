# Verificação — 13/11/2026

## Resultado

- 20 testes automatizados passaram (`.venv\Scripts\python.exe -m unittest -v`).
- Python compilado com `py_compile` e JavaScript verificado com `node --check`.
- Prévia web carregada no navegador em http://127.0.0.1:8081.
- Validação visual de faixa de preço invertida: mensagem correta antes de consultar a fonte.
- Teste real de `rtx 3060` pela interface: API respondeu `503 / LOGIN_REQUIRED`. Nenhum anúncio foi obtido; a fonte pediu login.
- Abertura de sessão pela interface: `/api/health` confirmou `sessionOpen: true`. O usuário informou não ter conta; a janela foi encerrada pelo botão Salvar sessão, sem login.

## Cobertura automatizada

Filtros, preço ausente, ordenação, paginação, deduplicação por ID, milhares no preço, parâmetros inválidos, páginas estáticas, proteção de arquivos privados, saúde da API, cache e expiração, resultado vazio, erro de login, falha inesperada sem exposição de detalhes internos, concorrência, intervalo de consultas, origem das requisições, endpoints inexistentes e ciclo de abertura/fechamento de sessão com processo simulado.

Os testes HTTP usam dados artificiais e um coletor simulado. Não equivalem à validação de extração real nem provam acesso anônimo. O limite atual é externo: é necessário entrar com uma conta aceita pelo Xianyu para prosseguir com a validação autenticada. Seletores, títulos e preços dos anúncios reais permanecem sem validação nesta sessão.

## Como continuar

O usuário não tem conta e deseja uma solução gratuita. Não há fonte anônima funcional comprovada nesta implementação. O fluxo de sessão está disponível caso uma conta própria se torne disponível, mas não resolve essa restrição atualmente. A prévia e a API local ficam abertas; não há API paga configurada nem resultados falsos na aplicação.
