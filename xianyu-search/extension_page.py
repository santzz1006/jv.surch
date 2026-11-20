"""Generate the public extension page, privacy notice and setup guide."""
from pathlib import Path
from html import escape
import re
from social_meta import social_meta, PUBLIC_URL

def document(title,body,name):
    return '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+' · Goofish Br</title>'+social_meta(title+' · Goofish Br',PUBLIC_URL+name)+'<link rel="icon" href="./assets/jv-mascot.png"><link rel="stylesheet" href="./shop.css?v=15"><link rel="stylesheet" href="./jv.css?v=15"><style>pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f5e9;padding:20px;border-radius:16px}code{overflow-wrap:anywhere}li{margin:10px 0}</style></head><body><header><div class="wrap header-row"><a class="brand" href="./"><img class="brand-mascot" src="./assets/jv-mascot.png" alt=""><b>Goofish <em>Br</em></b></a><a class="button" href="./">Ver produtos</a></div></header><main class="wrap legal-content">'+body+'</main></body></html>'

def markdown(text):
    output=[];code=False;paragraph=[]
    def flush():
        if paragraph: output.append('<p>'+'<br>'.join(paragraph)+'</p>');paragraph.clear()
    for line in text.splitlines():
        if line.startswith('```'):
            flush();output.append('</code></pre>' if code else '<pre><code>');code=not code;continue
        if code: output.append(escape(line)+'\n');continue
        if not line.strip():flush();continue
        m=re.match(r'^(#{1,3}) (.*)',line)
        if m:flush();n=len(m[1]);output.append(f'<h{n}>'+escape(m[2])+f'</h{n}>');continue
        value=escape(line)
        value=re.sub(r'(https://[^\s<>]+)',r'<a href="\1" target="_blank" rel="noopener">\1</a>',value)
        value=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',value)
        paragraph.append(value)
    flush();return ''.join(output)

def build_extension_page(public):
    root=Path(__file__).parent
    body="""<h1>Seus achados, sempre por perto.</h1><p>Salve anúncios, organize pastas, veja preços em reais e prepare informações para seu agente.</p><p><a class="button black" href="./downloads/goofish-br-extensao-1.1.0.zip" download>Baixar extensão · versão 1.1.0</a></p><h2>Instalação no Chrome</h2><p>A Goofish Br ainda não foi publicada na Chrome Web Store. Enquanto isso, use a instalação manual:</p><ol><li>Baixe e extraia o arquivo em uma pasta permanente.</li><li>Abra <code>chrome://extensions</code> e ative <strong>Modo do desenvolvedor</strong>.</li><li>Clique em <strong>Carregar sem compactação</strong> e selecione a pasta com <code>manifest.json</code>.</li><li>Fixe <strong>Goofish Br — Seus achados</strong> no menu do Chrome.</li></ol><p>Para atualizar, substitua os arquivos na mesma pasta e clique em Recarregar.</p><h2>O que você já pode fazer</h2><ul><li>Pesquisar no catálogo Goofish Br e abrir a busca original.</li><li>Salvar anúncios visíveis com fotos e informações, organizar pastas e copiar para o agente.</li><li>Guardar lojas, importar/exportar backup, comparar propostas inseridas por você e organizar códigos de encomendas.</li><li>Usar cotação manual ou consultar a cotação disponível no painel.</li></ul><h2>IA, alertas e sua coleção na nuvem</h2><p>O painel e o backend estão preparados para análise e tradução de anúncios, fotos de QC, rascunhos de mensagens, sincronização, compartilhamento e alertas. Esses recursos precisam da sua API Cloudflare configurada. A instalação não cria nem conecta uma conta automaticamente.</p><p><a class="button" href="./cloudflare.html">Guia para ativar os recursos online</a> <a class="button" href="./downloads/goofish-br-cloudflare-1.1.0.zip" download>Baixar projeto da API</a></p><p>Alertas dependem de dados verificáveis da origem. Se o Goofish exigir login, a consulta remota precisa de um coletor próprio; o pacote não transfere sua sessão do Chrome. IA pode errar. A busca por foto gera termos para pesquisa, sem acesso a um índice visual de todo o marketplace.</p><h2>Sobre esta versão</h2><p>Projeto independente, sem vínculo oficial com Goofish/Xianyu ou EVO Society. Não inclui envio de mensagens, importação automática de pedidos privados, rastreio por API, banco privado de fornecedores ou cotações automáticas dos agentes.</p><p>Testes automatizados validaram a extensão e o backend. A ativação na conta Cloudflare, a IA remota e a captura na sessão real ainda precisam ser conferidas. Preços e disponibilidade devem ser confirmados na origem.</p><p><a href="./privacidade-extensao.html">Privacidade da extensão</a> · <a href="mailto:jv.busca@gmail.com">Contato</a></p>"""
    (public/'extensao.html').write_text(document('Extensão',body,'extensao.html'),encoding='utf-8')
    (public/'cloudflare.html').write_text(document('Ativar recursos online',markdown((root/'cloudflare/LEIA-ME.md').read_text(encoding='utf-8')),'cloudflare.html'),encoding='utf-8')
    privacy=(root/'extension-shop/privacy.html').read_text(encoding='utf-8')
    body=re.search(r'<section>(.*?)</section>',privacy,re.S).group(1)
    (public/'privacidade-extensao.html').write_text(document('Privacidade da extensão',body,'privacidade-extensao.html'),encoding='utf-8')
