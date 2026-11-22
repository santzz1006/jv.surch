'use strict';
importScripts('catalog-search.js');
let cataloguePromise;
function getCatalogue(){if(!cataloguePromise)cataloguePromise=fetch(chrome.runtime.getURL('data/catalog.json')).then(r=>{if(!r.ok)throw Error('Catálogo indisponível. Reinstale a extensão.');return r.json();}).catch(e=>{cataloguePromise=null;throw e;});return cataloguePromise;}
async function catalogueMessage(request){
 const data=await getCatalogue();
 if(request.action==='meta')return {categories:data.categories,rate:data.rate,updatedAt:data.updatedAt,total:data.items.length};
 if(request.action==='search'){
  const filters={...request.filters,q:String(request.filters?.q||'').slice(0,120)};
  const rows=GBCatalog.search(data.items,filters),page=Math.min(Math.max(1,Math.floor(Number(request.page)||1)),Math.max(1,Math.ceil(rows.length/24)));
  return {items:rows.slice((page-1)*24,page*24),total:rows.length,page};
 }
 throw Error('Operação de catálogo desconhecida.');
}
chrome.runtime.onMessage.addListener((request,sender,reply)=>{
 if(request?.type!=='gb-catalog')return;
 if(sender.id!==chrome.runtime.id||!sender.url?.startsWith(chrome.runtime.getURL('')))return;
 catalogueMessage(request).then(data=>reply({ok:true,data}),e=>reply({ok:false,error:e.message}));return true;
});
