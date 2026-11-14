const state=document.getElementById('state');
async function show(){const x=await chrome.storage.local.get(['enabled','lastStatus']);state.textContent=(x.enabled?'Conexão ativada. ':'Conexão pausada. ')+(x.lastStatus||'');}
document.getElementById('on').onclick=async()=>{await chrome.storage.local.set({enabled:true});chrome.runtime.sendMessage({type:'poll'});show();};
document.getElementById('off').onclick=async()=>{await chrome.storage.local.set({enabled:false});show();};show();
