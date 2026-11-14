from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];p=r/'src/shared/Assets.luau';s=p.read_text();ids=json.loads((r/'assets/maps/manifest-v3.json').read_text());s=s[:s.index('Thumbnails={')]+'Thumbnails={'+','.join(k.removesuffix('Image')+'="rbxassetid://'+v+'"' for k,v in ids.items() if k.endswith('Image'))+'}}\n';p.write_text(s,encoding='utf-8')
print('Updated ten map thumbnails')
