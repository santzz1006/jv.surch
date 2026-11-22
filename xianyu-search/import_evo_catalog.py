"""Normalize the public catalogue pages without replacing richer existing ads."""
import copy
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent
RULES = {
 'celulares': r'手机|iphone|苹果\s*\d|小米\s*\d|华为|三星.*(?:s\d|fold)|荣耀\s*\d|红米',
 'computadores': r'笔记本|电脑|显卡|主板|处理器|内存条|固态硬盘|macbook|thinkpad|\brtx\b|\bgtx\b|\bryzen\b|chromebook',
 'eletronicos': r'相机|镜头|耳机|音箱|平板|手表|智能眼镜|无人机|ipad|airpods|apple\s*watch|数码|投影|充电器|充电宝',
 'moda': r'衣|裤|裙|衫|外套|羽绒|夹克|卫衣|短袖|长袖|背心|风衣|鞋|靴|凉鞋|拖鞋|帽子|围巾|袜子|衬衫',
 'bolsas': r'背包|双肩包|手提包|挎包|拉杆箱|行李箱|钱包|腰包|公文包|旅行包|单肩包|箱包',
 'esportes': r'运动鞋|跑步鞋|篮球鞋|足球鞋|网球|篮球|足球|羽毛球|乒乓球|健身|哑铃|滑雪|钓鱼|鱼竿|跑步机|高尔夫|登山|帐篷|骑行|\bjordan\b|\bair\s*max\b',
 'servicos': r'维修服务|代修|代练|上门服务|设计服务|摄影服务',
 'cupons': r'优惠券|代金券|礼品卡|会员卡|电影票',
 'colecionaveis': r'手办|盲盒|模型|潮玩|labubu|pop\s*mart|泡泡玛特|乐高|lego|公仔',
 'bebe': r'婴儿|宝宝|婴幼|奶瓶|婴儿车|儿童推车|纸尿裤|母婴',
 'beleza': r'口红|粉底|眼影|香水|腮红|化妆|唇膏|睫毛',
 'cuidados': r'洗发|沐浴|电动牙刷|剃须|护肤|面霜|精华液|防晒|洁面',
 'moveis': r'沙发|书桌|餐桌|衣柜|床垫|床架|茶几|书柜|椅子|家具',
 'eletrodomesticos': r'冰箱|洗衣机|空调|电饭煲|微波炉|烤箱|吸尘器|扫地机器人|吹风机|咖啡机',
 'decoracao': r'窗帘|壁纸|墙纸|吊灯|台灯|地毯|花瓶|装饰画',
 'antiguidades': r'古董|古玩|文玩|字画|古钱|瓷器|书法|油画',
 'joias': r'项链|手链|戒指|耳环|耳钉|珠宝|翡翠|钻石|黄金|银饰',
 'presentes': r'礼盒|礼物|礼品',
 'pets': r'宠物|猫粮|狗粮|猫砂|猫窝|狗窝|鱼缸',
 'plantas': r'盆栽|多肉|花苗|绿植|盆景|花卉',
 'livros': r'图书|教材|小说|绘本|教科书|漫画书|书籍|词典',
 'games': r'游戏机|游戏卡|游戏盘|游戏手柄|playstation|\bps[1-5]\b|\bxbox\b|nintendo|任天堂|switch|steam\s*deck|游戏掌机',
 'musica': r'吉他|钢琴|小提琴|黑胶|唱片|乐器|鼓机|合成器|萨克斯',
 'carros': r'汽车|轿车|轮胎|车载|行车记录仪|方向盘',
 'eletricos': r'电动车|电动自行车|电动滑板车|电摩',
 'imoveis': r'出租房|租房|公寓出租|房屋出租|商铺出租',
 'ferramentas': r'电钻|扳手|螺丝刀|电锯|工具箱|万用表|焊机',
 'equipamentos': r'工业设备|机床|印刷机|激光切割|缝纫机|3d打印机',
 'campo': r'农机|农用|割草机|拖拉机|种子|灌溉',
}
COMPILED = {k: re.compile(v, re.I) for k, v in RULES.items()}


def safe_image(value):
    value = str(value or '')
    if value.startswith('//'):
        value = 'https:' + value
    u = urlparse(value)
    return value if u.scheme == 'https' and u.hostname and (u.hostname == 'alicdn.com' or u.hostname.endswith('.alicdn.com')) and not u.username else ''


def normalize(row, collected_at):
    ident = str(row.get('item_id', ''))
    title = str(row.get('titulo') or '').strip()
    if not ident.isdigit() or not title:
        return None
    value = row.get('preco')
    try:
        price = float(value) if value is not None and not isinstance(value, bool) else None
        if price is not None and (not math.isfinite(price) or price < 0):
            price = None
    except (ValueError, TypeError):
        price = None
    # Only classify from the opening title, not unrelated seller terms further down.
    categories = [key for key, pattern in COMPILED.items() if pattern.search(title[:140])]
    image = safe_image(row.get('imagem'))
    credit = str(row.get('loja_level') or '')
    credit_pt = {'卖家信用极好': 'Excelente reputação como vendedor', '卖家信用优秀': 'Ótima reputação como vendedor', '卖家信用良好': 'Boa reputação como vendedor'}.get(credit, '')
    item = {'id': ident, 'title': title, 'description': '',
            'url': 'https://www.goofish.com/item?id=' + ident,
            'image': image, 'images': [image] if image else [], 'priceCny': price,
            'seller': {'name': str(row.get('loja_nome') or ''), 'avatarUrl': safe_image(row.get('loja_avatar')), 'creditLabel': credit},
            'tags': [], 'tagsPt': [], 'categories': categories,
            'catalogSource': 'evo-public', 'collectedAt': collected_at}
    if credit_pt:
        item['seller']['creditLabelPt'] = credit_pt
    if row.get('frete') is True:
        item['tagsPt'].append('Frete grátis informado na origem')
    # This API exposes one photograph, no verified sales totals or full gallery.
    return item


def merge(payload, imported, updated_at):
    result = copy.deepcopy(payload)
    items = {str(i['id']): i for i in result['items']}
    added = duplicates = 0
    valid_categories = {c['id'] for c in result['categories']}
    for new in imported:
        new = copy.deepcopy(new)
        new['categories'] = [c for c in new.get('categories', []) if c in valid_categories]
        old = items.get(new['id'])
        if old:
            duplicates += 1
            # Keep prior translated text, price snapshot, galleries and category assignments.
            old['images'] = list(dict.fromkeys([*old.get('images', []), *new.get('images', [])]))
            if not old.get('image'):
                old['image'] = new['image']
            old['seller'] = {**new.get('seller', {}), **{k: v for k, v in old.get('seller', {}).items() if v}}
            if not old.get('categories'):
                old['categories'] = new['categories']
        else:
            items[new['id']] = new
            added += 1
    result['items'] = list(items.values())
    category_ids = {c: [] for c in valid_categories}
    for item in result['items']:
        for cat in dict.fromkeys(item.get('categories', [])):
            if cat in category_ids:
                category_ids[cat].append(item['id'])
    for cat in result['categories']:
        cat.update(productIds=category_ids[cat['id']], count=len(category_ids[cat['id']]), updatedAt=updated_at)
    result['updatedAt'] = updated_at
    result['coverage'] = 'partial'
    return result, {'added': added, 'duplicates': duplicates, 'total': len(items)}


def run(allow_partial=False):
    cache = ROOT / 'references/evo-original/catalog-pages'
    progress = json.loads((cache / 'progress.json').read_text(encoding='utf-8'))
    if not progress.get('complete') and not allow_partial:
        raise RuntimeError('The page scan is not finished; existing catalogue was not changed.')
    rows = {}; offset = 0; pages = 0
    # Follow the contiguous chain, ignoring abandoned/cache files off that chain.
    while True:
        path = cache / f'{offset:09d}.json'
        if not path.exists() and allow_partial:
            break
        page = json.loads(path.read_text(encoding='utf-8'))
        pages += 1
        if not page:
            break
        for raw in page:
            item = normalize(raw, progress['updatedAt'])
            if item:
                rows.setdefault(item['id'], item)
        offset += len(page)
    target = ROOT / 'public/data/products.json'
    original = json.loads(target.read_text(encoding='utf-8'))
    backup = cache / 'goofish-br-before-import.json'
    if not backup.exists():
        backup.write_bytes(target.read_bytes())
    merged, stats = merge(original, list(rows.values()), progress['updatedAt'])
    report = {**progress, **stats, 'publicRowsImported': len(rows), 'pagesRead': pages,
              'source': 'EVO anonymous buscar_catalogo_xianyu RPC',
              'scope': 'Public Xianyu catalogue at collection time, not the entire Goofish marketplace',
              'classification': 'Title keyword rules; unknown items remain searchable without a category',
              'unclassified': sum(not i.get('categories') for i in rows.values()),
              'translation': 'Existing translations preserved; new original titles are not represented as translated',
              'photos': 'One image per imported record, as returned by the source',
              'categoryCounts': dict(Counter(c for i in rows.values() for c in i['categories']))}
    merged['imports'] = {**merged.get('imports', {}), 'evoPublic': report}
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(merged, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    temp.replace(target)
    (ROOT / 'EVO-IMPORTACAO.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(stats), flush=True)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--allow-partial', action='store_true')
    run(parser.parse_args().allow_partial)
