'use strict';
(function(root){
 function endpoint(value){const u=new URL(String(value).trim());if(u.protocol!=='https:'||!u.hostname.endsWith('.workers.dev')||u.username||u.password||u.search||u.hash||u.pathname!=='/')throw new Error('Use o endereço https://nome.conta.workers.dev, sem caminho ou parâmetros.');return u.origin;}
 async function config(){const s=await chrome.storage.local.get('goofishBrCloud');const c=s.goofishBrCloud;if(!c?.base||!c?.token)throw new Error('Conecte sua API Cloudflare no painel Nuvem.');return {...c,base:endpoint(c.base)};}
 async function call(path,method='GET',body,provided){const c=provided||await config();if(!/^\/(api\/[a-z0-9/]+|health)$/.test(path))throw new Error('Rota inválida.');const r=await fetch(endpoint(c.base)+path,{method,headers:{Authorization:'Bearer '+c.token,'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body),redirect:'error',cache:'no-store',signal:AbortSignal.timeout(90000)});let data;try{data=await r.json();}catch{throw new Error('A API não retornou uma resposta válida.');}if(!r.ok)throw new Error(data.error||'Falha na API: '+r.status);return data;}
 root.GBC={endpoint,config,call};if(typeof module==='object')module.exports=root.GBC;
})(globalThis);
