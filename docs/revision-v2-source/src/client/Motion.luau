local Run=game:GetService("RunService")
local Root=game.ReplicatedStorage.PaddleBrawl
local Data=require(Root.MotionData)
local M={Rigs={},Gestures={}}
local function pose(seq,t,name)
 if not seq or #seq<2 then return CFrame.identity end
 t=t%math.max(.01,seq[#seq].Time);local a,b=seq[1],seq[#seq]
 for i=2,#seq do if seq[i].Time>=t then a=seq[i-1];b=seq[i];break end end
 local pa=a.Poses[name];local pb=b.Poses[name];if not pa then return CFrame.identity end;if not pb then pb=pa end
 return CFrame.new(table.unpack(pa)):Lerp(CFrame.new(table.unpack(pb)),math.clamp((t-a.Time)/math.max(.001,b.Time-a.Time),0,1))
end
function M.Gesture(ch,kind) if ch then M.Gestures[ch]={At=os.clock(),Kind=kind} end end
function M.Init()
 local function add(ch)
  if not ch:IsA("Model") then return end
  local deadline=os.clock()+5
  while ch.Parent and os.clock()<deadline and (not ch:GetAttribute("PaddleCharacter") or not ch:FindFirstChild("Torso") or not ch:FindFirstChild("Right Arm")) do task.wait(.1) end
  if not ch:GetAttribute("PaddleCharacter") then return end
  local joints={};local bases={};for _,v in ch:GetDescendants() do if v:IsA("Motor6D") and v.Part1 then joints[v.Part1.Name]=v;bases[v]=v.C0 end end;M.Rigs[ch]={Joints=joints,Bases=bases,Phase=0};ch:SetAttribute("AnimationReady",true)
 end
 workspace.ChildAdded:Connect(function(ch) task.spawn(add,ch) end);for _,ch in workspace:GetChildren() do task.spawn(add,ch) end
 Run.PreSimulation:Connect(function(dt)
  local now=os.clock()
  for ch,state in M.Rigs do
   if not ch.Parent then M.Rigs[ch]=nil;M.Gestures[ch]=nil;continue end
   local h=ch:FindFirstChildOfClass("Humanoid");local root=ch:FindFirstChild("HumanoidRootPart");if not h or not root then continue end
   local speed=Vector3.new(root.AssemblyLinearVelocity.X,0,root.AssemblyLinearVelocity.Z).Magnitude
   state.Phase+=dt*math.clamp(speed/12,.5,2.2)
   local gesture=M.Gestures[ch];local age=gesture and now-gesture.At or 10
   local emote=gesture and gesture.Kind=="Emote" and age<6 and speed<2
   local seq=emote and Data['Default Dance'] or speed>24 and Data['Cartoony Run'] or Data.WalkyWalk
   for name,joint in state.Joints do
    local cf=CFrame.identity
    if emote or speed>1 then cf=pose(seq,emote and age or state.Phase,name) else cf=CFrame.Angles(name=="Torso" and math.sin(now*2)*.015 or 0,0,0) end
    if h.FloorMaterial==Enum.Material.Air and not emote then if name=="Right Arm" or name=="Left Arm" then cf=CFrame.Angles(-.45,0,name=="Right Arm" and .3 or -.3) elseif name=="Right Leg" or name=="Left Leg" then cf=CFrame.Angles(.3,0,0) end end
    if gesture and age<.5 and name=="Right Arm" then local a=math.sin(math.clamp(age/.5,0,1)*math.pi);cf=cf*CFrame.Angles(gesture.Kind=="Parry" and -1.2*a or -2.3*a,0,-.5*a) end
    if h.Health<=0 then cf=CFrame.Angles(0,0,name=="Torso" and .8 or .3) end
    joint.Transform=CFrame.identity
    joint.C0=joint.C0:Lerp(state.Bases[joint]*cf,1-math.exp(-18*dt))
   end
  end
 end)
end
return M
