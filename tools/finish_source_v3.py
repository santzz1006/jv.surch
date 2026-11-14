from pathlib import Path
import json
r=Path(__file__).resolve().parents[1]
p=r/'src/shared/Assets.luau';s=p.read_text();ids=json.loads((r/'assets/ui/v3/manifest.json').read_text());suffix=s[s.index('},Thumbnails'):]
p.write_text('return {Images={'+','.join(k+'="rbxassetid://'+v+'"' for k,v in ids.items())+suffix,encoding='utf-8')
p=r/'src/client/Main.client.luau';s=p.read_text(encoding='utf-8')
s=s.replace('local previousSlot=1','local previousSlot=1')
s=s.replace('HUD.Health.Text=math.ceil(h.Health).." / "..h.MaxHealth;HUD.HealthSprite.ImageColor3=h.Health<50 and Color3.fromRGB(255,140,140) or HUD.TeamColor','HUD.Health.Text=tostring(math.ceil(h.Health));HUD.HealthSprite.ImageColor3=Color3.new(1,1,1)')
s=s.replace('if data.Reload>0 then','if data.Reload>0 and os.clock()-reloadAt>reloadLength-.1 then')
s=s.replace('HUD.QuestPanel.Visible=not enabled;', 'HUD.QuestPanel.Visible=not HUD.MenuOpen and not HUD.Vote.Visible;HUD.LobbyBar.Visible=not playing and not HUD.MenuOpen;HUD.MenuBlur.Size=HUD.MenuOpen and 8 or 0;')
s=s.replace('aiming and C.AimFOV or C.BaseFOV','aiming and C.AimFOV or HUD.Settings.FOV')
s=s.replace('if not active() or view.Pending then return end;', 'if not active() or view.Pending or os.clock()-reloadAt<reloadLength then return end;')
p.write_text(s,encoding='utf-8')
p=r/'src/server/Main.server.luau';s=p.read_text(encoding='utf-8')
s=s.replace('local function profile(p) emit(p,"Profile",Profiles.Public(p)) end','local function profile(p) local d=Profiles.Public(p);if d then p:SetAttribute("PaddleElo",d.Elo);p:SetAttribute("PaddleLevel",1+math.floor(d.XP/150)) end;emit(p,"Profile",d) end')
s=s.replace('Kills=s.Kills or 0}', 'Kills=s.Kills or 0,Health=s.Character and s.Character:FindFirstChild("Humanoid") and s.Character.Humanoid.Health or 0,Level=s.Player and s.Player:GetAttribute("PaddleLevel") or 1}')
start=s.index(' local art=Root:FindFirstChild("PaddleArt")');end=s.index(' h.Died:Connect',start)
s=s[:start]+''' local assets=Root:FindFirstChild("WeaponAssets");local art=assets and (assets:FindFirstChild(s.Weapons[s.Slot or 1]) or assets:FindFirstChild("Classic"))
 if art then
  local copy=art:Clone();copy.Name="EquippedPaddle";copy:ScaleTo(.62);copy:PivotTo(ch['Right Arm'].CFrame*CFrame.new(0,-.95,-.15)*CFrame.Angles(math.pi/2,0,0));copy.Parent=ch
  for _,p in copy:GetDescendants()do if p:IsA("BasePart")then p.Anchored=false;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.Massless=true;if p.Name=="FrontRubber" then p.Color=s.Team==2 and Color3.fromRGB(255,48,75) or Color3.fromRGB(8,123,255) end;local w=Instance.new("WeldConstraint");w.Part0=ch['Right Arm'];w.Part1=p;w.Parent=p end end
 end
''' +s[end:]
p.write_text(s,encoding='utf-8')
p=r/'src/server/Maps.luau';s=p.read_text(encoding='utf-8');s=s.replace('if v.shape=="Ball" then p.Shape=Enum.PartType.Ball end','if v.shape=="Ball" then p.Shape=Enum.PartType.Ball elseif v.shape=="Octagon" then p.Shape=Enum.PartType.Cylinder;p.Size=Vector3.new(v.size[2],v.size[1],v.size[3]);p.CFrame*=CFrame.Angles(0,0,math.pi/2) end')
start=s.index(' sign("Welcome"');end=s.index(' local spawn=',start)
s=s[:start]+''' sign("Welcome","PADDLE\\nBRAWL",Vector3.new(0,39,-44.8),Vector3.new(44,11,.1),Color3.new(1,1,1))
 sign("Modes","MODOS DE JOGO",Vector3.new(-44,25,-5.8),Vector3.new(28,4,.1),Color3.new(1,1,1))
 sign("Shop","LOJA",Vector3.new(44,25,-5.8),Vector3.new(28,4,.1),Color3.new(1,1,1))
 for i,mode in {"1v1","2v2","3v3","FFA"} do local x=-44+((i-1)%2==0 and -7 or 7);local y=i<=2 and 17 or 8;sign("Queue"..mode,mode,Vector3.new(x,y,-5.8),Vector3.new(12,6,.1),Color3.new(1,1,1),mode)end
 sign("Training","CAMPO DE\\nTREINO",Vector3.new(-53,8,19.6),Vector3.new(21,8,.1),Color3.new(1,1,1),"Train")
 sign("Season","PASSE DE\\nTEMPORADA",Vector3.new(53,8,19.6),Vector3.new(21,8,.1),Color3.new(1,1,1),"Season")
''' +s[end:];p.write_text(s,encoding='utf-8')
print('Sources integrated')
