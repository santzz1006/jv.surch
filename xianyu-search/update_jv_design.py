from pathlib import Path
import re

root=Path(__file__).parent
p=root/'build_site.py';s=p.read_text(encoding='utf-8')
s=s.replace('Alpha Busca','JV Busca').replace('<b>ALPHA</b> BUSCA','<img class="brand-mascot" src="__BASE__assets/jv-mascot.png" alt=""><b>JV</b> BUSCA')
s=s.replace('seu próximo achado','Goofish em português').replace('Por onde começar?','Categorias')
s=s.replace('DA CHINA PARA SUAS IDEIAS','GOOFISH, EM PORTUGUÊS').replace('Grandes achados.<br>Novas possibilidades.','O que você procura<br>está por aqui.')
s=s.replace('Explore produtos, compare preços e encontre algo que tem a sua cara.','Veja os anúncios, compare os preços em reais e envie o link ao seu agente.').replace('Vamos garimpar ↗','Ver produtos ↗')
s=s.replace('assets/icon-tech.png" alt="" fetchpriority','assets/jv-mascot.png" alt="Mascote" fetchpriority')
start=s.index('<div class="mini-banners">');end=s.index('</section>\n<div class="benefit-row">',start)
s=s[:start]+'''<div class="mini-banners"><a href="__BASE__categoria/celulares/" class="mini-banner tech-promo"><div class="promo-copy"><span>TECNOLOGIA</span><h2>Celulares<br>e acessórios</h2><span>Ver produtos ↗</span></div><div class="promo-photos" data-promo="celulares"></div></a><a href="__BASE__categoria/moda/" class="mini-banner fashion-promo"><div class="promo-copy"><span>MODA E ESPORTE</span><h2>Roupas, tênis<br>e bolsas</h2><span>Ver produtos ↗</span></div><div class="promo-photos" data-promo="moda"></div></a></div></div>'''+s[end:]
s=s.replace('✦ Anúncios reais do Goofish','Anúncios do Goofish').replace('♡ Seus favoritos em um lugar','Salve seus favoritos').replace('↗ Copie e envie ao seu agente','Copie o link para o agente')
s=re.sub(r'<a href="__BASE__data/products.json"[^>]*>.*?</a>','',s)
s=s.replace('VALE A DESCOBERTA','PARA VOCÊ').replace('Uma seleção de diferentes categorias do nosso catálogo.','Produtos de várias categorias para começar sua busca.')
s=s.replace('Quer explorar além do catálogo salvo?','Não encontrou o que procura?').replace('DA DESCOBERTA AO SEU AGENTE','COMO USAR').replace('Gostou? Salve.<br>Encontrou? Compartilhe.','Escolha o produto.<br>Envie para seu agente.').replace('Abra o produto e copie as informações para conversar com seu agente de compras.','No anúncio, toque em “Copiar para colar no agente”. O link e o preço vão juntos.').replace('assets/icon-recommend.png','assets/jv-mascot.png')
s=re.sub(r'<details class="admin">.*?</details>', '<div class="currency-setting"><label>Cotação manual R$ / ¥ <input id="manual-rate" type="number" min="0.01" step="0.0001" placeholder="Usar cotação atual"></label></div>',s,flags=re.S)
s=s.replace('shop.css?v=11','shop.css?v=12').replace('shop.js?v=11','shop.js?v=12')
# SVG paths render consistently on Android/iOS, unlike Unicode arrows.
paths={'↗':'M7 17 17 7M7 7h10v10','→':'M4 12h16m-6-6 6 6-6 6','←':'M20 12H4m6-6-6 6 6 6','♡':'M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z'}
for char,path in paths.items():
    s=s.replace(char,'<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="'+path+'"/></svg>')
p.write_text(s,encoding='utf-8')
p=root/'public/shop.js';s=p.read_text(encoding='utf-8')
s=s.replace('Alpha Busca','JV Busca').replace('Detalhes atualizados e salvos no JSON.','Fotos e detalhes atualizados.')
s=s.replace('GARIMPE. SALVE. COMPARE.','NA SUA LISTA').replace('Um achado muda tudo.','Guarde para ver depois.').replace('Salve o que gostou e leve o link ao seu agente.','Toque no coração para salvar seus produtos favoritos.').replace("picture(BASE+'/assets/icon-gifts.png')","picture(BASE+'/assets/jv-mascot.png')")
s=s.replace("'no catálogo salvo'","'encontrados'").replace('Não há resultados salvos para esta pesquisa. Você pode consultar o Goofish abaixo.','Nenhum produto encontrado. Tente outro termo ou consulte o Goofish.').replace('Busca nos anúncios já salvos. Você também pode consultar a sessão do Goofish.','Confira os resultados ou busque mais anúncios no Goofish.')
s=s.replace("current.label+'. Novos achados para você.'","current.label").replace("'Explore a seleção de '+current.label.toLowerCase()+', compare os anúncios e descubra sua próxima ideia.'","'Compare os anúncios de '+current.label.toLowerCase()+' e veja os preços em reais.'")
s=s.replace("el('hero-art').src=BASE+'/assets/icon-'+current.icon+'.png';","el('hero-art').src=BASE+'/assets/jv-mascot.png';")
s=s.replace("'Categoria aguardando coleta'","'Novos produtos em breve'").replace("' · resultados salvos do Goofish.'","' · anúncios do Goofish.'").replace('SEU PRÓXIMO ACHADO','DETALHES DO PRODUTO')
s=s.replace('Uma foto disponível no catálogo. Atualize o anúncio para consultar a galeria.','Uma foto disponível. Consulte o anúncio para ver mais detalhes.')
s=s.replace('Anúncio não encontrado no catálogo.','Anúncio não encontrado.').replace('Os produtos salvos continuam disponíveis.','Os outros produtos continuam disponíveis.')
s=re.sub(r"async function health\(\)\{.*?\nasync function init",'async function init',s,flags=re.S)
s=s.replace('}health();','}')
s=re.sub(r"el\('collect'\).onclick=.*?\ninit\(\);",'init();',s,flags=re.S)
s=s.replace('categoryUI();const params=', 'categoryUI();promoPhotos();const params=')
# Consistent icons for dynamically created controls as well.
s=s.replace('if(text)n.textContent=text;','if(text)label(n,text);')
s=s.replace("b.textContent=favorites.includes(item.id)?'♥':'♡';","label(b,favorites.includes(item.id)?'♥':'♡');")
addition='''
function label(node,text){
  node.replaceChildren();
  const paths={'↗':'M7 17 17 7M7 7h10v10','→':'M4 12h16m-6-6 6 6-6 6','←':'M20 12H4m6-6-6 6 6 6','♡':'M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z'};
  for(const part of String(text).split(/([↗→←♡♥])/)){if(!part)continue;const key=part==='♥'?'♡':part;if(!paths[key]){node.append(document.createTextNode(part));continue;}const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');for(const [k,v]of Object.entries({class:'ui-icon',viewBox:'0 0 24 24',fill:part==='♥'?'currentColor':'none',stroke:'currentColor','stroke-width':'1.8','stroke-linecap':'round','stroke-linejoin':'round','aria-hidden':'true'}))svg.setAttribute(k,v);const p=document.createElementNS(svg.namespaceURI,'path');p.setAttribute('d',paths[key]);svg.append(p);node.append(svg);}
}
function promoPhotos(){for(const host of document.querySelectorAll('[data-promo]')){const choices=db.items.filter(i=>i.categories?.includes(host.dataset.promo)&&goodImage(i.image));for(const item of choices.slice(0,2))host.append(picture(item.image,title(item)));}}
'''
s=s.replace("const categoryId=",addition+"\nconst categoryId=",1)
p.write_text(s,encoding='utf-8')
print('Identidade e interface atualizadas.')
