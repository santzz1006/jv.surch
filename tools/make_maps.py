"""One geometry specification drives Blender art and Roblox collision hulls."""
from pathlib import Path
import json,math
r=Path(__file__).resolve().parents[1]
maps=[]
def make(key,name,theme):
 d={'Id':key,'Name':name,'Theme':theme,'Parts':[],'Spawns':[[0,4,-28],[0,4,28]],'KillY':-18}
 maps.append(d);return d
def part(d,n,s,p,c,shape='Box',ry=0,decor=False):d['Parts'].append({'name':n,'size':s,'pos':p,'color':c,'shape':shape,'yaw':ry,'decor':decor})
def shell(d,floor,wall):
 part(d,'Court',[88,2,76],[0,-1,0],floor)
 for x in [-45,45]:part(d,'SideWall',[2,14,80],[x,6,0],wall)
 for z in [-39,39]:part(d,'EndWall',[92,14,2],[0,6,z],wall)
 for z in [-31,31]:
  part(d,'SpawnStripe',[16,.12,6],[0,.08,z],'#9766ff' if z<0 else '#ffd348',decor=True)
def pair(d,n,s,p,c,shape='Box',yaw=0,decor=False):
 for sign in [-1,1]:part(d,n+str(sign),s,[p[0]*sign,p[1],p[2]*sign],c,shape,yaw if sign>0 else yaw+180,decor)
def table(d,x,z,y=0):
 part(d,'GiantTable',[16,1.1,9],[x,y+3,z],'#32bbaa')
 part(d,'TableLine',[.18,.06,8.8],[x,y+3.59,z],'#f4fff7',decor=True)
 for xx in [-6.5,6.5]:
  for zz in [-3.2,3.2]:part(d,'TableLeg',[.8,3,.8],[x+xx,y+1.3,z+zz],'#17263b')
 part(d,'TableNet',[.25,2,9],[x,y+4.5,z],'#d8fff5')
for key,name,theme in [('Ponte','Ponte','sky'),('Westown','Westown','wood'),('Cemiterio','Cemitério','lavender'),('Arena','Arena','white'),('Backrooms','Backrooms','yellow'),('Campo','Campo de Batalha','sand'),('Xadrez','Xadrez','chess'),('Portao','Portão','portal'),('Parquinho','Parquinho','play'),('Experimento','Área de Experimentação','lab')]:
 d=make(key,name,theme)
 colors={'sky':('#457da5','#bfd9ed'),'wood':('#d9b784','#bc8a5c'),'lavender':('#837ba5','#b9a9d6'),'white':('#dbe5f3','#f5f7ff'),'yellow':('#d5c990','#e5d99c'),'sand':('#cfb386','#8a9a8a'),'chess':('#cbd7ee','#7986ac'),'portal':('#83bca5','#a8d8c0'),'play':('#7fcda0','#beddf1'),'lab':('#64768c','#ccd8e4')};shell(d,*colors[theme])
 if key=='Ponte':
  d['Parts'][0]['pos'][1]=-12;d['KillY']=-8
  part(d,'Bridge',[20,2,64],[0,0,0],'#d9e6f6')
  for z in [-29,29]:part(d,'Island',[80,2,20],[0,0,z],'#8db9db')
  pair(d,'RicochetPylon',[5,9,7],[6,5,13],'#8064e8')
  pair(d,'Ramp',[9,5,15],[-20,2.5,24],'#ebbc4d','Wedge',90)
 elif key=='Westown':
  for x in [-27,27]:
   for z in [-15,15]:
    part(d,'Booth',[12,9,12],[x,4.5,z],'#ba8050');part(d,'Roof',[15,1,15],[x,9.6,z],'#7a4b83')
  pair(d,'Crate',[7,5,7],[12,2.5,10],'#dcac68');table(d,0,0)
 elif key=='Cemiterio':
  for x in [-26,-13,13,26]:
   for z in [-15,0,15]:
    part(d,'Memorial',[5,7,2],[x,3.5,z],'#b7accd');part(d,'BallMemorial',[4,4,4],[x,8,z],'#e9e3f7','Ball',decor=True)
  pair(d,'LowWall',[13,3,2],[11,1.5,23],'#9a8cac')
 elif key=='Arena':
  pair(d,'Tower',[10,12,10],[25,6,12],'#f6f7fe');pair(d,'LowCover',[14,4,5],[12,2,20],'#a6ace7');pair(d,'CenterCover',[5,8,15],[9,4,0],'#a98bff');table(d,0,0)
 elif key=='Backrooms':
  pair(d,'HallDivider',[2,12,40],[17,6,3],'#dbcf94');pair(d,'HallTurn',[18,12,2],[26,6,-13],'#e9ddaa');pair(d,'CenterWall',[16,12,2],[7,6,6],'#d1bd83')
  for x in [-34,0,34]:
   for z in [-24,24]:part(d,'Light',[6,.15,3],[x,11.5,z],'#fff8ce',decor=True)
 elif key=='Campo':
  pair(d,'Bunker',[17,7,10],[25,3.5,14],'#72877a');pair(d,'BunkerRamp',[12,6,14],[23,3,-6],'#a9b48d','Wedge',180);pair(d,'Sandbag',[12,3,4],[8,1.5,16],'#dfc895');table(d,0,0)
 elif key=='Xadrez':
  for ix in range(8):
   for iz in range(8):part(d,'Tile',[9,.1,8],[ix*9-31.5,.06,iz*8-28],'#eaf0fa' if (ix+iz)%2 else '#5b658e',decor=True)
  for x in [-24,24]:
   for z in [-14,14]:
    part(d,'RookBase',[9,2,9],[x,1,z],'#adb6d9');part(d,'Rook',[6,9,6],[x,6,z],'#e9e8fa')
    for xx in [-2,2]:part(d,'RookBattlement',[2,2,7],[x+xx,11.5,z],'#e9e8fa')
  pair(d,'Pawn',[5,5,5],[10,2.5,0],'#b9a0eb','Ball')
 elif key=='Portao':
  for x in [-12,12]:part(d,'PortalPillar',[6,17,8],[x,8.5,0],'#6a62a8')
  part(d,'PortalLintel',[30,4,8],[0,16,0],'#9c86d9');pair(d,'Ramp',[14,5,16],[24,2.5,15],'#accbb8','Wedge');pair(d,'Cover',[9,5,6],[13,2.5,23],'#d8e9ca')
 elif key=='Parquinho':
  for x,z in [(-24,-12),(24,12)]:
   part(d,'PlayTower',[14,1,14],[x,6,z],'#ffcb4b')
   for xx in [-5,5]:
    for zz in [-5,5]:part(d,'PlayPost',[1.5,6,1.5],[x+xx,3,z+zz],'#8b68cf')
   part(d,'Slide',[9,6,17],[x,3,z+15],'#f78298','Wedge')
  pair(d,'PlayBlock',[8,4,8],[9,2,12],'#6bbee3');table(d,0,0)
 else:
  pair(d,'BounceWall',[2,11,24],[18,5.5,3],'#d3e1ec',yaw=25);pair(d,'Pad',[13,3,9],[8,1.5,22],'#5dc8cb');pair(d,'LabRamp',[12,6,14],[29,3,10],'#9c87df','Wedge',90)
  for x in [-30,0,30]:part(d,'TestOrb',[4,4,4],[x,9,0],'#ffd75b','Ball',decor=True)
 (r/'assets/maps'/f'{key}.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
(r/'assets/maps/catalogue.json').write_text(json.dumps(maps,ensure_ascii=False),encoding='utf-8')
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 return str(v)
(r/'src/shared/MapData.luau').write_text('-- Shared source for art and collision geometry.\nreturn '+lua(maps)+'\n',encoding='utf-8')
print('Created',len(maps),'maps',sum(len(m['Parts']) for m in maps),'parts')
