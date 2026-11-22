const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),{JSDOM}=require('jsdom');
const event=()=>({listeners:[],addListener(f){this.listeners.push(f);},removeListener(f){this.listeners=this.listeners.filter(x=>x!==f);}});
test('worker attaches to existing Goofish tabs and coalesces duplicate injection requests',async()=>{
 const installed=event(),startup=event(),updated=event(),activated=event(),changed=event(),granted=event(),message=event(),calls=[];
 const c={console,chrome:{runtime:{id:'test',onInstalled:installed,onStartup:startup,onMessage:message},tabs:{query:async()=>[{id:1},{id:2}],get:async id=>({id,url:id===1?'https://www.goofish.com/':'chrome://extensions/'}),onUpdated:updated,onActivated:activated},storage:{onChanged:changed},permissions:{onAdded:granted},scripting:{executeScript:async args=>{calls.push(args);await new Promise(r=>setTimeout(r,5));}}}};
 vm.createContext(c);vm.runInContext(fs.readFileSync('extension-shop/overlay-lifecycle.js','utf8'),c);
 await c.ensureOpenGoofishPanels();assert.equal(calls.length,1);assert.equal(calls[0].target.tabId,1);
 await Promise.all([c.ensureGoofishPanel(1),c.ensureGoofishPanel(1)]);assert.equal(calls.length,2);
 assert.equal(installed.listeners.length,1);assert.equal(startup.listeners.length,1);assert.equal(activated.listeners.length,1);assert.equal(updated.listeners.length,1);assert.equal(granted.listeners.length,1);
});
test('overlay replaces stale host, avoids duplicate listeners and respects disabled preference',async()=>{
 const dom=new JSDOM('<div id="gb-quick-host">Stale extension</div>',{url:'https://www.goofish.com/',runScripts:'outside-only'}),w=dom.window,changed=event();
 w.chrome={runtime:{getURL:p=>'chrome-extension://test/'+p},storage:{local:{get:async()=>({gbQuickSearch:false})},onChanged:changed}};
 const source=fs.readFileSync('extension-shop/overlay.js','utf8');w.eval(source);await new Promise(r=>setTimeout(r,0));
 assert.equal(w.document.querySelectorAll('#gb-quick-host').length,1);assert.equal(w.document.getElementById('gb-quick-host').textContent,'');assert.equal(w.document.getElementById('gb-quick-host').style.display,'none');
 w.eval(source);await new Promise(r=>setTimeout(r,0));assert.equal(changed.listeners.length,1);
 changed.listeners[0]({gbQuickSearch:{newValue:true}},'local');assert.equal(w.document.getElementById('gb-quick-host').style.display,'block');
 w.document.getElementById('gb-quick-host').remove();w.eval(source);await new Promise(r=>setTimeout(r,0));assert.equal(changed.listeners.length,1);assert.equal(w.document.querySelectorAll('#gb-quick-host').length,1);w.close();
});
