/* First-party preference storage only. No analytics or advertising scripts. */
(()=>{
  const KEY='jv.privacy.v1',MAX_AGE=180*24*60*60*1000;
  let consent=null,lastFocus=null;
  try{const saved=JSON.parse(localStorage.getItem(KEY)||'null');if(saved?.version===1&&typeof saved.preferences==='boolean'&&Number.isFinite(saved.savedAt)&&Date.now()-saved.savedAt<MAX_AGE)consent=saved;}catch{}
  const purge=()=>{try{localStorage.removeItem('alpha.favorites');localStorage.removeItem('jv.favorites');}catch{}};
  if(!consent?.preferences)purge();
  const banner=document.getElementById('privacy-banner'),dialog=document.getElementById('privacy-dialog'),toggle=document.getElementById('privacy-preferences');
  function close(){if(dialog?.open)dialog.close();else if(dialog)dialog.hidden=true;lastFocus?.focus();}
  function save(preferences){
    consent={version:1,preferences:!!preferences,savedAt:Date.now()};
    try{localStorage.setItem(KEY,JSON.stringify(consent));}catch{}
    if(!preferences)purge();
    if(banner)banner.hidden=true;close();
    window.dispatchEvent(new CustomEvent('jv:privacy',{detail:{preferences:!!preferences}}));
  }
  function open(){lastFocus=document.activeElement;if(toggle)toggle.checked=!!consent?.preferences;if(dialog?.showModal)dialog.showModal();else if(dialog)dialog.hidden=false;}
  window.JVPrivacy={canRemember:()=>!!consent?.preferences,open};
  if(banner)banner.hidden=!!consent;
  document.querySelectorAll('[data-privacy-open]').forEach(b=>b.addEventListener('click',open));
  document.querySelectorAll('[data-privacy-reject]').forEach(b=>b.addEventListener('click',()=>save(false)));
  document.querySelectorAll('[data-privacy-allow]').forEach(b=>b.addEventListener('click',()=>save(true)));
  document.getElementById('privacy-save')?.addEventListener('click',()=>save(toggle.checked));
  document.getElementById('privacy-close')?.addEventListener('click',close);
  dialog?.addEventListener('cancel',()=>lastFocus?.focus());
  window.addEventListener('storage',event=>{if(event.key===KEY){try{const s=JSON.parse(event.newValue);consent=s?.version===1&&Date.now()-s.savedAt<MAX_AGE?s:null;}catch{consent=null;}if(!consent?.preferences)purge();window.dispatchEvent(new CustomEvent('jv:privacy',{detail:{preferences:!!consent?.preferences}}));if(banner)banner.hidden=!!consent;}});
})();
