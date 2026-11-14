import json,struct,pathlib,sys
root=pathlib.Path(__file__).resolve().parents[1];out={}
folder=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else root/'assets/models'
for path in folder.glob('*.glb'):
 b=path.read_bytes();j=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]]);items=[]
 for node in j['nodes']:
  if 'mesh' not in node:continue
  mesh=j['meshes'][node['mesh']];acc=[j['accessors'][p['attributes']['POSITION']] for p in mesh['primitives']]
  lo=[min(a['min'][i] for a in acc) for i in range(3)];hi=[max(a['max'][i] for a in acc) for i in range(3)]
  rgb=j['materials'][mesh['primitives'][0]['material']]['pbrMetallicRoughness']['baseColorFactor'][:3]
  rgb=[v*12.92 if v<=.0031308 else 1.055*v**(1/2.4)-.055 for v in rgb]
  color=''.join(f'{max(0,min(255,round(v*255))):02x}' for v in rgb)
  items.append({'mesh':mesh['name'],'name':node['name'],'translation':node.get('translation',[0,0,0]),'rotation':node.get('rotation',[0,0,0,1]),'scale':node.get('scale',[1,1,1]),'center':[(a+b)/2 for a,b in zip(lo,hi)],'size':[b-a for a,b in zip(lo,hi)],'color':color})
 out[path.stem]=items
(folder/'import-metadata.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
