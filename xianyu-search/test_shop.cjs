const {test}=require('node:test'),assert=require('node:assert/strict'),{JSDOM}=require('jsdom'),fs=require('node:fs');
const data=JSON.parse(fs.readFileSync('public/data/products.json','utf8'));
async function setup(path='public/index.html',query=''){
  const errors=[];const dom=new JSDOM(fs.readFileSync(path,'utf8'),{url:'http://127.0.0.1:8081/'+query,runScripts:'outside-only'}),w=dom.window;
  w.matchMedia=()=>({matches:true});w.HTMLElement.prototype.scrollIntoView=()=>{};
  w.fetch=async path=>({ok:true,json:async()=>path==='/data/products.json'?data:path==='/data/rate.json'?{rate:.8,updatedAt:'2026-11-14T00:00:00Z'}:path==='/api/health'?{bridge:{connected:false}}:{collection:{running:false,errors:[]}}});
  w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;};w.addEventListener('error',e=>errors.push(e.message));w.eval(fs.readFileSync('public/privacy.js','utf8'));w.eval(fs.readFileSync('public/shop.js','utf8'));await new Promise(r=>setTimeout(r,30));return {dom,w,d:w.document,errors};
}
test('home displays diverse real products and valid category links',async()=>{const {dom,d,errors}=await setup();assert.equal(d.querySelectorAll('#categories a').length,29);assert.equal(d.querySelectorAll('#grid .product-cell').length,20);assert.equal(d.querySelectorAll('#grid .inline-banner').length,1);assert.deepEqual(errors,[]);assert.ok(d.querySelector('#grid .product-price').textContent.includes('R$'));dom.window.close();});
test('every category has a real static HTML page',()=>{for(const c of data.categories){const file='public/categoria/'+c.id+'/index.html';assert.ok(fs.existsSync(file));assert.ok(fs.readFileSync(file,'utf8').includes('data-category="'+c.id+'"'));}});
test('category page limits cards to category and has matching hero icon',async()=>{const c=data.categories.find(x=>x.count),{dom,d}=await setup('public/categoria/'+c.id+'/index.html');assert.equal(d.querySelector('#results-title').textContent,c.label);assert.ok(d.querySelector('#hero-art').src.endsWith('category-'+c.id+'.png'));for(const a of d.querySelectorAll('#grid .product-photo'))assert.ok(c.productIds.includes(new URL(a.href).searchParams.get('id')));dom.window.close();});
test('saved favorites and filters work without live API',async()=>{const {dom,w,d}=await setup();d.querySelector('.save-button').click();d.querySelector('#favorites').click();assert.equal(d.querySelectorAll('#grid .product-cell').length,1);d.querySelector('#min').value='9999999';d.querySelector('#filters').dispatchEvent(new w.Event('submit',{cancelable:true}));assert.equal(d.querySelectorAll('#grid .product-cell').length,0);d.querySelector('#clear-filters').click();assert.equal(d.querySelectorAll('#grid .product-cell').length,1);dom.window.close();});
test('product page shows gallery and agent action',async()=>{const item=data.items.find(i=>i.image),{dom,d,errors}=await setup('public/produto.html','produto.html?id='+item.id);assert.equal(d.querySelector('#listing-view').hidden,true);assert.ok(d.querySelector('.gallery-main img'));assert.ok(d.querySelector('.product-detail').textContent.includes('Copiar para colar no agente'));assert.deepEqual(errors,[]);dom.window.close();});
test('unavailable product is handled without invented data',async()=>{const {dom,d}=await setup('public/produto.html','produto.html?id=nonexistent');assert.match(d.querySelector('#product-content').textContent,/não encontrado/);dom.window.close();});

test('all 29 category pages have distinct artwork, headlines and no banner eyebrows',()=>{
 const titles=new Set(),images=new Set();
 for(const c of data.categories){const dom=new JSDOM(fs.readFileSync('public/categoria/'+c.id+'/index.html','utf8')),d=dom.window.document;
 titles.add(d.querySelector('#hero-title').textContent);images.add(d.querySelector('#hero-art').getAttribute('src'));
 assert.ok(fs.existsSync('public/assets/category-'+c.id+'.png'));assert.equal(d.querySelectorAll('.hero .eyebrow,.wide-banner .eyebrow,.mini-banner .eyebrow').length,0);assert.equal(d.querySelectorAll('.mini-banners').length,0);assert.match(d.querySelector('.wide-banner h2').textContent,new RegExp(c.label.toLowerCase()));dom.window.close();}
 assert.equal(titles.size,29);assert.equal(images.size,29);
});
test('subcategory rows have their own images, and storefront hides technical exports',async()=>{
 const {dom,d}=await setup();assert.equal(d.querySelectorAll('#categories a img').length,29);assert.equal(new Set([...d.querySelectorAll('#categories a img')].map(i=>i.src)).size,29);
 assert.match(d.querySelector('#hero-title').textContent,/Sem criar conta/);assert.equal(d.querySelectorAll('a[download]').length,0);assert.doesNotMatch(d.body.textContent,/JSON|Alpha Busca|↗|→|←/);assert.ok(d.querySelector('.save-button svg'));dom.window.close();
});
test('favorites persist only after opting in; revocation deletes persistent data',async()=>{
 const {dom,w,d}=await setup();assert.equal(d.querySelector('#privacy-banner').hidden,false);assert.equal(w.JVPrivacy.canRemember(),false);
 d.querySelector('.save-button').click();assert.equal(w.localStorage.getItem('jv.favorites'),null);
 d.querySelector('[data-privacy-allow]').click();assert.equal(d.querySelector('#privacy-banner').hidden,true);assert.equal(JSON.parse(w.localStorage.getItem('jv.favorites')).length,1);
 d.querySelector('[data-privacy-open]').click();assert.equal(d.querySelector('#privacy-dialog').open,true);
 d.querySelector('#privacy-dialog [data-privacy-reject]').click();assert.equal(w.localStorage.getItem('jv.favorites'),null);assert.equal(w.JVPrivacy.canRemember(),false);assert.equal(d.querySelector('#privacy-dialog').open,false);dom.window.close();
});
test('stored consent is restored, expired consent asks again, and blocked storage is safe',()=>{
 const source=fs.readFileSync('public/privacy.js','utf8');
 for(const [age,expected]of [[0,true],[181*86400000,false]]){const dom=new JSDOM(fs.readFileSync('public/index.html','utf8'),{url:'https://example.test',runScripts:'outside-only'}),w=dom.window;
 w.localStorage.setItem('jv.privacy.v1',JSON.stringify({version:1,preferences:true,savedAt:Date.now()-age}));w.eval(source);assert.equal(w.JVPrivacy.canRemember(),expected);dom.window.close();}
 const dom=new JSDOM(fs.readFileSync('public/index.html','utf8'),{url:'https://example.test',runScripts:'outside-only'}),w=dom.window;
 Object.defineProperty(w,'localStorage',{get(){throw Error('blocked');}});assert.doesNotThrow(()=>w.eval(source));assert.equal(w.JVPrivacy.canRemember(),false);dom.window.close();
});
test('legal pages contain real contact and preference controls without claiming official affiliation',()=>{
 for(const name of ['termos','privacidade']){const dom=new JSDOM(fs.readFileSync('public/'+name+'.html','utf8')),d=dom.window.document;assert.ok(d.querySelector('a[href="mailto:jv.busca@gmail.com"]'));assert.ok(d.querySelector('[data-privacy-open]'));assert.ok(d.querySelector('#privacy-dialog'));dom.window.close();}
});
test('GitHub Pages uses the repository subpath and avoids unavailable live API',async()=>{
 const dom=new JSDOM(fs.readFileSync('public/index.html','utf8'),{url:'https://santzz1006.github.io/jv.surch/xianyu-search/public/',runScripts:'outside-only'}),w=dom.window,calls=[];
 w.matchMedia=()=>({matches:true});w.HTMLElement.prototype.scrollIntoView=()=>{};
 w.fetch=async url=>{calls.push(url);return {ok:true,json:async()=>url.endsWith('products.json')?data:{rate:.8,updatedAt:'2026-11-14'}};};
 w.eval(fs.readFileSync('public/privacy.js','utf8'));w.eval(fs.readFileSync('public/shop.js','utf8'));await new Promise(r=>setTimeout(r,30));
 assert.ok(calls.includes('/jv.surch/xianyu-search/public/data/products.json'));
 assert.ok(w.document.querySelector('.product-photo').href.startsWith('https://santzz1006.github.io/jv.surch/xianyu-search/public/produto.html'));
 w.document.querySelector('#query').value='zzzz-sem-produto';w.document.querySelector('#search-form').dispatchEvent(new w.Event('submit',{cancelable:true}));
 assert.match(w.document.querySelector('#status').textContent,/indisponível nesta versão/);assert.equal(calls.some(u=>u.includes('/api/')),false);dom.window.close();
});
