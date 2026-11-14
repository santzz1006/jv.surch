from pathlib import Path
import zipfile,json
r=Path(__file__).resolve().parents[1]
lines=['-- Restores source modules into the existing Paddle Brawl place. Does not publish.','local function folder(parent,name) local f=parent:FindFirstChild(name) or Instance.new("Folder");f.Name=name;f.Parent=parent;return f end','local shared=folder(game.ReplicatedStorage,"PaddleBrawl")','local server=folder(game.ServerScriptService,"PaddleBrawl")','local client=folder(game.StarterPlayer.StarterPlayerScripts,"PaddleBrawl")']
for p in sorted((r/'src').rglob('*.luau')):
 group=p.parent.name;root={'shared':'shared','server':'server','client':'client'}[group]
 cls='LocalScript' if p.name.endswith('.client.luau') else 'Script' if p.name.endswith('.server.luau') else 'ModuleScript'
 name=p.name.replace('.client','').replace('.server','').removesuffix('.luau');source=p.read_text(encoding='utf-8')
 lines.append(f'do local p={root};local s=p:FindFirstChild({json.dumps(name)}) or Instance.new("{cls}");s.Name={json.dumps(name)};s.Source=[====[{source}]====];s.Parent=p end')
lines.append('print("Paddle Brawl source revision restored")')
(r/'tools/InstallSources.luau').write_text('\n'.join(lines),encoding='utf-8')
out=r/'deliverables';out.mkdir(exist_ok=True)
path=out/'Paddle-Brawl-V3-fontes-e-assets.zip'
with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=5)as z:
 for directory in ['src','assets','tools','docs']:
  for p in (r/directory).rglob('*'):
   if not p.is_file()or p.suffix in ['.blend1','.pyc']or 'revision-v2-source' in p.parts:continue
   if directory=='docs' and p.suffix=='.json':continue
   z.write(p,p.relative_to(r))
print(str(path));print(path.stat().st_size)
