import bpy,math,json
from pathlib import Path
from mathutils import Vector
ROOT=Path('C:/Users/neila/OneDrive/Desktop/roblox')
S=.28
def material(hexcolor):
 name='PB_'+hexcolor[1:];m=bpy.data.materials.get(name)
 if m:return m
 m=bpy.data.materials.new(name);m.use_nodes=True;v=[int(hexcolor[i:i+2],16)/255 for i in (1,3,5)];v=[x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in v]
 node=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');node.inputs['Base Color'].default_value=(*v,1);node.inputs['Roughness'].default_value=.77;m.diffuse_color=(*v,1);return m
def boxmesh(name,size,pos,col,shape='Box',yaw=0,bevel=.07):
 if shape=='Octagon':bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=.5,depth=1,location=pos,rotation=(0,0,math.pi/8))
 elif shape=='Ball':bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.5,location=pos)
 elif shape=='Wedge':
  mesh=bpy.data.meshes.new(name);mesh.from_pydata([(-.5,-.5,-.5),(.5,-.5,-.5),(-.5,.5,-.5),(.5,.5,-.5),(-.5,.5,.5),(.5,.5,.5)],[],[(0,2,3,1),(2,4,5,3),(0,1,5,4),(0,4,2),(1,3,5)]);mesh.update();ob=bpy.data.objects.new(name,mesh);bpy.context.collection.objects.link(ob);bpy.context.view_layer.objects.active=ob;ob.select_set(True);ob.location=pos
 else:bpy.ops.mesh.primitive_cube_add(size=1,location=pos)
 ob=bpy.context.object;ob.name=name;ob.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.rotation_euler.z=math.radians(-yaw);ob.data.materials.append(material(col))
 if shape!='Ball' and bevel:
  mod=ob.modifiers.new('Soft cartoon edges','BEVEL');mod.width=min(bevel,min(size)*.12);mod.segments=2;bpy.context.view_layer.objects.active=ob;bpy.ops.object.modifier_apply(modifier=mod.name)
 return ob
def clear():
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
def light_scene():
 scene=bpy.context.scene
 try:scene.render.engine='CYCLES'
 except TypeError:pass
 scene.cycles.samples=16;scene.cycles.use_denoising=True
 scene.world.color=(.32,.32,.32)
 bpy.ops.object.light_add(type='AREA',location=(5,-5,22));bpy.context.object.data.energy=3800;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=15
 bpy.ops.object.light_add(type='SUN',location=(0,0,12));bpy.context.object.rotation_euler=(.35,-.4,-.3);bpy.context.object.data.energy=2
 bpy.ops.object.camera_add(location=(22,-26,27));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=32;scene.camera=cam
 scene.render.resolution_x=640;scene.render.resolution_y=420;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.film_transparent=False
def export_mesh(path):
 bpy.ops.object.select_all(action='DESELECT')
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH':ob.select_set(True)
 bpy.ops.export_scene.gltf(filepath=str(path),export_format='GLB',use_selection=True,export_yup=True)
 bpy.ops.export_scene.fbx(filepath=str(path.with_suffix('.fbx')),use_selection=True,object_types={'MESH'},apply_unit_scale=True,axis_forward='-Z',axis_up='Y',add_leaf_bones=False)
def build_map(key,thumbnail=True):
 clear();data=json.loads((ROOT/'assets/maps'/f'{key}.json').read_text(encoding='utf-8'));bpy.context.scene.unit_settings.system='METRIC';bpy.context.scene.unit_settings.scale_length=1
 for p in data['Parts']:
  x,y,z=p['pos'];w,h,d=p['size'];boxmesh(p['name'],(w*S,d*S,h*S),(x*S,-z*S,y*S),p['color'],p['shape'],p['yaw'],.06)
 # Join by material to keep import counts low while preserving flat colours.
 meshes=[o for o in bpy.context.scene.objects if o.type=='MESH']
 for m in set(o.data.materials[0] for o in meshes):
  group=[o for o in bpy.context.scene.objects if o.type=='MESH' and o.data.materials[0]==m];bpy.ops.object.select_all(action='DESELECT')
  for o in group:o.select_set(True)
  bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();group[0].name=key+'_'+m.name
 export_mesh(ROOT/'assets/models'/f'{key}.glb');light_scene();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/models'/f'{key}.blend'))
 if thumbnail:bpy.context.scene.render.filepath=str(ROOT/'assets/thumbnails'/f'{key}.png');bpy.ops.render.render(write_still=True)
 print('MAP_READY',key,flush=True)
def paddle():
 clear();bpy.context.scene.unit_settings.system='METRIC'
 # Head lies in XY, handle extends -Y. Thickness Z. Roblox height target 3.4 studs.
 def disc(name,rad,depth,z,col):
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=rad,depth=depth,location=(0,.18,z));ob=bpy.context.object;ob.name=name;ob.scale.y=1.12;ob.data.materials.append(material(col));mod=ob.modifiers.new('Rounded rim','BEVEL');mod.width=.018;mod.segments=3;bpy.ops.object.modifier_apply(modifier=mod.name)
 disc('MapleRim',.27,.052,0,'#e6cda5');disc('PurpleRubber',.258,.014,.032,'#8260ed');disc('OrangeRubber',.258,.014,-.032,'#ffb541')
 boxmesh('Handle',(.12,.43,.08),(0,-.31,0),'#263a57',bevel=.025);boxmesh('GripBand',(.13,.055,.085),(0,-.45,0),'#5ce8e2',bevel=.01)
 for i in range(5):boxmesh('GripRidge',(.125,.012,.084),(0,-.38+i*.045,0),'#52627a',bevel=.004)
 export_mesh(ROOT/'assets/models/Paddle.glb');light_scene();bpy.context.scene.camera.location=(1.5,-2.2,2);bpy.context.scene.camera.rotation_euler=(Vector((0,0,0))-bpy.context.scene.camera.location).to_track_quat('-Z','Y').to_euler();bpy.context.scene.camera.data.ortho_scale=1.4
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'assets/models/Paddle.blend'));bpy.context.scene.render.filepath=str(ROOT/'assets/thumbnails/Paddle.png');bpy.ops.render.render(write_still=True)
 print('PADDLE_READY',flush=True)
bpy.app.driver_namespace['pb_build_map']=build_map;bpy.app.driver_namespace['pb_paddle']=paddle
print('ASSET_BUILDERS_READY',flush=True)
