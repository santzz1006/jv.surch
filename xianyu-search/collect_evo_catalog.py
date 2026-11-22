"""Read the same anonymous catalogue RPC used by EVO's distributed client.

No account tokens, private tables or live/paid search. Checkpoints stay local.
"""
import base64
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
CACHE = ROOT / 'references/evo-original/catalog-pages'
PAGE_SIZE = 500


def public_config():
    code = (ROOT / 'references/evo-original/files/config.js').read_text(encoding='utf-8')
    section = code.split('const getFornecedoresConfig', 1)[1]
    url = re.search(r"url:\s*'([^']+)'", section)[1]
    key = re.search(r"key:\s*'([^']+)'", section)[1]
    claims = json.loads(base64.urlsafe_b64decode(key.split('.')[1] + '==='))
    if claims.get('role') != 'anon':
        raise ValueError('Only the distributed anonymous client configuration is supported.')
    if url != 'https://oxteieiotshecgmkqnjp.supabase.co':
        raise ValueError('Unexpected catalogue origin.')
    return url, key


def collect():
    url, key = public_config()
    CACHE.mkdir(parents=True, exist_ok=True)
    offset = 0
    unique = set()
    first_total = None
    pages = 0
    started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    while True:
        path = CACHE / f'{offset:09d}.json'
        if path.exists():
            rows = json.loads(path.read_text(encoding='utf-8'))
        else:
            body = {'p_termo': '', 'p_limite': PAGE_SIZE, 'p_inicio': offset}
            req = urllib.request.Request(url + '/rest/v1/rpc/buscar_catalogo_xianyu',
                data=json.dumps(body).encode(), method='POST', headers={
                    'apikey': key, 'Authorization': 'Bearer ' + key,
                    'Content-Type': 'application/json'})
            for attempt in range(3):
                try:
                    with urllib.request.urlopen(req, timeout=35) as response:
                        rows = json.load(response)
                    break
                except urllib.error.HTTPError as exc:
                    # No retries on access controls or throttling, and no alternate routes.
                    if exc.code in (401, 403, 429) or exc.code < 500 or attempt == 2:
                        raise RuntimeError(f'Catalogue stopped: HTTP {exc.code} at offset {offset}') from None
                    print(f'Temporary HTTP {exc.code}; pausing before retry at {offset}', flush=True)
                    time.sleep(10 * (attempt + 1))
                except (TimeoutError, urllib.error.URLError):
                    if attempt == 2:
                        raise RuntimeError(f'Network unavailable at offset {offset}') from None
                    time.sleep(10 * (attempt + 1))
            if not isinstance(rows, list) or any(not isinstance(x, dict) or not str(x.get('item_id', '')).isdigit() for x in rows):
                raise ValueError('Unexpected catalogue response; refusing to import it.')
            temp = path.with_suffix('.tmp')
            temp.write_text(json.dumps(rows, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
            temp.replace(path)
            time.sleep(0.8)
        total = int(rows[0].get('total', 0)) if rows else 0
        if first_total is None:
            first_total = total
        before = len(unique)
        unique.update(str(x['item_id']) for x in rows)
        progress = {'startedAt': started, 'updatedAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                    'offset': offset, 'nextOffset': offset + len(rows), 'unique': len(unique),
                    'firstReportedTotal': first_total, 'lastReportedTotal': total,
                    'complete': len(rows) == 0, 'pageSize': PAGE_SIZE}
        (CACHE / 'progress.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
        pages += 1
        if pages % 10 == 0 or not rows:
            print(json.dumps(progress), flush=True)
        if not rows:
            break
        if len(unique) == before:
            raise RuntimeError('Repeated page; stopping to avoid an infinite collection.')
        offset += len(rows)
    return progress


if __name__ == '__main__':
    collect()
