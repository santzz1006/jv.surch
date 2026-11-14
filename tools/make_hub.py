import json,pathlib,math
r=pathlib.Path(__file__).resolve().parents[1]
BLUE='#278fff';RED='#ff5266';NAVY='#182c4b';WHITE='#e8f4ff'
def scene(key,name):return {'Id':key,'Name':name,'Parts':[],'Spawns':[[0,4,-32],[0,4,32]],'KillY':-18}
def part(d,n,s,p,c,shape='Box',yaw=0,decor=False):d['Parts'].append(dict(name=n,size=s,pos=p,color=c,shape=shape,yaw=yaw,decor=decor))
lob=scene('Lobby','Paddle Plaza')
part(lob,'PlazaBase',[148,4,122],[0,-2,0],NAVY)
part(lob,'WarmCourt',[130,.3,104],[0,.15,0],'#c8deed')
for x in [-63,63]:part(lob,'SidePromenade',[15,.5,104],[x,.4,0],BLUE if x<0 else RED)
for z in [-57,57]:part(lob,'PlazaBorder',[148,1.6,4],[0,.8,z],WHITE)
for x in [-73,73]:part(lob,'SideBorder',[3,2,122],[x,1,0],WHITE)
part(lob,'CentralRunway',[24,.12,80],[0,.4,4],NAVY)
for x in [-13,13]:part(lob,'RunwayLight',[.7,.18,80],[x,.5,4],BLUE if x<0 else RED,decor=True)
# Raised stage, paired curved-feeling multi-segment gateway and center ball monument.
part(lob,'MainStage',[52,3,26],[0,1.5,-41],NAVY)
for i in range(3):part(lob,'StageStep',[36,1,4],[0,.5+i,-25-i*3],WHITE)
for x in [-25,25]:
 part(lob,'StageColumn',[4,25,5],[x,13,-44],BLUE if x<0 else RED)
 part(lob,'ColumnFoot',[8,2,9],[x,2,-44],WHITE)
part(lob,'MainMarquee',[54,9,4],[0,25,-44],NAVY)
part(lob,'MarqueeHighlight',[56,1.2,4.5],[0,30,-44],WHITE,decor=True)
part(lob,'HeroBall',[10,10,10],[0,9,-42],WHITE,'Ball',decor=True)
for x in [-8,8]:
 part(lob,'HeroPaddleHead',[8,9,1.4],[x,9,-40],BLUE if x<0 else RED,'Ball',decor=True)
 part(lob,'HeroPaddleGrip',[2,7,1.6],[x,3.5,-40],NAVY,decor=True)
# Queue portals / kiosk islands and benches.
for x in [-44,44]:
 color=BLUE if x<0 else RED
 for z in [-20,17]:
  part(lob,'PortalIsland',[26,1,22],[x,.7,z],NAVY)
  for side in [-1,1]:part(lob,'PortalSide',[2.5,14,3],[x+side*9,7,z-6],color)
  part(lob,'PortalTop',[21,3,3],[x,14,z-6],color)
  part(lob,'PortalScreen',[15,10,1],[x,7,z-7],NAVY)
  part(lob,'PortalThreshold',[17,.3,7],[x,1.4,z],color,decor=True)
  part(lob,'QueueBall',[2.5,2.5,2.5],[x-10,17,z-6],WHITE,'Ball',decor=True)
for x in [-31,31]:
 for z in [32,43]:
  part(lob,'Bench',[16,1,4],[x,2.8,z],NAVY)
  for dx in [-6,6]:part(lob,'BenchFoot',[1.5,2.8,3],[x+dx,1.4,z],WHITE)
for x in [-63,63]:
 for z in [-40,40]:
  part(lob,'Planter',[9,3,9],[x,1.5,z],WHITE)
  part(lob,'TreeTrunk',[2,8,2],[x,6,z],'#8c7266')
  part(lob,'RoundCanopy',[13,13,13],[x,13,z],'#6cc6a0','Ball',decor=True)
for x in [-55,55]:
 for z in [-4,45]:
  part(lob,'LightPole',[.7,22,.7],[x,11,z],NAVY)
  part(lob,'LightBall',[3,3,3],[x,23,z],WHITE,'Ball',decor=True)
train=scene('Treino','Centro de Treinamento')
part(train,'Floor',[112,2,104],[0,-1,0],'#d5e7ef')
for x in [-57,57]:part(train,'SideWall',[2,15,108],[x,6.5,0],NAVY)
for z in [-53,53]:part(train,'EndWall',[116,15,2],[0,6.5,z],NAVY)
for x in [-36,0,36]:
 part(train,'Lane',[29,.12,88],[x,.1,0],BLUE if x<0 else RED if x>0 else '#edf8ff')
 part(train,'FiringLine',[29,.16,.8],[x,.2,-27],NAVY,decor=True)
 for z in [-10,14,36]:
  part(train,'TargetBase',[8,1,6],[x,.5,z],NAVY)
  part(train,'TargetPost',[1,6,1],[x,3,z],NAVY)
  part(train,'TargetRing',[6,6,1],[x,6,z],WHITE,'Ball')
  part(train,'TargetBullseye',[3,3,1.2],[x,6,z-.1],RED if x<0 else BLUE,'Ball',decor=True)
for x in [-18,18]:
 part(train,'Divider',[2,5,60],[x,2.5,6],NAVY)
 part(train,'RicochetPanel',[2,10,12],[x,5,-20],WHITE,yaw=30 if x<0 else -30)
part(train,'MovementPlatform',[22,4,14],[36,2,32],NAVY)
part(train,'MovementRamp',[12,4,15],[36,2,18],BLUE,'Wedge')
part(train,'JumpBlock',[8,2,8],[29,1,0],RED)
part(train,'SlideGate',[20,1,2],[36,4,-15],NAVY)
for x in [26,46]:part(train,'SlideGatePost',[1.5,4,2],[x,2,-15],NAVY)
for d in [lob,train]:(r/'assets/maps'/f"{d['Id']}.json").write_text(json.dumps(d,indent=2),encoding='utf-8')
maps=json.loads((r/'assets/maps/catalogue.json').read_text(encoding='utf-8'));maps=[d for d in maps if d['Id']!='Treino'];maps.append(train)
for d in maps:
 for p in d['Parts']:
  if p['color']=='#9766ff':p['color']=BLUE
  elif p['color']=='#ffd348':p['color']=RED
def lua(v):
 if isinstance(v,dict):return '{'+','.join('['+json.dumps(k)+']='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,list):return '{'+','.join(lua(x) for x in v)+'}'
 if isinstance(v,bool):return 'true' if v else 'false'
 if isinstance(v,str):return json.dumps(v,ensure_ascii=False)
 return str(v)
(r/'src/shared/MapData.luau').write_text('return '+lua(maps),encoding='utf-8')
(r/'src/shared/LobbyData.luau').write_text('return '+lua(lob),encoding='utf-8')
print('Lobby',len(lob['Parts']),'Training',len(train['Parts']))
