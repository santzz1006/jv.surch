'use strict';
(function(root){
  const fold=s=>String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
  function search(items,{q='',category='',min='',max='',sort='relevance',condition='',color=''}={}){
    const terms=fold(q).split(/\s+/).filter(Boolean);const lower=min===''?null:Number(min),upper=max===''?null:Number(max);
    if(lower!==null&&(!Number.isFinite(lower)||lower<0)||upper!==null&&(!Number.isFinite(upper)||upper<0)||lower!==null&&upper!==null&&lower>upper)throw new Error('Confira os limites de preço em yuan.');
    const colors={preto:['preto','preta','black','黑'],branco:['branco','branca','white','白'],azul:['azul','blue','蓝'],vermelho:['vermelho','vermelha','red','红']};
    const rows=items.filter(i=>{const body=fold([i.title,i.titleOriginal,i.description,...(i.tags||[])].join(' '));if(!terms.every(t=>body.includes(t)))return false;if(category&&!i.categories?.includes(category))return false;if((lower!==null||upper!==null)&&i.priceCny===null)return false;if(lower!==null&&i.priceCny<lower||upper!==null&&i.priceCny>upper)return false;if(color&&!colors[color]?.some(c=>/[\u3400-\u9fff]/.test(c)?body.includes(c):new RegExp('(^|[^a-z])'+c+'($|[^a-z])').test(body)))return false;if(condition==='new'&&(!/全新|lacrado|lacrada|sem uso|brand new/.test(body)||/不全新|非全新|nao lacrad|nao.*sem uso|not new/.test(body)))return false;return true;});
    if(sort==='price-asc')rows.sort((a,b)=>(a.priceCny??Infinity)-(b.priceCny??Infinity));if(sort==='price-desc')rows.sort((a,b)=>(b.priceCny??-Infinity)-(a.priceCny??-Infinity));return rows;
  }
  root.GBCatalog={search,fold};if(typeof module==='object')module.exports=root.GBCatalog;
})(globalThis);
