'use strict';
const GB_GOOFISH_ORIGINS=['https://www.goofish.com/*','https://goofish.com/*'];
const gbInjecting=new Map();
async function ensureGoofishPanel(tabId){
 if(gbInjecting.has(tabId))return gbInjecting.get(tabId);
 const task=(async()=>{
  try{
   const tab=await chrome.tabs.get(tabId);
   if(!/^https:\/\/(www\.)?goofish\.com\//.test(tab.url||'')||tab.discarded)return;
   await chrome.scripting.executeScript({target:{tabId},files:['overlay.js']});
  }catch{/* A tab can close, navigate or lose host permission during installation. */}
 })();gbInjecting.set(tabId,task);
 try{await task;}finally{gbInjecting.delete(tabId);}
}
async function ensureOpenGoofishPanels(){
 const tabs=await chrome.tabs.query({url:GB_GOOFISH_ORIGINS});
 await Promise.all(tabs.filter(t=>t.id).map(t=>ensureGoofishPanel(t.id)));
}
const gbEnsurePanels=()=>ensureOpenGoofishPanels().catch(()=>{});
chrome.runtime.onInstalled.addListener(gbEnsurePanels);
chrome.runtime.onStartup.addListener(gbEnsurePanels);
chrome.tabs.onUpdated.addListener((id,change)=>{if(change.status==='complete')ensureGoofishPanel(id);});
chrome.tabs.onActivated.addListener(({tabId})=>{ensureGoofishPanel(tabId);});
chrome.storage.onChanged.addListener((changes,area)=>{if(area==='local'&&changes.gbQuickSearch?.newValue!==false&&changes.gbQuickSearch)gbEnsurePanels();});
chrome.permissions.onAdded.addListener(gbEnsurePanels);
chrome.runtime.onMessage.addListener((message,sender,reply)=>{
 if(message?.type!=='gb-ensure-overlay'||sender.id!==chrome.runtime.id)return;
 ensureOpenGoofishPanels().then(()=>reply({ok:true}),()=>reply({ok:false}));return true;
});
// Enabling/reloading an unpacked extension starts its worker but does not reload existing tabs.
gbEnsurePanels();
