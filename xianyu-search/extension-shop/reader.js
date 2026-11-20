'use strict';
// Executed only after the user clicks to read the current tab. No cookies or account storage.
function readGoofishProduct(){
  if(!['www.goofish.com','goofish.com'].includes(location.hostname)||location.pathname!='/item')throw new Error('Abra um anúncio do Goofish para salvar.');
  const visible=e=>Boolean(e&&e.getClientRects().length);
  const main=document.querySelector('main,[class*="ItemDetail--"],[class*="itemDetail--"]')||document.body;
  const first=selectors=>[...main.querySelectorAll(selectors)].find(visible);
  const title=first('h1,[class*="title--"],[class*="Title--"]')?.textContent?.trim()||document.querySelector('meta[property="og:title"]')?.content||document.title;
  const desc=first('[class*="desc--"],[class*="Desc--"],[class*="description--"]');
  const priceEl=first('[class*="price--"],[class*="Price--"]');
  const text=priceEl?.textContent||desc?.textContent||'';
  const m=text.replace(/,/g,'').match(/[¥￥]\s*(\d+(?:\s*\.\s*\d+)?)(\s*万)?/);
  const images=[...main.querySelectorAll('img')].filter(i=>visible(i)&&i.naturalWidth>=250&&i.naturalHeight>=180).map(i=>i.currentSrc||i.src).filter(u=>/^https:\/\//.test(u));
  const seller=first('[class*="sellerName"],[class*="SellerName"],[class*="userName--"]')?.textContent?.trim()||'';
  if(!m&&!desc&&!images.length)throw new Error('O anúncio não está disponível na página. Aguarde carregar ou conclua o login/verificação no Goofish.');
  return {url:location.href,title,description:desc?.textContent?.trim()||'',priceCny:m?Number(m[1].replace(/\s/g,''))*(m[2]?10000:1):null,images:[...new Set(images)].slice(0,12),seller};
}
