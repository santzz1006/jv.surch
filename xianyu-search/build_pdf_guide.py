from pathlib import Path
import json
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image,Preformatted
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'output/pdf';OUT.mkdir(parents=True,exist_ok=True)
pdfmetrics.registerFont(TTFont('Body','C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('BodyBold','C:/Windows/Fonts/arialbd.ttf'))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold')
pdfmetrics.registerFont(TTFont('Round',str(ROOT/'extension-shop/assets/junegull.ttf')))
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Copy',fontName='Body',fontSize=10.5,leading=15,spaceAfter=10,textColor=colors.HexColor('#24271e')))
styles.add(ParagraphStyle(name='TitleCustom',fontName='Round',fontSize=28,leading=30,spaceAfter=18,textColor=colors.HexColor('#161b12')))
styles.add(ParagraphStyle(name='HCustom',fontName='BodyBold',fontSize=14,leading=18,spaceBefore=12,spaceAfter=8))
styles.add(ParagraphStyle(name='SmallCustom',fontName='Body',fontSize=8.5,leading=12,spaceAfter=7))
styles.add(ParagraphStyle(name='CodeCustom',fontName='Courier',fontSize=9,leading=13,backColor=colors.HexColor('#f2f3ea'),borderPadding=9,spaceBefore=8,spaceAfter=13))
P=lambda s:Paragraph(s,styles['Copy'])
H=lambda s:Paragraph(s,styles['HCustom'])
S=lambda s:Paragraph(s,styles['SmallCustom'])
def title(n,t):return [S('GUIA PRÁTICO  /  '+n),Paragraph(t,styles['TitleCustom'])]
def code(s):return Preformatted(s,styles['CodeCustom'])
def box(s):
 t=Table([[P(s)]],colWidths=[480]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#fff4a7')),('BOX',(0,0),(-1,-1),.7,colors.HexColor('#e0ca36')),('LEFTPADDING',(0,0),(-1,-1),13),('RIGHTPADDING',(0,0),(-1,-1),13),('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),4)]));return t
count=len(json.loads((ROOT/'public/data/products.json').read_text(encoding='utf-8'))['items'])
report=json.loads((ROOT/'EVO-IMPORTACAO.json').read_text(encoding='utf-8'))
f=lambda n:f'{n:,}'.replace(',','.')
story=[]
story+=title('01','GOOFISH BR\nNA CLOUDFLARE')
story += [P('Configuração, teste de acesso e etapas para o login remoto.<br/><b>Versão 1.3.3 - 22 de novembro de 2026</b>'),box('<b>Atenção ao estado atual:</b> a API e o banco estão publicados. O Goofish recusou o navegador remoto antes de mostrar o login. Ainda não falta somente escanear um QR.'),Spacer(1,16),H('Seu catálogo ampliado'),P(f'<b>{f(count)} produtos no total</b>, com {f(count-46011)} novos anúncios únicos nesta continuação. Foram obtidos {f(report["publicRowsImported"])} registros únicos da fonte externa. A contagem total também preserva o acervo anterior e remove repetições.'),P('A fonte informou aproximadamente 75 mil anúncios, mas a exportação ampla retornou erro 500. A coleta por termos recuperou mais páginas; não foi possível confirmar uma cópia integral. Títulos e fotos novos foram mantidos como fornecidos, preservando traduções e galerias anteriores.'),H('O que já está funcionando')]
rows=[['Recurso','Situação verificada'],['API e banco D1','Publicados na Cloudflare'],['Catálogo e extensão','Busca sem conta chinesa; versão 1.3.3'],['Painel flutuante','Goofish e site Goofish Br'],['Alertas locais','Mudanças observadas no catálogo; Chrome aberto'],['Salvar novos resultados','Implementado na API; depende da fonte ao vivo'],['Sessão, QR e conversa','Não ativados: acesso remoto recusado']]
t=Table([[S(v) for v in row] for row in rows],colWidths=[170,310]);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#ffe615')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d9dccb')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),4)]));story += [t,PageBreak()]
story+=title('02','COMO ABRIR\nO TESTE DE LOGIN')
story += [P('O comando abaixo abre um navegador real na Cloudflare e cria um link privado de controle. É um diagnóstico: ele não configura a coleta nem salva um login permanente.'),H('1. Abra a pasta correta'),P('No terminal, entre na pasta <b>xianyu-search/cloudflare</b> do projeto. O arquivo <b>browser-login.mjs</b> acompanha o pacote da API 1.3.3.'),H('2. Confira sua autorização'),code('npx wrangler whoami'),P('O comando deve mostrar sua conta. Se não houver autorização, execute <b>npx wrangler login</b> e conclua a autorização oficial no navegador. Autorizar a Cloudflare não faz login no Goofish.'),H('3. Crie o navegador remoto'),code('node browser-login.mjs start'),P('Abra o arquivo <b>.env.browser-login.html</b>, criado nessa mesma pasta, e clique em <b>Abrir navegador remoto</b>. O endereço inicial expira em cinco minutos. O arquivo contém acesso privado à sessão: não envie para outras pessoas. [1]'),H('4. Se o login do Goofish aparecer'),P('Leia o QR exibido pelo próprio Goofish com o aplicativo da sua conta e confirme o acesso no celular. Use o código da sessão remota atual, não uma imagem antiga ou o QR do Chrome local. Se o código expirar, atualize-o pela própria tela oficial.'),box('<b>Se aparecer “acesso inválido / use um navegador normal”, pare o teste.</b> Esse foi o resultado observado nesta entrega. Não há QR válido nessa tela.'),H('5. Encerre o diagnóstico'),code('node browser-login.mjs stop'),P('O comando encerra o navegador e invalida o arquivo de controle. Este teste não exporta cookies para a extensão e não conecta a busca automaticamente.'),PageBreak()]
story+=title('03','POR QUE A SESSÃO\nAINDA NÃO ATIVOU')
story += [P('Dois testes no navegador da Cloudflare chegaram ao site oficial, mas receberam a mensagem de acesso inválido antes da autenticação. O helper de abertura e encerramento do painel remoto também foi testado.'),H('Tela recebida no teste')]
screenshot=ROOT/'cloudflare/.env.goofish-remote.png'
if screenshot.exists():
 from PIL import Image as PILImage
 w,h=PILImage.open(screenshot).size
 story.append(Image(str(screenshot),width=420,height=420*h/w))
story += [S('Captura do teste remoto, sem conta autenticada ou QR. A mensagem pede acesso por um navegador normal.'),H('Cloudflare online não significa Goofish conectado'),P('O Worker atende a API e o D1 guarda os produtos. Browser Run é outro serviço, que executa o navegador. O site de destino pode recusá-lo; a documentação informa que suas requisições são identificadas como automação. [3]'),H('Limites do plano gratuito'),P('O plano Workers Free oferece 10 minutos de navegador por dia. O navegador fecha após inatividade; aumentar esse intervalo não elimina a franquia diária. Portanto, o plano gratuito não mantém uma sessão de navegador ligada 24 horas. Nenhum plano pago foi ativado. [2]'),H('O que permanece pendente'),P('É necessário primeiro conseguir uma origem aceita pelo Goofish. Depois, implementar o coletor, armazenar o estado da sessão apenas no servidor, proteger o painel do proprietário e validar a restauração após reiniciar o navegador. Esses componentes não estão concluídos e não surgem apenas ao ler o QR.'),PageBreak()]
story+=title('04','ATIVAÇÃO E\nVERIFICAÇÃO FINAL')
story += [H('Quando existir um coletor autenticado válido'),P('No Worker <b>goofish-br-api</b>, configure <b>SEARCH_SOURCE_URL</b> com o endereço do seu coletor. Ele deve implementar <b>GET /search?q=TERMO&amp;page=1&amp;limit=48</b>. Para a rotina privada de preços, configure <b>PRODUCT_SOURCE_URL</b>, com <b>GET /products/ID</b>. Os formatos de resposta estão no LEIA-ME do pacote.'),P('Se a origem exigir chave, guarde-a em <b>SEARCH_SOURCE_TOKEN</b> e <b>PRODUCT_SOURCE_TOKEN</b> usando segredos da Cloudflare. Não coloque cookies ou a chave administrativa na extensão pública. Esses endereços não estão configurados porque o coletor autenticado ainda não existe.'),H('Como conferir o serviço publicado'),P('<link href="https://goofish-br-api.neilan-sttephan1.workers.dev/health" color="#394d20">Abrir diagnóstico da API</link><br/>Agora, <b>database</b> é verdadeiro e <b>liveSearch</b> é falso. A busca ao vivo devolve 503 com a explicação de indisponibilidade. O catálogo salvo continua funcionando.'),P('Após conectar a fonte, confirme uma busca real, as fotos e o preço contra o anúncio de origem. Confirme também que o produto aparece na consulta pública do catálogo, sem credencial administrativa. A busca pública tem limite global de 100 tentativas por dia nesta versão.'),H('Conversas e tradução'),P('O chat e o tradutor de conversas ainda não foram implementados. Eles dependem do acesso autenticado aceito pelo Goofish. As mensagens da conta devem ficar restritas ao proprietário; uma implementação futura precisa mostrar original e tradução e permitir revisão antes de enviar.'),H('Extensão e alertas disponíveis agora'),P('Baixe a versão 1.3.3, substitua os arquivos da instalação anterior e use <b>Recarregar</b> em <b>chrome://extensions</b>. Para alertas: salve um anúncio, abra Alertas, selecione o item e ative as notificações. O Chrome compara dados observados no catálogo; sem dados novos, mantém o último preço. Isso não equivale a consultar o Goofish continuamente.'),H('Referências e arquivos'),S('[1] <link href="https://developers.cloudflare.com/browser-run/cdp/session-management/" color="#394d20">Cloudflare: gerenciamento de sessões e painel privado</link><br/>[2] <link href="https://developers.cloudflare.com/browser-run/limits/" color="#394d20">Cloudflare: limites do Browser Run</link><br/>[3] <link href="https://developers.cloudflare.com/browser-run/puppeteer/" color="#394d20">Cloudflare: Puppeteer e identificação de automação</link><br/>Documentação consultada em 22/11/2026. Consulte os limites atuais antes de ampliar o uso.'),S('<link href="https://santzz1006.github.io/jv.surch/xianyu-search/public/extensao.html" color="#394d20">Página da extensão e download</link> - Projeto independente do Goofish/Xianyu.')]
def frame(c,doc):
 c.setFillColor(colors.HexColor('#ffe615'));c.rect(0,802,595.28,40,fill=1,stroke=0)
 c.setFillColor(colors.HexColor('#161b12'));c.setFont('Round',15);c.drawString(48,816,'GOOFISH BR')
 c.setFont('Body',8);c.setFillColor(colors.HexColor('#6b705f'));c.drawString(48,26,'Guia de operação | 22/11/2026 | Sem credenciais neste documento');c.drawRightString(547,26,str(doc.page))
file=OUT/'Guia-Goofish-Br-Cloudflare.pdf'
SimpleDocTemplate(str(file),pagesize=(595.28,841.89),rightMargin=57,leftMargin=58,topMargin=66,bottomMargin=48,title='Goofish Br - Guia Cloudflare e sessão Goofish',author='Goofish Br').build(story,onFirstPage=frame,onLaterPages=frame)
print(file)
