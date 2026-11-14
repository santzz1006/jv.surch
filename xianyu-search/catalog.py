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
    rows=bridge.normalize_products(items)
    payload={**BY_ID[category_id],'items':rows,'count':len(rows),'updatedAt':stamp(),'source':'goofish','coverage':'partial','method':'rendered_cards','note':'Amostra dos resultados carregados na sessão; não representa todo o catálogo.'}
    ROOT.mkdir(exist_ok=True)
    path=ROOT/(category_id+'.json');tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
    return payload

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
    tmp.write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(path)
    return payload

def save_live(items):
    """Persist new live results so they remain available without the bridge."""
    path=BASE/'live-results.json'
    with LOCK:
        data=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        for item in bridge.normalize_products(items):
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
