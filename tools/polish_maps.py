import json
from pathlib import Path
r=Path(__file__).resolve().parents[1];maps=[]
keys=['Ponte','Westown','Cemiterio','Arena','Backrooms','Campo','Xadrez','Portao','Parquinho','Experimento','Treino']
for key in keys:
 d=json.loads((r/'assets/maps'/f'{key}.json').read_text(encoding='utf-8'));d['Parts']=[p for p in d['Parts'] if not p['name'].startswith('V3_')]
 def add(n,s,p,c,shape='Box',yaw=0,decor=True):d['Parts'].append(dict(name='V3_'+n,size=s,pos=p,color=c,shape=shape,yaw=yaw,decor=decor))
 if key!='Treino':
  for part in d['Parts']:
   if part['name']=='SpawnStripe':part['color']='#087bff' if part['pos'][2]<0 else '#ff304b'
  for side in [-1,1]:
   c='#087bff' if side<0 else '#ff304b'
   add('EndTrim',[87,.45,.4],[0,9,side*37.8],c)
   add('SpawnBoard',[13,3,.4],[0,6,side*37.6],c)
   for x in [-35,35]:
    add('WallButtress',[3,15,3],[x,7,side*38],'#b5c6df')
    add('Cap',[3.5,.6,3.5],[x,14.5,side*38],c)
   for x in [-43,43]:add('SideTrim',[.4,.5,32],[x,10,side*19],c)
  if key=='Westown':
   for x in [-27,27]:
    for z in [-15,15]:
     add('Window',[3,3,.25],[x,5,z+6.15],'#17213a');add('Door',[2.5,5,.25],[x-3,2.5,z+6.15],'#85512f')
     add('Porch',[15,.6,3],[x,.3,z+7.5],'#b68146')
     for dx in [-5.5,5.5]:add('Post',[.65,9,.65],[x+dx,4.5,z+7],'#6d4432')
  elif key=='Ponte':
   for x in [-10,10]:
    for z in range(-20,21,10):add('BridgePost',[.7,3,.7],[x,2.5,z],'#17213a')
    add('BridgeRail',[.6,.6,44],[x,3.9,0],'#087bff')
   for z in range(-22,23,6):add('ExpansionJoint',[18,.04,.15],[0,1.02,z],'#879ab8')
  elif key=='Arena':
   for x in [-42,42]:
    for z in [-25,0,25]:
     add('LightHousing',[1.5,4,6],[x,11,z],'#18213d');add('StadiumLight',[.3,2.6,4.5],[x*.975,11,z],'#fff4ce')
   for x in [-25,25]:add('TowerBand',[10.4,1,10.4],[x,9,12 if x>0 else -12],'#087bff' if x<0 else '#ff304b')
  elif key=='Cemiterio':
   for x in [-26,-13,13,26]:
    for z in [-15,0,15]:
     add('Plinth',[6,.8,4],[x,.4,z],'#544969');add('Inscription',[2.7,.28,.2],[x,4,z-1.15],'#78628e');add('Inscription2',[1.7,.2,.2],[x,3.4,z-1.15],'#78628e')
  elif key=='Backrooms':
   for x in [-44,44]:
    for z in [-24,0,24]:
     add('WallSeam',[.15,12,.3],[x,6,z],'#b0a06e');add('Baseboard',[.4,.65,75],[x,.4,0],'#8c8054')
   for x in [-33,33]:add('DoorFrame',[.5,9,5],[x,4.5,0],'#887645')
  elif key=='Campo':
   for side in [-1,1]:
    for dx in [-5,0,5]:add('BunkerVent',[.8,2,.3],[side*25+dx,5,side*14-5.2],'#263a36')
    for x in [-4,0,4]:add('SandbagSeam',[.2,2.8,4.2],[side*8+x,1.5,side*16],'#b9a074')
  elif key=='Xadrez':
   for x in [-24,24]:
    for z in [-14,14]:
     add('RookFoot',[10,.6,10],[x,1.1,z],'#273354');add('RookCollar',[7,.7,7],[x,8,z],'#273354')
  elif key=='Portao':
   for x in [-12,12]:add('PortalLight',[.45,13,8.3],[x,8,0],'#00d9ff')
   add('PortalEnergyLintel',[20,.4,8.2],[0,13.8,0],'#00d9ff')
  elif key=='Parquinho':
   for x,z in [(-24,-12),(24,12)]:
    for dz in [-5,5]:add('SafetyRail',[14,1,.7],[x,8,z+dz],'#ff685b')
    add('TowerRoof',[17,1,17],[x,12,z],'#087bff')
    for dx in [-5,5]:add('RoofPost',[.65,6,.65],[x+dx,9,z-5],'#ffc928')
  elif key=='Experimento':
   for side in [-1,1]:
    add('ObservationScreen',[12,6,.5],[side*22,8,side*37.7],'#18213d');add('ScreenGlow',[10,.4,.6],[side*22,9,side*37.3],'#00d9ff')
   for z in [-19,19]:add('TestLine',[75,.08,.3],[0,.05,z],'#ffc928')
 unique={json.dumps(p,sort_keys=True):p for p in d['Parts']};d['Parts']=list(unique.values())
 (r/'assets/maps'/f'{key}.json').write_text(json.dumps(d,indent=2),encoding='utf-8');maps.append(d)
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 return str(v)
(r/'src/shared/MapData.luau').write_text('return '+lua(maps),encoding='utf-8')
(r/'assets/maps/catalogue.json').write_text(json.dumps(maps,ensure_ascii=False),encoding='utf-8')
print('10 arenas received architectural and team landmarks')
