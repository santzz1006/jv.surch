# Goofish Br — Seus achados 1.1.0

## Instalação

Extraia o ZIP em uma pasta permanente. Abra chrome://extensions, ative Modo do desenvolvedor, escolha Carregar sem compactação e selecione a pasta com manifest.json. Para atualizar, substitua os arquivos na mesma pasta e clique Recarregar. Fixe a extensão no Chrome. O conector de coleta anterior pode continuar instalado.

## Uso local

Busca no catálogo Goofish Br ou abertura da pesquisa original; captura explícita de anúncios visíveis; pastas, filtro, ordenação, lojas salvas e cópia para agente. O painel completo acrescenta backup/importação, cotação diária opcional, propostas de agentes e códigos de encomendas.

## Recursos online preparados

Abra o painel pelo popup e conecte sua própria API Cloudflare. O guia está no projeto em cloudflare/LEIA-ME.md e no site, na página da extensão.

- IA: análise de anúncio, tradução, dúvidas, rascunho em chinês, descrição de foto para pesquisa e análise de QC com referência opcional.
- Alertas: preço, preço desejado e venda confirmada; cron a cada seis horas, dez anúncios por execução. Requer fonte de preços acessível.
- Nuvem: sincronização manual protegida contra conflitos entre dispositivos.
- Coleções: link por pasta, atualização após sincronizar, colaboração por código separado e revogação.

## Limites

Não é uma reprodução integral da EVO. IA e nuvem aguardam a criação/configuração da conta Cloudflare. A sessão do Goofish não é transferida automaticamente. Se a origem exigir login ou não expuser dados verificáveis, a consulta remota depende de coletor próprio. O contrato está no guia; um navegador remoto autenticado não foi implementado neste pacote.

Não há importação automática de pedidos ou álbuns privados dos agentes, rastreio por API, envio de mensagens, banco privado de fornecedores, cotação automática entre agentes ou índice visual de todo o Goofish. A busca por foto gera termos para pesquisar. IA pode errar. As coleções da extensão e do site são separadas. Nenhuma API, chave ou código de afiliado da EVO é reutilizado.

Testes automatizados cobrem DOM, persistência, banco SQLite e API; o Worker passou pelo empacotamento Wrangler. A instalação no seu Chrome, a IA remota e a leitura na sessão real ainda precisam de validação.

Consulte privacy.html. Contato: jv.busca@gmail.com.
