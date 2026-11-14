const {test}=require('node:test'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom'),fs=require('node:fs');
const data=JSON.parse(fs.readFileSync('public/data/products.json','utf8'));
async function setup(path='public/index.html',query=''){
  const errors=[];const dom=new JSDOM(fs.readFileSync(path,'utf8'),{url:'http://127.0.0.1:8081/'+query,runScripts:'outside-only'}),w=dom.window;
  w.matchMedia=()=>({matches:true});w.HTMLElement.prototype.scrollIntoView=()=>{};
  w.fetch=async path=>({ok:true,json:async()=>path==='/data/products.json'?data:path==='/data/rate.json'?{rate:.8,updatedAt:'2026-11-14T00:00:00Z'}:path==='/api/health'?{bridge:{connected:false}}:{collection:{running:false,errors:[]}}});
  w.addEventListener('error',e=>errors.push(e.message));w.eval(fs.readFileSync('public/shop.js','utf8'));await new Promise(r=>setTimeout(r,30));return {dom,w,d:w.document,errors};
}
test('home displays diverse real products and valid category links',async()=>{const {dom,d,errors}=await setup();assert.equal(d.querySelectorAll('#categories a').length,29);assert.equal(d.querySelectorAll('#grid .product-cell').length,20);assert.equal(d.querySelectorAll('#grid .inline-banner').length,1);assert.deepEqual(errors,[]);assert.ok(d.querySelector('#grid .product-price').textContent.includes('R$'));dom.window.close();});
test('every category has a real static HTML page',()=>{for(const c of data.categories){const file='public/categoria/'+c.id+'/index.html';assert.ok(fs.existsSync(file));assert.ok(fs.readFileSync(file,'utf8').includes('data-category="'+c.id+'"'));}});

test('JV storefront hides technical exports and uses SVG controls',async()=>{const {dom,d}=await setup();assert.match(d.querySelector('.brand').textContent,/JV/);assert.doesNotMatch(d.body.textContent,/JSON|Alpha Busca|H3X|↗|→|←/i);assert.equal(d.querySelectorAll('a[download]').length,0);assert.ok(d.querySelector('#search-form button svg'));assert.ok(d.querySelector('.save-button svg'));assert.equal(d.querySelectorAll('.promo-photos img').length,4);dom.window.close();});
test('category page limits cards to category and has matching hero icon',async()=>{const c=data.categories.find(x=>x.count),{dom,d}=await setup('public/categoria/'+c.id+'/index.html');assert.equal(d.querySelector('#results-title').textContent,c.label);assert.ok(d.querySelector('#hero-art').src.endsWith('jv-mascot.png'));for(const a of d.querySelectorAll('#grid .product-photo'))assert.ok(c.productIds.includes(new URL(a.href).searchParams.get('id')));dom.window.close();});
test('saved favorites and filters work without live API',async()=>{const {dom,w,d}=await setup();d.querySelector('.save-button').click();d.querySelector('#favorites').click();assert.equal(d.querySelectorAll('#grid .product-cell').length,1);d.querySelector('#min').value='9999999';d.querySelector('#filters').dispatchEvent(new w.Event('submit',{cancelable:true}));assert.equal(d.querySelectorAll('#grid .product-cell').length,0);d.querySelector('#clear-filters').click();assert.equal(d.querySelectorAll('#grid .product-cell').length,1);dom.window.close();});
test('product page shows gallery and agent action',async()=>{const item=data.items.find(i=>i.image),{dom,d,errors}=await setup('public/produto.html','produto.html?id='+item.id);assert.equal(d.querySelector('#listing-view').hidden,true);assert.ok(d.querySelector('.gallery-main img'));assert.ok(d.querySelector('.product-detail').textContent.includes('Copiar para colar no agente'));assert.deepEqual(errors,[]);dom.window.close();});
test('unavailable product is handled without invented data',async()=>{const {dom,d}=await setup('public/produto.html','produto.html?id=nonexistent');assert.match(d.querySelector('#product-content').textContent,/não encontrado/);dom.window.close();});

test('large clothing and sport catalogs paginate through every saved product',async()=>{
  for(const key of ['moda','esportes']){
    const category=data.categories.find(c=>c.id===key),{dom,d}=await setup('public/categoria/'+key+'/index.html');
    const seen=new Set();let pages=0;
    do{
      for(const a of d.querySelectorAll('#grid .product-photo'))seen.add(new URL(a.href).searchParams.get('id'));
      pages++;
      if(d.querySelector('#next').disabled)break;
      d.querySelector('#next').click();
    }while(pages<=Math.ceil(category.count/20));
    assert.equal(seen.size,category.count);
    assert.equal(pages,Math.ceil(category.count/20));
    assert.deepEqual([...seen].sort(),[...category.productIds].sort());
    dom.window.close();
  }
});

