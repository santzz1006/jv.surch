const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const code=fs.readFileSync('extension/background.js','utf8');
function context(text){
  const image={width:200,height:200,currentSrc:'https://img.alicdn.com/item.jpg',alt:'Produto'};
  const card={innerText:text,href:'https://www.goofish.com/item?id=123',querySelectorAll:()=>[image],querySelector:()=>null,getClientRects:()=>[1],scrollIntoView:()=>{}};
  const addListener=()=>{};
  const c={importScripts:()=>{},chrome:{runtime:{onInstalled:{addListener},onStartup:{addListener},onMessage:{addListener}},alarms:{onAlarm:{addListener}}},document:{querySelectorAll:()=>[card],body:{innerText:''}},window:{innerHeight:800,scrollBy:()=>{}},setTimeout:fn=>fn()};
  vm.createContext(c);vm.runInContext(code,c);return c;
}
for(const [text,expected] of [['Produto\n¥\n19\n.99\n97人想要',19.99],['Produto\n¥\n1\n.19\n万\n¥15550',11900],['Produto\n¥ 1,500.50',1500.5],['Produto\n¥ 0',0],['Preço sob consulta',null]]){
  test('DOM price '+JSON.stringify(text),async()=>{const c=context(text);const result=await c.readCards();assert.equal(result.items[0].priceCny,expected);assert.equal(result.items.length,1);});
}
test('verification does not produce fabricated products',async()=>{const c=context('');c.document.querySelectorAll=()=>[];c.document.body.innerText='安全验证';const result=await c.readCards();assert.match(result.error,/verificação/);assert.equal(result.items,undefined);});

test('pagination reads new page after its product IDs change',async()=>{const c=context('Produto\n¥ 50');const card=c.document.querySelectorAll()[0];const page={children:[],textContent:'2',scrollIntoView(){},click(){card.href='https://www.goofish.com/item?id=456';}};c.document.querySelector=()=>({querySelectorAll:()=>[page]});const result=await c.readCards(2);assert.equal(result.items[0].url,'https://www.goofish.com/item?id=456');});

test('pagination does not pretend a repeated page is new',async()=>{const c=context('Produto\n¥ 50');c.document.querySelector=()=>({querySelectorAll:()=>[{children:[],textContent:'2',scrollIntoView(){},click(){}}]});const result=await c.readCards(2);assert.match(result.error,/não carregou/);assert.equal(result.items,undefined);});

test('pagination can jump beyond the ten visible page numbers',async()=>{
  const c=context('Produto\n¥ 50'),card=c.document.querySelectorAll()[0];
  const input={type:'text',disabled:false,scrollIntoView(){},dispatchEvent(){}};
  const confirm={children:[],textContent:'确定',click(){assert.equal(input.value,'11');card.href='https://www.goofish.com/item?id=789';}};
  function Input(){}Object.defineProperty(Input.prototype,'value',{set(value){this.value=value;}});
  c.HTMLInputElement=Input;c.Event=function(){};
  c.document.querySelector=()=>({querySelectorAll:()=>[],parentElement:{querySelectorAll:selector=>selector==='input'?[input]:[confirm]}});
  const result=await c.readCards(11,10);assert.equal(result.items[0].url,'https://www.goofish.com/item?id=789');
});

test('next arrow never labels page two as a resumed distant page',async()=>{
  const c=context('Produto\n¥ 50');let clicked=false;
  c.document.querySelector=()=>({querySelectorAll:()=>[],querySelector:()=>({disabled:false,getAttribute(){return null;},click(){clicked=true;}})});
  const result=await c.readCards(11,1);assert.match(result.error,/não está disponível/);assert.equal(clicked,false);
});
