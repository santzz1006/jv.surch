local C=require(game.ReplicatedStorage.PaddleBrawl.Config)
local Movement={}
-- A short server displacement budget tolerates replication bursts, slides and knockback.
-- Corrections never ban a player or change progression.
function Movement.Validate(s,now)
 local root=s.Character and s.Character:FindFirstChild('HumanoidRootPart');if not root then return end
 if not s.Match or now-(s.SpawnAt or now)<2 then s.MoveCheckAt=now;s.MoveCheckPos=root.Position;s.MoveBudget=10;return end
 if now-(s.MoveCheckAt or now)<.2 then return end
 local dt=math.min(1,now-s.MoveCheckAt);local pos=root.Position;local delta=pos-(s.MoveCheckPos or pos)
 local allowed=math.max(C.SlideSpeed,C.SprintSpeed+C.BunnyHopBonus)+10
 s.MoveBudget=math.min(12,(s.MoveBudget or 12)+dt*allowed)-Vector3.new(delta.X,0,delta.Z).Magnitude
 if s.MoveBudget<0 or pos.Y>s.Match.Origin.Y+65 then
  local safe=s.LastSafe or s.Match.Origin+Vector3.new(0,4,-28)
  root.CFrame=CFrame.new(safe)*root.CFrame.Rotation;root.AssemblyLinearVelocity=Vector3.zero;s.MoveBudget=8;pos=safe
 else s.LastSafe=pos end
 s.MoveCheckAt=now;s.MoveCheckPos=pos
end
return Movement
