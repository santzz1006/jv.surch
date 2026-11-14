"""Generate real static category pages and product-only catalog exports."""
from pathlib import Path
from html import escape
import catalog
import re
from category_design import design
from legal_pages import PRIVACY_UI, FOOTER_LINKS, build_legal
ROOT=Path(__file__).parent
PUBLIC=ROOT/'public'
ICONS={'Tecnologia':'tech','Moda e esporte':'fashion','Serviços e colecionáveis':'services','Cuidados':'care','Casa':'home','Arte e presentes':'gifts','Dia a dia':'daily','Lazer':'gaming','Mobilidade e imóveis':'mobility','Ferramentas e campo':'tools'}

TEMPLATE='''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Explore anúncios do Goofish em português na JV Busca. Catálogo por categoria, favoritos e links para seu agente."><title>__TITLE__ · JV Busca</title><link rel="icon" href="__BASE__assets/jv-mascot.png"><link rel="stylesheet" href="__BASE__shop.css?v=12"><link rel="stylesheet" href="__BASE__jv.css?v=12"><script defer src="__BASE__assets/vendor/gsap.min.js"></script><script defer src="__BASE__assets/vendor/ScrollTrigger.min.js"></script><script defer src="__BASE__shop.js?v=12"></script></head>
<body data-category="__CATEGORY__" data-view="__VIEW__"><a class="skip" href="#conteudo">Pular para os produtos</a>
<header><div class="wrap header-row"><a href="__BASE__" class="brand" aria-label="JV Busca início"><img class="brand-mascot" src="__BASE__assets/jv-mascot.png" alt=""><b>JV</b> BUSCA<span>Goofish em português</span></a><form id="search-form" role="search"><label class="sr-only" for="query">O que você procura?</label><input id="query" type="search" maxlength="120" placeholder="O que você quer encontrar hoje?" required><button>Buscar <span aria-hidden="true"><svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></span></button></form><div class="header-actions"><button id="favorites" class="outline"><svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/></svg> <span>Favoritos</span></button><button class="outline" disabled title="Convite do Discord em breve">Comunidade</button></div></div><nav class="wrap quick-nav" aria-label="Explore"><a href="__BASE__">Destaques</a><a href="__BASE__categoria/celulares/">Celulares</a><a href="__BASE__categoria/moda/">Moda</a><a href="__BASE__categoria/games/">Games</a><a href="__BASE__categoria/decoracao/">Casa</a><span>Descubra no Goofish. Explore em português.</span></nav></header>
<main class="wrap" id="conteudo"><div id="listing-view"><nav class="breadcrumb" id="breadcrumb" aria-label="Caminho">Início / Seus próximos achados</nav><section class="discovery"><aside class="category-menu"><h2>Categorias</h2><nav id="categories" aria-label="Categorias"></nav></aside><div class="hero-area"><section class="hero" id="hero"><div class="hero-copy"><span class="eyebrow" id="hero-eyebrow">GOOFISH, EM PORTUGUÊS</span><h1 id="hero-title">O que você procura<br>está por aqui.</h1><p id="hero-description">Veja os anúncios, compare os preços em reais e envie o link ao seu agente.</p><a class="button yellow" href="#products" id="hero-cta">Ver produtos <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></a></div><img class="hero-art" id="hero-art" src="__BASE__assets/jv-mascot.png" alt="Mascote" fetchpriority="high"></section><div class="mini-banners"><a href="__BASE__categoria/celulares/" class="mini-banner tech-promo"><div class="promo-copy"><span>TECNOLOGIA</span><h2>Celulares<br>e acessórios</h2><span>Ver produtos <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></span></div><div class="promo-photos" data-promo="celulares"></div></a><a href="__BASE__categoria/moda/" class="mini-banner fashion-promo"><div class="promo-copy"><span>MODA E ESPORTE</span><h2>Roupas, tênis<br>e bolsas</h2><span>Ver produtos <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></span></div><div class="promo-photos" data-promo="moda"></div></a></div></div></section>
<div class="benefit-row"><span>Anúncios do Goofish</span><span>Salve seus favoritos</span><span>Copie o link para o agente</span></div>
<section id="products"><div class="section-heading"><div><span class="eyebrow">PARA VOCÊ</span><h2 id="results-title">Destaques para você</h2><p id="results-note">Produtos de várias categorias para começar sua busca.</p></div></div><div class="category-pills" id="category-pills"></div><form id="filters" class="filter-bar"><label>Mínimo ¥<input id="min" type="number" min="0" step="0.01" placeholder="0"></label><label>Máximo ¥<input id="max" type="number" min="0" step="0.01" placeholder="Sem limite"></label><label>Ordenar<select id="sort"><option value="featured">Ordem da seleção</option><option value="asc">Menor preço</option><option value="desc">Maior preço</option></select></label><button class="button black">Filtrar</button><button type="button" id="clear-filters" class="text-link">Limpar</button></form><p id="status" role="status" aria-live="polite">Carregando achados…</p><div class="live-options" id="live-options" hidden><p>Não encontrou o que procura?</p><button class="button yellow" id="live-search">Buscar no Goofish agora <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg></button><label>Idioma da consulta<select id="query-language"><option value="pt">Português / original</option><option value="zh">Chinês</option><option value="ja">Japonês</option><option value="en">Inglês</option></select></label></div><ul id="grid" class="grid"></ul><nav id="pager" class="pager" hidden aria-label="Paginação"><button id="previous" class="button"><svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4m6-6-6 6 6 6"/></svg> Anterior</button><span id="page-label"></span><button id="next" class="button">Próxima <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16m-6-6 6 6-6 6"/></svg></button></nav></section>
<section class="wide-banner"><div><span class="eyebrow">COMO USAR</span><h2>Escolha o produto.<br>Envie para seu agente.</h2><p>No anúncio, toque em “Copiar para colar no agente”. O link e o preço vão juntos.</p><button class="button yellow" id="banner-favorites">Ver meus favoritos <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/></svg></button></div><img src="__BASE__assets/jv-mascot.png" alt="" loading="lazy"></section></div>
<section id="product-view" hidden><nav class="breadcrumb"><a href="__BASE__">Início</a> / <span>Detalhes do achado</span></nav><div id="product-content"></div><section class="section-heading"><div><span class="eyebrow">CONTINUE EXPLORANDO</span><h2>Outros achados da categoria</h2></div></section><ul id="related" class="grid"></ul></section>
<div class="currency-setting"><label>Cotação manual R$ / ¥ <input id="manual-rate" type="number" min="0.01" step="0.0001" placeholder="Usar cotação atual"></label></div></main>
<footer class="wrap"><a href="__BASE__" class="brand"><img class="brand-mascot" src="__BASE__assets/jv-mascot.png" alt=""><b>JV</b> BUSCA</a><p>Projeto independente, sem vínculo com o Goofish. Preços e disponibilidade podem mudar. Valores em reais são estimativas sem frete, taxas ou impostos.</p><p id="rate-note"></p><a href="https://www.exchangerate-api.com" target="_blank" rel="noopener noreferrer">Cotação: ExchangeRate-API</a></footer><div id="toast" role="status" hidden></div></body></html>'''

# Replace banner content at build time, so every category has its own static art and copy.
TEMPLATE=re.sub(r'<section class="hero" id="hero">.*?</section>', '__HERO__', TEMPLATE)
TEMPLATE=TEMPLATE.replace('<span>TECNOLOGIA</span>','').replace('<span>MODA E ESPORTE</span>','')
TEMPLATE=TEMPLATE.replace('<span class="eyebrow">COMO USAR</span>','')
TEMPLATE=TEMPLATE.replace('v=12','v=13')
TEMPLATE=TEMPLATE.replace('<script defer src="__BASE__shop.js?v=13">','<script defer src="__BASE__privacy.js?v=13"></script><script defer src="__BASE__shop.js?v=13">')
TEMPLATE=TEMPLATE.replace('data-view="__VIEW__"','data-view="__VIEW__" data-banner-note="__BANNER_NOTE__"')
TEMPLATE=TEMPLATE.replace('</footer>',FOOTER_LINKS+'</footer>')
TEMPLATE=TEMPLATE.replace('</body>',PRIVACY_UI+'</body>')
TEMPLATE=TEMPLATE.replace('<img src="__BASE__assets/jv-mascot.png" alt="" loading="lazy">','<img src="__BASE__assets/mascot-wave.png" alt="" loading="lazy">')


def hero(category=None):
    if category:
        d=design(category)
        title,description,image,color=d['title'],d['description'],d['image'],d['color']
        cta='Explorar '+category['label'].lower()
        visual=f'<div class="category-art"><img class="hero-art" id="hero-art" src="__BASE__{image}" alt="Ilustração de {escape(category["label"])}" fetchpriority="high"><img class="category-mascot" src="__BASE__assets/mascot-wave.png" alt="" loading="lazy"></div>'
    else:
        title='Busque no Goofish. Sem criar conta.'
        description='Seu novo jeito de encontrar produtos: anúncios em português, preços em reais e o link pronto para seu agente.'
        color='#ffe615';cta='Encontrar produtos'
        visual='<img class="hero-art" id="hero-art" src="__BASE__assets/mascot-search.png" alt="Mascote pesquisando com uma lupa" fetchpriority="high">'
    return f'<section class="hero {"category-hero" if category else "home-hero"}" id="hero" style="--category-color:{color}"><div class="hero-copy"><h1 id="hero-title">{escape(title)}</h1><p id="hero-description">{escape(description)}</p><a class="button black" href="#products" id="hero-cta">{escape(cta)} <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 12h16m-6-6 6 6-6 6"/></svg></a></div>{visual}</section>'


def render_page(title,view,base,category=None):
    html=TEMPLATE.replace('__HERO__',hero(category))
    note=design(category)['secondary'] if category else 'Guarde para ver depois.'
    if category:
        # Category landing pages have a dedicated large hero instead of repeated home promos.
        html=re.sub(r'<div class="mini-banners">.*?</a></div>', '', html)
        html=html.replace('Escolha o produto.<br>Envie para seu agente.',escape('Seus achados de '+category['label'].lower()+', prontos para compartilhar.'))
        html=html.replace('No anúncio, toque em “Copiar para colar no agente”. O link e o preço vão juntos.',escape(design(category)['secondary'])+' Abra o produto e copie as informações para seu agente.')
    return html.replace('__TITLE__',escape(title)).replace('__CATEGORY__',category['id'] if category else '').replace('__VIEW__',view).replace('__BANNER_NOTE__',escape(note,quote=True)).replace('__BASE__',base)


def build():
    catalog.export()
    (PUBLIC/'index.html').write_text(render_page('Seus próximos achados','home','./'),encoding='utf-8')
    (PUBLIC/'produto.html').write_text(render_page('Detalhes do produto','product','./'),encoding='utf-8')
    for c in catalog.CATEGORIES:
        folder=PUBLIC/'categoria'/c['id'];folder.mkdir(parents=True,exist_ok=True)
        (folder/'index.html').write_text(render_page(c['label'],'category','../../',c),encoding='utf-8')
    build_legal(PUBLIC)
    print(f'{len(catalog.CATEGORIES)} páginas de categoria com banners exclusivos, termos e privacidade gerados.')

if __name__=='__main__':build()
