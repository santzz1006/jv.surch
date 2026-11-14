from pathlib import Path
p=Path(__file__).parent/'public'
file=p/'index.html';s=file.read_text(encoding='utf-8')
s=s.replace('?v=6','?v=7').replace('<script defer src="/app.js?v=7"></script>','<script defer src="/assets/vendor/gsap.min.js"></script><script defer src="/assets/vendor/ScrollTrigger.min.js"></script><script defer src="/app.js?v=7"></script><script defer src="/catalog.js?v=7"></script><script defer src="/motion.js?v=7"></script>')
start=s.index('<aside class="categories"');end=s.index('</aside>',start)+len('</aside>')
s=s[:start]+'''<aside class="categories" aria-label="Categorias"><h2>Explore categorias</h2><button id="home-feed"><img src="/assets/icon-recommend.png" alt=""><span>Todos os achados</span><span aria-hidden="true">♡</span></button><div id="category-list"></div></aside>'''+s[end:]
marker='<section class="recommendation-heading">'
s=s.replace(marker,'''<section class="promo-band promo-fashion" aria-label="Destaque de moda"><div><span class="eyebrow">UMA NOVA HISTÓRIA</span><h2>Seu estilo.<br>Seu próximo achado.</h2><p>Roupas, tênis e acessórios para descobrir.</p><button class="btn" data-catalog="moda">Explorar moda ↗</button></div></section><section class="collection-toolbar"><div><h2>Um mundo de categorias</h2><p id="catalog-progress" role="status">Carregando catálogo…</p></div><button id="collect-categories" class="btn">Coletar categorias</button></section>'''+marker)
s=s.replace('<details class="filter-panel">','<a id="download-category" class="download-json" hidden download>Baixar JSON desta categoria ↓</a><details class="filter-panel">')
s=s.replace('<section class="session-panel"','''<section class="promo-band promo-home" aria-label="Destaque de casa"><div><span class="eyebrow">PEQUENOS ACHADOS, NOVAS IDEIAS</span><h2>Dê outra vida<br>ao seu cantinho.</h2><p>Explore móveis e decoração no catálogo.</p><button class="btn" data-catalog="decoracao">Ver casa e decoração ↗</button></div></section><section class="session-panel"''')
file.write_text(s,encoding='utf-8')
file=p/'app.js';s=file.read_text(encoding='utf-8')
s=s.replace("const li=node('li'), card=", "const li=node('li',null,'product-cell'), card=")
s=s.replace("$('grid').append(li);", "$('grid').append(li);if($('grid').querySelectorAll('.product-cell').length===10){const promo=node('li',null,'inline-promo');promo.append(node('span','GARIMPE. SALVE. COMPARE.'),node('h2','Seu próximo achado pode estar logo aqui.'),node('p','Salve seus favoritos e leve o link ao seu agente de compras.'));$('grid').append(promo);}")
s=s.replace("translationQueue.then(async()=>{try{", "translationQueue.then(async()=>{if(!title.isConnected)return;try{")
s=s.replace("$('search').onsubmit=e=>{e.preventDefault();page=1;search();}","$('search').onsubmit=e=>{e.preventDefault();imported=null;page=1;search();}")
s=s.replace("function showImported(){let rows=", "function showImported(){if(!$('filters').reportValidity())return;if($('min').value!==''&&$('max').value!==''&&Number($('min').value)>Number($('max').value)){$('status').className='error';$('status').textContent='O preço mínimo deve ser menor ou igual ao máximo.';return;}let rows=")
s=s.replace("if($('sort').value!=='relevance')rows.sort", "page=Math.max(1,Math.min(page,Math.ceil(rows.length/20)||1));if($('sort').value!=='relevance')rows.sort")
s=s.replace("'Recomendações da sua sessão'","'Achados coletados'")
s=s.replace("'Anúncios da página inicial do seu Goofish.';", "'Anúncios coletados por categoria no Goofish.';")
s=s.replace("loadRecommendations();\n", "if(initial.get('q'))search();else loadRecommendations();\n")
file.write_text(s,encoding='utf-8')
