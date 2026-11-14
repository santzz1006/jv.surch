import bpy,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('C:/Users/neila/OneDrive/Desktop/roblox');OUT=ROOT/'assets/models/v3';OUT.mkdir(exist_ok=True)
THUMBS=ROOT/'assets/weapon-icons';THUMBS.mkdir(exist_ok=True)
def material(name,hexcolor,rough=.6):
 m=bpy.data.materials.get('P3_'+name) or bpy.data.materials.new('P3_'+name);m.use_nodes=True
 rgb=[int(hexcolor[i:i+2],16)/255 for i in (0,2,4)];rgb=[v/12.92 if v<.04045 else ((v+.055)/1.055)**2.4 for v in rgb]
 node=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');node.inputs['Base Color'].default_value=(*rgb,1);node.inputs['Roughness'].default_value=rough;m.diffuse_color=(*rgb,1);return m
def finish(obj,name,mat,bevel=.009):
 obj.name=name;obj.data.name=name;obj.data.materials.append(mat)
 if bevel:
  mod=obj.modifiers.new('Soft edge','BEVEL');mod.width=bevel;mod.segments=4;bpy.context.view_layer.objects.active=obj;bpy.ops.object.modifier_apply(modifier=mod.name)
 for p in obj.data.polygons:p.use_smooth=True
 try:mod=obj.modifiers.new('Weighted normals','WEIGHTED_NORMAL');bpy.ops.object.modifier_apply(modifier=mod.name)
 except Exception:pass
 return obj
def oval(name,width,height,depth,pos,mat,vertices=96):
 # Blender X/Z is paddle face; Y is thickness. Root is the grip center.
 bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=1,depth=1,location=pos,rotation=(math.pi/2,0,0));o=bpy.context.object;o.scale=(width/2,height/2,depth);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,mat)
def box(name,size,pos,mat,bevel=.009):
 bpy.ops.mesh.primitive_cube_add(size=1,location=pos);o=bpy.context.object;o.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return finish(o,name,mat,bevel)
def handle(name,width,length,depth,mat):
 # Flared, short wooden grip. Deliberately no long sci-fi ridges.
 z0,z1=-length*.52,length*.48;xs=[-width*.52,width*.52,-width*.43,width*.43]
 verts=[(x,y,z) for z,left,right in [(z0,xs[0],xs[1]),(z1,xs[2],xs[3])] for y in [-depth/2,depth/2] for x in [left,right]]
 faces=[(0,2,3,1),(4,5,7,6),(0,1,5,4),(2,6,7,3),(0,4,6,2),(1,3,7,5)]
 mesh=bpy.data.meshes.new(name);mesh.from_pydata(verts,[],faces);mesh.update();obj=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(obj);bpy.context.view_layer.objects.active=obj;obj.select_set(True);return finish(obj,name,mat,.012)
def build(key):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
 rubber=material('Rubber','e81940',.82);rim=material('Rim','17213a',.43);wood=material('Maple','e9bb7e',.62);cream=material('WoodStripe','fff1cf');metal=material('Steel','a2d8ef',.35)
 configs={'Classic':(.58,.66,.065,96),'LongSmash':(.47,.78,.075,96),'TripleServe':(.68,.64,.085,48),'RallyRapid':(.49,.58,.055,96),'SpinMaster':(.61,.63,.065,96),'Homing':(.56,.65,.08,64),'MegaSmash':(.76,.78,.105,64),'Melee':(.56,.62,.10,32)}
 w,h,t,verts=configs[key];center=.14+h/2
 oval('OuterRim',w,h,t,(0,0,center),rim,verts)
 oval('MaplePly',w-.018,h-.018,t+.004,(0,0,center),wood,verts)
 oval('RimLip',w-.012,h-.012,t+.008,(0,0,center),rim,verts)
 oval('FrontRubber',w-.04,h-.04,.014,(0,-t/2-.009,center),rubber,verts)
 oval('BackRubber',w-.04,h-.04,.014,(0,t/2+.009,center),rim,verts)
 handle('WoodHandle',.145,.31,.09,wood)
 box('HandleInlay',(.025,.004,.22),(0,-.049,-.015),cream,.001)
 box('HandleButt',(.15,.102,.025),(0,0,-.154),rim,.008)
 box('Neck',(.12,.085,.09),(0,0,.16),wood,.01)
 if key=='LongSmash':
  for sign in [-1,1]:box('PrecisionRail'+str(sign),(.035,.035,.45),(sign*w*.36,-t*.65,center),metal,.007)
 elif key=='TripleServe':
  for x in [-.14,0,.14]:oval('ServePort'+str(x),.08,.08,.008,(x,-t*.75,center-.12),rim,32)
 elif key=='RallyRapid':
  for i in range(3):box('SpeedMark'+str(i),(.18-i*.035,.006,.022),(.06,-t*.72,center+.04+i*.06),cream,.006)
 elif key=='SpinMaster':
  for i in range(3):oval('SpinGroove'+str(i),w-.12-i*.09,h-.12-i*.09,.005,(0,-t*.75-i*.001,center),rim if i%2==0 else rubber,96)
 elif key=='Homing':oval('TargetCircle',.18,.18,.018,(0,-t*.75,center),metal,64);oval('TargetCore',.07,.07,.024,(0,-t*.84,center),rubber,48)
 elif key=='MegaSmash':
  for sign in [-1,1]:box('PowerGuard'+str(sign),(.09,.12,.26),(sign*w*.42,0,center-.13),metal,.018)
 elif key=='Melee':
  for x in [-.18,0,.18]:box('ImpactBand'+str(x),(.04,.012,h*.65),(x,-t*.7,center),metal,.009)
 scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1
 bpy.ops.object.select_all(action='DESELECT')
 for o in scene.objects:
  if o.type=='MESH':o.select_set(True)
 bpy.ops.export_scene.gltf(filepath=str(OUT/f'{key}.glb'),export_format='GLB',use_selection=True,export_yup=True)
 bpy.ops.export_scene.fbx(filepath=str(OUT/f'{key}.fbx'),use_selection=True,object_types={'MESH'},axis_forward='-Z',axis_up='Y',add_leaf_bones=False)
 # Original transparent weapon icon, using the actual mesh.
 scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True;scene.render.film_transparent=True;scene.world.color=(.4,.4,.4)
 bpy.ops.object.light_add(type='AREA',location=(-1.7,-3,4));bpy.context.object.data.energy=170;bpy.context.object.data.size=4
 bpy.ops.object.camera_add(location=(.72,-2.4,1.3));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.33))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.14;scene.camera=cam
 scene.render.resolution_x=512;scene.render.resolution_y=512;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.filepath=str(THUMBS/f'{key}.png')
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT/f'{key}.blend'));bpy.ops.render.render(write_still=True)
 print('PADDLE_V3_READY',key,flush=True)
bpy.app.driver_namespace['pb_paddle_v3']=build
