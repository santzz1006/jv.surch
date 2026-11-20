# Goofish Br — Seus achados 1.0.0

Extensão independente para Chrome e navegadores Chromium. Esta é a versão de uso pessoal: não precisa do servidor local nem da extensão de coleta antiga.

## Instalar

1. Extraia o ZIP em uma pasta permanente.
2. Abra `chrome://extensions` e ative **Modo do desenvolvedor**.
3. Clique em **Carregar sem compactação** e selecione a pasta que contém `manifest.json`.
4. Fixe **Goofish Br — Seus achados** no menu de extensões.

Não é necessário desinstalar o conector de coleta. São extensões diferentes; o conector antigo continua responsável pelas consultas autenticadas da API local.

## Usar

- **Buscar:** pesquise no catálogo público Goofish Br, em português, ou abra a busca do Goofish original. A origem pode pedir login.
- **Salvar anúncio aberto:** abra um anúncio no Goofish e clique no botão. Título, descrição, fotos grandes visíveis, preço e nome visível do vendedor são salvos localmente.
- **Pastas:** digite uma pasta antes de salvar ou use **Mover** em um anúncio. Filtre por pasta ou texto e ordene por preço.
- **Copiar para agente:** copia as informações e o link original. Cole onde preferir; a extensão não envia mensagens.
- **Cotação:** em Ajustes, informe quantos reais equivalem a 1 yuan. A conversão é estimada, manual e não inclui despesas de importação.
- **Preços na aba:** em Ajustes, ative os rótulos em reais na aba do Goofish. Recarregar a página remove os rótulos. Ative novamente para usar outra cotação.
- **Atualizar anúncio:** salve novamente o anúncio aberto para atualizar os dados e registrar uma mudança de preço. Não há monitoramento automático em segundo plano.
- **Fornecedores:** cadastre os links das suas lojas. Não é uma lista de fornecedores verificados.
- **Backup:** exporta a coleção e a cotação para um arquivo local. Esta versão ainda não importa backups.

## Limites reais desta versão

O catálogo público funciona sem servidor no computador. Os anúncios novos lidos pela extensão precisam estar visíveis no Goofish; login e verificações continuam sujeitos às regras da origem. A extensão não traduz automaticamente textos recém-capturados, não possui IA, planos pagos, sincronização em nuvem, consulta de QC, conversão de links afiliados ou monitoramento automático de disponibilidade. Os serviços privados da EVO não fazem parte do pacote baixado e não são reutilizados.

Fotos que ainda não carregaram ou não foram mostradas na galeria podem não ser capturadas. Os seletores foram testados com páginas de teste; mudanças no Goofish podem exigir atualização. Não foi realizada instalação nem validação com uma sessão real do navegador nesta entrega.

Coleção da extensão e favoritos do site são separados. Dados e permissões estão descritos em `privacy.html`. Não há leitura de cookies, senhas, mensagens ou pedidos, nem envio de capturas para terceiros. As imagens são carregadas de suas URLs originais.

Contato: jv.busca@gmail.com.
