import asyncio
import json
import math
import threading
import time
import subprocess
import sys
import urllib.request
import bridge
import catalog
import secrets
from urllib.parse import urlencode
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from scraper import collect, ScrapeError

ROOT = Path(__file__).parent
CACHE = {}
LOCK = threading.Lock()
LAST_RUN = 0
TTL = 300
LOGIN_PROCESS = None
LOGIN_LOCK = threading.Lock()
LAST_SOURCE = {'state':'not_checked','message':'A fonte ainda não foi consultada nesta execução.'}
TRANSLATIONS = {}

def translate_text(text, lang):
    if not isinstance(text,str) or not text.strip() or len(text.encode('utf-8'))>3000 or lang not in ('zh-CN','ja','en'):
        raise ValueError('Tradução: use até 3.000 bytes de texto e um idioma suportado.')
    key=(text,lang)
    if key in TRANSLATIONS: return TRANSLATIONS[key]
    chunks=[]
    current=''
    for char in text:
        if len((current+char).encode('utf-8'))>450:
            chunks.append(current);current=''
        current+=char
    if current:chunks.append(current)
    output=[]
    for chunk in chunks:
        url='https://api.mymemory.translated.net/get?'+urlencode({'q':chunk,'langpair':lang+'|pt-BR'})
        with urllib.request.urlopen(url,timeout=20) as response: data=json.load(response)
        if str(data.get('responseStatus'))!='200': raise RuntimeError('Serviço de tradução indisponível ou limite atingido.')
        output.append(data['responseData']['translatedText'])
    result=' '.join(output)
    if len(TRANSLATIONS)>200:TRANSLATIONS.clear()
    TRANSLATIONS[key]=result
    return result

def filter_items(items, params):
    def number(key):
        value = params.get(key, [''])[0]
        if value == '': return None
        value = float(value)
        if not math.isfinite(value) or value < 0: raise ValueError('Preço inválido.')
        return value
    low, high = number('min'), number('max')
    if low is not None and high is not None and low > high:
        raise ValueError('O preço mínimo deve ser menor ou igual ao máximo.')
    result = [x for x in items if (low is None or x['priceCny'] is not None and x['priceCny'] >= low) and (high is None or x['priceCny'] is not None and x['priceCny'] <= high)]
    order = params.get('sort', ['relevance'])[0]
    if order not in ('relevance', 'asc', 'desc'): raise ValueError('Ordenação inválida.')
    if order != 'relevance':
        result.sort(key=lambda x:(x['priceCny'] is None, (x['priceCny'] or 0) * (-1 if order == 'desc' else 1)))
    page = int(params.get('page', ['1'])[0])
    if page < 1 or page > 100: raise ValueError('Página inválida.')
    return {'items':result[(page-1)*20:page*20], 'total':len(result), 'collected':len(items), 'page':page, 'hasMore':page*20<len(result)}

class Handler(SimpleHTTPRequestHandler):
    def log_message(self,format,*args):
        if '/api/bridge/job' not in str(args):super().log_message(format,*args)
    def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT/'public'), **kwargs)
    def reply(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        try: self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError): pass
    def local_request(self):
        host = self.headers.get('Host', '')
        allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
        origin = self.headers.get('Origin')
        return host in allowed and self.headers.get('Sec-Fetch-Site') != 'cross-site' and (not origin or origin in {'http://' + h for h in allowed})
    def do_POST(self):
        global LOGIN_PROCESS
        if urlsplit(self.path).path == '/api/bridge/result':
            if not secrets.compare_digest(self.headers.get('X-Alpha-Bridge',''),bridge.KEY):return self.reply(403,{'error':'Conexão não autorizada.'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=1000000:raise ValueError('Payload inválido.')
                bridge.submit(json.loads(self.rfile.read(size)))
                return self.reply(200,{'ok':True})
            except (ValueError,TypeError,AttributeError):return self.reply(400,{'error':'Resposta inválida ou consulta expirada.'})
        if not self.local_request(): return self.reply(403, {'error':'Origem não permitida.'})
        path = urlsplit(self.path).path
        if path.startswith('/api/product/') and path.endswith('/refresh'):
            ident=path.split('/')[3]
            if not ident.isdigit():return self.reply(400,{'error':'ID inválido.'})
            try:
                items=bridge.collect(ident,kind='detail',timeout=100)
                item=next((x for x in items if x['id']==ident),None)
                if not item:raise RuntimeError('A fonte não forneceu detalhes deste produto.')
                return self.reply(200,{'item':catalog.save_detail(item)})
            except RuntimeError as exc:return self.reply(503,{'error':str(exc)})
        if path == '/api/catalog/collect':
            try:
                category_id=parse_qs(urlsplit(self.path).query).get('category',[None])[0]
                return self.reply(202,catalog.start(category_id))
            except ValueError as exc:return self.reply(400,{'error':str(exc)})
            except RuntimeError as exc:return self.reply(409,{'error':str(exc)})
        if path == '/api/recommendations/refresh':
            try:
                items=bridge.collect(kind='recommendations')
                return self.reply(200,{'items':items,**bridge.status()})
            except RuntimeError as exc:return self.reply(503,{'error':str(exc)})
        if path == '/api/translate':
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=20000: raise ValueError('Tamanho inválido.')
                data=json.loads(self.rfile.read(size))
                result=translate_text(data.get('text'),data.get('lang'))
                return self.reply(200,{'text':result,'provider':'MyMemory'})
            except (ValueError,TypeError,AttributeError) as exc:
                return self.reply(400,{'error':str(exc)})
            except Exception:
                return self.reply(502,{'error':'Não foi possível traduzir. O serviço gratuito pode estar indisponível ou ter atingido o limite.'})
        source = parse_qs(urlsplit(self.path).query).get('source',['goofish'])[0]
        if source not in ('goofish','h3x'): return self.reply(400, {'error':'Fonte inválida.'})
        if path not in ('/api/session/open', '/api/session/finish'):
            return self.reply(404, {'error':'Endpoint inexistente.'})
        with LOGIN_LOCK:
            active = LOGIN_PROCESS is not None and LOGIN_PROCESS.poll() is None
            if path.endswith('/open'):
                if active: return self.reply(200, {'state':'open'})
                if not LOCK.acquire(blocking=False): return self.reply(409, {'error':'Aguarde a busca atual terminar.'})
                try:
                    command = [sys.executable, str(ROOT/'scraper.py'), '--login'] + (['--h3x'] if source == 'h3x' else [])
                    LOGIN_PROCESS = subprocess.Popen(command, cwd=str(ROOT), stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, text=True)
                except Exception:
                    return self.reply(500, {'error':'Não foi possível abrir a sessão.'})
                finally: LOCK.release()
                return self.reply(200, {'state':'opening'})
            if active:
                try:
                    if not LOGIN_PROCESS.stdin.closed:
                        LOGIN_PROCESS.stdin.write('\n')
                        LOGIN_PROCESS.stdin.flush()
                        LOGIN_PROCESS.stdin.close()
                    LOGIN_PROCESS.wait(timeout=15)
                except subprocess.TimeoutExpired:
                    return self.reply(409, {'error':'O navegador ainda está carregando. Aguarde e tente concluir novamente.'})
                except (BrokenPipeError, OSError):
                    pass
            CACHE.clear()
            return self.reply(200, {'state':'closed','message':'Janela encerrada. Faça uma busca para verificar o acesso; isso não confirma login.'})
    def do_GET(self):
        global LAST_RUN, LAST_SOURCE
        parsed = urlsplit(self.path)
        if parsed.path == '/api/bridge/job':
            if not secrets.compare_digest(self.headers.get('X-Alpha-Bridge',''),bridge.KEY):return self.reply(403,{'error':'Conexão não autorizada.'})
            return self.reply(200,{'job':bridge.poll()})
        if parsed.path.startswith('/api/') and not self.local_request():
            return self.reply(403, {'error':'Origem não permitida.'})
        if parsed.path == '/api/health':
            return self.reply(200, {'status':'ok','source':LAST_SOURCE,'bridge':bridge.status(),'sessionOpen':LOGIN_PROCESS is not None and LOGIN_PROCESS.poll() is None})
        if parsed.path == '/api/recommendations':
            return self.reply(200,{'items':bridge.FEED or catalog.all_items(),**bridge.status()})
        if parsed.path == '/api/catalog':
            return self.reply(200,catalog.index())
        if parsed.path.startswith('/api/catalog/'):
            category_id=parsed.path.rsplit('/',1)[-1]
            if category_id not in catalog.BY_ID:return self.reply(404,{'error':'Categoria inexistente.'})
            return self.reply(200,catalog.read(category_id))
        if parsed.path.startswith('/api/') and parsed.path != '/api/search':
            return self.reply(404, {'error':'Endpoint inexistente.'})
        if parsed.path != '/api/search': return super().do_GET()
        # Local-only: reject cross-origin browser fetches to prevent unwanted runs.
        if self.headers.get('Sec-Fetch-Site') == 'cross-site':
            return self.reply(403, {'error':'Origem não permitida.'})
        params = parse_qs(parsed.query, keep_blank_values=True)
        q = params.get('q',[''])[0].strip()
        source = params.get('source',['goofish'])[0]
        language = params.get('lang',['pt'])[0]
        if source not in ('goofish','h3x','chrome') or language not in ('pt','en','zh','ja'):
            return self.reply(400, {'error':'Fonte ou idioma inválido.'})
        cache_key = q if source == 'goofish' and language == 'pt' else source + ':' + language + ':' + q
        if not 1 <= len(q) <= 120: return self.reply(400, {'error':'Digite entre 1 e 120 caracteres.'})
        try:
            filter_items([], params)
        except (ValueError, TypeError):
            return self.reply(400, {'error':'Filtros inválidos. Confira os preços e a página.'})
        if not LOCK.acquire(blocking=False): return self.reply(429, {'error':'Uma busca está em andamento. Aguarde terminar.'})
        try:
            now = time.monotonic()
            if LOGIN_PROCESS is not None and LOGIN_PROCESS.poll() is None:
                return self.reply(409, {'error':'Conclua a sessão no navegador e clique em Salvar sessão antes de buscar.'})
            entry = CACHE.get(cache_key)
            cached = bool(entry and now-entry[0]<TTL)
            if not cached:
                if now-LAST_RUN<10: return self.reply(429, {'error':'Aguarde 10 segundos entre novas consultas.'})
                LAST_RUN = now
                if source=='chrome':
                    try:items=catalog.save_live(bridge.collect(q))
                    except RuntimeError as exc:raise ScrapeError(str(exc),'BROWSER_CONNECTION_REQUIRED') from None
                else:items = asyncio.run(collect(q, provider=source, language=language))
                LAST_SOURCE = {'state':'available','message':'Última consulta concluída.','count':len(items)}
                CACHE[cache_key] = (time.monotonic(),items)
                if len(CACHE)>50: CACHE.pop(next(iter(CACHE)))
            else: items = entry[1]
            self.reply(200, {**filter_items(items,params),'cached':cached,'query':q})
        except ScrapeError as exc:
            LAST_SOURCE = {'state':exc.code,'message':str(exc)}
            self.reply(503, {'error':str(exc),'code':exc.code})
        except Exception:
            self.reply(502, {'error':'O coletor não conseguiu carregar o Xianyu. Tente novamente mais tarde.'})
        finally: LOCK.release()

if __name__ == '__main__':
    print('Abra http://127.0.0.1:8081 — Ctrl+C para encerrar.', flush=True)
    ThreadingHTTPServer(('127.0.0.1',8081), Handler).serve_forever()
