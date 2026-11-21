'use strict';
(function(root){
  function product(value){
    let input=String(value||'').trim();const embedded=input.match(/https?:\/\/[^\s<>"']+/);if(embedded)input=embedded[0];
    let u;try{u=new URL(input);}catch{throw new Error('Cole o link completo de um anúncio.');}
    if(!['https:','http:'].includes(u.protocol)||u.username||u.password)throw new Error('Link inválido.');
    const host=u.hostname.toLowerCase().replace(/^www\./,'');let platform,id;
    if(host==='goofish.com'||host==='h5.m.goofish.com'){platform='goofish';id=u.searchParams.get('id')||u.searchParams.get('itemId');}
    else if(host==='2.taobao.com'){platform='goofish';id=u.searchParams.get('id');}
    else if(['item.taobao.com','m.intl.taobao.com'].includes(host)){platform='taobao';id=u.searchParams.get('id');}
    else if(host==='detail.tmall.com'){platform='tmall';id=u.searchParams.get('id');}
    else if(host==='weidian.com'||host.endsWith('.weidian.com')){platform='weidian';id=u.searchParams.get('itemID');}
    else if(['detail.1688.com','m.1688.com'].includes(host)){platform='1688';id=u.pathname.match(/\/offer\/(\d+)\.html/)?.[1];}
    else if(host==='hubbuy.com'||host==='hubbuy.app'){const m=u.pathname.match(/^\/(?:m\/)?product\/([0127])\/(\d+)\/?$/);if(m){platform={'0':'1688','1':'taobao','2':'weidian','7':'goofish'}[m[1]];id=m[2];}}
    else if(host==='cssbuy.com'||host==='fansbuy.com'){const m=u.pathname.match(/^\/item-(?:(xianyu|1688|micro)-)?(\d+)\.html$/);if(m){platform={xianyu:'goofish','1688':'1688',micro:'weidian'}[m[1]]||'taobao';id=m[2];}}
    else if(host==='usfans.com'){const m=u.pathname.match(/^\/product\/([137])\/(\d+)\/?$/);if(m){platform={'1':'1688','3':'weidian','7':'goofish'}[m[1]];id=m[2];}}
    if(!platform||!/^\d{1,30}$/.test(id||''))throw new Error('Link não reconhecido. Abra o anúncio e copie o endereço completo; links encurtados não são resolvidos automaticamente.');
    const source=platform==='goofish'?'https://www.goofish.com/item?id='+id:platform==='weidian'?'https://weidian.com/item.html?itemID='+id:platform==='1688'?'https://detail.1688.com/offer/'+id+'.html':platform==='tmall'?'https://detail.tmall.com/item.htm?id='+id:'https://item.taobao.com/item.htm?id='+id;
    return {id,platform,url:source};
  }
  function links(value){const p=product(value),channel={'1688':0,taobao:1,tmall:1,weidian:2,goofish:7}[p.platform],suffix=p.platform==='goofish'?'xianyu-':p.platform==='1688'?'1688-':p.platform==='weidian'?'micro-':'';
    const result=[{name:'Hubbuy',url:'https://www.hubbuy.com/product/'+channel+'/'+p.id},{name:'Superbuy',url:'https://www.superbuy.com/en/page/buy/?url='+encodeURIComponent(p.url)},{name:'CSSBuy',url:'https://www.cssbuy.com/item-'+suffix+p.id+'.html'},{name:'Fansbuy',url:'https://fansbuy.com/item-'+suffix+p.id+'.html'}];
    if(['goofish','weidian','1688'].includes(p.platform))result.push({name:'USFans',url:'https://usfans.com/product/'+({goofish:7,weidian:3,'1688':1}[p.platform])+'/'+p.id});
    return result;
  }
  root.GBAgents={product,links};if(typeof module==='object')module.exports=root.GBAgents;
})(globalThis);
