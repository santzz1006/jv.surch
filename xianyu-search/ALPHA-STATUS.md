# Alpha Busca — estado da implementação

## Entregue

- Identidade Alpha Busca, amarelo/preto, cantos arredondados e posições ajustadas.
- Três banners originais gerados pela ferramenta de imagens: eletrônicos, câmeras e busca de achados. Arquivos em `public/assets/banner-{tech,camera,search}.png`.
- Prompts: ilustrações 3D de produtos à direita com espaço livre à esquerda, paleta amarelo/preto; tecnologia em fundo escuro, câmeras em fundo creme e lupa em fundo amarelo. Textos promocionais aplicados em HTML acessível.
- Favoritos locais, filtro de preço, ordenação, importação de JSON com `items` e cópia de informações para agente.
- Ficha de produto com descrição e campos de vendedor, foto, nível, vendas e avaliações quando presentes no JSON. Ausências são indicadas, sem fabricação de dados.
- Preços em yuan e reais quando fornecidos; cotação manual substitui o valor em reais e não representa cotação do dia.
- Tradução de títulos chineses/japoneses e descrição para português via MyMemory; sujeita à disponibilidade, limite gratuito e tamanho máximo de 3.000 bytes. Teste real de tradução retornou “câmera”.
- Consultas em texto original PT/EN/ZH/JA. Escolher japonês não muda o marketplace para um site japonês.
- Comunidade sem link, conforme solicitado.

## Integração e limites verificados

O Chrome do usuário mostrou uma conta conectada ao Goofish. Esse perfil não foi copiado nem conectado automaticamente ao Chromium isolado do coletor. O login no navegador normal não torna a API local autenticada.

O provedor opcional do site de referência abre a página normalmente e observa a resposta bem-sucedida de `/api/search`. Não extrai ou replica tokens. No teste real desta execução, a página não liberou produtos e exigiu verificação na sessão separada. Portanto, a integração foi implementada, mas a busca ao vivo NÃO está validada ponta a ponta.

Para usar essa fonte: selecione a fonte de referência, abra Gerenciar acesso, use Abrir sessão, conclua pessoalmente a verificação no navegador e salve a sessão. Isso não garante que a verificação permaneça válida numa nova navegação. Alternativamente, exporte somente a resposta JSON de produtos que você já recebeu e importe pela interface. Não importe cookies, tokens, HAR ou dados de sessão.

As capturas mostram que `search` contém produtos; `rum` apresenta dados de telemetria, não uma credencial de catálogo. O texto codificado não foi tratado como JSON de produtos. O vídeo foi inspecionado por quadros distribuídos pelos 43 segundos e a transcrição dos áudios foi fornecida pelo usuário.

Nenhum anúncio real foi obtido pela nova integração durante os testes. Não há extração completa de vendedores, comentários ou histórico: a interface suporta esses dados quando a fonte os entrega. A cópia integral do catálogo não foi realizada.

## Executar

Use `iniciar.ps1` e abra http://127.0.0.1:8081. O servidor permanece local. Testes: `.venv\Scripts\python.exe -m unittest -v`. As imagens ficam no próprio projeto; não dependem de caminhos temporários.
