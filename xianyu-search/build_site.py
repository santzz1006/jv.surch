"""Generate real static category pages and product-only catalog exports."""
from pathlib import Path
from html import escape
import catalog
import re
from category_design import DESIGNS
from legal_pages import PRIVACY_UI, FOOTER_LINKS, build_legal
from social_meta import social_meta, SITE, PUBLIC_URL
from extension_page import build_extension_page
ROOT=Path(__file__).parent
PUBLIC=ROOT/'public'
ICONS={'Tecnologia':'tech','Moda e esporte':'fashion','Serviços e colecionáveis':'services','Cuidados':'care','Casa':'home','Arte e presentes':'gifts','Dia a dia':'daily','Lazer':'gaming','Mobilidade e imóveis':'mobility','Ferramentas e campo':'tools'}

TEMPLATE='''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Explore anúncios do Goofish em português na Alpha Busca. Catálogo por categoria, favoritos e links para seu agente."><title>__TITLE__ · Alpha Busca</title><link rel="icon" href="__BASE__favicon.svg"><link rel="stylesheet" href="__BASE__shop.css?v=11"><script defer src="__BASE__assets/vendor/gsap.min.js"></script><script defer src="__BASE__assets/vendor/ScrollTrigger.min.js"></script><script defer src="__BASE__shop.js?v=11"></script></head>
<body data-category="__CATEGORY__" data-view="__VIEW__"><a class="skip" href="#conteudo">Pular para os produtos</a>
<header><div class="wrap header-row"><a href="__BASE__" class="brand" aria-label="Alpha Busca início"><b>ALPHA</b> BUSCA<span>seu próximo achado</span></a><form id="search-form" role="search"><label class="sr-only" for="query">O que você procura?</label><input id="query" type="search" maxlength="120" placeholder="O que você quer encontrar hoje?" required><button>Buscar <span aria-hidden="true">↗</span></button></form><div class="header-actions"><button id="favorites" class="outline">♡ <span>Favoritos</span></button><button class="outline" disabled title="Convite do Discord em breve">Comunidade</button></div></div><nav class="wrap quick-nav" aria-label="Explore"><a href="__BASE__">Destaques</a><a href="__BASE__categoria/celulares/">Celulares</a><a href="__BASE__categoria/moda/">Moda</a><a href="__BASE__categoria/games/">Games</a><a href="__BASE__categoria/decoracao/">Casa</a><span>Descubra no Goofish. Explore em português.</span></nav></header>
<main class="wrap" id="conteudo"><div id="listing-view"><nav class="breadcrumb" id="breadcrumb" aria-label="Caminho">Início / Seus próximos achados</nav><section class="discovery"><aside class="category-menu"><h2>Por onde começar?</h2><nav id="categories" aria-label="Categorias"></nav></aside><div class="hero-area"><section class="hero" id="hero"><div class="hero-copy"><span class="eyebrow" id="hero-eyebrow">DA CHINA PARA SUAS IDEIAS</span><h1 id="hero-title">Grandes achados.<br>Novas possibilidades.</h1><p id="hero-description">Explore produtos, compare preços e encontre algo que tem a sua cara.</p><a class="button yellow" href="#products" id="hero-cta">Vamos garimpar ↗</a></div><img class="hero-art" id="hero-art" src="__BASE__assets/icon-tech.png" alt="" fetchpriority="high"></section><div class="mini-banners"><a href="__BASE__categoria/moda/" class="mini-banner fashion"><span>SEU ESTILO, SUA ESCOLHA</span><h2>Achados para<br>renovar o visual.</h2><span>Explorar moda ↗</span></a><a href="__BASE__categoria/decoracao/" class="mini-banner home"><span>IDEIAS PARA O SEU ESPAÇO</span><h2>Um novo olhar<br>para sua casa.</h2><span>Ver decoração ↗</span></a></div></div></section>
<div class="benefit-row"><span>✦ Anúncios reais do Goofish</span><span>♡ Seus favoritos em um lugar</span><span>↗ Copie e envie ao seu agente</span></div>
<section id="products"><div class="section-heading"><div><span class="eyebrow">VALE A DESCOBERTA</span><h2 id="results-title">Destaques para você</h2><p id="results-note">Uma seleção de diferentes categorias do nosso catálogo.</p></div><a href="__BASE__data/products.json" class="text-link" download>Baixar catálogo JSON ↓</a></div><div class="category-pills" id="category-pills"></div><form id="filters" class="filter-bar"><label>Mínimo ¥<input id="min" type="number" min="0" step="0.01" placeholder="0"></label><label>Máximo ¥<input id="max" type="number" min="0" step="0.01" placeholder="Sem limite"></label><label>Ordenar<select id="sort"><option value="featured">Ordem da seleção</option><option value="asc">Menor preço</option><option value="desc">Maior preço</option></select></label><button class="button black">Filtrar</button><button type="button" id="clear-filters" class="text-link">Limpar</button></form><p id="status" role="status" aria-live="polite">Carregando achados…</p><div class="live-options" id="live-options" hidden><p>Quer explorar além do catálogo salvo?</p><button class="button yellow" id="live-search">Buscar no Goofish agora ↗</button><label>Idioma da consulta<select id="query-language"><option value="pt">Português / original</option><option value="zh">Chinês</option><option value="ja">Japonês</option><option value="en">Inglês</option></select></label></div><ul id="grid" class="grid"></ul><nav id="pager" class="pager" hidden aria-label="Paginação"><button id="previous" class="button">← Anterior</button><span id="page-label"></span><button id="next" class="button">Próxima →</button></nav></section>
<section class="wide-banner"><div><span class="eyebrow">DA DESCOBERTA AO SEU AGENTE</span><h2>Gostou? Salve.<br>Encontrou? Compartilhe.</h2><p>Abra o produto e copie as informações para conversar com seu agente de compras.</p><button class="button yellow" id="banner-favorites">Ver meus favoritos ♡</button></div><img src="__BASE__assets/icon-recommend.png" alt="" loading="lazy"></section></div>
<section id="product-view" hidden><nav class="breadcrumb"><a href="__BASE__">Início</a> / <span>Detalhes do achado</span></nav><div id="product-content"></div><section class="section-heading"><div><span class="eyebrow">CONTINUE EXPLORANDO</span><h2>Outros achados da categoria</h2></div></section><ul id="related" class="grid"></ul></section>
<details class="admin"><summary>Minha coleção e conexão local</summary><p id="connection">Verificando conexão…</p><p id="collection-status"></p><div class="admin-actions"><button id="collect" class="button">Coletar categorias pendentes</button><a href="__BASE__data/products.json" class="button" download>Exportar JSON</a><label>Cotação manual R$ / ¥<input id="manual-rate" type="number" min="0.01" step="0.0001" placeholder="Usar cotação salva"></label></div><p>O catálogo salvo abre sem extensão. Novas buscas e atualizações usam o Chrome conectado do administrador. Não é necessário login dos visitantes para consultar o catálogo.</p></details></main>
<footer class="wrap"><a href="__BASE__" class="brand"><b>ALPHA</b> BUSCA</a><p>Projeto independente, sem vínculo com o Goofish. Preços e disponibilidade podem mudar. Valores em reais são estimativas sem frete, taxas ou impostos.</p><p id="rate-note"></p><a href="https://www.exchangerate-api.com" target="_blank" rel="noopener noreferrer">Cotação: ExchangeRate-API</a></footer><div id="toast" role="status" hidden></div></body></html>'''


ARROWS={'↗':'M7 17 17 7M7 7h10v10','→':'M4 12h16m-6-6 6 6-6 6','←':'M20 12H4m6-6-6 6 6 6','♡':'M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z'}
def svg(path):return f'<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="{path}"/></svg>'
TEMPLATE=TEMPLATE.replace('Alpha Busca','Goofish Br').replace('<b>ALPHA</b>','<img class="brand-mascot" src="__BASE__assets/jv-mascot.png" alt=""><b>Goofish <em>Br</em></b>').replace('seu próximo achado','Seu próximo achado').replace(' BUSCA','').replace('v=11','v=15')
TEMPLATE=TEMPLATE.replace('__BASE__favicon.svg','__BASE__assets/jv-mascot.png')
TEMPLATE=TEMPLATE.replace('<script defer src="__BASE__shop.js?v=15">','<link rel="stylesheet" href="__BASE__jv.css?v=15"><script defer src="__BASE__privacy.js?v=15"></script><script defer src="__BASE__shop.js?v=15">')
TEMPLATE=re.sub(r'<section class="hero" id="hero">.*?</section>','__HERO__',TEMPLATE)
TEMPLATE=re.sub(r'<div class="mini-banners">.*?</a></div>','__PROMOS__',TEMPLATE)
TEMPLATE=re.sub(r'<span class="eyebrow"[^>]*>.*?</span>','',TEMPLATE)
TEMPLATE=re.sub(r'<a [^>]*download>.*?</a>','',TEMPLATE)
TEMPLATE=re.sub(r'<details class="admin">.*?</details>','<div class="currency-setting"><label>Cotação manual R$ / ¥ <input id="manual-rate" type="number" min="0.01" step="0.0001" placeholder="Usar cotação salva"></label></div>',TEMPLATE)
TEMPLATE=TEMPLATE.replace('data-view="__VIEW__"','data-view="__VIEW__" data-banner-note="__NOTE__"')
TEMPLATE=TEMPLATE.replace('Gostou? Salve.<br>Encontrou? Compartilhe.','__SECONDARY__').replace('__BASE__assets/icon-recommend.png','__BASE__assets/mascot-wave.png')
TEMPLATE=TEMPLATE.replace('Por onde começar?','Categorias').replace('Quer explorar além do catálogo salvo?','Não encontrou o que procura?')
TEMPLATE=TEMPLATE.replace('</footer>',FOOTER_LINKS+'</footer>').replace('</body>',PRIVACY_UI+'</body>')
for char,path in ARROWS.items():TEMPLATE=TEMPLATE.replace(char,svg(path))
TEMPLATE=TEMPLATE.replace('✦ ','')

TEMPLATE=TEMPLATE.replace('<script defer src="__BASE__shop.js?v=15">', '<script defer src="__BASE__catalog-loader.js?v=13"></script><script defer src="__BASE__shop.js?v=16">')

def hero(category=None):
    if category:
        title,description,note,color=DESIGNS[category['id']]
        visual=f'<div class="category-art"><img class="hero-art" id="hero-art" src="__BASE__assets/category-{category["id"]}.png" alt="Ilustração de {escape(category["label"])}" fetchpriority="high"><img class="category-mascot" src="__BASE__assets/mascot-wave.png" alt="" loading="lazy"></div>'
        cta='Explorar '+category['label'].lower()
    else:
        title='Busque no Goofish. Sem criar conta.';description='Seu novo jeito de encontrar produtos: anúncios em português, preços em reais e o link pronto para seu agente.';color='#ffe615';cta='Encontrar produtos'
        visual='<img class="hero-art" id="hero-art" src="__BASE__assets/mascot-search.png" alt="Mascote pesquisando com uma lupa" fetchpriority="high">'
    return f'<section class="hero {"category-hero" if category else "home-hero"}" id="hero" style="--category-color:{color}"><div class="hero-copy"><h1 id="hero-title">{escape(title)}</h1><p id="hero-description">{escape(description)}</p><a class="button black" href="#products">{escape(cta)} {svg(ARROWS["→"])}</a></div>{visual}</section>'

PROMOS='<div class="mini-banners"><a href="__BASE__categoria/moda/" class="mini-banner"><div><h2>Roupas e tênis.<br>Do seu jeito.</h2><span>Explorar moda</span></div><img src="__BASE__assets/category-moda.png" alt="" loading="lazy"></a><a href="__BASE__categoria/computadores/" class="mini-banner"><div><h2>Seu próximo<br>setup.</h2><span>Ver computadores</span></div><img src="__BASE__assets/category-computadores.png" alt="" loading="lazy"></a></div>'
def render(title,view,base,category=None):
    url=PUBLIC_URL+'categoria/'+category['id']+'/' if category else (PUBLIC_URL+'produto.html' if view=='product' else SITE)
    template=re.sub(r'<meta name="description"[^>]*>', '', TEMPLATE)
    template=template.replace('</head>',social_meta(title+' · Goofish Br',url)+'</head>')
    note=DESIGNS[category['id']][2] if category else 'Guarde para ver depois.'
    secondary='Seus achados de '+category['label'].lower()+', prontos para compartilhar.' if category else 'Escolha o produto. Envie para seu agente.'
    return template.replace('__TITLE__',escape(title)).replace('__HERO__',hero(category)).replace('__PROMOS__','' if category else PROMOS).replace('__NOTE__',escape(note,quote=True)).replace('__SECONDARY__',escape(secondary)).replace('__CATEGORY__',category['id'] if category else '').replace('__VIEW__',view).replace('__BASE__',base)
def build():
    # Page generation does not rewrite or shrink the existing product catalog.
    (PUBLIC/'index.html').write_text(render('Seus próximos achados','home','./'),encoding='utf-8')
    (PUBLIC/'produto.html').write_text(render('Detalhes do produto','product','./'),encoding='utf-8')
    for c in catalog.CATEGORIES:
        folder=PUBLIC/'categoria'/c['id'];folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(render(c['label'],'category','../../',c),encoding='utf-8')
    build_legal(PUBLIC)
    build_extension_page(PUBLIC)
    root=ROOT.parent/'index.html'
    entry=root.read_text(encoding='utf-8')
    entry=re.sub(r'\n?<!-- social-preview -->.*?<!-- /social-preview -->\n?', '', entry, flags=re.S)
    entry=entry.replace('</head>','<!-- social-preview -->\n'+social_meta()+'\n<!-- /social-preview -->\n</head>')
    root.write_text(entry,encoding='utf-8')
    print('29 categorias com banners exclusivos, termos e privacidade gerados.')
if __name__=='__main__':build()
