"""Local queue for the explicitly installed Alpha Chrome extension. No cookies stored."""
import json
import math
import secrets
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).parent
KEY_PATH = ROOT / '.bridge-key'
if not KEY_PATH.exists(): KEY_PATH.write_text(secrets.token_urlsafe(32), encoding='utf-8')
KEY = KEY_PATH.read_text(encoding='utf-8').strip()
LOCK = threading.Lock()
JOB = None
LAST_SEEN = 0
FEED = []
FEED_TIME = None

def normalize_products(rows):
    if not isinstance(rows,list): raise ValueError('Lista inválida.')
    result,seen=[],set()
    for row in rows[:200]:
        if not isinstance(row,dict): continue
        url=urlsplit(str(row.get('url','')))
        ident=parse_qs(url.query).get('id',[''])[0]
        if url.scheme not in ('http','https') or url.hostname not in ('www.goofish.com','goofish.com') or url.path!='/item' or not ident.isdigit() or ident in seen:continue
        title=row.get('title')
        if not isinstance(title,str) or not title.strip():continue
        seen.add(ident)
        price=row.get('priceCny')
        if type(price) not in (int,float) or not math.isfinite(price) or price<0:price=None
        def image(value):
            value=str(value or '')[:3000]
            return value if urlsplit(value).scheme in ('https','http') else ''
        seller=row.get('seller') if isinstance(row.get('seller'),dict) else {}
        gallery=row.get('images',[]) if isinstance(row.get('images'),list) else []
        gallery=list(dict.fromkeys(image(x) for x in [row.get('image'),*gallery] if image(x)))[:12]
        result.append({'id':ident,'title':title[:2000],'description':str(row.get('description',''))[:12000],'url':'https://www.goofish.com/item?id='+ident,'image':image(row.get('image')),'images':gallery,'priceCny':price,'area':str(row.get('area',''))[:100],'seller':{'name':str(seller.get('name',''))[:120],'avatarUrl':image(seller.get('avatarUrl')),'creditLabel':str(seller.get('creditLabel',''))[:120]},'tags':[str(x)[:80] for x in row.get('tags',[])[:5]] if isinstance(row.get('tags',[]),list) else []})
    return result

def status():
    with LOCK:return {'connected':time.monotonic()-LAST_SEEN<50,'busy':JOB is not None,'count':len(FEED),'updatedAt':FEED_TIME}

def poll():
    global LAST_SEEN
    with LOCK:
        LAST_SEEN=time.monotonic()
        if JOB and not JOB['claimed']:
            JOB['claimed']=True
            return {k:JOB[k] for k in ('id','kind','query')}
        return None

def submit(payload):
    global FEED,FEED_TIME
    with LOCK:
        if not JOB or payload.get('id')!=JOB['id']:raise ValueError('Consulta expirada.')
        if payload.get('error'):
            JOB['error']=str(payload['error'])[:500]
        else:
            JOB['items']=normalize_products(payload.get('items'))
            if JOB['kind']=='recommendations':
                FEED=JOB['items'];FEED_TIME=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
                (ROOT/'recommendations.json').write_text(json.dumps({'items':FEED,'updatedAt':FEED_TIME},ensure_ascii=False),encoding='utf-8')
        JOB['event'].set()

def collect(query='',kind='search',timeout=75):
    global JOB
    with LOCK:
        if time.monotonic()-LAST_SEEN>=50:raise RuntimeError('Conecte a extensão Alpha Busca no Chrome que está logado no Goofish.')
        if JOB:raise RuntimeError('Já existe uma consulta no Chrome. Aguarde.')
        job={'id':secrets.token_hex(16),'kind':kind,'query':query,'claimed':False,'event':threading.Event()}
        JOB=job
    try:
        if not job['event'].wait(timeout):raise RuntimeError('O Chrome não respondeu a tempo. Confira a extensão e a sessão do Goofish.')
        if job.get('error'):raise RuntimeError(job['error'])
        return job.get('items',[])
    finally:
        with LOCK:
            if JOB is job:JOB=None

if (ROOT/'recommendations.json').exists():
    try:
        saved=json.loads((ROOT/'recommendations.json').read_text(encoding='utf-8'))
        FEED=normalize_products(saved.get('items',[]));FEED_TIME=saved.get('updatedAt')
    except (ValueError,TypeError):pass
