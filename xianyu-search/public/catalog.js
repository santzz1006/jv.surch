let selectedCategory=null,catalogTimer=null;
async function refreshCatalog(){
  try{
    const response=await fetch('/api/catalog');if(!response.ok)throw new Error('Não foi possível carregar as categorias.');
    const data=await response.json();const container=$('category-list');container.replaceChildren();
    const groups=Object.groupBy(data.categories,c=>c.group);
    for(const [group,rows] of Object.entries(groups)){
      const detail=node('details',null,'category-group');detail.open=rows.some(c=>c.id===selectedCategory);
      const summary=node('summary');const icon=node('img');icon.src='/assets/icon-'+rows[0].icon+'.png';icon.alt='';summary.append(icon,node('span',group));detail.append(summary);
      for(const cat of rows){const button=node('button');button.type='button';button.dataset.category=cat.id;button.setAttribute('aria-pressed',String(selectedCategory===cat.id));button.append(node('span',cat.label),node('small',cat.updatedAt?String(cat.count):'—'));button.onclick=()=>loadCategory(cat.id);detail.append(button);}
      container.append(detail);
    }
    const state=data.collection;const total=data.categories.reduce((n,c)=>n+c.count,0);
    $('catalog-progress').textContent=state.running?`Coletando ${state.current||'…'} · ${state.completed}/${state.total} categorias · ${total} anúncios salvos`:`${data.categories.filter(c=>c.updatedAt).length} de ${data.categories.length} categorias coletadas · ${total} anúncios salvos`;
    if(state.errors.length)$('catalog-progress').textContent+=' · '+state.errors.at(-1).error;
    $('collect-categories').disabled=state.running;
    clearTimeout(catalogTimer);if(state.running)catalogTimer=setTimeout(refreshCatalog,5000);
  }catch(e){$('catalog-progress').textContent=e.message;}
}
async function loadCategory(id){
  if(busy)return;busy=true;
  try{const response=await fetch('/api/catalog/'+encodeURIComponent(id));const data=await response.json();if(!response.ok)throw new Error(data.error);
    selectedCategory=id;imported=data.items;page=1;dataLabel=data.label;$('q').value='';$('feed-title').textContent=data.label;
    $('feed-note').textContent=data.updatedAt?'Coletado em '+new Date(data.updatedAt).toLocaleString('pt-BR')+' · amostra dos resultados do Goofish.':'Esta categoria ainda não foi coletada.';
    showImported();if(!data.updatedAt)$('status').textContent='Clique em Coletar categorias para preencher o catálogo usando seu Chrome conectado.';
    $('download-category').href='/api/catalog/'+id;$('download-category').hidden=false;
    refreshCatalog();
  }catch(e){$('status').className='error';$('status').textContent=e.message;}
  finally{busy=false;}
}
$('collect-categories').onclick=async()=>{
  $('collect-categories').disabled=true;
  try{const r=await fetch('/api/catalog/collect',{method:'POST'});const d=await r.json();if(!r.ok)throw new Error(d.error);await refreshCatalog();}
  catch(e){$('catalog-progress').textContent=e.message;$('collect-categories').disabled=false;}
};
document.querySelectorAll('[data-catalog]').forEach(button=>button.onclick=()=>loadCategory(button.dataset.catalog));
refreshCatalog();
