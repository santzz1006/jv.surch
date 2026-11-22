'use strict';
importScripts('catalog-search.js');
let cataloguePromise;
function getCatalogue(){if(!cataloguePromise)cataloguePromise=fetch(chrome.runtime.getURL('data/catalog.json')).then(r=>{if(!r.ok)throw Error('Catálogo indisponível. Reinstale a extensão.');return r.json();}).catch(e=>{cataloguePromise=null;throw e;});return cataloguePromise;}
const sharedCache=new Map();
async function sharedProducts(q){
 const cached=sharedCache.get(q);if(cached&&Date.now()-cached.at<30000)return cached.items;
 try{
  const response=await fetch('https://goofish-br-api.neilan-sttephan1.workers.dev/api/catalog/search?q='+encodeURIComponent(q),{signal:AbortSignal.timeout(4000),credentials:'omit'});
  if(!response.ok)throw Error('Catálogo remoto indisponível');
  const data=await response.json();if(!Array.isArray(data.items))throw Error('Resposta inválida');
  const items=data.items.filter(i=>/^\d+$/.test(i.id)&&typeof i.title==='string'&&Array.isArray(i.images)).slice(0,48);
  if(sharedCache.size>=50)sharedCache.delete(sharedCache.keys().next().value);
  sharedCache.set(q,{at:Date.now(),items});return items;
 }catch{return cached?.items||[];}
}
async function catalogueMessage(request){
 const data=await getCatalogue();
 if(request.action==='meta')return {categories:data.categories,rate:data.rate,updatedAt:data.updatedAt,total:data.items.length};
 if(request.action==='search'){
  const filters={...request.filters,q:String(request.filters?.q||'').slice(0,120)};
  const fresh=await sharedProducts(filters.q),merged=new Map(data.items.map(i=>[i.id,i]));for(const item of fresh)merged.set(item.id,item);
  const rows=GBCatalog.search([...merged.values()],filters),page=Math.min(Math.max(1,Math.floor(Number(request.page)||1)),Math.max(1,Math.ceil(rows.length/24)));
  return {items:rows.slice((page-1)*24,page*24),total:rows.length,page};
 }
 throw Error('Operação de catálogo desconhecida.');
}
chrome.runtime.onMessage.addListener((request,sender,reply)=>{
 if(request?.type!=='gb-catalog')return;
 if(sender.id!==chrome.runtime.id||!sender.url?.startsWith(chrome.runtime.getURL('')))return;
 catalogueMessage(request).then(data=>reply({ok:true,data}),e=>reply({ok:false,error:e.message}));return true;
});
