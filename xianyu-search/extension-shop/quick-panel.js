'use strict';
(()=>{
 const $=id=>document.getElementById(id),node=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
 const message=t=>$('status').textContent=t;
 const action=fn=>async()=>{try{await fn();}catch(e){message(e.message);}};
 let local={items:[],suppliers:[]};
 async function refresh(){const d=await chrome.storage.local.get(['goofishBr','gbQuickSearch']);local=d.goofishBr||{items:[],suppliers:[]};$('quick-enabled').checked=d.gbQuickSearch!==false;draw();}
 async function patch(values){const d=await chrome.storage.local.get('goofishBr');local={...(d.goofishBr||{}),...values};await chrome.storage.local.set({goofishBr:local});window.dispatchEvent(new Event('gb-collection-change'));draw();}
 function button(text,fn){const b=node('button',text);b.type='button';b.onclick=action(fn);return b;}
 function draw(){const q=$('saved-filter').value.trim().toLocaleLowerCase('pt-BR');$('saved-list').replaceChildren();
  for(const item of (local.items||[]).filter(i=>[i.title,i.folder].join(' ').toLocaleLowerCase('pt-BR').includes(q))){const card=node('article');card.className='saved-card';const img=node('img');img.src=GB.safeUrl(item.images?.[0])||'assets/mascot-heart.png';img.alt='';img.loading='lazy';img.referrerPolicy='no-referrer';const copy=node('div');copy.append(node('h3',item.title),node('p',item.folder||'Meus achados'));const actions=node('div');actions.className='actions';actions.append(button('Ver produto',()=>GBExplore.show(item)),button('Remover',()=>patch({items:(local.items||[]).filter(i=>i.id!==item.id)})));copy.append(actions);card.append(img,copy);$('saved-list').append(card);}
  if(!$('saved-list').children.length)$('saved-list').append(node('p','Salve um produto da pesquisa para encontrá-lo aqui.'));
  $('saved-suppliers').replaceChildren();for(const store of local.suppliers||[]){const card=node('div');card.className='supplier-card';const a=node('a',store.name);a.href=GB.safeUrl(store.url);a.target='_blank';a.rel='noopener noreferrer';card.append(a,button('Remover',()=>patch({suppliers:local.suppliers.filter(s=>s.url!==store.url)})));$('saved-suppliers').append(card);}
 }
 $('saved-filter').oninput=draw;
 $('capture').onclick=action(async()=>{const [tab]=await chrome.tabs.query({active:true,currentWindow:true});if(!tab?.id||!/^https:\/\/(www\.)?goofish\.com\//.test(tab.url||''))throw Error('Abra um anúncio no Goofish para salvá-lo.');const [r]=await chrome.scripting.executeScript({target:{tabId:tab.id},func:readGoofishProduct});if(!r?.result)throw Error('Anúncio indisponível nesta página.');const d=await chrome.storage.local.get('goofishBr');await patch({items:GB.save(d.goofishBr?.items||[],r.result,$('save-folder').value)});message('Anúncio salvo na sua coleção.');});
 $('quick-enabled').onchange=action(async()=>{await chrome.storage.local.set({gbQuickSearch:$('quick-enabled').checked});message($('quick-enabled').checked?'Atalho ativado no Goofish.':'Atalho ocultado no Goofish.');});
 $('quick-prices').onclick=action(async()=>{if(!local.rate)throw Error('Salve uma cotação primeiro.');const [tab]=await chrome.tabs.query({active:true,currentWindow:true});if(!tab?.id||!/^https:\/\/(www\.)?goofish\.com\//.test(tab.url||''))throw Error('Abra o Goofish para exibir os valores em reais.');const [r]=await chrome.scripting.executeScript({target:{tabId:tab.id},func:addGoofishPrices,args:[local.rate]});message((r?.result||0)+' preços identificados nesta aba.');});
 $('quick-rate-form').onsubmit=e=>{e.preventDefault();action(async()=>{await patch({rate:GB.rate($('quick-rate').value)});message('Cotação atualizada.');})();};
 $('quick-supplier-form').onsubmit=e=>{e.preventDefault();action(async()=>{const name=$('quick-supplier-name').value.trim(),url=GB.safeUrl($('quick-supplier-url').value);if(!name||!url)throw Error('Informe o nome e um endereço https válido.');await patch({suppliers:[{name:name.slice(0,100),url},...(local.suppliers||[]).filter(s=>s.url!==url)].slice(0,500)});$('quick-supplier-form').reset();})();};
 window.addEventListener('gb-collection-change',()=>refresh().catch(e=>message(e.message)));
 chrome.storage.onChanged?.addListener((changes,area)=>{if(area==='local'&&(changes.goofishBr||changes.gbQuickSearch))refresh().catch(e=>message(e.message));});
 refresh().catch(e=>message(e.message));
})();
