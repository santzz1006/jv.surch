from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
p=r/'src/server/Main.server.luau';s=p.read_text(encoding='utf-8');s=s.replace('local Combat=require(script.Parent.Combat)','local Combat=require(script.Parent.Combat)\nlocal WeaponService=require(script.Parent.WeaponService)')
start=s.index(' local assets=Root:FindFirstChild("WeaponAssets")');end=s.index(' h.Died:Connect',start);s=s[:start]+' WeaponService.Equip(s)\n'+s[end:]
s=s.replace('then Combat.Action(s,action,value)','then Combat.Action(s,action,value);if action=="Slot" then WeaponService.Equip(s) end')
p.write_text(s,encoding='utf-8')
p=r/'src/shared/Assets.luau';s=p.read_text();ids=json.loads((r/'assets/models/v3/manifest.json').read_text());icons={k.removesuffix('Image'):v for k,v in ids.items() if k.endswith('Image')};s=s.replace('Images={','Images={'+','.join(k+'="rbxassetid://'+v+'"' for k,v in icons.items())+',',1);p.write_text(s,encoding='utf-8')
p=r/'src/client/Main.client.luau';s=p.read_text(encoding='utf-8');s=s.replace('local bullets={};','local chargeAt;local bullets={};')
s=s.replace('if w.Charge then request("Charge")','if w.Charge then chargeAt=os.clock();request("Charge")')
s=s.replace('end;holding=false','end;holding=false;chargeAt=nil')
s=s.replace('MouseDelta=mouse,Aim=aiming','MouseDelta=mouse,Aim=aiming,Charge=chargeAt and math.clamp((now-chargeAt)/.65,0,1)')
p.write_text(s,encoding='utf-8')
print('Weapon service and distinct icons wired')
