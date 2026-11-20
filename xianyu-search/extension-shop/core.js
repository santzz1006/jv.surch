'use strict';
(function(root){
  const SITE='https://santzz1006.github.io/jv.surch/xianyu-search/public/';
  function safeUrl(value){try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password?u.href:'';}catch{return '';}}
  function itemUrl(value){try{const u=new URL(value);return /^https:$/.test(u.protocol)&&['www.goofish.com','goofish.com'].includes(u.hostname)&&u.pathname==='/item'&&/^\d+$/.test(u.searchParams.get('id')||'')?'https://www.goofish.com/item?id='+u.searchParams.get('id'):'';}catch{return '';}}
  function price(value){const m=String(value).replace(/,/g,'').match(/[¥￥]\s*(\d+(?:\s*\.\s*\d+)?)(\s*万)?/);if(!m)return null;const n=Number(m[1].replace(/\s/g,''))*(m[2]?10000:1);return Number.isFinite(n)?n:null;}
  function rate(value){const n=Number(value);if(!Number.isFinite(n)||n<=0||n>100)throw new Error('Informe uma cotação maior que zero e até 100.');return n;}
  function brl(value,r){return Number.isFinite(value)&&r?new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(value*rate(r)):'Cotação não definida';}
  function normalize(raw){const url=itemUrl(raw.url);if(!url)throw new Error('Abra um anúncio válido do Goofish.');const n=raw.priceCny;return {id:new URL(url).searchParams.get('id'),url,title:String(raw.title||'Anúncio do Goofish').slice(0,300),description:String(raw.description||'').slice(0,4000),priceCny:typeof n==='number'&&Number.isFinite(n)&&n>=0?n:null,images:[...new Set((Array.isArray(raw.images)?raw.images:[]).map(safeUrl).filter(Boolean))].slice(0,12),seller:String(raw.seller||'').slice(0,100)};}
  function save(items,raw,folder,now=new Date().toISOString()) {const item=normalize(raw),old=items.find(x=>x.id===item.id);return [{...item,folder:String(folder||old?.folder||'Meus achados').trim().slice(0,60)||'Meus achados',savedAt:old?.savedAt||now,checkedAt:now,previousPrice:old&&old.priceCny!==item.priceCny?old.priceCny:(old?.previousPrice??null)},...items.filter(x=>x.id!==item.id)].slice(0,1000);}
  function agentText(item,r){return [item.title,item.description,item.priceCny!==null?'Preço: ¥ '+item.priceCny+(r?' / '+brl(item.priceCny,r)+' (estimativa)':''):'Preço não informado',item.seller?'Vendedor: '+item.seller:'',item.url,'Confirmar disponibilidade, estado, frete e taxas com o vendedor.'].filter(Boolean).join('\n');}
  function searchUrl(q,source){q=String(q).trim().slice(0,200);if(!q)throw new Error('Digite o que você procura.');return source==='goofish'?'https://www.goofish.com/search?q='+encodeURIComponent(q):SITE+'?q='+encodeURIComponent(q);}
  root.GB={SITE,safeUrl,itemUrl,price,rate,brl,normalize,save,agentText,searchUrl};
  if(typeof module==='object')module.exports=root.GB;
})(globalThis);
