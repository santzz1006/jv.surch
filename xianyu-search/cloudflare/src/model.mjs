export class ApiError extends Error {constructor(status,message){super(message);this.status=status;}}
export const text=(v,n=300)=>String(v??'').trim().slice(0,n);
export function https(value){try{const u=new URL(value);return u.protocol==='https:'&&!u.username&&!u.password?u.href:'';}catch{return '';}}
export function item(raw){const id=text(raw?.id||new URL(https(raw?.url)||'https://invalid').searchParams.get('id'),30);if(!/^\d{1,30}$/.test(id))throw new ApiError(400,'ID de anúncio inválido.');return {id,url:'https://www.goofish.com/item?id='+id,title:text(raw.title||'Anúncio do Goofish'),description:text(raw.description,4000),priceCny:typeof raw.priceCny==='number'&&Number.isFinite(raw.priceCny)&&raw.priceCny>=0?raw.priceCny:null,images:(Array.isArray(raw.images)?raw.images:[]).map(https).filter(Boolean).slice(0,12),folder:text(raw.folder||'Meus achados',60),seller:text(raw.seller,100),savedAt:text(raw.savedAt,40),checkedAt:text(raw.checkedAt,40),previousPrice:typeof raw.previousPrice==='number'&&Number.isFinite(raw.previousPrice)?raw.previousPrice:null};}
export function collection(raw){if(!raw||typeof raw!=='object'||!Array.isArray(raw.items)||raw.items.length>1000||['suppliers','parcels','offers'].some(k=>raw[k]!==undefined&&!Array.isArray(raw[k])))throw new ApiError(400,'Coleção inválida ou maior que 1.000 anúncios.');return {items:[...new Map(raw.items.map(x=>{const i=item(x);return [i.id,i];})).values()],suppliers:(raw.suppliers||[]).slice(0,500).map(s=>({name:text(s.name,100),url:https(s.url)})).filter(s=>s.url),parcels:(raw.parcels||[]).slice(0,100).map(p=>({id:text(p.id,100),label:text(p.label,100),code:text(p.code,60),url:https(p.url),note:text(p.note,500)})),offers:(raw.offers||[]).slice(0,100).map(o=>({id:text(o.id,100),name:text(o.name,100),url:https(o.url),price:Number.isFinite(o.price)&&o.price>=0?o.price:0,shipping:Number.isFinite(o.shipping)&&o.shipping>=0?o.shipping:0})),rate:Number.isFinite(raw.rate)&&raw.rate>0&&raw.rate<=100?raw.rate:null};}
export function changes(old,next){const found=[];if(next.priceCny!==null&&old.price!==null&&next.priceCny!==old.price)found.push({kind:next.priceCny<old.price?'price_down':'price_up',message:`Preço mudou de ¥ ${old.price} para ¥ ${next.priceCny}.`});if(old.target!==null&&next.priceCny!==null&&next.priceCny<=old.target&&(old.price===null||old.price>old.target))found.push({kind:'target',message:`Atingiu seu preço desejado: ¥ ${next.priceCny}.`});if(next.availability==='sold'&&old.availability!=='sold')found.push({kind:'sold',message:'A fonte informou que o anúncio foi vendido.'});return found;}
export function productFromHtml(html,id){
 const scripts=[...html.matchAll(/<script\b[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
 for(const match of scripts){let parsed;try{parsed=JSON.parse(match[1]);}catch{continue;}const nodes=Array.isArray(parsed)?parsed:parsed['@graph']||[parsed];
  for(const p of nodes){if(p['@type']!=='Product')continue;const url=https(p.url||p['@id']);if(!url||new URL(url).searchParams.get('id')!==id)continue;const offer=Array.isArray(p.offers)?p.offers[0]:p.offers;if(!offer||offer.priceCurrency!=='CNY')continue;const price=Number(offer.price);if(offer.price==null||!Number.isFinite(price)||price<0)continue;
   // OutOfStock does not prove that the item was sold.
   return {...item({id,title:p.name,description:p.description,priceCny:price,images:Array.isArray(p.image)?p.image:[p.image]}),availability:/SoldOut$/.test(offer.availability||'')?'sold':/InStock$/.test(offer.availability||'')?'available':'unknown'};
  }
 }
 throw new ApiError(503,'A origem não expôs dados verificáveis deste anúncio. Login, verificação ou um coletor próprio podem ser necessários.');
}
export async function readProduct(env,id,fetcher=fetch){
 if(!/^\d{1,30}$/.test(id))throw new ApiError(400,'ID inválido.');
 if(env.PRODUCT_SOURCE_URL){const base=https(env.PRODUCT_SOURCE_URL);if(!base)throw new ApiError(503,'Endereço do coletor inválido.');const r=await fetcher(base.replace(/\/$/,'')+'/products/'+id,{headers:env.PRODUCT_SOURCE_TOKEN?{Authorization:'Bearer '+env.PRODUCT_SOURCE_TOKEN}:{},redirect:'error',signal:AbortSignal.timeout(15000)});if(!r.ok)throw new ApiError(503,'O coletor não conseguiu consultar o anúncio.');const raw=await r.json();if(String(raw.id)!==id||!raw.observedAt||Date.now()-Date.parse(raw.observedAt)>86400000||!Number.isFinite(Date.parse(raw.observedAt))||Date.parse(raw.observedAt)>Date.now()+60000)throw new ApiError(503,'O coletor retornou dados antigos ou de outro anúncio.');return {...item(raw),availability:['sold','available'].includes(raw.availability)?raw.availability:'unknown'};}
 const r=await fetcher('https://www.goofish.com/item?id='+id,{redirect:'error',signal:AbortSignal.timeout(15000)});if(!r.ok)throw new ApiError(503,'Anúncio indisponível para consulta pública.');const html=await r.text();if(html.length>2000000)throw new ApiError(503,'Página da origem muito grande.');return productFromHtml(html,id);
}

export async function liveSearch(env,input,fetcher=fetch){
 const q=text(input.q,120),page=Number(input.page||1);
 const min=input.min===''||input.min==null?null:Number(input.min),max=input.max===''||input.max==null?null:Number(input.max);
 if(!q||!Number.isInteger(page)||page<1||page>20||[min,max].some(n=>n!==null&&(!Number.isFinite(n)||n<0))||min!==null&&max!==null&&min>max)throw new ApiError(400,'Confira o termo, a página e os limites de preço.');
 const base=https(env.SEARCH_SOURCE_URL);if(!base)throw new ApiError(503,'A busca ao vivo ainda não tem uma fonte própria configurada. A pesquisa no catálogo funciona sem login.');
 const url=new URL(base.replace(/\/$/,'')+'/search');url.searchParams.set('q',q);url.searchParams.set('page',String(page));url.searchParams.set('limit','48');if(min!==null)url.searchParams.set('min',String(min));if(max!==null)url.searchParams.set('max',String(max));
 const r=await fetcher(url.href,{headers:env.SEARCH_SOURCE_TOKEN?{Authorization:'Bearer '+env.SEARCH_SOURCE_TOKEN}:{},redirect:'error',signal:AbortSignal.timeout(25000)});
 if(!r.ok)throw new ApiError(503,'A fonte de busca não está disponível. Use o catálogo enquanto isso.');const data=await r.json();
 if(!Array.isArray(data.items))throw new ApiError(503,'A fonte não retornou uma lista de anúncios válida.');
 const items=data.items.slice(0,48).map(raw=>({...item(raw),titleOriginal:text(raw.titleOriginal||raw.title,500),description:text(raw.description,4000),categories:Array.isArray(raw.categories)?raw.categories.slice(0,6).map(c=>text(c,40)):[],sellerCredit:text(raw.sellerCredit,120),area:text(raw.area,100)}));
 return {items,page,hasMore:Boolean(data.hasMore),note:'Anúncios da fonte configurada pelo proprietário; confira a disponibilidade na origem.'};
}
