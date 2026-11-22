import {ApiError,item,text} from './model.mjs';
const fold=s=>s.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
export async function saveSearchResults(env,items){
 const at=new Date().toISOString(),unique=new Map();
 for(const raw of items){const i=item(raw);const product={id:i.id,url:i.url,title:i.title,description:i.description,priceCny:i.priceCny,images:i.images,seller:i.seller,titleOriginal:text(raw.titleOriginal,500),sellerCredit:text(raw.sellerCredit,120),area:text(raw.area,100),categories:(raw.categories||[]).slice(0,6).map(c=>text(c,40))};unique.set(i.id,product);}
 if(!unique.size)return 0;
 await env.DB.batch([...unique.values()].map(i=>env.DB.prepare('INSERT INTO catalog_products(id,payload,search_text,price,first_seen,updated_at) VALUES(?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,search_text=excluded.search_text,price=excluded.price,updated_at=excluded.updated_at WHERE excluded.updated_at>=catalog_products.updated_at').bind(i.id,JSON.stringify(i),fold([i.title,i.titleOriginal,i.description,...i.categories].join(' ')),i.priceCny,at,at)));
 return unique.size;
}
export async function searchCatalog(env,url){
 const q=text(url.searchParams.get('q'),120),page=Number(url.searchParams.get('page')||1);
 if(!Number.isInteger(page)||page<1||page>2000)throw new ApiError(400,'Página inválida.');
 const terms=fold(q).split(/\s+/).filter(Boolean).slice(0,12),where=terms.length?' WHERE '+terms.map(()=>"search_text LIKE ? ESCAPE '\\'").join(' AND '):'';
 const args=terms.map(t=>'%'+t.replace(/[\\%_]/g,'\\$&')+'%');
 const rows=await env.DB.prepare('SELECT payload,updated_at FROM catalog_products'+where+' ORDER BY updated_at DESC,id DESC LIMIT 49 OFFSET ?').bind(...args,(page-1)*48).all();
 return {items:rows.results.slice(0,48).map(r=>({...JSON.parse(r.payload),observedAt:r.updated_at})),page,hasMore:rows.results.length>48,source:'saved-search-results'};
}
