'use strict';
window.GBCatalogStore={async open(base){
 const r=await fetch(base+'/data/catalog-index.json');if(!r.ok)throw Error('Não foi possível carregar o catálogo.');
 const db=await r.json(),items=new Map(db.items.map(i=>[i.id,i])),requests=new Map();
 async function chunk(n){if(requests.has(n))return requests.get(n);const task=(async()=>{const r=await fetch(base+'/data/'+db.chunks[n].file);if(!r.ok)throw Error('Não foi possível carregar estes produtos. Tente novamente.');const rows=await r.json();for(const i of rows)items.set(i.id,i);})();requests.set(n,task);try{await task;}catch(e){requests.delete(n);throw e;}}
 async function load({category,ids,all}={}){let needed=[];if(db.chunks){if(all)needed=db.chunks.map((_,n)=>n);else if(ids)needed=[...new Set(ids.map(id=>db.productChunks[id]).filter(n=>n!==undefined))];else if(category)needed=db.chunks.map((c,n)=>c.categories.includes(category)?n:-1).filter(n=>n>=0);}
  // Four concurrent static downloads; no third-party RPCs in the public site.
  let cursor=0;await Promise.all(Array.from({length:Math.min(4,needed.length)},async()=>{while(cursor<needed.length)await chunk(needed[cursor++]);}));db.items=[...items.values()];return db;
 }
 return {db,load};
}};
