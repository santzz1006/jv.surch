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
