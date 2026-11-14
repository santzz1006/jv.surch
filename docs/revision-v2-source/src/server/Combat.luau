-- Logical projectiles stay server-owned; clients render their replicated positions.
local RS=game:GetService("RunService")
local C=require(game.ReplicatedStorage.PaddleBrawl.Config)
local Combat={Balls={},Serial=0}
local states,send,targets,onKill
local function alive(s) return s and s.Character and s.Character.Parent and s.Character:FindFirstChild("Humanoid") and s.Character.Humanoid.Health>0 end
local function enemy(a,b) return a~=b and alive(b) and a.Match and a.Match==b.Match and (a.Match.Mode=="FFA" or a.Team~=b.Team) end
local function snapshot(s) if not s.Player then return end;send(s.Player,"Weapon",{Slot=s.Slot,Ammo=s.Ammo,Reserve=s.Reserve,Reload=s.ReloadUntil or 0,Ultimate=s.Ultimate,Weapons=s.Weapons}) end
function Combat.Reset(s)
 s.Slot=1;s.Ammo={};s.Reserve={};s.Ultimate=s.Ultimate or 0;s.NextFire=0;s.ReloadUntil=0;s.Charge=nil
 for i,id in s.Weapons do local w=C.Weapons[id];s.Ammo[i]=w.Magazine;s.Reserve[i]=w.Reserve end
 snapshot(s)
end
local function damage(a,b,n,head,freeze,dir)
 if not enemy(a,b) or not a.Match or a.Match.Phase~="Live" then return end
 local h=b.Character.Humanoid;if h.Health<=0 then return end
 local before=h.Health;h:TakeDamage(n);a.Ultimate=math.min(C.UltimateRequired,(a.Ultimate or 0)+C.UltimateHitCharge)
 if freeze then b.FrozenUntil=os.clock()+freeze end
 if dir then b.Character.HumanoidRootPart.AssemblyLinearVelocity=dir*34+Vector3.yAxis*9 end
 send(a.Player,"Hit",{Damage=math.min(before,n),Head=head,Kill=h.Health<=0});snapshot(a)
 if h.Health<=0 and not b.KillCredited then b.KillCredited=true;a.Ultimate=math.min(C.UltimateRequired,a.Ultimate+C.UltimateKillCharge);onKill(a,b);snapshot(a) end
end
local function explode(ball,pos)
 for _,s in targets() do if enemy(ball.Owner,s) then local d=(s.Character.HumanoidRootPart.Position-pos).Magnitude
  if d<=ball.W.Radius then
   local params=RaycastParams.new();params.FilterType=Enum.RaycastFilterType.Exclude;params.FilterDescendantsInstances={ball.Owner.Character,s.Character}
   if not workspace:Raycast(pos,(s.Character.HumanoidRootPart.Position-pos),params) then damage(ball.Owner,s,ball.W.Damage*(1-.5*d/ball.W.Radius),false,ball.W.Freeze) end
  end
 end end
end
local function remove(id,point)
 local b=Combat.Balls[id];if not b then return end
 if point then if b.W.Radius then explode(b,point) end;send(nil,"Impact",{Position=point,Color=b.W.Color,Radius=b.W.Radius or 1},b.Owner.Match) end
 send(nil,"BallEnd",id,b.Owner.Match);Combat.Balls[id]=nil
end
local function launch(s,w,dir)
 if not alive(s) then return end
 local count=0;for _ in Combat.Balls do count+=1 end;if count>=C.MaxProjectiles then return end
 local head=s.Character:FindFirstChild("Head");if not head then return end
 Combat.Serial+=1;local id=Combat.Serial
 local b={Id=id,Owner=s,W=w,Position=head.Position,Velocity=dir*w.Speed,Age=0,Distance=0,Bounces=w.Bounces or 0,Pierce=w.Pierce or 0,Ignore={s.Character}}
 Combat.Balls[id]=b;send(nil,"Ball",{Id=id,Owner=s.Player and s.Player.UserId or 0,Position=b.Position,Velocity=b.Velocity,Color=w.Color,Size=w.BallSize or .75,Super=w.Super},s.Match)
end
function Combat.Fire(s,dir,ultimate)
 if not alive(s) or not s.Match or s.Match.Phase~="Live" or typeof(dir)~="Vector3" then return end
 if dir.X~=dir.X or dir.Y~=dir.Y or dir.Z~=dir.Z or dir.Magnitude<.9 or dir.Magnitude>1.1 then return end
 dir=dir.Unit;local now=os.clock();if now<(s.NextFire or 0) or now<(s.ReloadUntil or 0) then return end
 local baseWeapon=C.Weapons[s.Weapons[s.Slot]];if not baseWeapon then return end;local w=table.clone(baseWeapon);w.Color=s.Team==2 and Color3.fromRGB(255,82,102) or Color3.fromRGB(39,143,255)
 if ultimate then
  if (s.Ultimate or 0)<C.UltimateRequired then return end
  s.Ultimate=0;w={Damage=C.UltimateDamage,Speed=360,Bounces=2,Pierce=5,Color=Color3.fromRGB(255,140,25),BallSize=1.6,Super=true,Interval=1.2}
 elseif s.Slot~=3 then
  if s.Ammo[s.Slot]<=0 then return end
  if w.Charge and (not s.Charge or now-s.Charge<w.Charge) then return end
  s.Ammo[s.Slot]-=1
 end
 s.Charge=nil;s.NextFire=now+w.Interval
 send(nil,"Gesture",{Character=s.Character,Kind=ultimate and "Super" or "Swing"},s.Match)
 if s.Slot==3 and not ultimate then
  for _,b in targets() do if enemy(s,b) then
   local delta=b.Character.HumanoidRootPart.Position-s.Character.Head.Position
   if delta.Magnitude<=w.Range and delta.Unit:Dot(dir)>.45 then
    local params=RaycastParams.new();params.FilterDescendantsInstances={s.Character};local hit=workspace:Raycast(s.Character.Head.Position,delta,params)
    if hit and hit.Instance:IsDescendantOf(b.Character) then damage(s,b,w.Damage,false,nil,dir) end
   end
  end end
 else
  local match=s.Match;task.delay(.07,function() if not alive(s) or s.Match~=match or match.Phase~="Live" then return end;for i=1,w.Pellets or 1 do local d=dir;if w.Spread then d=(CFrame.lookAt(Vector3.zero,dir)*CFrame.Angles(0,(i-2)*w.Spread,0)).LookVector end;launch(s,w,d) end end)
 end
 snapshot(s)
end
function Combat.Action(s,action,value)
 if not alive(s) or not s.Match or s.Match.Phase~="Live" then return end
 local now=os.clock()
 if action=="Slot" and type(value)=="number" and value%1==0 and value>=1 and value<=4 then s.Slot=value;s.ReloadUntil=0;s.Charge=nil;s.ReloadToken=(s.ReloadToken or 0)+1;snapshot(s)
 elseif action=="Charge" then s.Charge=now
 elseif action=="Parry" and now>(s.NextParry or 0) then s.NextParry=now+C.ParryCooldown;s.ParryUntil=now+C.ParryWindow;send(nil,"Gesture",{Character=s.Character,Kind="Parry"},s.Match)
 elseif action=="Reload" then
  local slot=s.Slot;local w=C.Weapons[s.Weapons[slot]]
  if s.Ammo[slot]>=w.Magazine or s.Reserve[slot]<=0 or now<(s.ReloadUntil or 0) then return end
  s.ReloadUntil=now+w.Reload;s.Charge=nil;s.ReloadToken=(s.ReloadToken or 0)+1;local token=s.ReloadToken;snapshot(s)
  task.delay(w.Reload,function() if s.ReloadToken~=token or not alive(s) then return end;local n=math.min(w.Magazine-s.Ammo[slot],s.Reserve[slot]);s.Ammo[slot]+=n;s.Reserve[slot]-=n;s.ReloadUntil=0;snapshot(s) end)
 end
end
function Combat.Clear(match) for id,b in Combat.Balls do if b.Owner.Match==match then remove(id) end end end
function Combat.Init(allStates,emit,getTargets,kill)
 states=allStates;send=emit;targets=getTargets;onKill=kill
 local sync=0
 RS.Heartbeat:Connect(function(dt)
  dt=math.min(dt,.15);sync+=dt
  for id,b in Combat.Balls do
   if not b.Owner.Match or b.Owner.Match.Phase~="Live" then remove(id);continue end
   b.Age+=dt;if b.Age>C.ProjectileLife or b.Distance>(b.W.Range or 1500) then remove(id);continue end
   if b.W.Curve then b.Velocity=CFrame.Angles(0,b.W.Curve*dt,0):VectorToWorldSpace(b.Velocity) end
   if b.W.Homing and b.Age<b.W.Homing then
    local best,dist=nil,70;for _,s in targets() do if enemy(b.Owner,s) then local d=(s.Character.HumanoidRootPart.Position-b.Position).Magnitude;if d<dist then best=s;dist=d end end end
    if best then local goal=(best.Character.HumanoidRootPart.Position-b.Position).Unit;b.Velocity=b.Velocity.Unit:Lerp(goal,math.min(1,dt*b.W.TurnRate)).Unit*b.Velocity.Magnitude end
   end
   local steps=math.max(1,math.ceil(dt/.025));local step=dt/steps
   for _=1,steps do
    if not Combat.Balls[id] then break end
    local params=RaycastParams.new();params.FilterType=Enum.RaycastFilterType.Exclude;params.FilterDescendantsInstances=b.Ignore
    local travel=b.Velocity*step;local hit=workspace:Raycast(b.Position,travel,params);b.Distance+=travel.Magnitude
    if hit then
     local victim=nil;for _,s in targets() do if s.Character and hit.Instance:IsDescendantOf(s.Character) then victim=s;break end end
     if victim then
      if enemy(b.Owner,victim) and (victim.ParryUntil or 0)>os.clock() and victim.Character.HumanoidRootPart.CFrame.LookVector:Dot(-b.Velocity.Unit)>.1 then
       b.Owner=victim;b.Velocity=(victim.Aim or victim.Character.HumanoidRootPart.CFrame.LookVector)*math.min(C.MaxBallSpeed,b.Velocity.Magnitude*C.RicochetGain);b.Ignore={victim.Character};b.Position=hit.Position+b.Velocity.Unit*.6;send(victim.Player,"Notice","DEFESA PERFEITA!")
      elseif enemy(b.Owner,victim) then
       if not b.W.Radius then damage(b.Owner,victim,b.W.Damage*(hit.Instance.Name=="Head" and C.HeadshotMultiplier or 1),hit.Instance.Name=="Head",b.W.Freeze) end
       if b.Pierce>0 then b.Pierce-=1;table.insert(b.Ignore,victim.Character);b.Position=hit.Position+b.Velocity.Unit*.1 else remove(id,hit.Position) end
      else table.insert(b.Ignore,victim.Character);b.Position=hit.Position+b.Velocity.Unit*.1 end
     elseif hit.Instance.Name=="TargetRing" and b.Owner.Match.Training then send(b.Owner.Player,"Hit",{Damage=b.W.Damage,Head=false,Kill=false});send(b.Owner.Player,"Notice","ALVO ATINGIDO • "..b.W.Damage);b.Owner.Ultimate=math.min(100,(b.Owner.Ultimate or 0)+8);snapshot(b.Owner);remove(id,hit.Position)
     elseif b.W.Radius or b.Bounces<=0 then remove(id,hit.Position)
     else b.Bounces-=1;b.Velocity=(b.Velocity-2*b.Velocity:Dot(hit.Normal)*hit.Normal).Unit*math.min(C.MaxBallSpeed,b.Velocity.Magnitude*C.RicochetGain);b.Position=hit.Position+hit.Normal*.08;send(nil,"Impact",{Position=hit.Position,Color=b.W.Color,Radius=.6},b.Owner.Match) end
    else b.Position+=travel end
   end
   if sync>.07 and Combat.Balls[id] then send(nil,"BallMove",{Id=id,Position=b.Position,Velocity=b.Velocity},b.Owner.Match) end
  end
  if sync>.07 then sync=0 end
 end)
end
return Combat
