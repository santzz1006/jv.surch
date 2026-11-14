from pathlib import Path
p=Path('build_site.py')
s=p.read_text(encoding='utf-8')
s=s.replace('import catalog','import catalog\nimport re\nfrom category_design import design\nfrom legal_pages import PRIVACY_UI, FOOTER_LINKS, build_legal')
a=s.index('def build():')
s=s[:a]+'''# Replace banner content at build time, so every category has its own static art and copy.
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
'''
p.write_text(s,encoding='utf-8')
p=Path('public/shop.js');s=p.read_text(encoding='utf-8')
s=s.replace("localStorage.getItem('alpha.favorites')", "(window.JVPrivacy?.canRemember()?localStorage.getItem('jv.favorites'):null)")
s=s.replace("localStorage.setItem('alpha.favorites',JSON.stringify(favorites));", "if(window.JVPrivacy?.canRemember())localStorage.setItem('jv.favorites',JSON.stringify(favorites));else toast('Favorito salvo nesta página. Para lembrar depois, permita preferências no rodapé.');")
s=s.replace("copy.append(make('span','NA SUA LISTA','eyebrow'),make('h2','Guarde para ver depois.'),", "copy.append(make('h2',document.body.dataset.bannerNote||'Guarde para ver depois.'),")
s=s.replace("picture(BASE+'/assets/jv-mascot.png'));el('grid')", "picture(BASE+'/assets/mascot-heart.png'));el('grid')")
s=s.replace("picture(BASE+'/assets/icon-'+categories[0].icon+'.png')", "picture(BASE+'/assets/categories/'+categories[0].id+'.png')")
s=s.replace("a.append(make('span',c.label),make('small',String(c.count)))", "a.append(picture(BASE+'/assets/categories/'+c.id+'.png','','subcategory-icon'),make('span',c.label),make('small',String(c.count)))")
s=s.replace("const a=make('a',c.label,'pill'+", "const a=make('a',null,'pill'+")
s=s.replace("el('category-pills').append(a);", "a.append(picture(BASE+'/assets/categories/'+c.id+'.png'),make('span',c.label));el('category-pills').append(a);")
start=s.index("el('hero-title').textContent=current.label;")
end=s.index("el('results-title').textContent=current.label;",start)
s=s[:start]+s[end:]
s=s.replace("init();", "window.addEventListener('jv:privacy',e=>{if(e.detail.preferences){try{localStorage.setItem('jv.favorites',JSON.stringify(favorites));}catch{}}});\ninit();")
p.write_text(s,encoding='utf-8')
