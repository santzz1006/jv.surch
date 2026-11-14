"""Coletor local: lê somente anúncios visíveis em uma sessão normal do navegador."""
import asyncio
import re
from pathlib import Path
from urllib.parse import quote, urlsplit, parse_qs

PROFILE = Path(__file__).parent / '.browser-profile'

class ScrapeError(Exception):
    def __init__(self, message, code='SOURCE_UNAVAILABLE'):
        super().__init__(message)
        self.code = code

def price_number(text):
    match = re.search(r'[¥￥]\s*(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)', text)
    return float(match.group(1).replace(',', '')) if match else None

def normalize(rows):
    items, seen = [], set()
    for row in rows:
        url = row.get('url', '')
        parsed = urlsplit(url)
        if parsed.scheme not in ('https', 'http') or parsed.hostname not in ('www.goofish.com', 'goofish.com') or parsed.path != '/item':
            continue
        item_id = parse_qs(parsed.query).get('id', [''])[0]
        if not item_id.isdigit(): continue
        url = 'https://www.goofish.com/item?id=' + item_id
        if url in seen or not row.get('title', '').strip():
            continue
        seen.add(url)
        items.append({'id': item_id, 'title': row['title'].strip(), 'url': url,
                      'image': row.get('image', ''), 'priceCny': price_number(row.get('text', ''))})
    return items

async def collect(query, login=False, provider='goofish', language='pt'):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise ScrapeError('Instale as dependências seguindo o GUIA.md.') from None
    async with async_playwright() as p:
        try:
            profile = PROFILE if provider == 'goofish' else PROFILE.parent / '.reference-profile'
            context = await p.chromium.launch_persistent_context(str(profile), headless=False, viewport={'width':1280,'height':900})
        except Exception:
            raise ScrapeError('Não foi possível abrir o navegador. Instale o Chromium e feche outra execução deste coletor.') from None
        try:
            page = context.pages[0] if context.pages else await context.new_page()
            if provider == 'h3x':
                # Observe only the normal page's successful response. No token replay.
                responses = []
                page.on('response', lambda r: responses.append(r) if urlsplit(r.url).hostname == 'h3xsearch.com' and urlsplit(r.url).path == '/api/search' else None)
                await page.goto('https://h3xsearch.com/?q=' + quote(query), wait_until='domcontentloaded', timeout=45000)
                if login:
                    print('Conclua a verificação pessoalmente no navegador e depois salve a sessão.', flush=True)
                    await asyncio.to_thread(input)
                    return []
                for _ in range(25):
                    if responses:
                        response = responses.pop(0)
                        if response.status == 200:
                            data = await response.json()
                            if not isinstance(data.get('items'), list):
                                raise ScrapeError('A fonte não retornou uma lista de produtos.', 'INVALID_RESPONSE')
                            result = []
                            for item in data['items']:
                                if not isinstance(item, dict) or not isinstance(item.get('title'), str): continue
                                result.append({'id':str(item.get('id','')), 'title':item.get('titleTranslated') or item['title'], 'image':item.get('image',''), 'priceCny':item.get('priceCny'), 'priceBrl':item.get('priceBrl'), 'area':item.get('area',''), 'url':item.get('buyUrl') or 'https://www.goofish.com/item?id='+quote(str(item.get('id','')))})
                            return result
                    await asyncio.sleep(1)
                raise ScrapeError('O site de referência não liberou resultados nesta sessão. Abra a sessão da fonte para concluir pessoalmente a verificação. Você também pode importar o JSON de produtos.', 'VERIFICATION_REQUIRED')
            try:
                await page.goto('https://www.goofish.com/search?q=' + quote(query), wait_until='domcontentloaded', timeout=45000)
            except Exception:
                raise ScrapeError('Não foi possível carregar a página do Xianyu em 45 segundos. Confira sua conexão e tente abrir o site normalmente.') from None
            if login:
                print('Use o navegador para entrar normalmente, se necessário. Depois pressione Enter aqui.', flush=True)
                await asyncio.to_thread(input)
                return []
            try:
                await page.locator('a[href*="/item?"]').first.wait_for(timeout=20000)
            except Exception:
                body = await page.locator('body').inner_text()
                if re.search(r'验证码|安全验证|滑块|人机|captcha|verify you are human', body, re.I):
                    raise ScrapeError('O Xianyu pediu verificação humana. Abra a sessão e conclua pessoalmente a verificação.', 'VERIFICATION_REQUIRED')
                if re.search(r'登录|扫码|login|sign in', body, re.I):
                    raise ScrapeError('O Xianyu exige login nesta sessão. Abra a sessão para entrar com uma conta sua; sem isso, a fonte não libera os anúncios.', 'LOGIN_REQUIRED')
                if re.search(r'暂无|没有找到|无搜索结果', body):
                    return []
                raise ScrapeError('Não foram encontrados cartões reconhecíveis. A página pode ter mudado; ajuste os seletores conforme o guia.')
            # Leitura do DOM renderizado. Não chama endpoints privados nem resolve desafios.
            rows = await page.locator('a[href*="/item?"]').evaluate_all('''links => links.slice(0,60).map(a => {
                const img = a.querySelector('img');
                const text = a.innerText || '';
                const lines = text.split('\\n').map(s => s.trim()).filter(Boolean);
                return {url:a.href, text, image:img?.currentSrc || img?.src || '',
                    title:img?.alt || a.getAttribute('title') || lines.find(s => !/^[¥￥]/.test(s)) || ''};
            })''')
            items = normalize(rows)
            if not items:
                raise ScrapeError('A página abriu, mas os anúncios não puderam ser extraídos. Ajuste os seletores do coletor.')
            return items
        finally:
            await context.close()

if __name__ == '__main__':
    import sys
    try:
        provider = 'h3x' if '--h3x' in sys.argv else 'goofish'
        items = asyncio.run(collect('rtx 3060', login='--login' in sys.argv, provider=provider))
        if '--login' not in sys.argv:
            print('Anúncios coletados:', len(items))
    except ScrapeError as exc:
        print('Coleta indisponível:', exc)
        sys.exit(1)
