local Players=game:GetService("Players")
local Run=game:GetService("RunService")
local UIS=game:GetService("UserInputService")
local Tween=game:GetService("TweenService")
local Root=game.ReplicatedStorage:WaitForChild("PaddleBrawl")
local C=require(Root.Config);local HUD=require(script.Parent.HUD);local Motion=require(script.Parent.Motion)
local player=Players.LocalPlayer;local Event=Root.Event;local cam=workspace.CurrentCamera
local playing=false;local holding=false;local aiming=false;local lastFire=0;local lastSwing=-10;local reloadAt=-10;local reloadLength=1;local inspectAt=-10;local switchAt=-10;local superAt=-10
local bullets={};local vm;local paddle;local arm;local arm2;local serveBall;local previousSlot=1
local effects=Instance.new("Folder");effects.Name="PaddleClientEffects";effects.Parent=cam
local function request(action,value,extra)
 if action=="Ultimate" then if not playing or HUD.MenuOpen then return end;value=cam.CFrame.LookVector;superAt=os.clock() end
 Event:FireServer(action,value,extra)
end
HUD.Init(request);Motion.Init();pcall(function()game:GetService("StarterGui"):SetCoreGuiEnabled(Enum.CoreGuiType.PlayerList,false)end)
local function makePart(name,size,color,parent)
 local p=Instance.new("Part");p.Name=name;p.Size=size;p.Color=color;p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.CastShadow=false;p.Material=Enum.Material.SmoothPlastic;p.Parent=parent;return p
end
local function buildViewmodel()
 if vm then vm:Destroy() end
 vm=Instance.new("Model");vm.Name="PaddleViewmodel";vm.Parent=cam
 local skin=player.Character and player.Character:FindFirstChild("Right Arm") and player.Character['Right Arm'].Color or Color3.fromRGB(255,205,155)
 arm=makePart("R6 Right Arm",Vector3.new(.48,1.4,.48),skin,vm);arm2=makePart("R6 Left Arm",Vector3.new(.48,1.4,.48),skin,vm)
 serveBall=makePart("ReadyBall",Vector3.one*.4,Color3.fromRGB(246,250,255),vm);serveBall.Shape=Enum.PartType.Ball
 local source=Root:FindFirstChild("PaddleArt")
 if source then paddle=source:Clone();paddle.Name="Paddle";paddle.Parent=vm;paddle:ScaleTo(.42);for _,p in paddle:GetDescendants() do if p:IsA("BasePart") then p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.CanTouch=false;p.CastShadow=false end end
 else paddle=Instance.new("Model");paddle.Parent=vm;local h=makePart("PaddleHead",Vector3.new(1.65,1.8,.16),Color3.fromRGB(120,80,240),paddle);h.Shape=Enum.PartType.Ball;makePart("Grip",Vector3.new(.35,1.2,.28),Color3.fromRGB(35,42,65),paddle).Position=Vector3.new(0,-1.25,0) end
end
buildViewmodel()
local function updateSkin()
 if not paddle then return end;local d=HUD.Profile;local color=d and d.Skin~="Default" and C.Cosmetics[d.Skin].Color or HUD.TeamColor
 for _,p in paddle:GetDescendants() do if p:IsA("BasePart") and (p.Name:find("Purple") or p.Name=="PaddleHead") then p.Color=color end end
end
player.CharacterAdded:Connect(function(ch)
 local h=ch:WaitForChild("Humanoid");local root=ch:WaitForChild("HumanoidRootPart");cam.CameraSubject=h;cam.CameraType=Enum.CameraType.Custom;HUD.Death.Text="";buildViewmodel();updateSkin()
 local function health()HUD.Health.Text=math.ceil(h.Health).." / "..h.MaxHealth;HUD.HealthSprite.ImageColor3=h.Health<50 and Color3.fromRGB(255,140,140) or HUD.TeamColor end
 h.HealthChanged:Connect(health);health();task.defer(function()Run.RenderStepped:Wait();if ch==player.Character then cam.CFrame=CFrame.lookAt(ch.Head.Position+Vector3.new(0,.2,0),ch.Head.Position+root.CFrame.LookVector*20) end end)
end)
local function impact(data)
 local p=makePart("Impact",Vector3.one*.2,data.Color,effects);p.Shape=Enum.PartType.Ball;p.Material=Enum.Material.Neon;p.Position=data.Position
 Tween:Create(p,TweenInfo.new(.22),{Size=Vector3.one*math.clamp(data.Radius*2,.6,14),Transparency=1}):Play();game.Debris:AddItem(p,.25)
end
Event.OnClientEvent:Connect(function(kind,data)
 if kind=="Profile" then HUD.UpdateProfile(data);updateSkin()
 elseif kind=="Lobby" then playing=false;holding=false;HUD.SetMatch(false)
 elseif kind=="Enter" then playing=true;HUD.SetTeam(data.Team);HUD.SetMatch(true);updateSkin()
 elseif kind=="Match" then HUD.UpdateMatch(data)
 elseif kind=="Queue" then HUD.Toast(data and "BUSCANDO "..data.." • aguardando jogadores" or "Busca cancelada")
 elseif kind=="Notice" then HUD.Toast(data)
 elseif kind=="Weapon" then
  if data.Reload>0 then reloadAt=os.clock();reloadLength=C.Weapons[data.Weapons[data.Slot]].Reload end
  if data.Slot~=previousSlot then switchAt=os.clock();previousSlot=data.Slot end;HUD.UpdateWeapon(data);updateSkin()
 elseif kind=="Gesture" then Motion.Gesture(data.Character,data.Kind);if data.Character==player.Character then if os.clock()-lastSwing>.15 then lastSwing=os.clock() end;if data.Kind=="Super" then superAt=os.clock() end end
 elseif kind=="Hit" then HUD.Hit.Visible=true;HUD.Hit.Text=data.Kill and "✕" or "+";HUD.Hit.TextColor3=data.Head and Color3.fromRGB(255,96,110) or Color3.fromRGB(255,225,99);task.delay(.12,function()HUD.Hit.Visible=false end)
 elseif kind=="Death" then holding=false;HUD.Death.Text=data.Respawn>0 and "ELIMINADO • voltando em "..data.Respawn.."s" or "ELIMINADO • aguardando a próxima rodada"
 elseif kind=="Result" then HUD.ShowResult(data)
 elseif kind=="Feed" then HUD.Feed.Text=data.Killer.."  →  "..data.Victim;task.delay(5,function()HUD.Feed.Text=""end)
 elseif kind=="Ball" then
  if data.Owner==player.UserId and arm2 then lastSwing=os.clock() end
  local p=makePart("Ball_"..data.Id,Vector3.one*data.Size,data.Color,effects);p.Shape=Enum.PartType.Ball;p.Material=Enum.Material.Neon;p.Position=data.Position
  local a=Instance.new("Attachment");a.Position=Vector3.new(0,.18,0);a.Parent=p;local b=Instance.new("Attachment");b.Position=Vector3.new(0,-.18,0);b.Parent=p
  local trail=Instance.new("Trail");trail.Attachment0=a;trail.Attachment1=b;trail.Color=ColorSequence.new(data.Color);trail.Lifetime=data.Super and .35 or .14;trail.LightEmission=1;trail.FaceCamera=true;trail.Parent=p
  bullets[data.Id]={Part=p,Position=data.Position,Velocity=data.Velocity,At=os.clock()}
 elseif kind=="BallMove" then local b=bullets[data.Id];if b then b.Position=data.Position;b.Velocity=data.Velocity;b.At=os.clock() end
 elseif kind=="BallEnd" then local b=bullets[data];if b then b.Part:Destroy();bullets[data]=nil end
 elseif kind=="Impact" then impact(data)
 end
end)
local context=game.ReplicatedStorage:WaitForChild("Inputs"):WaitForChild("PaddleCombat")
local function active() return playing and not HUD.MenuOpen and HUD.Match and HUD.Match.Phase=="Live" and player.Character and player.Character:FindFirstChild("Humanoid") and player.Character.Humanoid.Health>0 end
local function fire()
 if not active() then return end;local w=C.Weapons[HUD.Weapons[HUD.Slot]];local now=os.clock();if now-lastFire<w.Interval then return end;lastFire=now;request("Fire",cam.CFrame.LookVector);lastSwing=now
end
for _,a in context:GetChildren() do if a:IsA("InputAction") then
 a.Pressed:Connect(function()
  local n=a.Name
  if n=="Menu" then HUD.ToggleMenu();return end
  if not active() then return end
  if n=="Fire" then holding=true;local w=C.Weapons[HUD.Weapons[HUD.Slot]];if w.Charge then request("Charge") else fire() end
  elseif n=="Parry" then aiming=true;request("Parry")
  elseif n=="Sprint" or n=="Crouch" then request(n,true)
  elseif n=="Inspect" then inspectAt=os.clock()
  elseif n=="CycleNext" then request("Slot",HUD.Slot%4+1)
  elseif n=="CyclePrev" then request("Slot",(HUD.Slot+2)%4+1)
  elseif n:sub(1,4)=="Slot" then request("Slot",tonumber(n:sub(5)))
  elseif n=="Emote" then request("Emote")
  else request(n) end
 end)
 a.Released:Connect(function()
  if a.Name=="Fire" then if holding and C.Weapons[HUD.Weapons[HUD.Slot]].Charge then fire() end;holding=false
  elseif a.Name=="Parry" then aiming=false
  elseif a.Name=="Sprint" or a.Name=="Crouch" then request(a.Name,false) end
 end)
 if HUD.Mobile[a.Name] then local binding=a:FindFirstChild("Touch");if binding then binding.UIButton=HUD.Mobile[a.Name] end end
end end
local fpsTime,frames=0,0;local sway=Vector2.zero;local elapsed=0
Run:BindToRenderStep("PaddlePresentation",Enum.RenderPriority.Camera.Value+1,function(dt)
 local now=os.clock();elapsed+=dt;frames+=1;fpsTime+=dt
 if fpsTime>=1 then HUD.Stats.Text=math.floor(frames/fpsTime).." FPS";fpsTime=0;frames=0 end
 local enabled=playing and not HUD.MenuOpen and not HUD.Vote.Visible and not HUD.Result.Visible
 player.CameraMode=enabled and Enum.CameraMode.LockFirstPerson or Enum.CameraMode.Classic
 UIS.MouseIconEnabled=not enabled;if not enabled then UIS.MouseBehavior=Enum.MouseBehavior.Default end
 HUD.Cross.Visible=enabled;HUD.QuestPanel.Visible=not enabled;HUD.Menu.Visible=HUD.MenuOpen
 local char=player.Character;local h=char and char:FindFirstChildOfClass("Humanoid");local speed=h and h.MoveDirection.Magnitude or 0
 local targetFov=aiming and C.AimFOV or C.BaseFOV;local superAge=now-superAt;if superAge<.7 then targetFov+=math.sin(superAge/.7*math.pi)*14 end
 cam.FieldOfView+=(targetFov-cam.FieldOfView)*(1-math.exp(-14*dt))
 if holding and active() then local w=C.Weapons[HUD.Weapons[HUD.Slot]];if not w.Charge then fire() end end
 local mouse=UIS:GetMouseDelta();sway=sway:Lerp(Vector2.new(math.clamp(mouse.X,-20,20),math.clamp(mouse.Y,-20,20))*.002,1-math.exp(-12*dt))
 local swingAge=now-lastSwing;local swing=swingAge<.035 and -math.sin(swingAge/.035*math.pi/2)*.4 or swingAge<.095 and -.4+((swingAge-.035)/.06)*1.4 or swingAge<.21 and (1-(swingAge-.095)/.115)^2 or 0
 local reloadAge=now-reloadAt;local reload=reloadAge<reloadLength and math.sin(reloadAge/reloadLength*math.pi) or 0
 local inspectAge=now-inspectAt;local inspect=inspectAge<1.5 and math.sin(inspectAge/1.5*math.pi) or 0
 local switchAge=now-switchAt;local switch=switchAge<.3 and math.sin(switchAge/.3*math.pi) or 0
 local base=cam.CFrame*CFrame.new(1.15+math.sin(elapsed*10)*.035*speed-sway.X,-1.05+math.abs(math.sin(elapsed*10))*.045*speed-sway.Y-reload*.65-switch*.8,-2.35)*CFrame.Angles(-.15+swing*1.1+reload*.5,-swing*.45+inspect*.6,.15+inspect*.7)
 if vm then
  vm.Parent=enabled and h and h.Health>0 and cam or nil
  arm.CFrame=base*CFrame.new(.25,-.48,.65)*CFrame.Angles(math.rad(-65),0,0)
  arm2.CFrame=base*CFrame.new(-1.1,-.55+math.max(0,swing)*.3,.4)*CFrame.Angles(math.rad(-65)-swing*.35,0,-.12)
  serveBall.CFrame=base*CFrame.new(-1.1,.05+math.max(0,swing)*.8,-.35);serveBall.Transparency=(swingAge>.07 and swingAge<.2) and 1 or 0
  paddle:PivotTo(base*CFrame.new(-swing*.7,.1+swing*.15,-.45-swing*.45)*CFrame.Angles(math.pi/2+swing*.5,0,-swing*.65))
 end
 for id,b in bullets do local age=now-b.At;if age>5 then b.Part:Destroy();bullets[id]=nil else local target=b.Position+b.Velocity*math.min(age,.13);b.Part.Position=b.Part.Position:Lerp(target,1-math.exp(-35*dt)) end end
end)
task.delay(1,function()request("Ready")end)
print("[PADDLE BRAWL] Client ready — individual PNG HUD, R6 motion and IAS controls")
