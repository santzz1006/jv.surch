'use strict';
(()=>{
 if(document.getElementById('gb-quick-host'))return;
 const host=document.createElement('div');host.id='gb-quick-host';
 // Isolate our controls from the marketplace CSS; no login/session data is read.
 const root=host.attachShadow({mode:'closed'}),style=document.createElement('style');
 style.textContent=':host{all:initial;position:fixed;top:16px;right:16px;z-index:2147483000;font:14px Arial,sans-serif}.bar{display:flex;justify-content:flex-end;gap:6px}button{display:grid;place-items:center;width:48px;height:48px;border:1px solid #272820;border-radius:18px;background:#ffe615;color:#191b13;cursor:pointer;box-shadow:0 4px 18px #0002}button:focus-visible{outline:3px solid #000;outline-offset:3px}button:hover{background:#ffed66}svg{width:23px;height:23px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.panel{display:none;margin-top:8px;width:min(460px,calc(100vw - 32px));height:min(680px,calc(100dvh - 96px));background:#fafaf5;border:2px solid #25261c;border-radius:24px;overflow:hidden;box-shadow:0 16px 70px #0004}.panel.open{display:block}iframe{width:100%;height:100%;border:0;display:block}@media(max-width:480px){:host{top:10px;right:10px}.panel{width:calc(100vw - 20px);height:calc(100dvh - 82px)}}';
 const bar=document.createElement('div');bar.className='bar';const panel=document.createElement('div');panel.className='panel';let frame,active='';
 function toggle(view){if(active===view&&panel.classList.contains('open')){panel.classList.remove('open');active='';return;}active=view;if(!frame){frame=document.createElement('iframe');frame.title='Pesquisa rápida Goofish Br';panel.append(frame);}frame.src=chrome.runtime.getURL('popup.html')+'?surface=overlay#'+view;panel.classList.add('open');}
 function icon(label,path,view){const b=document.createElement('button');b.type='button';b.title=label;b.setAttribute('aria-label',label);const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('viewBox','0 0 24 24');const p=document.createElementNS(svg.namespaceURI,'path');p.setAttribute('d',path);svg.append(p);b.append(svg);b.onclick=()=>toggle(view);bar.append(b);}
 icon('Pesquisar no Goofish Br','M21 21l-5-5M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0','explore');
 icon('Meus favoritos','M12 21s-9-5-9-12a5 5 0 0 1 9-3 5 5 0 0 1 9 3c0 7-9 12-9 12','saved');
 icon('Agentes e ferramentas','M5 7h14v13H5zM9 7V4h6v3M5 12h14','tools');
 const close=document.createElement('button');close.type='button';close.textContent='×';close.style.fontSize='25px';close.setAttribute('aria-label','Fechar painel');close.onclick=()=>{panel.classList.remove('open');active='';};bar.append(close);
 root.append(style,bar,panel);document.documentElement.append(host);
 function enabled(value){host.style.display=value===false?'none':'block';if(value===false){panel.classList.remove('open');active='';}}
 chrome.storage.local.get('gbQuickSearch').then(s=>enabled(s.gbQuickSearch));
 chrome.storage.onChanged.addListener((changes,area)=>{if(area==='local'&&changes.gbQuickSearch)enabled(changes.gbQuickSearch.newValue);});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){panel.classList.remove('open');active='';}});
})();
