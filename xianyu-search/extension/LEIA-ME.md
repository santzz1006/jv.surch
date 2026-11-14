# Alpha Busca — conexão com o Chrome

Esta extensão local abre uma aba temporária no Goofish usando a sessão que já existe no seu Chrome. Ela lê cartões de produtos renderizados e envia título, imagem, preço e dados de vendedor visíveis para `http://127.0.0.1:8081`. Não lê cookies, senhas, mensagens, pedidos ou armazenamento do Goofish. Não realiza compras e não resolve CAPTCHA.

Permissões: executar o coletor apenas em `www.goofish.com`, comunicar com a API local, armazenar o estado ativado/pausado e verificar a fila a cada 30 segundos. Nenhum outro domínio recebe dados coletados. A tradução opcional de títulos no site usa MyMemory, conforme a interface informa.

1. Inicie `iniciar.ps1`.
2. Execute `python prepare_extension.py` se o arquivo `config.js` ainda não existir.
3. No Chrome conectado ao Goofish, abra `chrome://extensions`.
4. Ative o modo do desenvolvedor, escolha **Carregar sem compactação** e selecione esta pasta `extension`.
5. Abra o botão da extensão e clique **Ativar conexão**.
6. Na Alpha Busca, selecione **Meu Chrome conectado** e clique **Atualizar recomendações** ou faça uma pesquisa.

O servidor aceita resultados somente com a chave de pareamento local em `config.js`. Não compartilhe esse arquivo nem `.bridge-key`. A extensão inicia pausada e pode ser pausada ou removida a qualquer momento.

Recomendações são os produtos que aparecem na página inicial da sua sessão, não recomendações calculadas pela Alpha Busca. O arquivo de anúncios `recommendations.json` fica no servidor local para sobreviver a reinícios e a interface mostra a data da captura. A coleta não comprova a qualidade dos vendedores nem a disponibilidade atual dos anúncios.

Enquanto a extensão não estiver instalada e ativada, não existe conexão com seu Chrome. Seletores de cartões precisam ser validados na página real. O funcionamento com a conta conectada só pode ser confirmado após esse teste.
