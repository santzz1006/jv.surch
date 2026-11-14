importScripts('config.js');
let running=false,pollTimer=null;
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function local(path,body){const r=await fetch('http://127.0.0.1:8081/api/bridge/'+path,{method:body?'POST':'GET',headers:{'X-Alpha-Bridge':ALPHA_BRIDGE_KEY,'Content-Type':'application/json'},body:body?JSON.stringify(body):undefined,signal:AbortSignal.timeout(10000)});if(!r.ok)throw new Error('API local: '+r.status);return r.json();}
// Runs in an isolated world. Reads rendered public cards, never browser cookies/storage.
async function readCards(){
  const collected=new Map();let stable=0,lastCount=0;
  let preloaded=false;
  for(let attempt=0;attempt<22;attempt++){
    const links=[...document.querySelectorAll('a[href*="/item?"]')].filter(a=>a.getClientRects().length);
    if(links.length&&!preloaded){
      preloaded=true;
      // Trigger the site's own lazy images, including cards outside the viewport.
      for(const link of links.slice(0,160)){link.scrollIntoView({block:'center',inline:'center'});await new Promise(r=>setTimeout(r,120));}
      await new Promise(r=>setTimeout(r,1000));
    }
    const items=links.slice(0,200).map(a=>{
      const text=a.innerText||'';const imgs=[...a.querySelectorAll('img')];
      const image=imgs.filter(i=>i.width>70||i.height>70).find(i=>!/-tps-2-2\.|data:image/.test(i.currentSrc||i.src))||imgs.find(i=>i.width>70||i.height>70)||imgs[0];
      const titleNode=a.querySelector('[class*="title"],[class*="Title"]');
      const lines=text.split('\n').map(x=>x.trim()).filter(Boolean);
      const title=titleNode?.innerText||image?.alt||lines.find(x=>x.length>4&&!/^[¥￥]/.test(x))||'';
      const priceNode=a.querySelector('[class*="price"],[class*="Price"]');
      const match=(priceNode?.innerText||text).match(/[¥￥]\s*(\d{1,3}(?:,\d{3})+|\d+)(?:\s*\.\s*(\d+))?\s*(万)?/);
      const sellerNode=a.querySelector('[class*="username" i],[class*="nick" i],[class*="seller-name" i]');
      const avatar=a.querySelector('img[class*="avatar"],img[class*="Avatar"]');
      const credit=lines.find(x=>/信用|信誉/.test(x))||'';
      return {url:a.href,title,image:image?.currentSrc||image?.src||'',priceCny:match?Number(match[1].replaceAll(',','')+'.'+(match[2]||'0'))*(match[3]?10000:1):null,seller:{name:sellerNode?.innerText||avatar?.parentElement?.innerText?.trim()||lines.find(x=>/\*{2,}/.test(x))||'',avatarUrl:avatar?.src||'',creditLabel:credit},tags:lines.filter(x=>x.length<25&&/包邮|验货|全新/.test(x)).slice(0,3)};
    }).filter(x=>x.title);
    for(const item of items)collected.set(item.url,item);
    if(collected.size){
      stable=collected.size===lastCount?stable+1:0;lastCount=collected.size;
      if(collected.size>=160||stable>=4||attempt>=19)return {items:[...collected.values()].slice(0,160)};
      window.scrollBy(0,Math.max(window.innerHeight*1.4,900));
    }
    const text=document.body.innerText;
    if(attempt>4 && /安全验证|验证码|滑块|人机验证/.test(text))return {error:'Goofish pediu verificação. Conclua pessoalmente no Chrome e tente novamente.'};
    if(attempt>10 && /扫码登录|登录后|请先登录/.test(text))return {error:'Esta página exige login. Entre normalmente no Goofish neste Chrome.'};
    if(attempt>10 && /暂无搜索结果|没有找到相关/.test(text))return {items:[]};
    await new Promise(r=>setTimeout(r,1000));
  }
  return collected.size?{items:[...collected.values()]}:{error:'Nenhum cartão reconhecível. A página pode estar bloqueada ou os seletores precisam de ajuste.'};
}
async function readProduct(){
  for(let attempt=0;attempt<20;attempt++){
    const text=document.body.innerText;
    if(/安全验证|滑块验证|人机验证/.test(text))return {error:'Goofish pediu verificação. Conclua no Chrome.'};
    const description=document.querySelector('[class*="desc" i]');
    const images=[...document.querySelectorAll('img')].filter(i=>i.width>=180&&i.height>=120&&!i.closest('a[href*="/item?"]')).map(i=>i.currentSrc||i.src).filter(s=>/^https?:/.test(s)&&!/-tps-2-2\./.test(s));
    const unique=[...new Set(images.map(s=>s.replace(/_\d+x\d+.*$/,'')))].slice(0,12);
    const meta=document.querySelector('meta[property="og:title"]')?.content;
    const title=document.querySelector('[class*="title" i]')?.innerText||meta||description?.innerText?.split('\n')[0];
    const price=text.match(/[¥￥]\s*(\d+)(?:\s*\.\s*(\d+))?\s*(万)?/);
    if(attempt>2&&title&&unique.length){
      const seller=document.querySelector('[class*="seller" i]');
      const avatar=seller?.querySelector('img');
      return {items:[{url:location.href,title,description:description?.innerText||'',image:unique[0],images:unique,priceCny:price?Number(price[1]+'.'+(price[2]||'0'))*(price[3]?10000:1):null,seller:{name:seller?.querySelector('[class*="name" i]')?.innerText||'',avatarUrl:avatar?.src||'',creditLabel:seller?.innerText?.split('\n').find(x=>/信用|信誉/.test(x))||''}}]};
    }
    if(attempt>8&&/扫码登录|请先登录/.test(text))return {error:'O produto exige uma sessão válida no Chrome.'};
    window.scrollBy(0,350);await new Promise(r=>setTimeout(r,500));
  }
  return {error:'Não foi possível carregar a galeria e descrição deste anúncio.'};
}
async function tick(){
  clearTimeout(pollTimer);
  if(running)return;running=true;let tab=null;
  try{
    if(!(await chrome.storage.local.get('enabled')).enabled)return;
    const {job}=await local('job');if(!job)return;
    try{
      if(job.kind==='detail'&&!/^\d+$/.test(job.query))throw new Error('ID inválido.');
      const url=job.kind==='detail'?'https://www.goofish.com/item?id='+job.query:job.kind==='recommendations'?'https://www.goofish.com/':'https://www.goofish.com/search?q='+encodeURIComponent(job.query);
      tab=await chrome.tabs.create({url,active:true});
      let ready=false;
      for(let i=0;i<30;i++){await sleep(1000);const state=await chrome.tabs.get(tab.id);if(state.status==='complete'&&/^https:\/\/(www\.)?goofish\.com\//.test(state.url||'')){ready=true;break;}}
      if(!ready)throw new Error('A aba não carregou uma página Goofish autorizada. Confira se houve redirecionamento ou login.');
      // Zoom is cosmetic: its failure must never prevent a permitted DOM read.
      await chrome.tabs.setZoom(tab.id,.67).catch(()=>{});
      let results;
      try{results=await chrome.scripting.executeScript({target:{tabId:tab.id},func:job.kind==='detail'?readProduct:readCards});}
      catch(e){throw new Error('Leitura dos anúncios (v0.2.0): '+e.message);}
      const result=results[0]?.result||{error:'Não foi possível ler a página.'};
      await local('result',{id:job.id,...result});
      await chrome.storage.local.set({lastStatus:result.error||`${result.items.length} anúncios enviados.`});
      // Preserve the tab on a challenge so the user can complete it themselves.
      if(!result.error){await chrome.tabs.remove(tab.id);tab=null;}
    }catch(e){await local('result',{id:job.id,error:'Falha ao ler a página: '+e.message}).catch(()=>{});}
  }catch(e){await chrome.storage.local.set({lastStatus:'API desconectada. Inicie o servidor local.'});}
  finally{running=false;pollTimer=setTimeout(tick,5000);}
}
chrome.runtime.onInstalled.addListener(async()=>{chrome.alarms.create('alpha-poll',{periodInMinutes:.5});if((await chrome.storage.local.get('enabled')).enabled===undefined)await chrome.storage.local.set({enabled:false});tick();});
chrome.runtime.onStartup.addListener(()=>chrome.alarms.create('alpha-poll',{periodInMinutes:.5}));
chrome.alarms.onAlarm.addListener(a=>{if(a.name==='alpha-poll')tick();});
chrome.runtime.onMessage.addListener((m)=>{if(m.type==='poll')tick();});
