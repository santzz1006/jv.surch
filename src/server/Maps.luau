local Data=require(game.ReplicatedStorage.PaddleBrawl.MapData)
local M={};M.Data=Data
local function color(s) return Color3.fromHex(s) end
function M.Build(index,origin,parent)
 local d=type(index)=="table" and index or Data[index] or Data[4];local model=Instance.new("Model");model.Name=d.Id
 local template=game.ServerStorage:FindFirstChild("PaddleMapArt")
 local art=template and template:FindFirstChild(d.Id)
 if art then
  local copy=art:Clone();copy:PivotTo(CFrame.new(origin)*copy:GetPivot());copy.Parent=model
  for _,p in copy:GetDescendants() do if p:IsA("BasePart") then p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false end end
 end
 for i,v in d.Parts do
  local p=Instance.new(v.shape=="Wedge" and "WedgePart" or "Part")
  p.Name=v.name;p.Size=Vector3.new(table.unpack(v.size));p.CFrame=CFrame.new(origin+Vector3.new(table.unpack(v.pos)))*CFrame.Angles(0,math.rad(v.yaw),0)
  p.Color=color(v.color);p.Material=Enum.Material.SmoothPlastic;p.Anchored=true;p.TopSurface=Enum.SurfaceType.Smooth;p.BottomSurface=Enum.SurfaceType.Smooth
  if v.shape=="Ball" then p.Shape=Enum.PartType.Ball elseif v.shape=="Octagon" then p.Shape=Enum.PartType.Cylinder;p.Size=Vector3.new(v.size[2],v.size[1],v.size[3]);p.CFrame*=CFrame.Angles(0,0,math.pi/2) end
  p.CanCollide=not v.decor;p.CanTouch=false;p.CanQuery=not v.decor;p.Transparency=art and 1 or 0;p.Parent=model
 end
 model.Parent=parent;return model,d
end
function M.Lobby()
 local d=require(game.ReplicatedStorage.PaddleBrawl.LobbyData)
 local root=M.Build(d,Vector3.zero,workspace);root.Name="PaddleLobby"
 local function sign(name,label,pos,size,color,action)
  local p=Instance.new("Part");p.Name=name;p.Size=size;p.Position=pos;p.Transparency=1;p.Anchored=true;p.CanCollide=false;p.CanQuery=false;p.Parent=root
  local gui=Instance.new("SurfaceGui");gui.Face=Enum.NormalId.Back;gui.CanvasSize=Vector2.new(1000,350);gui.Parent=p
  local text=Instance.new("TextLabel");text.BackgroundTransparency=1;text.Size=UDim2.fromScale(1,1);text.Font=Enum.Font.FredokaOne;text.Text=label;text.TextScaled=true;text.TextColor3=color;text.Parent=gui
  if action then local prompt=Instance.new("ProximityPrompt");prompt.Name="PaddlePortal";prompt.ActionText="ENTRAR";prompt.ObjectText=label;prompt.MaxActivationDistance=16;prompt.RequiresLineOfSight=false;prompt.HoldDuration=0;prompt:SetAttribute("PaddleAction",action);prompt.Parent=p end
 end
 sign("Welcome","PADDLE\nBRAWL",Vector3.new(0,39,-44.8),Vector3.new(44,11,.1),Color3.new(1,1,1))
 sign("Modes","MODOS DE JOGO",Vector3.new(-44,25,-5.8),Vector3.new(28,4,.1),Color3.new(1,1,1))
 sign("Shop","LOJA",Vector3.new(44,10,-4),Vector3.new(28,4,.1),Color3.new(1,1,1),"Shop")
 for i,mode in {"1v1","2v2","3v3","FFA"} do local x=-44+((i-1)%2==0 and -7 or 7);local y=i<=2 and 17 or 8;sign("Queue"..mode,mode,Vector3.new(x,y,-5.8),Vector3.new(12,6,.1),Color3.new(1,1,1),mode)end
 sign("Training","CAMPO DE\nTREINO",Vector3.new(-53,8,19.6),Vector3.new(21,8,.1),Color3.new(1,1,1),"Train")
 sign("Season","PASSE DE\nTEMPORADA",Vector3.new(53,8,19.6),Vector3.new(21,8,.1),Color3.new(1,1,1),"Season")
 local spawn=Instance.new("SpawnLocation");spawn.Name="LobbySpawn";spawn.Size=Vector3.new(8,1,8);spawn.Position=Vector3.new(0,1,36);spawn.Anchored=true;spawn.Transparency=1;spawn.CanCollide=false;spawn.Duration=0;spawn.Neutral=true;spawn.Parent=root
 return root
end
return M
