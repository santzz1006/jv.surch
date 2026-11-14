"""Original orthographic 3D UI sprites, each rendered to its own clean alpha PNG."""
import bpy,math
from mathutils import Vector
from pathlib import Path
OUT=Path('C:/Users/neila/OneDrive/Desktop/roblox/assets/ui/v3');OUT.mkdir(exist_ok=True,parents=True)
def mat(name,c):
 m=bpy.data.materials.get('UI_'+name) or bpy.data.materials.new('UI_'+name);m.use_nodes=True
 n=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');n.inputs['Base Color'].default_value=(*c,1);n.inputs['Roughness'].default_value=.38;return m
WHITE=mat('White',(.91,.96,1));DARK=mat('Dark',(.012,.023,.065));MID=mat('Mid',(.025,.18,.62))
def meshpoly(name,points,z=0,material=None):
 if material is None:material=WHITE
 me=bpy.data.meshes.new(name);me.from_pydata([(x,y,z) for x,y in points],[],[tuple(range(len(points)))]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 sol=o.modifiers.new('Depth','SOLIDIFY');sol.thickness=.14;be=o.modifiers.new('Soft edges','BEVEL');be.width=.05;be.segments=4;return o
def box(name,w,h,x=0,y=0,z=0,mat=None,r=.15):
 if mat is None:mat=WHITE
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,z));o=bpy.context.object;o.name=name;o.dimensions=(w,h,.22);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat);b=o.modifiers.new('Bubble corners','BEVEL');b.width=min(r,min(w,h)*.45);b.segments=8;return o
def disc(name,r,x=0,y=0,z=0,mat=None):
 if mat is None:mat=WHITE
 bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=r,depth=.18,location=(x,y,z));o=bpy.context.object;o.name=name;o.data.materials.append(mat);b=o.modifiers.new('Round rim','BEVEL');b.width=.065;b.segments=4;return o
def line(name,pts,bevel=.12,mat=None):
 if mat is None:mat=WHITE
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=bevel;cu.bevel_resolution=5;sp=cu.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat)
def panel(w,h):box('WhiteBorder',w,h,mat=WHITE,r=.3);box('DarkCenter',w-.22,h-.22,z=.15,mat=DARK,r=.26)
def render(key):
 global WHITE,DARK,MID
 WHITE=mat('White',(.91,.96,1));DARK=mat('Dark',(.012,.023,.065));MID=mat('Mid',(.025,.18,.62))
 accent={'Heart':(.08,.95,.025),'Health':(.05,.95,.015),'Trophy':(1,.58,.015),'Star':(1,.72,.025),'Crate':(.42,.035,.9),'Paddle':(.95,.01,.045),'Shield':(.015,.55,1),'Sprint':(.06,.82,.22),'Reload':(.025,.65,1),'ScoreBlue':(.015,.28,1),'ScoreRed':(1,.025,.08),'Coin':(1,.66,.015),'Key':(1,.66,.015)}
 if key in accent:WHITE=mat('Accent_'+key,accent[key])

 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=16;scene.view_settings.view_transform='Standard';scene.cycles.use_denoising=True
 scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
 w=h=4;rx=ry=512
 if key=='Panel':w,h=8,5;rx,ry=1024,640;panel(w,h)
 elif key=='Button':w,h=8,1.75;rx,ry=1024,224;panel(w,h)
 elif key in ['ScoreBlue','ScoreRed']:w,h=5,2;rx,ry=640,256;panel(w,h)
 elif key=='MapCard':w,h=4,5;rx,ry=512,640;panel(w,h)
 elif key=='Slot':disc('Rim',1.8,mat=DARK);disc('Center',1.57,z=.14,mat=mat('SlotInner',(.025,.055,.14)))
 elif key=='Health':w,h=8,.7;rx,ry=1024,90;box('Rim',w,h,mat=DARK,r=.25);box('Bar',w-.12,h-.12,z=.15,r=.22)
 elif key=='Heart':
  points=[]
  for i in range(96):
   t=2*math.pi*i/96;points.append((16*math.sin(t)**3/10,(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t))/10))
  meshpoly('Heart',list(reversed(points)))
 elif key=='Crosshair':
  for x,y,ww,hh in [(0,1,.16,.8),(0,-1,.16,.8),(1,0,.8,.16),(-1,0,.8,.16)]:box('Tick',ww,hh,x,y,r=.07)
 elif key=='Paddle':disc('PaddleHead',1.2,y=.5);disc('Rubber',1.02,y=.5,z=.14);box('Handle',.5,1.5,y=-1,z=0,mat=mat('Wood',(.85,.55,.24)),r=.14)
 elif key=='Balls':
  for x,y in [(-.85,-.5),(.85,-.5),(0,.85)]:
   bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=.84,location=(x,y,0));bpy.context.object.data.materials.append(WHITE)
   for p in bpy.context.object.data.polygons:p.use_smooth=True
 elif key=='Shield':meshpoly('Shield',[(-1.4,1.2),(0,1.7),(1.4,1.2),(1.2,-.7),(0,-1.7),(-1.2,-.7)])
 elif key=='Sprint':meshpoly('Shoe',[(-1.7,-.8),(1.7,-.8),(1.6,.4),(.8,.8),(.5,.3),(-.3,.5),(-.7,-.1),(-1.4,-.3)]);line('Lace',[(-.1,0,.2),(.5,-.1,.2)]);line('Lace2',[(-.4,-.3,.2),(.2,-.4,.2)])
 elif key=='Reload':
  pts=[(1.3*math.cos(t),1.3*math.sin(t),0) for t in [math.radians(35+i*285/40) for i in range(41)]];line('ArrowArc',pts,.21);meshpoly('Arrowhead',[(.5,-1.5),(1.7,-1.5),(1.45,-.3)])
 elif key=='Crate':box('Gift',2.8,2.6,y=-.2,mat=WHITE,r=.2);box('Ribbon',.45,2.8,y=-.2,z=.2,mat=mat('Gold',(1,.65,.015)));box('Lid',3.1,.5,y=1,z=.25);line('Bow',[(-1,.9,0),(-.9,1.6,0),(0,1.1,0),(.9,1.6,0),(1,.9,0)],.17)
 elif key=='Trophy':meshpoly('Cup',[(-1.1,1.4),(1.1,1.4),(.9,0),(.3,-.5),(-.3,-.5),(-.9,0)]);box('Stem',.35,1,y=-.8);box('Base',1.8,.35,y=-1.5);line('HandleLeft',[(-1,1,0),(-1.6,1,0),(-1.55,.2,0),(-.85,0,0)]);line('HandleRight',[(1,1,0),(1.6,1,0),(1.55,.2,0),(.85,0,0)])
 elif key=='Star':meshpoly('Star',[(math.cos(math.pi/2+i*math.pi/5)*(1.8 if i%2==0 else .85),math.sin(math.pi/2+i*math.pi/5)*(1.8 if i%2==0 else .85)) for i in range(10)])
 elif key=='Play':meshpoly('Play',[(-1.1,-1.4),(1.4,0),(-1.1,1.4)])
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
  meshpoly('Sand',[(-.6,-1.25),(.6,-1.25),(0,-.55)],material=mat('Sand',(1,.7,.03)))
 elif key=='Tasks':
  box('Board',2.4,3,mat=mat('Cyan',(.01,.6,1)),r=.2);box('Paper',1.95,2.45,z=.2,r=.1);box('Clip',1,.4,y=1.4,z=.3,mat=MID)
  for y in [.6,0,-.6]:box('Line',1.1,.14,x=.2,y=y,z=.4,mat=MID,r=.04)
 elif key=='Chart':
  for x,y,h in [(-1,-.4,1.6),(0,.3,3),(1,-.1,2.2)]:box('Bar',.65,h,x=x,y=y,r=.08)
 elif key=='Coin':disc('Gold',1.55);disc('Inset',1.25,z=.15,mat=mat('CoinInset',(.85,.32,.01)));box('Mark',.32,1.5,z=.3,r=.12)
 elif key=='Key':disc('Ring',.85,x=-.6,y=.65);disc('Hole',.35,x=-.6,y=.65,z=.2,mat=DARK);box('Stem',.4,1.9,x=-.15,y=-.5);box('Bit',.9,.35,x=.1,y=-1.3)
 bpy.ops.object.light_add(type='AREA',location=(-3,4,7));bpy.context.object.data.energy=450;bpy.context.object.data.size=7
 scene.world.color=(.45,.45,.45);bpy.ops.object.camera_add(location=(0,0,12));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=w*1.05;scene.camera=cam
 scene.render.resolution_x=rx;scene.render.resolution_y=ry;scene.render.resolution_percentage=100;scene.render.filepath=str(OUT/f'{key}.png');bpy.ops.render.render(write_still=True)
 print('UI_READY',key,flush=True)
bpy.app.driver_namespace['pb_ui_render']=render
