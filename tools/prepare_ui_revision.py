from pathlib import Path
r=Path(__file__).resolve().parents[1]
s=(r/'tools/blender_ui.py').read_text(encoding='utf-8')
s=s.replace('assets/ui/v2','assets/ui/v3').replace("OUT.mkdir(exist_ok=True)","OUT.mkdir(exist_ok=True,parents=True)")
s=s.replace("(.88,.88,.88)","(.91,.96,1)").replace("(.045,.045,.045)","(.012,.023,.065)").replace("(.26,.26,.26)","(.025,.18,.62)")
s=s.replace("def render(key):",'''def render(key):
 global WHITE,DARK,MID
 WHITE=mat('White',(.91,.96,1));DARK=mat('Dark',(.012,.023,.065));MID=mat('Mid',(.025,.18,.62))
 accent={'Heart':(.08,.95,.025),'Health':(.05,.95,.015),'Trophy':(1,.58,.015),'Star':(1,.72,.025),'Crate':(.42,.035,.9),'Paddle':(.95,.01,.045),'Shield':(.015,.55,1),'Sprint':(.06,.82,.22),'Reload':(.025,.65,1),'ScoreBlue':(.015,.28,1),'ScoreRed':(1,.025,.08),'Coin':(1,.66,.015),'Key':(1,.66,.015)}
 if key in accent:WHITE=mat('Accent_'+key,accent[key])
''')
# Defaults bind at declaration; reset geometry defaults to current colored material.
s=s.replace("material=WHITE):","material=None):\n if material is None:material=WHITE")
s=s.replace("mat=WHITE,r=.15):","mat=None,r=.15):\n if mat is None:mat=WHITE")
s=s.replace("mat=WHITE):","mat=None):\n if mat is None:mat=WHITE")
s=s.replace("elif key=='Score':", "elif key in ['ScoreBlue','ScoreRed']:")
s=s.replace("box('Bar',w,h,r=.25)","box('Rim',w,h,mat=DARK,r=.25);box('Bar',w-.12,h-.12,z=.15,r=.22)")
s=s.replace("disc('Rim',1.8);", "disc('Rim',1.8,mat=DARK);")
s=s.replace("disc('Center',1.57,z=.14,mat=DARK)","disc('Center',1.57,z=.14,mat=mat('SlotInner',(.025,.055,.14)))")
s=s.replace("disc('Rubber',1.02,y=.5,z=.14,mat=MID);box('Handle',.5,1.5,y=-1,z=0,mat=WHITE", "disc('Rubber',1.02,y=.5,z=.14);box('Handle',.5,1.5,y=-1,z=0,mat=mat('Wood',(.85,.55,.24))")
s=s.replace("box('Gift',2.8,2.6,y=-.2,mat=MID", "box('Gift',2.8,2.6,y=-.2,mat=WHITE")
s=s.replace("box('Ribbon',.45,2.8,y=-.2,z=.2)", "box('Ribbon',.45,2.8,y=-.2,z=.2,mat=mat('Gold',(1,.65,.015)))")
extra=''' elif key=='Play':meshpoly('Play',[(-1.1,-1.4),(1.4,0),(-1.1,1.4)])
 elif key=='Shop':
  line('Cart',[(-1.6,1.4,0),(-1.1,1.4,0),(-.65,-.65,0),(1.2,-.65,0)],.17);meshpoly('Basket',[(-1,1),(1.5,1),(1.15,-.25),(-.7,-.25)])
  disc('Wheel',.25,x=-.5,y=-1.25);disc('Wheel',.25,x=1,y=-1.25)
 elif key=='Inventory':
  box('Bag',2.5,2.6,y=-.25,r=.4);line('Handle',[(-.65,1,0),(-.65,1.65,0),(.65,1.65,0),(.65,1,0)],.16);box('Pocket',1.6,.8,y=-.65,z=.24,mat=MID,r=.15)
 elif key=='Settings':
  disc('Gear',1.25)
  for i in range(8):
   a=i*math.pi/4;o=box('Tooth',.6,.7,x=math.sin(a)*1.3,y=math.cos(a)*1.3,r=.1);o.rotation_euler.z=-a
  disc('Center',.55,z=.2,mat=DARK)
 elif key=='Exit':
  box('Door',1.4,3,x=-.65);box('DoorInside',.7,2.4,x=-.55,z=.2,mat=DARK);box('ArrowStem',1.4,.4,x=.7,z=.3);meshpoly('Arrow',[(.9,-.8),(1.8,0),(.9,.8)],.3)
 elif key=='Hourglass':
  box('Top',2.2,.3,y=1.5);box('Bottom',2.2,.3,y=-1.5);line('Glass',[(-.85,1.3,0),(-.7,.5,0),(.7,-.5,0),(.85,-1.3,0)],.12);line('Glass2',[(.85,1.3,0),(.7,.5,0),(-.7,-.5,0),(-.85,-1.3,0)],.12)
  meshpoly('Sand',[(-.6,-1.25),(.6,-1.25),(0,-.55)],mat=mat('Sand',(1,.7,.03)))
 elif key=='Tasks':
  box('Board',2.4,3,mat=mat('Cyan',(.01,.6,1)),r=.2);box('Paper',1.95,2.45,z=.2,r=.1);box('Clip',1,.4,y=1.4,z=.3,mat=MID)
  for y in [.6,0,-.6]:box('Line',1.1,.14,x=.2,y=y,z=.4,mat=MID,r=.04)
 elif key=='Chart':
  for x,y,h in [(-1,-.4,1.6),(0,.3,3),(1,-.1,2.2)]:box('Bar',.65,h,x=x,y=y,r=.08)
 elif key=='Coin':disc('Gold',1.55);disc('Inset',1.25,z=.15,mat=mat('CoinInset',(.85,.32,.01)));box('Mark',.32,1.5,z=.3,r=.12)
 elif key=='Key':disc('Ring',.85,x=-.6,y=.65);disc('Hole',.35,x=-.6,y=.65,z=.2,mat=DARK);box('Stem',.4,1.9,x=-.15,y=-.5);box('Bit',.9,.35,x=.1,y=-1.3)
'''
# meshpoly accepts 'material', not mat.
extra=extra.replace("] ,mat=", "] ,material=").replace("] ,", "],").replace("],mat=mat('Sand'", "],material=mat('Sand'")
s=s.replace(" bpy.ops.object.light_add(type='AREA'",extra+" bpy.ops.object.light_add(type='AREA'")
s=s.replace("scene.cycles.samples=12", "scene.cycles.samples=16;scene.view_settings.view_transform='Standard'")
(r/'tools/blender_ui_v3.py').write_text(s,encoding='utf-8')
compile(s,'ui_v3','exec')
print('UI v3 renderer ready')
