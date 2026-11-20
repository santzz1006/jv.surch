"""Static metadata readable by social crawlers without JavaScript."""
from html import escape

SITE = 'https://santzz1006.github.io/jv.surch/'
PUBLIC_URL = SITE + 'xianyu-search/public/'
IMAGE = PUBLIC_URL + 'assets/goofish-br-share-v1.jpg'
DESCRIPTION = 'Encontre produtos do Goofish em português, veja preços em reais e compartilhe seus achados com seu agente.'

def social_meta(title='Goofish Br — Seu próximo achado', url=SITE, description=DESCRIPTION):
    fields = {
        'og:title': title, 'og:type': 'website', 'og:url': url,
        'og:site_name': 'Goofish Br', 'og:locale': 'pt_BR',
        'og:description': description, 'og:image': IMAGE,
        'og:image:secure_url': IMAGE, 'og:image:type': 'image/jpeg',
        'og:image:width': '1200', 'og:image:height': '630',
        'og:image:alt': 'Goofish Br: seu próximo achado está aqui. Mascote amarelo com uma lupa.',
    }
    tags = [f'<meta property="{k}" content="{escape(v, quote=True)}">' for k, v in fields.items()]
    for k,v in {'twitter:card':'summary_large_image', 'twitter:title':title, 'twitter:description':description, 'twitter:image':IMAGE, 'twitter:image:alt':fields['og:image:alt']}.items():
        tags.append(f'<meta name="{k}" content="{escape(v, quote=True)}">')
    tags += [f'<meta name="description" content="{escape(description, quote=True)}">', f'<link rel="canonical" href="{escape(url, quote=True)}">']
    return '\n'.join(tags)
