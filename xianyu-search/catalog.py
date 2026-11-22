"""Persistent category snapshots. Only genuine collector output is stored."""
import json
import threading
import time
import itertools
import os
from pathlib import Path
import bridge

BASE = Path(__file__).parent
ROOT = BASE / 'catalog'
# Search labels observed in the Goofish homepage category sidebar.
GROUPS = [
 ('Tecnologia','tech',[('celulares','Celulares','手机'),('eletronicos','Eletrônicos','数码'),('computadores','Computadores','电脑')]),
 ('Moda e esporte','fashion',[('moda','Roupas','服饰'),('bolsas','Bolsas e malas','箱包'),('esportes','Esportes','运动')]),
 ('Serviços e colecionáveis','recommend',[('servicos','Serviços','技能'),('cupons','Cupons','卡券'),('colecionaveis','Colecionáveis','潮玩')]),
 ('Cuidados','fashion',[('bebe','Bebê e maternidade','母婴'),('beleza','Beleza','美妆'),('cuidados','Cuidados pessoais','个护')]),
 ('Casa','home',[('moveis','Móveis','家具'),('eletrodomesticos','Eletrodomésticos','家电'),('decoracao','Decoração','家装')]),
 ('Arte e presentes','recommend',[('antiguidades','Arte e antiguidades','文玩'),('joias','Joias','珠宝'),('presentes','Presentes','礼品')]),
 ('Dia a dia','home',[('pets','Pets','宠物'),('plantas','Plantas','花卉')]),
 ('Lazer','gaming',[('livros','Livros','图书'),('games','Games','游戏'),('musica','Música e vídeo','音像')]),
 ('Mobilidade e imóveis','tech',[('carros','Carros','汽车'),('eletricos','Veículos elétricos','电动车'),('imoveis','Aluguéis','租房')]),
 ('Ferramentas e campo','home',[('ferramentas','Ferramentas','五金'),('equipamentos','Equipamentos','设备'),('campo','Campo e agro','农牧')]),
]
ICONS={'Tecnologia':'tech','Moda e esporte':'fashion','Serviços e colecionáveis':'services','Cuidados':'care','Casa':'home','Arte e presentes':'gifts','Dia a dia':'daily','Lazer':'gaming','Mobilidade e imóveis':'mobility','Ferramentas e campo':'tools'}
CATEGORIES = [{'id':i,'label':label,'query':q,'group':group,'icon':ICONS[group]} for group,icon,rows in GROUPS for i,label,q in rows]
BY_ID = {c['id']:c for c in CATEGORIES}
LOCK = threading.Lock()
STATE = {'running':False,'current':None,'completed':0,'total':0,'errors':[], 'startedAt':None}

def stamp(): return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())

def read(category_id):
    category=BY_ID[category_id]
    path=ROOT/(category_id+'.json')
    if path.exists():
        try: return json.loads(path.read_text(encoding='utf-8'))
        except (ValueError,OSError): pass
    return {**category,'items':[],'updatedAt':None,'source':'goofish','coverage':'not_collected'}

def save(category_id,items):
    unique={}
    for offset in range(0,len(items),200):
        for item in bridge.normalize_products(items[offset:offset+200]):unique[item['id']]=item
    rows=list(unique.values())
    payload={**BY_ID[category_id],'items':rows,'count':len(rows),'updatedAt':stamp(),'source':'goofish','coverage':'partial','method':'rendered_cards','note':'Amostra dos resultados carregados na sessão; não representa todo o catálogo.'}
    ROOT.mkdir(exist_ok=True)
    path=ROOT/(category_id+'.json');tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
    return payload


def save_page(category_id,items,page,query=None):
    old=read(category_id)
    result=save(category_id,[*old['items'],*items])
    result['scanPage']=old.get('scanPage',0) if query else page
    result['scanPages']={**old.get('scanPages',{})}
    if query:result['scanPages'][query]=page
    path=ROOT/(category_id+'.json');tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
    export()
    return result


PRIORITY=['moda','esportes','eletronicos']
SEARCH_VARIETY={
    'moda':['男装','女装','运动鞋','外套','牛仔裤'],
    'esportes':['跑步鞋','运动服','健身器材','篮球','羽毛球'],
}


def start_deep(target=1000):
    if not bridge.status()['connected']:raise RuntimeError('Ative a conexão no Chrome com sua sessão do Goofish.')
    if bridge.status().get('version')!='0.3.1':raise RuntimeError('Recarregue a extensão para a versão 0.3.1 antes da coleta paginada.')
    with LOCK:
        if STATE['running']:raise RuntimeError('Uma coleta já está em andamento.')
        STATE.update(running=True,current=None,completed=0,total=len(PRIORITY),errors=[],startedAt=stamp(),target=target)
    threading.Thread(target=_deep,args=(target,),daemon=True).start()
    return index()


def _deep(target):
    try:
        for category_id in PRIORITY:
            category=BY_ID[category_id];old=read(category_id)
            if category_id in SEARCH_VARIETY:
                _collect_variety(category_id,target)
                with LOCK:STATE['completed']+=1
                continue
            for page in range(old.get('scanPage',0)+1,51):
                if len(read(category_id)['items'])>=target:break
                with LOCK:STATE['current']=f"{category['label']} · página {page} · {len(read(category_id)['items'])}/{target}"
                items=bridge.collect(category['query'],kind='category',page=page,timeout=130)
                if not items:break
                before=len(read(category_id)['items'])
                result=save_page(category_id,items,page)
                if result['count']==before and page>1:
                    raise RuntimeError('A página não trouxe novos IDs. Coleta interrompida para evitar duplicação.')
                time.sleep(4)
            with LOCK:STATE['completed']+=1
    except Exception as exc:
        with LOCK:STATE['errors'].append({'category':category_id,'error':str(exc)})
    finally:
        with LOCK:STATE.update(running=False,current=None)


def _collect_variety(category_id,target):
    """Collect diverse search terms with independent resumable checkpoints."""
    queries=SEARCH_VARIETY[category_id]
    # First give each term seven pages, then expand if deduplication leaves a gap.
    for last_page in (7,15,30,50):
        for query in queries:
            old=read(category_id)
            for page in range(old.get('scanPages',{}).get(query,0)+1,last_page+1):
                before=len(read(category_id)['items'])
                if before>=target:return
                with LOCK:STATE['current']=f"{BY_ID[category_id]['label']} · {query} · página {page} · {before}/{target}"
                items=bridge.collect(query,kind='category',page=page,timeout=130)
                if not items:break
                result=save_page(category_id,items,page,query=query)
                if result['count']==before and page>1:break
                time.sleep(4)

def index():
    categories=[]
    for category in CATEGORIES:
        data=read(category['id'])
        categories.append({**category,'count':len(data['items']),'updatedAt':data['updatedAt']})
    with LOCK: state={**STATE,'errors':list(STATE['errors'])}
    return {'categories':categories,'collection':state}

def all_items():
    rows={}
    for category in CATEGORIES:
        for item in read(category['id'])['items']:rows.setdefault(item['id'],item)
    return list(rows.values())

def start(category_id=None, resume=True):
    if category_id is not None and category_id not in BY_ID:raise ValueError('Categoria inválida.')
    if not bridge.status()['connected']:raise RuntimeError('Conecte a extensão Alpha Busca no Chrome antes de coletar.')
    categories=[BY_ID[category_id]] if category_id else [c for c in CATEGORIES if not resume or not read(c['id'])['updatedAt']]
    with LOCK:
        if STATE['running']:raise RuntimeError('Uma coleta de categorias já está em andamento.')
        STATE.update(running=True,current=None,completed=0,total=len(categories),errors=[],startedAt=stamp())
    threading.Thread(target=_run,args=(categories,),daemon=True).start()
    return index()

def _run(categories):
    try:
        for category in categories:
            with LOCK:STATE['current']=category['label']
            try:
                items=bridge.collect(category['query'],timeout=100)
                save(category['id'],items)
                export()
            except Exception as exc:
                with LOCK:STATE['errors'].append({'category':category['id'],'error':str(exc)})
                # Stop on access challenges; do not repeatedly request blocked pages.
                break
            with LOCK:STATE['completed']+=1
            time.sleep(3)
    finally:
        with LOCK:STATE.update(running=False,current=None)

def export():
    """Build public product-only JSON. Never export browser state or credentials."""
    target=BASE/'public'/'data';target.mkdir(parents=True,exist_ok=True)
    products={};categories=[]
    detail_path=BASE/'details.json'
    details=json.loads(detail_path.read_text(encoding='utf-8')) if detail_path.exists() else {}
    translation_path=BASE/'translations.json'
    translations=json.loads(translation_path.read_text(encoding='utf-8')) if translation_path.exists() else {}
    live_path=BASE/'live-results.json'
    live=json.loads(live_path.read_text(encoding='utf-8')) if live_path.exists() else {}
    sources=[(c,read(c['id'])) for c in CATEGORIES]
    sources.append((None,{'items':list(live.values())}))
    for category,data in sources:
        ids=[]
        for raw in data['items']:
            item=dict(raw);ident=item['id'];ids.append(ident)
            if ident in details:
                detail=details[ident]
                item.update({k:v for k,v in detail.items() if v not in (None,'',[],{}) and k!='seller'})
                item['seller']={**item.get('seller',{}),**{k:v for k,v in detail.get('seller',{}).items() if v}}
            item['images']=list(dict.fromkeys([item.get('image',''),*item.get('images',[])]))
            item['images']=[x for x in item['images'] if x and '-tps-2-2.' not in x]
            if '-tps-2-2.' in item.get('image',''):item['image']=item['images'][0] if item['images'] else ''
            for field in ('title','description','area'):
                if item.get(field) in translations:item[field+'Pt']=translations[item[field]]
            seller=item.get('seller',{})
            if seller.get('creditLabel') in translations:seller['creditLabelPt']=translations[seller['creditLabel']]
            item['tagsPt']=[translations.get(t,t) for t in item.get('tags',[])]
            if item.get('titlePt'):item['translationProvider']='Argos Translate (local)'
            if ident not in products:products[ident]={**item,'categories':[]}
            if category:products[ident]['categories'].append(category['id'])
        if category:categories.append({**category,'productIds':ids,'count':len(ids),'updatedAt':data['updatedAt']})
    # Round-robin categories so the home page is diverse, not just cellphones.
    candidates=[[i['id'] for i in read(c['id'])['items'] if i.get('image') and '-tps-2-2.' not in i['image']] for c in CATEGORIES]
    featured=list(dict.fromkeys(x for row in itertools.zip_longest(*candidates) for x in row if x))[:60]
    payload={'schemaVersion':2,'updatedAt':stamp(),'source':'Goofish','coverage':'partial','categories':categories,'items':list(products.values()),'featuredIds':featured}
    path=target/'products.json';tmp=path.with_suffix(f'.{os.getpid()}.{threading.get_ident()}.tmp')
    if path.exists():
        previous=json.loads(path.read_text(encoding='utf-8'))
        if previous.get('imports'):
            from import_evo_catalog import merge
            payload,_=merge(payload,[i for i in previous['items'] if i.get('catalogSource')=='evo-public'],payload['updatedAt'])
            payload['imports']=previous['imports']
    tmp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8');tmp.replace(path)
    return payload

def save_live(items):
    """Persist new live results so they remain available without the bridge."""
    items=bridge.normalize_products(items)
    path=BASE/'live-results.json'
    with LOCK:
        data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        for item in items:
            data[item['id']]={**item,'collectedAt':stamp()}
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)
    payload=export();ids={i['id'] for i in items}
    return [i for i in payload['items'] if i['id'] in ids]


def save_detail(item):
    path=BASE/'details.json'
    with LOCK:
        data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        data[item['id']]={**item,'detailsUpdatedAt':stamp()}
        temp=path.with_suffix('.tmp');temp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(path)
    save_live([item])
    payload=export()
    return next((x for x in payload['items'] if x['id']==item['id']),item)

