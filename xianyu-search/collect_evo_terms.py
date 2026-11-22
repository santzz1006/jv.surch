"""Resume ordinary keyword searches on the distributed anonymous catalogue RPC.
Preserves checkpoints, pauses between requests, and stops on access controls.
"""
import json,time,urllib.request,urllib.error
from collect_evo_catalog import public_config,CACHE
import sys
sys.stdout.reconfigure(encoding="utf-8")
url,key=public_config()
terms=['鞋','衣','电脑','手机','包','手表','游戏','运动','相机','耳机','全新','闲置','二手','出售','转让','玩具','键盘','裤','裙','外套','显卡','饰品','笔','书','模型','收藏','家具','儿童']
terms=sys.argv[1:] or terms
if any(not term.isalnum() for term in terms):raise ValueError("Use somente letras e números nos termos.")
for term in terms:
 for offset in range(0,60000,500):
  dest=CACHE/('term-'+term+'-'+str(offset)+'.json')
  if dest.exists():
   cached=json.loads(dest.read_text(encoding='utf-8'))
   if len(cached)<500:break
   continue
  req=urllib.request.Request(url+'/rest/v1/rpc/buscar_catalogo_xianyu',data=json.dumps({'p_termo':term,'p_limite':500,'p_inicio':offset}).encode(),headers={'apikey':key,'Authorization':'Bearer '+key,'Content-Type':'application/json'})
  try:
   with urllib.request.urlopen(req,timeout=35) as response: rows=json.load(response)
  except urllib.error.HTTPError as e:
   print('Stopped term',term,'HTTP',e.code,flush=True)
   if e.code in [401,403,429]:raise SystemExit(1)
   break
  except Exception as e:print(type(e).__name__,flush=True);break
  if not isinstance(rows,list):break
  temp=dest.with_suffix('.tmp');temp.write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8');temp.replace(dest);print(term,offset,len(rows),flush=True)
  if len(rows)<500:break
  time.sleep(2)
