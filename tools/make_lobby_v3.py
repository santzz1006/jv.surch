"""Editable architectural source; identical dimensions drive Blender art and Roblox collision."""
import json,math
from pathlib import Path
r=Path(__file__).resolve().parents[1]
d={'Id':'Lobby','Name':'Paddle Plaza','Parts':[],'Spawns':[[0,4,36]],'KillY':-18}
N='#18213d';W='#d9e4fa';B='#087bff';R='#ff304b';C='#00d9ff';Y='#ffc928';P='#762bff'
def part(n,s,p,c,shape='Box',yaw=0,decor=False):d['Parts'].append(dict(name=n,size=s,pos=p,color=c,shape=shape,yaw=yaw,decor=decor))
part('Foundation',[160,4,144],[0,-2,0],N)
part('Plaza',[154,.4,138],[0,.2,0],W)
# A true octagonal dais, neon segmented ring and radial paving.
for rad,h,y,col in [(24,1,.5,N),(23,.25,1.1,C),(21.8,.3,1.4,B),(20,.25,1.7,W)]:part('OctagonalDais',[rad*2,h,rad*2],[0,y,30],col,'Octagon')
for x in [-14,14]:part('PortalRunwayLight',[.5,.15,51],[x,.5,-11],C,decor=True)
part('Runway',[27,.12,52],[0,.43,-11],N)
for z in range(-35,15,8):part('WalkwayTile',[25,.13,6],[0,.54,z],'#a5b9df')
# Stadium back walls and terraced stands, mirrored with team colors.
for side in [-1,1]:
 color=B if side<0 else R
 part('StadiumWall',[51,28,5],[side*48,14,-62],N)
 part('WallFace',[47,24,1],[side*48,13,-58.8],'#687cae')
 for i in range(5):
  part('GrandstandStep',[31,1.8+i*1.6,5],[side*57,(1.8+i*1.6)/2,-23-i*5],W)
  part('SeatRow',[28,1,1.8],[side*57,2.6+i*1.6,-23-i*5],color)
 for x in [31,75]:
  part('Buttress',[5,32,7],[side*x,16,-61],W)
  part('ButtressBand',[5.3,1.5,7.3],[side*x,23,-61],color)
 for z in [-48,48]:
  x=side*68
  part('TreePlanter',[12,3,12],[x,1.5,z],N)
  part('PlanterCap',[12.5,.6,12.5],[x,3,z],W)
  part('Trunk',[2.8,11,2.8],[x,8,z],'#97603d')
  part('BlockFoliage',[16,10,13],[x,16,z],'#32bf53')
  part('CrownFoliage',[12,5,11],[x-2,23,z],'#68e65b')
  part('LeafCluster',[9,7,10],[x+5,17,z+3],'#14933b')
 for z in [-35,35]:
  x=side*73
  part('FloodlightPole',[1.4,32,1.4],[x,16,z],N)
  part('FloodlightFrame',[11,8,2],[x,32,z],N)
  for dx in [-3.4,0,3.4]:
   for dy in [-1.7,1.7]:part('LightPanel',[2.6,2.6,.4],[x+dx,32+dy,z+1.3],'#fff8d7',decor=True)
# Portal, flanking ribs and raised logo pedestal.
for x in [-20,20]:
 part('PortalOuter',[7,28,8],[x,14,-45],N)
 part('PortalInner',[1,24,1],[x-3 if x>0 else x+3,13,-40.7],C,decor=True)
 part('PortalFoot',[12,3,14],[x,1.5,-44],W)
part('PortalLintel',[47,8,8],[0,29,-45],N)
part('PortalLight',[35,1,1],[0,25,-40.5],C,decor=True)
part('PortalCeiling',[32,1,21],[0,24,-52],W)
part('PortalBack',[32,24,1],[0,12,-61],B,decor=True)
for x in [-12,12]:part('PortalInnerGlow',[.45,18,.6],[x,12,-60],C,decor=True)
part('PortalInnerTop',[24,.45,.6],[0,21,-60],C,decor=True)
part('LogoBacking',[48,13,4],[0,39,-47],N)
part('LogoUnderline',[41,1.2,5],[0,31.5,-46],C,decor=True)
# Interactive signage positions are specified in Maps.luau.
for x,label,color in [(-44,'Modes',B),(44,'Shop',Y)]:
 part(label+'Kiosk',[29,20,3],[x,12,-8],N)
 part(label+'Border',[29.5,21,1],[x,12,-9.7],color)
 part(label+'Header',[31,6,4],[x,25,-8],color)
 part(label+'Foot',[34,2,12],[x,1,-7],N)
 part(label+'Neon',[31,.4,12.3],[x,2.1,-7],color,decor=True)
 for side in [-1,1]:part(label+'Pillar',[2.5,26,4],[x+side*16,13,-9],W)
 if label=='Shop':
  for dx in [-9,0,9]:
   part('DisplayPaddle',[5,6,1],[x+dx,16,-5.9],R if dx<0 else B if dx==0 else P,'Ball',decor=True)
   part('DisplayGrip',[1.1,4,1],[x+dx,11.8,-5.9],'#e9bb7e',decor=True)
   part('DisplayBall',[2.5,2.5,2.5],[x+dx,6,-5.9],W if dx==0 else color,'Ball',decor=True)
  part('ShopShelf',[27,.5,3],[x,8,-5.5],Y)
for x in [-55,55]:
 part('SideWalk',[25,.25,20],[x,.5,35],N)
 for i in range(3):part('SideStep',[25,1+i,3],[x,(1+i)/2,48+i*3],W)
 part('Banner',[16,14,1],[x,14,55],B if x<0 else R)
part('TrainingSign',[23,10,3],[-53,8,18],B)
part('SeasonSign',[23,10,3],[53,8,18],P)
for x in [-74,74]:part('SideBoundary',[3,7,138],[x,3.5,0],N)
for z in [-71,71]:part('Boundary',[154,3,3],[0,1.5,z],N)
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 return str(v)
(r/'assets/maps/Lobby.json').write_text(json.dumps(d,indent=2),encoding='utf-8')
(r/'src/shared/LobbyData.luau').write_text('return '+lua(d),encoding='utf-8')
print('Lobby V3',len(d['Parts']),'parts')
