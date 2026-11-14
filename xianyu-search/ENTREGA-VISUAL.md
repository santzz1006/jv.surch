# Goofish Br — recursos visuais e verificação

Atualizado em 14/11/2026.

## Implementado

- Nome público Goofish Br, mantendo o aviso de projeto independente.
- 29 ilustrações PNG distintas para subcategorias, exibidas no menu, nos botões e no banner da categoria.
- 29 banners principais com título, descrição, cor e arte próprios; chamadas secundárias próprias de cada categoria.
- Três novas poses: lupa, boas-vindas e coração.
- Página inicial com a chamada “Busque no Goofish. Sem criar conta.”
- Textos pequenos acima dos títulos removidos dos banners.
- Botões de categorias com quebra em linhas e sem encolher/cortar os rótulos.
- Termos de uso, privacidade e opções para permitir ou recusar preferências. Contato: jv.busca@gmail.com.
- Persistência de favoritos somente após permitir preferências; revogação apaga a lista persistida.

## Arquivos finais

Artes: public/assets/category-*.png (29 arquivos).
Poses: public/assets/mascot-search.png, mascot-wave.png, mascot-heart.png.
Mascote original: public/assets/jv-mascot.png.
Direção de cada categoria: category_design.py.
Páginas e textos: build_site.py e legal_pages.py.
Estilos: public/jv.css. Preferências: public/privacy.js.

## Geração das imagens

Ferramenta utilizada: image_gen integrada, sem API/CLI externo. As imagens originais foram preservadas em C:/Users/neila/.codex/generated_images/01a1d55b-76f5-77a3-984a-6d45c292b938. As cópias do site foram reduzidas para até 560 px, preservando transparência. O mapa dos primeiros arquivos recuperados está em review/asset-source-map.json.

Prompt das 26 primeiras categorias, com o assunto substituído a cada imagem:

> Use case: product-mockup. Asset: a single category illustration for JV Busca marketplace, readable as small sidebar icon and large banner art. Subject: [assunto]. Square composition, isolated full objects with ample margins, centered cohesive arrangement. Refined soft 3D product render, rounded friendly forms, matte materials, yellow #ffe615 and charcoal #191915 with cream accents, subtle ambient shadow only under objects. No background, true transparency. No pedestal, no scattered particles, no stars, no text except any explicitly requested symbol, no brand logos, no watermark. Simple recognizable silhouette, consistent professional shop illustration system.

Assuntos: celular e fones sem fio; câmera e headphones; notebook e mouse; moletom e jeans; bolsa e mala; tênis e basquete; caixa de ferramentas; cupons com porcentagem; robô colecionável; carrinho e mamadeira; perfume e batom; frasco e aparador; poltrona e mesa; batedeira e chaleira; luminária e vaso; bule e moeda; colar e caixa de anel; presente; tigela e coleira; planta e pá; livros; controle e console portátil; toca-discos; carro; scooter; casa e chave.

Prompt das três últimas categorias:

> Single category illustration for JV Busca, [assunto]. Professional soft 3D product render, friendly rounded shapes, matte yellow #ffe615 and charcoal black, cream accents. Isolated centered square composition, ample margins, complete silhouette. True transparent background, subtle contact shadow, no text, logos, characters, particles, pedestal or scenery. Readable as a sidebar icon and banner art.

Assuntos: a yellow cordless drill beside black adjustable wrench; a compact yellow industrial bench drill press on a black platform; a yellow miniature farm tractor with black wheels and small green sprout.

Prompt da pose com lupa:

> Use case: identity-preserve. Asset: JV Busca website mascot pose, transparent PNG. Reference image is the exact mascot identity, preserve rounded yellow fish body, orange dorsal fins and little orange hands, huge white eyes black pupils, happy red mouth, soft toy-like 3D style. Create one new full-body pose: inquisitive smiling mascot holding a black-rim magnifying glass near one open eye, looking toward viewer, slight 3/4 turn. Both eyes open. No text, no logo, no background, no floor, no extra characters. Entire silhouette comfortably inside square frame. Truly transparent background.

Prompt das poses de boas-vindas e coração:

> Use case: identity-preserve. Asset: one transparent PNG mascot for JV Busca website. Reference image defines exact identity: plump yellow fish body, orange dorsal fins, small orange hands, huge white eyes with black pupils, joyful red mouth, soft toy-like 3D style. Create one new full-body [pose]. Preserve body and face identity. Full silhouette, centered square with generous margins. No text, no logos, no backdrop, no ground. Transparent background.

Poses: happy welcoming pose, holding one orange hand up in a friendly wave and other hand open pointing to the side, eyes open; happy excited pose hugging a black heart-shaped cushion, one eye winking, joyful little orange hands wrapped around the heart.

## Verificação

32 testes Python e 11 testes de interface/privacidade passaram. Os testes de interface usam DOM simulado. Foram conferidas 33 páginas por HTTP, links locais, recursos e unicidade das 29 imagens. A revisão visual automática no navegador foi interrompida pela ferramenta, que não conseguiu confirmar o endereço da janela; não houve validação visual final em celular real.

O desenho das opções de privacidade foi orientado pelo guia da ANPD: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf

## Estado do catálogo e publicação

A versão origin/main foi incorporada em 14/11/2026. O catálogo recuperado tem 4.720 anúncios únicos: 1.012 em Roupas, 1.017 em Esportes, 1.020 em Computadores, 972 em Eletrônicos e 330 em Celulares. Os lotes anteriores estão novamente na pasta e entram na publicação.

O cabeçalho usa uma grade: mascote e nome ocupam a primeira linha, com o selo Br centralizado no nome. O subtítulo ocupa sua própria linha. A faixa de categorias quebra em linhas sem encolher os textos.

O GitHub Pages publica o catálogo e a interface estática. A API Python e a sessão do Goofish continuam locais; sua migração Cloudflare não faz parte deste deploy.
