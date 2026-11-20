'use strict';
// Optional, tab-scoped price labels. Does not hide login or verification dialogs.
function addGoofishPrices(rate){
  if(!['goofish.com','www.goofish.com'].includes(location.hostname))throw new Error('Abra o Goofish para mostrar preços em reais.');
  if(!Number.isFinite(rate)||rate<=0)throw new Error('Configure a cotação primeiro.');
  if(window.__gbPrices){window.__gbPrices.disconnect();document.querySelectorAll('[data-gb-price]').forEach(n=>n.remove());}
  let timer;const scan=()=>{
    document.querySelectorAll('[class*="price--"],[class*="Price--"]').forEach(node=>{
      if(node.querySelector('[class*="price--"],[class*="Price--"]'))return;
      const next=node.nextElementSibling;
      const m=node.textContent.replace(/,/g,'').match(/[¥￥]\s*(\d+(?:\s*\.\s*\d+)?)(\s*万)?/);
      if(!m){if(next?.hasAttribute('data-gb-price'))next.remove();return;}
      const amount=Number(m[1].replace(/\s/g,''))*(m[2]?10000:1);
      const text='≈ '+new Intl.NumberFormat('pt-BR',{style:'currency',currency:'BRL'}).format(amount*rate);
      if(next?.hasAttribute('data-gb-price')){if(next.textContent!==text)next.textContent=text;return;}
      const label=document.createElement('span');label.setAttribute('data-gb-price','');label.textContent=text;label.title='Goofish Br: estimativa sem frete, taxas e impostos; cotação manual.';
      label.style.cssText='display:inline-block;margin:4px;padding:3px 8px;border-radius:12px;background:#ffe615;color:#17150f;font:700 12px system-ui';node.after(label);
    });
  };
  scan();const observer=new MutationObserver(()=>{clearTimeout(timer);timer=setTimeout(scan,350);});observer.observe(document.body,{childList:true,subtree:true,characterData:true});window.__gbPrices={disconnect(){observer.disconnect();clearTimeout(timer);}};
  return document.querySelectorAll('[data-gb-price]').length;
}
