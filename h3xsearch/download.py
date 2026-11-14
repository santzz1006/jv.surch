"""Baixa recursos públicos referenciados pelo site, sem autenticação."""
import hashlib
import json
import re
import subprocess
from collections import deque
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote

ROOT = Path(__file__).resolve().parent
BASE = 'https://h3xsearch.com'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.json_blocks = []
        self.in_json = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('href', 'src', 'poster'):
            if attrs.get(key): self.urls.append(attrs[key])
        if tag == 'meta' and attrs.get('property') == 'og:image':
            self.urls.append(attrs.get('content', ''))
        self.in_json = tag == 'script' and attrs.get('type') == 'application/ld+json'
    def handle_endtag(self, tag):
        if tag == 'script': self.in_json = False
    def handle_data(self, data):
        if self.in_json:
            try: self.json_blocks.append(json.loads(data))
            except ValueError: pass

def main():
    queue = deque([BASE + '/', BASE + '/api/config'])
    seen, records = set(), []
    while queue and len(seen) < 250:
        url = queue.popleft().split('#')[0]
        parsed = urlsplit(url)
        if parsed.netloc != 'h3xsearch.com' or parsed.scheme != 'https' or parsed.query or url in seen:
            continue
        seen.add(url)
        relative = unquote(parsed.path).lstrip('/')
        if not relative or relative.endswith('/'): relative += 'index.html'
        target = (ROOT / 'site' / relative).resolve()
        if not target.is_relative_to((ROOT / 'site').resolve()): continue
        target.parent.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(['curl.exe', '-L', '--max-time', '30', '-A', 'Mozilla/5.0', '-sS', '-w', '%{http_code}|%{content_type}', url, '-o', str(target)], capture_output=True, text=True)
        status, _, content_type = result.stdout.partition('|')
        record = {'url': url, 'status': status, 'content_type': content_type}
        if status != '200':
            if target.exists(): target.unlink()
            record['error'] = result.stderr or 'Resposta HTTP não disponível'
            records.append(record)
            print(status, url, flush=True)
            continue
        data = target.read_bytes()
        record.update(path=str(target.relative_to(ROOT)), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        records.append(record)
        print(status, url, len(data), flush=True)
        refs = []
        if 'html' in content_type:
            parser = Links()
            parser.feed(data.decode('utf-8', 'replace'))
            refs += parser.urls
            if parser.json_blocks:
                dest = ROOT / 'json-ld' / (relative.replace('/', '__') + '.json')
                dest.parent.mkdir(exist_ok=True)
                dest.write_text(json.dumps(parser.json_blocks, ensure_ascii=False, indent=2), encoding='utf-8')
        elif 'css' in content_type:
            refs += re.findall(r'url\([\s\"\']*([^\)\"\']+)', data.decode('utf-8', 'replace'))
        elif 'javascript' in content_type:
            text = data.decode('utf-8', 'replace')
            refs += re.findall(r'[\"\'`](/[^\"\'`\s<>]+\.(?:js|css|json|png|svg|woff2))[\"\'`]', text)
        elif 'manifest' in content_type:
            try: refs += [item['src'] for item in json.loads(data).get('icons', [])]
            except ValueError: pass
        queue.extend(urljoin(url, ref) for ref in refs)
    (ROOT / 'manifest-download.json').write_text(json.dumps({'source':BASE,'captured_at':datetime.now(timezone.utc).isoformat(),'files':records},ensure_ascii=False,indent=2),encoding='utf-8')

if __name__ == '__main__': main()
