local Players=game:GetService("Players")
local Run=game:GetService("RunService")
local UIS=game:GetService("UserInputService")
local Tween=game:GetService("TweenService")
local Root=game.ReplicatedStorage:WaitForChild("PaddleBrawl")
local C=require(Root.Config);local HUD=require(script.Parent.HUD);local Motion=require(script.Parent.Motion)
local player=Players.LocalPlayer;local Event=Root.Event;local cam=workspace.CurrentCamera
local playing=false;local holding=false;local aiming=false;local lastFire=0;local lastSwing=-10;local reloadAt=-10;local reloadLength=1;local inspectAt=-10;local switchAt=-10;local superAt=-10
local chargeAt;local bullets={};local previousSlot=1
local effects=Instance.new("Folder");effects.Name="PaddleClientEffects";effects.Parent=cam
local Pool=require(script.Parent.EffectPool);local ballPool=Pool.new(effects,256);local impactPool=Pool.new(effects,48)
local function request(action,value,extra)
 if action=="Ultimate" then if not playing or HUD.MenuOpen or (HUD.Ultimate or 0)<100 then return end;value=cam.CFrame.LookVector end
 Event:FireServer(action,value,extra)
end
HUD.Init(request);Motion.Init();pcall(function()game:GetService("StarterGui"):SetCoreGuiEnabled(Enum.CoreGuiType.PlayerList,false)end)
local function makePart(name,size,color,parent)
 local p=Instance.new("Part");p.Name=name;p.Size=size;p.Color=color;p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.CastShadow=false;p.Material=Enum.Material.SmoothPlastic;p.Parent=parent;return p
end
local Viewmodel=require(script.Parent.ViewmodelController)
local Audio=require(script.Parent.AudioController)
local view=Viewmodel.new(cam)
local function updateSkin()
 local d=HUD.Profile;local color=d and d.Skin~="Default" and C.Cosmetics[d.Skin].Color or HUD.TeamColor
 view:SetColor(color)
end
local boundCharacter
local function onCharacter(ch)
 if boundCharacter==ch then return end;boundCharacter=ch
 local h=ch:WaitForChild("Humanoid");local root=ch:WaitForChild("HumanoidRootPart");local head=ch:WaitForChild("Head",10);if not head or ch~=player.Character then return end;cam.CameraSubject=h;cam.CameraType=Enum.CameraType.Custom;HUD.Death.Text="";view:SetCharacter(ch);updateSkin()
 local function health()HUD.UpdateHealth(h.Health,h.MaxHealth) end
 h.HealthChanged:Connect(health);health();task.defer(function()Run.RenderStepped:Wait();if ch==player.Character and head.Parent then cam.CFrame=CFrame.lookAt(head.Position+Vector3.new(0,.2,0),head.Position+root.CFrame.LookVector*20) end end)
end
player.CharacterAdded:Connect(onCharacter);if player.Character then task.spawn(onCharacter,player.Character)end
local function impact(data)
 local p=impactPool:Acquire(.2,data.Color);if not p then return end;p.Trail.Enabled=false;p.Position=data.Position
 Tween:Create(p,TweenInfo.new(.22),{Size=Vector3.one*math.clamp(data.Radius*2,.6,14),Transparency=1}):Play();task.delay(.25,function()impactPool:Release(p)end)
end
Event.OnClientEvent:Connect(function(kind,data)
 if kind=="Profile" then HUD.UpdateProfile(data);updateSkin()
 elseif kind=="Lobby" then playing=false;holding=false;HUD.SetMatch(false)
 elseif kind=="Enter" then playing=true;HUD.SetTeam(data.Team);HUD.SetMatch(true);updateSkin()
 elseif kind=="Match" then HUD.UpdateMatch(data)
 elseif kind=="Queue" then HUD.Toast(data and "BUSCANDO "..data.." • aguardando jogadores" or "Busca cancelada")
 elseif kind=="Notice" then HUD.Toast(data)
 elseif kind=="OpenPage" then HUD.MenuOpen=true;HUD.ShowPage(data)
 elseif kind=="Pong" then HUD.Ping=math.floor((os.clock()-data)*1000+.5)
 elseif kind=="Weapon" then
  if data.Reload>0 and os.clock()-reloadAt>reloadLength-.1 then reloadAt=os.clock();reloadLength=C.Weapons[data.Weapons[data.Slot]].Reload;view:Play("Reload",{Duration=reloadLength});Audio.Play("Reload") elseif data.Reload<=0 then reloadAt=-10 end
  if data.Slot~=previousSlot or view.Weapon~=data.Weapons[data.Slot] then switchAt=os.clock();previousSlot=data.Slot;view:Equip(data.Weapons[data.Slot]) end;HUD.UpdateWeapon(data);updateSkin()
 elseif kind=="Gesture" then Motion.Gesture(data.Character,data.Kind);if data.Character==player.Character then if os.clock()-lastSwing>.15 then lastSwing=os.clock();view:Play(data.Kind=="Super" and "Super" or data.Kind=="Parry" and "Parry" or "Swing",{Weapon=HUD.Weapons[HUD.Slot]}) end;if data.Kind=="Super" then superAt=os.clock() end end
 elseif kind=="Hit" then Audio.Play("Hit",data.Head and 1.2 or 1);HUD.Hit.Visible=true;HUD.Hit.Text=data.Kill and "✕" or "+";HUD.Hit.TextColor3=data.Head and Color3.fromRGB(255,96,110) or Color3.fromRGB(255,225,99);task.delay(.12,function()HUD.Hit.Visible=false end)
 elseif kind=="Death" then holding=false;HUD.Death.Text=data.Respawn>0 and "ELIMINADO • voltando em "..data.Respawn.."s" or "ELIMINADO • aguardando a próxima rodada"
 elseif kind=="Result" then HUD.ShowResult(data)
 elseif kind=="Feed" then HUD.Feed.Text=data.Killer.."  →  "..data.Victim;task.delay(5,function()HUD.Feed.Text=""end)
 elseif kind=="Ball" then
  
  local p=ballPool:Acquire(data.Size,data.Color);if not p then return end;p.Position=data.Position;p.Trail.Lifetime=data.Super and .35 or .14
  bullets[data.Id]={Part=p,Position=data.Position,Velocity=data.Velocity,At=os.clock()}
 elseif kind=="BallMove" then local b=bullets[data.Id];if b then b.Position=data.Position;b.Velocity=data.Velocity;b.At=os.clock() end
 elseif kind=="BallEnd" then local b=bullets[data];if b then ballPool:Release(b.Part);bullets[data]=nil end
 elseif kind=="Impact" then impact(data)
 end
end)
local context=game.ReplicatedStorage:WaitForChild("Inputs"):WaitForChild("PaddleCombat")
local function active() return playing and not HUD.MenuOpen and HUD.Match and HUD.Match.Phase=="Live" and player.Character and player.Character:FindFirstChild("Humanoid") and player.Character.Humanoid.Health>0 end
local function fire()
 if not active() or view.Pending or os.clock()-reloadAt<reloadLength then return end;if HUD.Slot~=3 and HUD.AmmoCounts and HUD.AmmoCounts[HUD.Slot]<=0 then return end;local w=C.Weapons[HUD.Weapons[HUD.Slot]];local now=os.clock();if now-lastFire<w.Interval then return end;lastFire=now;request("Fire",cam.CFrame.LookVector);lastSwing=now;Audio.Play("Serve",HUD.Weapons[HUD.Slot]=="RallyRapid" and 1.3 or .95+math.random()*.1);view:Play("Swing",{Weapon=HUD.Weapons[HUD.Slot]})
end
for _,a in context:GetChildren() do if a:IsA("InputAction") then
 a.Pressed:Connect(function()
  local n=a.Name
  if n=="Menu" then HUD.ToggleMenu();return end
  if not active() then return end
  if n=="Fire" then holding=true;local w=C.Weapons[HUD.Weapons[HUD.Slot]];if w.Charge then chargeAt=os.clock();request("Charge") else fire() end
  elseif n=="Parry" then aiming=true;view:Play("Parry");request("Parry")
  elseif n=="Sprint" or n=="Crouch" then request(n,true)
  elseif n=="Inspect" then inspectAt=os.clock();view:Play("Inspect")
  elseif n=="CycleNext" then request("Slot",HUD.Slot%4+1)
  elseif n=="CyclePrev" then request("Slot",(HUD.Slot+2)%4+1)
  elseif n:sub(1,4)=="Slot" then request("Slot",tonumber(n:sub(5)))
  elseif n=="Emote" then request("Emote")
  else request(n) end
 end)
 a.Released:Connect(function()
  if a.Name=="Fire" then if holding and C.Weapons[HUD.Weapons[HUD.Slot]].Charge then fire() end;holding=false;chargeAt=nil
  elseif a.Name=="Parry" then aiming=false
  elseif a.Name=="Sprint" or a.Name=="Crouch" then request(a.Name,false) end
 end)
 if HUD.Mobile[a.Name] then local binding=a:FindFirstChild("Touch");if binding then binding.UIButton=HUD.Mobile[a.Name] end end
end end
local fpsTime,frames=0,0;local sway=Vector2.zero;local elapsed=0
Run:BindToRenderStep("PaddlePresentation",Enum.RenderPriority.Camera.Value+1,function(dt)
 local now=os.clock();elapsed+=dt;frames+=1;fpsTime+=dt
 if fpsTime>=1 then HUD.Stats.Text=(HUD.Ping and HUD.Ping.." ms • " or "")..math.floor(frames/fpsTime).." FPS";fpsTime=0;frames=0 end
 local enabled=playing and not HUD.MenuOpen and not HUD.Vote.Visible and not HUD.Result.Visible
 player.CameraMode=enabled and Enum.CameraMode.LockFirstPerson or Enum.CameraMode.Classic
 UIS.MouseIconEnabled=not enabled;if not enabled then UIS.MouseBehavior=Enum.MouseBehavior.Default end
 HUD.Cross.Visible=enabled;HUD.QuestPanel.Visible=not HUD.MenuOpen and not HUD.Vote.Visible and not (UIS.TouchEnabled and playing);HUD.LobbyBar.Visible=not playing and not HUD.MenuOpen;HUD.MenuBlur.Size=HUD.MenuOpen and 8 or 0;HUD.Menu.Visible=HUD.MenuOpen;if HUD.TouchLayer then HUD.TouchLayer.Visible=enabled end
 local char=player.Character;local h=char and char:FindFirstChildOfClass("Humanoid");local speed=h and h.MoveDirection.Magnitude or 0
 local targetFov=aiming and C.AimFOV or HUD.Settings.FOV;local superAge=now-superAt;if superAge<.7 then targetFov+=math.sin(superAge/.7*math.pi)*14 end
 cam.FieldOfView+=(targetFov-cam.FieldOfView)*(1-math.exp(-14*dt))
 if holding and active() then local w=C.Weapons[HUD.Weapons[HUD.Slot]];if not w.Charge then fire() end end
 local mouse=UIS:GetMouseDelta();sway=sway:Lerp(Vector2.new(math.clamp(mouse.X,-20,20),math.clamp(mouse.Y,-20,20))*.002,1-math.exp(-12*dt))
 local root=char and char:FindFirstChild("HumanoidRootPart")
 local velocity=root and Vector3.new(root.AssemblyLinearVelocity.X,0,root.AssemblyLinearVelocity.Z).Magnitude or 0
 local anim=view:Update(dt,{Visible=enabled and h and h.Health>0,Speed=velocity,Sprint=h and h.WalkSpeed>25,Air=h and h.FloorMaterial==Enum.Material.Air,Crouch=h and h.WalkSpeed<14,MouseDelta=mouse,Aim=aiming,Charge=chargeAt and math.clamp((now-chargeAt)/.65,0,1)})
 local spread=anim.Kind=="Swing" and math.sin(anim.Progress*math.pi)*12 or aiming and -5 or 0
 HUD.Cross.Size=UDim2.fromOffset(36+spread,36+spread);HUD.Cross.Position=UDim2.fromOffset(720-(36+spread)/2,450-(36+spread)/2)
 for id,b in bullets do local age=now-b.At;if age>5 then ballPool:Release(b.Part);bullets[id]=nil else local target=b.Position+b.Velocity*math.min(age,.13);b.Part.Position=b.Part.Position:Lerp(target,1-math.exp(-35*dt)) end end
end)
task.delay(1,function()request("Ready")end)
task.spawn(function()while script.Parent do task.wait(3);request("Ping",os.clock())end end)
print("[PADDLE BRAWL] Client ready — individual PNG HUD, R6 motion and IAS controls")
