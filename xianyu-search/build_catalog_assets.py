"""Build small category chunks and the self-contained extension catalogue."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')


def build():
    folder = ROOT / 'public/data'
    source = json.loads((folder / 'products.json').read_text(encoding='utf-8'))
    grouped = defaultdict(list)
    for item in source['items']:
        grouped[(item.get('categories') or ['other'])[0]].append(item)
    index = {k: v for k, v in source.items() if k not in ('items', 'imports')}
    index.update(total=len(source['items']), chunks=[], productChunks={}, items=[i for i in source['items'] if i['id'] in source['featuredIds']])
    for category, items in grouped.items():
        for offset in range(0, len(items), 1200):
            rows = items[offset:offset + 1200]
            file = f'chunks/{category}-{offset // 1200}.json'
            number = len(index['chunks'])
            index['chunks'].append({'file': file, 'count': len(rows), 'categories': sorted({c for i in rows for c in i.get('categories', [])})})
            index['productChunks'].update({i['id']: number for i in rows})
            write(folder / file, rows)
    write(folder / 'catalog-index.json', index)
    rate = json.loads((folder / 'rate.json').read_text(encoding='utf-8'))['rate']
    labels = {c['id']: c['label'] for c in source['categories']}
    items = []
    for i in source['items']:
        items.append({'id': i['id'], 'url': i['url'], 'title': i.get('titlePt') or i['title'],
                      'titleOriginal': i['title'], 'description': i.get('descriptionPt') or i.get('description', ''),
                      'priceCny': i.get('priceCny'), 'images': i.get('images') or [i.get('image', '')],
                      'seller': i.get('seller', {}).get('name', ''), 'sellerCredit': i.get('seller', {}).get('creditLabelPt') or i.get('seller', {}).get('creditLabel', ''),
                      'categories': i.get('categories', []), 'area': i.get('areaPt') or i.get('area', ''),
                      'tags': [*i.get('tagsPt', i.get('tags', [])), *[labels[c] for c in i.get('categories', []) if c in labels]]})
    write(ROOT / 'extension-shop/data/catalog.json', {'updatedAt': source['updatedAt'], 'rate': rate,
        'categories': [{k: c[k] for k in ('id', 'label', 'group', 'count')} for c in source['categories']], 'items': items})
    print(f"Catalogue: {len(items)} products; {len(index['chunks'])} chunks; index { (folder / 'catalog-index.json').stat().st_size } bytes")


if __name__ == '__main__':
    build()
