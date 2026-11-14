const $ = id => document.getElementById(id);
let page = 1, busy = false, imported = null, dataLabel = "Resultados importados";
let saved=[];try{const value=JSON.parse(localStorage.getItem('alpha.favorites')||'[]');if(Array.isArray(value))saved=value;}catch{}
let translationQueue=Promise.resolve();
const yuan = new Intl.NumberFormat('pt-BR', {style:'currency',currency:'CNY'});
function node(tag, text, cls) {const n=document.createElement(tag);if(text)n.textContent=text;if(cls)n.className=cls;return n;}
function safeUrl(value) {try {const u=new URL(value);return ['https:','http:'].includes(u.protocol)?u.href:'';}catch{return '';}}
function render(items) {
  $('grid').replaceChildren();
  for(const raw of items){const item={...raw};const rate=Number($('exchange').value);if(rate>0&&item.priceCny!==null)item.priceBrl=Number((item.priceCny*rate).toFixed(2));
    const li=node('li',null,'product-cell'), card=node('article',null,'card'), photo=node('div',null,'photo'), inside=node('div',null,'in');
    const image=safeUrl(item.image);
    if(image){const img=node('img');img.src=image;img.alt='';img.loading='lazy';img.referrerPolicy='no-referrer';img.onerror=()=>photo.replaceChildren(node('span','Sem imagem','empty-image'));photo.append(img);}else photo.append(node('span','Sem imagem','empty-image'));
    const title=node('h3',item.title),price=node('div',null,'price');price.append(node('strong',item.priceCny===null?'Preço não informado':yuan.format(item.priceCny)));
    inside.append(title,price);if(item.seller?.name){const seller=node('div',null,'seller');if(safeUrl(item.seller.avatarUrl)){const avatar=node('img');avatar.src=safeUrl(item.seller.avatarUrl);avatar.alt='';seller.append(avatar);}seller.append(node('span',item.seller.name));inside.append(seller);}if(/[\u3400-\u9fff\u3040-\u30ff]/.test(item.title)){title.title=item.title;translationQueue=translationQueue.then(async()=>{if(!title.isConnected)return;try{const r=await fetch('/api/translate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:item.title,lang:/[\u3040-\u30ff]/.test(item.title)?'ja':'zh-CN'})});const data=await r.json();if(r.ok&&title.isConnected)title.textContent=data.text;}catch{}});}const star=node('button',saved.some(x=>x.id===item.id)?'♥ Salvo':'♡ Salvar','star');star.onclick=()=>{const exists=saved.some(x=>x.id===item.id);saved=exists?saved.filter(x=>x.id!==item.id):[...saved,item];localStorage.setItem('alpha.favorites',JSON.stringify(saved));star.textContent=exists?'♡ Salvar':'♥ Salvo';};inside.append(star);const copy=node('button','Copiar link para o agente','star');copy.onclick=async()=>{try{await navigator.clipboard.writeText([item.title,item.description||'',item.priceCny!==null?'¥ '+item.priceCny:'',item.priceBrl!=null?'R$ '+item.priceBrl:'',item.url].filter(Boolean).join('\n'));copy.textContent='Link copiado ✓';}catch{copy.textContent='Abra o anúncio e copie a URL';}};inside.append(copy);if(item.area)inside.append(node('p',item.area,'meta'));if(item.priceBrl!=null)price.prepend(node('strong',new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(item.priceBrl)+' · '));const url=safeUrl(item.url);if(url){const link=node('a','Ver no Xianyu ↗','buy');link.href=url;link.target='_blank';link.rel='noopener noreferrer';inside.append(link);}
    const details=node('button','Ver produto e vendedor','star');details.onclick=()=>openProduct(item);inside.append(details);card.append(photo,inside);li.append(card);$('grid').append(li);if($('grid').querySelectorAll('.product-cell').length===10){const promo=node('li',null,'inline-promo');promo.append(node('span','GARIMPE. SALVE. COMPARE.'),node('h2','Seu próximo achado pode estar logo aqui.'),node('p','Salve seus favoritos e leve o link ao seu agente de compras.'));$('grid').append(promo);}
  }
}
async function search(){
  if(busy)return;if(imported){showImported();return;}if(!$('q').value.trim())return;
  if(!$('filters').reportValidity())return;
  if($('min').value!=='' && $('max').value!=='' && Number($('min').value)>Number($('max').value)){$('status').className='error';$('status').textContent='O preço mínimo deve ser menor ou igual ao máximo.';return;}
  busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);
  $('intro').hidden=true;$('pager').hidden=true;$('feed-title').textContent='Resultados da busca';$('feed-note').textContent=$('q').value.trim();render([]);$('status').className='';$('status').textContent='Consultando o Xianyu… O navegador local pode abrir; aguarde até um minuto.';
  const params=new URLSearchParams({q:$('q').value.trim(),page:String(page),min:$('min').value,max:$('max').value,sort:$('sort').value,source:$('source').value,lang:$('language').value});
  history.replaceState(null,'','?'+params);
  const controller=new AbortController();const timeout=setTimeout(()=>controller.abort(),90000);
  try{const response=await fetch('/api/search?'+params,{signal:controller.signal});const data=await response.json();if(!response.ok)throw new Error(data.error || 'Falha ao buscar.');
    render(data.items);$('status').textContent=data.total?`${data.total} anúncios após os filtros, de ${data.collected} coletados.${data.cached?' Consulta em cache (até 5 minutos).':''}`:'Nenhum anúncio encontrado para esta consulta e faixa de preço.';
    $('pager').hidden=page===1&&!data.hasMore;$('page').textContent=`Página ${page}`;$('prev').dataset.disabled=String(page<=1);$('next').dataset.disabled=String(!data.hasMore);
  }catch(error){$('status').className='error';$('status').textContent=error.name==='AbortError'?'A busca demorou demais. Aguarde o coletor encerrar antes de tentar novamente.':error.message;}
  finally{clearTimeout(timeout);busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);$('prev').disabled=$('prev').dataset.disabled==='true';$('next').disabled=$('next').dataset.disabled==='true';$('community').disabled=!localStorage.getItem('alpha.discord');refreshHealth();}
}
$('search').onsubmit=e=>{e.preventDefault();imported=null;page=1;search();};$('filters').onsubmit=e=>{e.preventDefault();page=1;search();};
document.querySelectorAll('[data-query]').forEach(b=>b.onclick=()=>{$('q').value=b.dataset.query;imported=null;page=1;search();});
$('prev').onclick=()=>{page--;search();};$('next').onclick=()=>{page++;search();};
const initial=new URLSearchParams(location.search);for(const key of ['q','min','max','sort'])if(initial.has(key))$(key).value=initial.get(key);
async function refreshHealth(){
  try{const response=await fetch('/api/health');if(!response.ok)throw new Error();const data=await response.json();$('connection').textContent=data.bridge?.connected?'Chrome conectado · a API usa os anúncios visíveis na sua sessão.':'API local online · conecte a extensão no Chrome para usar sua sessão.';$('finish-session').hidden=!data.sessionOpen;}
  catch{$('connection').textContent='API local desconectada. Inicie o servidor para pesquisar.';}
}
async function session(action){
  if($('source').value==='chrome'){$('session-note').textContent='Instale a extensão Alpha Busca no Chrome conectado ao Goofish e clique em Ativar conexão. A pasta extension está no projeto.';return;}
  if(busy)return;busy=true;$('open-session').disabled=true;$('finish-session').disabled=true;
  try{const response=await fetch('/api/session/'+action+'?source='+$('source').value,{method:'POST'});const data=await response.json();if(!response.ok)throw new Error(data.error);
    $('session-note').textContent=action==='open'?'Entre na janela do Xianyu. Depois volte aqui e clique em Salvar sessão.':data.message;
    $('finish-session').hidden=action!=='open';
  }catch(error){$('session-note').textContent=error.message;}
  finally{busy=false;$('open-session').disabled=false;$('finish-session').disabled=false;refreshHealth();}
}
$('open-session').onclick=()=>session('open');$('finish-session').onclick=()=>session('finish');refreshHealth();

function showImported(){if(!$('filters').reportValidity())return;if($('min').value!==''&&$('max').value!==''&&Number($('min').value)>Number($('max').value)){$('status').className='error';$('status').textContent='O preço mínimo deve ser menor ou igual ao máximo.';return;}let rows=imported.filter(x=>($('min').value===''||x.priceCny!==null&&x.priceCny>=Number($('min').value))&&($('max').value===''||x.priceCny!==null&&x.priceCny<=Number($('max').value)));page=Math.max(1,Math.min(page,Math.ceil(rows.length/20)||1));if($('sort').value!=='relevance')rows.sort((a,b)=>(a.priceCny===null)-(b.priceCny===null)||((a.priceCny||0)-(b.priceCny||0))*($('sort').value==='asc'?1:-1));render(rows.slice((page-1)*20,page*20));$('intro').hidden=true;$('status').className='';$('status').textContent=`${dataLabel}: ${rows.length} anúncios. Filtros aplicados à lista carregada.`;$('pager').hidden=rows.length<=20;$('page').textContent=`Página ${page}`;$('prev').disabled=page<=1;$('next').disabled=page*20>=rows.length;}
$('json-file').onchange=async e=>{try{const file=e.target.files[0];if(!file)return;if(file.size>5000000)throw new Error('JSON muito grande (máximo 5 MB).');const data=JSON.parse(await file.text());const rows=data.items;if(!Array.isArray(rows))throw new Error('Selecione uma resposta com items, não uma sessão ou telemetria.');imported=rows.filter(x=>x&&typeof x.title==='string').map(x=>({id:String(x.id||x.url||x.title),title:x.titleTranslated||x.title,image:x.image||x.pictureUrl||'',priceCny:typeof x.priceCny==='number'&&Number.isFinite(x.priceCny)?x.priceCny:null,priceBrl:typeof x.priceBrl==='number'&&Number.isFinite(x.priceBrl)?x.priceBrl:null,description:x.descriptionTranslated||x.description||'',seller:x.seller||null,reviews:Array.isArray(x.reviews)?x.reviews:[],area:typeof x.area==='string'?x.area:'',url:x.buyUrl||x.url||(x.id?'https://www.goofish.com/item?id='+encodeURIComponent(x.id):'')}));page=1;showImported();}catch(err){$('status').className='error';$('status').textContent=err.message;}};
$('favorites').onclick=()=>{dataLabel='Favoritos';$('feed-title').textContent='Seus favoritos';imported=[...saved];page=1;showImported();};
$('source').onchange=()=>{imported=null;$('status').textContent='Fonte alterada. Faça uma nova busca.';};
$('q').addEventListener('input',()=>{imported=null;});
$('discord-url').value=localStorage.getItem('alpha.discord')||'';
$('save-discord').onclick=()=>{try{const u=new URL($('discord-url').value);if(u.protocol!=='https:'||!['discord.gg','discord.com'].includes(u.hostname))throw new Error();localStorage.setItem('alpha.discord',u.href);$('status').textContent='Comunidade configurada.';}catch{$('status').textContent='Informe um convite HTTPS válido do Discord.';}};
$('community').onclick=()=>{const u=localStorage.getItem('alpha.discord');if(u)window.open(u,'_blank','noopener,noreferrer');else{document.querySelector('.import-panel').open=true;$('discord-url').focus();$('status').textContent='Configure o convite do seu Discord para ativar o botão.';}};

function openProduct(item){const host=$('detail-body');host.replaceChildren();host.append(node('h2',item.title));if(safeUrl(item.image)){const image=node('img');image.src=safeUrl(item.image);image.alt=item.title;host.append(image);}const desc=node('p',item.description||'A fonte não forneceu a descrição completa.','detail-copy');host.append(desc);const translate=node('button','Traduzir título e descrição para português','btn');translate.onclick=async()=>{translate.disabled=true;try{const r=await fetch('/api/translate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:[item.title,item.description||''].join('\n'),lang:$('language').value==='ja'?'ja':'zh-CN'})});const d=await r.json();if(!r.ok)throw new Error(d.error);desc.textContent=d.text;}catch(e){desc.textContent=e.message;}finally{translate.disabled=false;}};host.append(translate);host.append(node('h3','Vendedor'));const seller=item.seller;if(seller&&typeof seller==='object'){const box=node('div',null,'seller');const pic=safeUrl(seller.avatarUrl||seller.avatar||'');if(pic){const img=node('img');img.src=pic;img.alt='Foto do vendedor';box.append(img);}box.append(node('p',String(seller.name||'Nome não informado')));host.append(box);host.append(node('p','Nível / reputação: '+String(seller.creditLabel||seller.level||'não informado')));host.append(node('p','Vendas: '+String(seller.stats?.totalSold??seller.totalSold??'não informado')));const url=safeUrl(seller.url||'');if(url){const a=node('a','Ver loja e histórico disponível ↗','btn');a.href=url;a.target='_blank';a.rel='noopener noreferrer';host.append(a);}}else host.append(node('p','Perfil, reputação e histórico não foram fornecidos pela fonte.'));host.append(node('h3','Avaliações'));if(item.reviews?.length){for(const review of item.reviews.slice(0,20))host.append(node('p',typeof review==='string'?review:String(review.text||review.content||'')));}else host.append(node('p','Nenhuma avaliação foi fornecida pela fonte.'));host.append(node('p','Conversão manual ou valor recebido da fonte. Não inclui frete, taxas ou impostos.'));$('product-detail').showModal();if(/[\u3400-\u9fff\u3040-\u30ff]/.test(item.description||''))translate.click();}
$('close-detail').onclick=()=>$('product-detail').close();

async function loadRecommendations(refresh=false){
  if(busy)return;busy=true;$('refresh-feed').disabled=true;page=1;
  $('feed-title').textContent='Recomendados para explorar';
  if(refresh){$('status').className='';$('status').textContent='Carregando a página inicial do Goofish no seu Chrome…';}
  try{const r=await fetch('/api/recommendations'+(refresh?'/refresh':''),refresh?{method:'POST'}:{});const data=await r.json();if(!r.ok)throw new Error(data.error);
    imported=data.items;dataLabel='Achados coletados';
    $('feed-note').textContent=data.updatedAt?'Capturado em '+new Date(data.updatedAt).toLocaleString('pt-BR')+' · recomendações exibidas pelo Goofish.':'Anúncios coletados por categoria no Goofish.';
    if(imported.length){showImported();}
    else{render([]);$('pager').hidden=true;$('status').className='empty-feed';$('status').replaceChildren();const icon=node('img');icon.src='/assets/icon-recommend.png';icon.alt='';$('status').append(icon,node('h3','Seus próximos achados aparecem aqui'),node('p','Conecte a extensão ao Chrome que já está logado no Goofish e atualize as recomendações. Esta área mostra apenas anúncios reais coletados da sua sessão.'));}
  }catch(e){$('status').className='error';$('status').textContent=e.message;}
  finally{busy=false;$('refresh-feed').disabled=false;refreshHealth();}
}
$('refresh-feed').onclick=()=>loadRecommendations(true);$('home-feed').onclick=()=>loadRecommendations();if(initial.get('q'))search();else loadRecommendations();
