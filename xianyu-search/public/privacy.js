(()=>{
  const KEY='jv.privacy.v1',AGE=180*86400000;
  let consent=null,lastFocus=null;
  function read(raw){try{const s=JSON.parse(raw);return s?.version===1&&typeof s.preferences==='boolean'&&Number.isFinite(s.savedAt)&&Date.now()-s.savedAt<AGE?s:null;}catch{return null;}}
  try{consent=read(localStorage.getItem(KEY));}catch{}
  const purge=()=>{try{localStorage.removeItem('alpha.favorites');localStorage.removeItem('jv.favorites');}catch{}};
  if(!consent?.preferences)purge();
  const banner=document.getElementById('privacy-banner'),dialog=document.getElementById('privacy-dialog'),toggle=document.getElementById('privacy-preferences');
  function close(){if(dialog.open)dialog.close();else dialog.hidden=true;lastFocus?.focus();}
  function save(preferences){consent={version:1,preferences:!!preferences,savedAt:Date.now()};try{localStorage.setItem(KEY,JSON.stringify(consent));}catch{}if(!preferences)purge();banner.hidden=true;close();window.dispatchEvent(new CustomEvent('jv:privacy',{detail:{preferences:!!preferences}}));}
  function open(){lastFocus=document.activeElement;toggle.checked=!!consent?.preferences;if(dialog.showModal)dialog.showModal();else dialog.hidden=false;}
  window.JVPrivacy={canRemember:()=>!!consent?.preferences,open};banner.hidden=!!consent;
  document.querySelectorAll('[data-privacy-open]').forEach(b=>b.addEventListener('click',open));
  document.querySelectorAll('[data-privacy-reject]').forEach(b=>b.addEventListener('click',()=>save(false)));
  document.querySelectorAll('[data-privacy-allow]').forEach(b=>b.addEventListener('click',()=>save(true)));
  document.getElementById('privacy-save').onclick=()=>save(toggle.checked);
  document.getElementById('privacy-close').onclick=close;
  dialog.addEventListener('cancel',()=>lastFocus?.focus());
  window.addEventListener('storage',e=>{if(e.key===KEY){consent=read(e.newValue);if(!consent?.preferences)purge();banner.hidden=!!consent;window.dispatchEvent(new CustomEvent('jv:privacy',{detail:{preferences:!!consent?.preferences}}));}});
})();
