/** Owner-only diagnostic. No cookies or credentials are exported to the extension. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
const config=JSON.parse(fs.readFileSync(new URL('./wrangler.jsonc',import.meta.url),'utf8'));
const stored=new URL('./.env.browser-login.json',import.meta.url);
const html=new URL('./.env.browser-login.html',import.meta.url);
const toml=fs.readFileSync(path.join(os.homedir(),'.wrangler/config/default.toml'),'utf8');
const token=toml.match(/oauth_token\s*=\s*"([^"]+)"/)?.[1];
if(!token)throw Error('Execute npx wrangler login antes de continuar.');
const base='https://api.cloudflare.com/client/v4/accounts/'+config.account_id+'/browser-rendering/devtools/browser';
async function api(url,method){const r=await fetch(url,{method,headers:{Authorization:'Bearer '+token},signal:AbortSignal.timeout(30000)});const data=await r.json();if(!r.ok||data.success===false)throw Error('Cloudflare HTTP '+r.status+'. Execute npx wrangler whoami e confira a cota de Browser Run.');return data;}
const action=process.argv[2]||'status';
if(action==='start'){
 if(fs.existsSync(stored)){const old=JSON.parse(fs.readFileSync(stored,'utf8'));try{await api(base+'/'+old.sessionId,'DELETE');}catch{}}
 const session=await api(base+'?keep_alive=120000','POST');
 if(!session.sessionId)throw Error('A Cloudflare não retornou a sessão.');
 try{
  const target=await api(base+'/'+session.sessionId+'/json/new?url='+encodeURIComponent('https://www.goofish.com/'),'PUT');
  if(!target.devtoolsFrontendUrl?.startsWith('https://'))throw Error('Painel remoto não retornado.');
  fs.writeFileSync(stored,JSON.stringify({sessionId:session.sessionId,createdAt:new Date().toISOString(),devtoolsFrontendUrl:target.devtoolsFrontendUrl}));
  const link=target.devtoolsFrontendUrl.replaceAll('&','&amp;').replaceAll('"','&quot;');
  fs.writeFileSync(html,'<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Goofish Br - sessão privada</title><h1>Painel remoto privado</h1><p>Este link permite controlar sua sessão. Não compartilhe este arquivo.</p><a href="'+link+'">Abrir navegador remoto</a><p>Se o Goofish recusar o acesso, pare o teste. Este diagnóstico não configura coleta, chat ou persistência de login.</p></html>');
  console.log('Abra o arquivo privado .env.browser-login.html nesta pasta. O link inicial vence em cinco minutos.');
  console.log('Para encerrar: node browser-login.mjs stop');
 }catch(e){await api(base+'/'+session.sessionId,'DELETE').catch(()=>{});throw e;}
}else if(action==='stop'){
 if(fs.existsSync(stored)){const session=JSON.parse(fs.readFileSync(stored,'utf8'));await api(base+'/'+session.sessionId,'DELETE');fs.writeFileSync(stored,JSON.stringify({sessionId:session.sessionId,closedAt:new Date().toISOString()}));if(fs.existsSync(html))fs.writeFileSync(html,'<!doctype html><meta charset="utf-8"><p>Sessão encerrada.</p>');console.log('Sessão encerrada.');}else console.log('Nenhuma sessão de diagnóstico salva.');
}else if(action==='status'){
 const r=await fetch('https://goofish-br-api.neilan-sttephan1.workers.dev/health');const data=await r.json();console.log(JSON.stringify({api:r.status,liveSearch:data.liveSearch,database:data.database}));
}else throw Error('Use start, status ou stop.');
