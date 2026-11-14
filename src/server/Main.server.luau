local editorPreview=workspace:FindFirstChild("EditorPreview");if editorPreview then editorPreview:Destroy() end
local Players=game:GetService("Players")
local Run=game:GetService("RunService")
local Root=game.ReplicatedStorage:WaitForChild("PaddleBrawl")
local C=require(Root.Config)
local Profiles=require(script.Parent.Profiles)
local Maps=require(script.Parent.Maps)
local Combat=require(script.Parent.Combat)
local WeaponService=require(script.Parent.WeaponService)
local MovementService=require(script.Parent.MovementService)
local TeamService=require(script.Parent.TeamService)
local VotingService=require(script.Parent.VotingService)
local Event=Root.Event
local States,Matches,Queues={}, {}, {['1v1']={},['2v2']={},['3v3']={},FFA={}}
local Bots={};local Templates={};local nextMatch=0
Players.CharacterAutoLoads=false
local arenaFolder=Instance.new("Folder");arenaFolder.Name="PaddleArenas";arenaFolder.Parent=workspace
Maps.Lobby()
local function emit(p,kind,data,match)
 if p then if p.Parent==Players then Event:FireClient(p,kind,data) end
 elseif match then for _,s in match.Members do if s.Player then Event:FireClient(s.Player,kind,data) end end
 elseif kind=="Gesture" then Event:FireAllClients(kind,data) end
end
local function allTargets() local t={};for _,s in States do table.insert(t,s) end;for _,s in Bots do table.insert(t,s) end;return t end
local function profile(p) local d=Profiles.Public(p);if d then p:SetAttribute("PaddleElo",d.Elo);p:SetAttribute("PaddleLevel",1+math.floor(d.XP/150)) end;emit(p,"Profile",d) end
local function removeQueue(p) for _,q in Queues do for i=#q,1,-1 do if q[i]==p then table.remove(q,i) end end end end
local function notify(p,text) emit(p,"Notice",text) end
local spawnCharacter,roundEnd,finishMatch,lobby
local function statePacket(m)
 local roster={};for _,s in m.Members do table.insert(roster,{Name=s.Player and s.Player.DisplayName or "Sparring",UserId=s.Player and s.Player.UserId or 0,Team=s.Team,Alive=s.Character and s.Character:FindFirstChild("Humanoid") and s.Character.Humanoid.Health>0,Kills=s.Kills or 0,Health=s.Character and s.Character:FindFirstChild("Humanoid") and s.Character.Humanoid.Health or 0,Level=s.Player and s.Player:GetAttribute("PaddleLevel") or 1}) end
 local votes={};local voters={};for p,n in m.Votes or {} do votes[n]=(votes[n] or 0)+1;table.insert(voters,{UserId=p.UserId,Choice=n}) end
 return {Id=m.Id,Mode=m.Mode,Phase=m.Phase,Time=math.max(0,math.ceil((m.Deadline or 0)-os.clock())),Scores=m.Scores,Map=m.MapName,Choices=m.Choices,Votes=votes,Voters=voters,Roster=roster,Training=m.Training,Sparring=m.Sparring==true}
end
local function broadcast(m) emit(nil,"Match",statePacket(m),m) end
local function makeTemplate(p)
 local desc=Instance.new("HumanoidDescription")
 if p and p.UserId>0 then local ok,d=pcall(function() return Players:GetHumanoidDescriptionFromUserIdAsync(p.UserId) end);if ok then desc=d end end
 desc.Head=0;desc.Torso=0;desc.LeftArm=0;desc.RightArm=0;desc.LeftLeg=0;desc.RightLeg=0
 local ok,model=pcall(function() return Players:CreateHumanoidModelFromDescriptionAsync(desc,Enum.HumanoidRigType.R6) end)
 if not ok then model=game.ServerStorage:WaitForChild("PaddleR6"):Clone() end
 for _,x in model:GetDescendants() do if x:IsA("BaseScript") then x:Destroy() end end
 model.Archivable=true;return model
end
local function died(s)
 local m=s.Match;if not m or m.Phase~="Live" then return end
 emit(s.Player,"Death",{Respawn=(m.Training or m.Mode=="FFA") and C.RespawnSeconds or 0})
 if m.Training or m.Mode=="FFA" then task.delay(C.RespawnSeconds,function() if s.Match==m and m.Phase=="Live" then spawnCharacter(s,m.Origin+Vector3.new(math.random(-22,22),4,s.Team==1 and -26 or 26));Combat.Reset(s) end end)
 else task.delay(.15,function()
  if m.Phase~="Live" then return end
  local living={0,0};for _,member in m.Members do if member.Character and member.Character.Humanoid.Health>0 then living[member.Team]+=1 end end
  if living[1]==0 or living[2]==0 then roundEnd(m,living[1]==0 and (living[2]==0 and 0 or 2) or 1) end
 end) end
end
spawnCharacter=function(s,pos)
 if s.Spawning then return end;s.Spawning=true
 local template=s.Player and Templates[s.Player] or game.ServerStorage.PaddleR6
 local ch=template:Clone();ch.Name=s.Player and s.Player.Name or "Sparring";ch:SetAttribute("PaddleCharacter",true);ch:SetAttribute("Side",s.Team or 1)
 local h=ch:FindFirstChildOfClass("Humanoid");h.MaxHealth=C.Health;h.Health=C.Health;h.WalkSpeed=C.WalkSpeed;h.UseJumpPower=true;h.JumpPower=C.JumpPower;h.BreakJointsOnDeath=false;h.DisplayDistanceType=Enum.HumanoidDisplayDistanceType.None
 ch.PrimaryPart=ch:FindFirstChild("HumanoidRootPart");ch:PivotTo(CFrame.new(pos)*CFrame.Angles(0,s.Match and s.Team==1 and math.pi or 0,0));local old=s.Character;s.Character=ch;s.KillCredited=false;s.LastPosition=pos;s.LastSafe=pos;s.SpawnAt=os.clock();s.ReloadToken=(s.ReloadToken or 0)+1
 if s.Player then s.Player.Character=ch end;ch.Parent=workspace;if old then old:Destroy() end
 local root=ch:FindFirstChild("HumanoidRootPart");if root then pcall(function() root:SetNetworkOwner(s.Player) end) end
 WeaponService.Equip(s)
 h.Died:Connect(function() died(s) end)
 h.StateChanged:Connect(function(_,new)
  if new==Enum.HumanoidStateType.Landed then s.LastLand=os.clock()
  elseif new==Enum.HumanoidStateType.Jumping then s.Hop=(s.LastLand and os.clock()-s.LastLand<.16) and math.min((s.Hop or 0)+C.BunnyHopBonus,C.BunnyHopCap-C.SprintSpeed) or 0 end
 end)
 s.Spawning=false
end
lobby=function(s)
 s.Match=nil;s.Team=1;s.Ultimate=0;s.Sprint=false;s.Crouch=false;s.SlideUntil=0
 if s.Player and s.Player.Parent then spawnCharacter(s,Vector3.new(math.random(-10,10),4,36));emit(s.Player,"Lobby",true);profile(s.Player) end
end
finishMatch=function(m,winner)
 if m.Phase=="Finished" then return end;m.Phase="Finished";m.Deadline=os.clock()+5;Combat.Clear(m)
 local rating={0,0};local counts={0,0};for _,s in m.Members do if s.Player and Profiles.Data[s.Player] then rating[s.Team]=(rating[s.Team] or 0)+Profiles.Data[s.Player].Elo;counts[s.Team]=(counts[s.Team] or 0)+1 end end
 for _,s in m.Members do if s.Player then
  local d=Profiles.Data[s.Player];local won=m.Mode=="FFA" and winner==s or m.Mode~="FFA" and winner==s.Team
  if d and not m.Training then
   Profiles.Add(s.Player,"duels",1);d.Coins+=won and 70 or 30;d.XP+=won and 100 or 45
   if won then d.Wins+=1;Profiles.Add(s.Player,"wins",1) end
   if m.Mode=="1v1" then local opponent=3-s.Team;local expected=1/(1+10^(((rating[opponent]/math.max(1,counts[opponent]))-d.Elo)/400));d.Elo=math.max(0,d.Elo+math.floor(C.EloK*((winner==0 and .5 or won and 1 or 0)-expected)+.5)) end
   table.insert(d.History,1,{Mode=m.Mode,Map=m.MapName,Won=won,Draw=winner==0,Kills=s.Kills or 0,Elo=d.Elo,At=os.time()});while #d.History>20 do table.remove(d.History)end
  end
  emit(s.Player,"Result",{Won=won,Draw=winner==0,Training=m.Training});profile(s.Player)
 end end
 broadcast(m)
 task.delay(5,function()
  for _,s in m.Members do if s.Match==m then if s.Player then lobby(s) else if s.Character then s.Character:Destroy() end;Bots[s]=nil end end end
  if m.Model then m.Model:Destroy() end;Matches[m.Id]=nil
 end)
end
local function startRound(m)
 if not Matches[m.Id] then return end
 m.Phase="Countdown";m.Deadline=os.clock()+C.RoundCountdown;Combat.Clear(m)
 for i,s in m.Members do
  spawnCharacter(s,m.Origin+TeamService.SpawnOffset(m,i,s));Combat.Reset(s);s.Character.HumanoidRootPart.Anchored=true
 end
 broadcast(m)
 task.delay(C.RoundCountdown,function()
  if m.Phase~="Countdown" then return end;m.Phase="Live";m.Deadline=os.clock()+(m.Training and 3600 or m.Mode=="FFA" and C.FFASeconds or C.RoundSeconds)
  for _,s in m.Members do if s.Character then s.Character.HumanoidRootPart.Anchored=false end end;broadcast(m)
 end)
end
roundEnd=function(m,winner)
 if m.Phase~="Live" then return end
 m.Phase="RoundEnd";m.Deadline=os.clock()+3;Combat.Clear(m)
 if winner>0 then m.Scores[winner]+=1 end
 emit(nil,"Notice",winner==0 and "RODADA EMPATADA" or (winner==1 and "AZUL" or "VERMELHO").." VENCEU A RODADA",m);broadcast(m)
 if m.Scores[1]>=C.RoundsToWin or m.Scores[2]>=C.RoundsToWin then finishMatch(m,winner) else task.delay(3,function() if m.Phase=="RoundEnd" then startRound(m) end end) end
end
local function createMatch(players,mode,training)
 local slot;for i=1,C.MaxMatches do local occupied=false;for _,m in Matches do if m.ArenaSlot==i then occupied=true end end;if not occupied then slot=i;break end end
 if not slot then for _,p in players do notify(p,"Todas as arenas estão ocupadas. Tente novamente.") end;return end
 nextMatch+=1;local m={Id=nextMatch,ArenaSlot=slot,Mode=mode,Training=training,Members={},Scores={0,0},Phase="Vote",Votes={},Choices={},Origin=Vector3.new(slot*C.ArenaSpacing,30,0),Deadline=os.clock()+C.VoteSeconds};Matches[m.Id]=m
 local choices={};for i=1,10 do table.insert(choices,i) end
 for _=1,3 do local i=math.random(#choices);table.insert(m.Choices,table.remove(choices,i)) end
 for i,p in players do local s=States[p];removeQueue(p);s.Match=m;s.Team=mode=="FFA" and i or (i%2==1 and 1 or 2);s.Kills=0;s.Ultimate=0;table.insert(m.Members,s);emit(p,"Enter",{Team=s.Team,Training=training}) end
 if training then local bot={Team=2,Match=m,Weapons={"Classic","RallyRapid","Melee","Explosive"},Ultimate=0,Kills=0};Bots[bot]=bot;table.insert(m.Members,bot) end
 if training then m.Choices={11};m.Deadline=os.clock()+.3 end
 broadcast(m)
 task.delay(training and .3 or C.VoteSeconds,function()
  if m.Phase~="Vote" then return end
  local selected=training and 11 or VotingService.Winner(m)
  local model,data=Maps.Build(selected,m.Origin,arenaFolder);m.Model=model;m.MapName=data.Name;m.KillY=m.Origin.Y+data.KillY;startRound(m)
 end)
end
Combat.Init(States,emit,allTargets,function(a,b)
 a.Kills=(a.Kills or 0)+1
 if a.Player and not a.Match.Training then local d=Profiles.Data[a.Player];if d then d.Kills+=1;d.Coins+=5;d.XP+=15;Profiles.Add(a.Player,"kills",1);profile(a.Player) end end
 emit(nil,"Feed",{Killer=a.Player and a.Player.DisplayName or "Sparring",Victim=b.Player and b.Player.DisplayName or "Sparring"},a.Match)
 if a.Match.Mode=="FFA" and a.Kills>=C.FFATarget then finishMatch(a.Match,a) end
end)
local function setup(p)
 local s={Player=p,Team=1,Weapons={"Classic","RallyRapid","Melee","Explosive"},Tokens=C.RemoteBurst,TokenAt=os.clock(),Ultimate=0};States[p]=s
 Templates[p]=makeTemplate(p);if not p.Parent then return end;spawnCharacter(s,Vector3.new(0,4,36));emit(p,"Lobby",true)
 local d=Profiles.Load(p);if not d or not p.Parent then return end;s.Weapons={d.Primary,d.Secondary,"Melee",d.Utility};profile(p);Combat.Reset(s)
end
Players.PlayerAdded:Connect(function(p) task.spawn(setup,p) end);for _,p in Players:GetPlayers() do task.spawn(setup,p) end
Players.PlayerRemoving:Connect(function(p)
 removeQueue(p);local s=States[p];if s and s.Match then local m=s.Match;for i=#m.Members,1,-1 do if m.Members[i]==s then table.remove(m.Members,i) end end;if m.Training then finishMatch(m,0) elseif m.Mode~="FFA" then finishMatch(m,3-s.Team) end end
 if Templates[p] then Templates[p]:Destroy();Templates[p]=nil end;States[p]=nil
end)
Event.OnServerEvent:Connect(function(p,action,value,extra)
 local s=States[p];if not s or type(action)~="string" then return end
 local now=os.clock();s.Tokens=math.min(C.RemoteBurst,s.Tokens+(now-s.TokenAt)*C.RemoteRate);s.TokenAt=now;if s.Tokens<1 then return end;s.Tokens-=1
 if action=="Ping" and type(value)=="number" and value==value and math.abs(value)<1e12 then emit(p,"Pong",value)
 elseif action=="Ready" then profile(p);if s.Match then emit(p,"Enter",{Team=s.Team,Training=s.Match.Training});emit(p,"Match",statePacket(s.Match)) else emit(p,"Lobby",true) end
 elseif action=="Fire" or action=="Ultimate" then if typeof(value)=="Vector3" and value.Magnitude>.9 and value.Magnitude<1.1 then s.Aim=value.Unit end;Combat.Fire(s,value,action=="Ultimate")
 elseif action=="Reload" or action=="Slot" or action=="Charge" or action=="Parry" then Combat.Action(s,action,value);if action=="Slot" then WeaponService.Equip(s) end
 elseif action=="Sprint" or action=="Crouch" then
  if type(value)~="boolean" then return end
  if action=="Sprint" then s.Sprint=value else s.Crouch=value;if value and s.Sprint and now>(s.NextSlide or 0) and s.Character and s.Character.Humanoid.FloorMaterial~=Enum.Material.Air then s.NextSlide=now+C.SlideCooldown;s.SlideUntil=now+C.SlideDuration;s.SlideDirection=s.Character.Humanoid.MoveDirection end end
 elseif action=="Vote" then local m=s.Match;if m and VotingService.Cast(m,p,value) then broadcast(m) end
 elseif action=="Queue" and not s.Match and C.Modes[value] then removeQueue(p);table.insert(Queues[value],p);emit(p,"Queue",value)
 elseif action=="CancelQueue" then removeQueue(p);emit(p,"Queue",false)
 elseif action=="Train" and not s.Match then createMatch({p},"1v1",true)
 elseif action=="ToggleSparring" and s.Match and s.Match.Training then s.Match.Sparring=not s.Match.Sparring;broadcast(s.Match)
 elseif action=="Leave" then
  removeQueue(p);local m=s.Match;if m then if m.Training then finishMatch(m,0) elseif m.Mode=="FFA" then for i=#m.Members,1,-1 do if m.Members[i]==s then table.remove(m.Members,i) end end;lobby(s);if #m.Members<2 then finishMatch(m,m.Members[1] or 0) end else notify(p,"Ao sair, seu time perde o duelo.");finishMatch(m,3-s.Team) end end
 elseif action=="Loadout" and not s.Match and type(value)=="string" and C.Weapons[value] then
  local d=Profiles.Data[p];if d then if extra=="Primary" and table.find(C.WeaponOrder,value) then d.Primary=value elseif extra=="Secondary" and table.find(C.WeaponOrder,value) then d.Secondary=value elseif extra=="Utility" and (value=="Freeze" or value=="Explosive") then d.Utility=value end;s.Weapons={d.Primary,d.Secondary,"Melee",d.Utility};Combat.Reset(s);profile(p) end
 elseif action=="Skin" and type(value)=="string" then local d=Profiles.Data[p];if d and d.Owned[value] then d.Skin=value;profile(p) end
 elseif action=="Buy" or action=="Crate" or action=="Claim" or action=="Season" then
  if now<(s.NextPurchase or 0) then return end;s.NextPurchase=now+.5
  local ok,msg;if action=="Buy" then ok,msg=Profiles.Buy(p,value) elseif action=="Crate" then ok,msg=Profiles.Crate(p) elseif action=="Claim" then ok,msg=Profiles.Claim(p,value) else ok,msg=Profiles.SeasonClaim(p,value) end
  notify(p,msg);profile(p)
 elseif action=="Emote" then emit(nil,"Gesture",{Character=s.Character,Kind="Emote"})
 end
end)
game:GetService("ProximityPromptService").PromptTriggered:Connect(function(prompt,p)
 local s=States[p];local action=prompt:GetAttribute("PaddleAction");if not s or s.Match or not action then return end
 if action=="Train" then createMatch({p},"1v1",true) elseif action=="Shop" or action=="Season" then emit(p,"OpenPage",action) elseif Queues[action] then removeQueue(p);table.insert(Queues[action],p);emit(p,"Queue",action) end
end)
local acc=0;local botAcc=0
Run.Heartbeat:Connect(function(dt)
 local now=os.clock();acc+=dt;botAcc+=dt
 for _,s in allTargets() do local ch=s.Character;local h=ch and ch:FindFirstChildOfClass("Humanoid");local r=ch and ch:FindFirstChild("HumanoidRootPart")
  if h and r and h.Health>0 then
   MovementService.Validate(s,now)
   h.WalkSpeed=(s.FrozenUntil or 0)>now and 8 or s.Crouch and C.CrouchSpeed or s.Sprint and C.SprintSpeed+(s.Hop or 0) or C.WalkSpeed
   if (s.SlideUntil or 0)>now then local d=s.SlideDirection or r.CFrame.LookVector;r.AssemblyLinearVelocity=Vector3.new(d.X*C.SlideSpeed,r.AssemblyLinearVelocity.Y,d.Z*C.SlideSpeed) end
   if s.Match and r.Position.Y<(s.Match.KillY or 0) then h.Health=0 end
   -- Tolerant server movement envelope prevents teleports between arenas.
   if s.Match and (r.Position-s.Match.Origin).Magnitude>130 and now-s.SpawnAt>2 then ch:PivotTo(CFrame.new(s.LastSafe or (s.Match.Origin+Vector3.new(0,4,-28)))) end
   if acc>=1 and s.Match and (r.Position-s.Match.Origin).Magnitude<110 then s.LastSafe=r.Position end
  end
 end
 if botAcc>.25 then botAcc=0;for _,b in Bots do local m=b.Match;if m and m.Phase=="Live" and b.Character and b.Character.Humanoid.Health>0 then
  local opponent=m.Members[1];local root=b.Character.HumanoidRootPart;local target=m.Origin+Vector3.new(math.sin(now*.55)*23,3,12+math.cos(now*.4)*10);b.Character.Humanoid:MoveTo(target)
  if (not m.Training or m.Sparring) and opponent and opponent.Character and opponent.Character.Humanoid.Health>0 and now>(b.BotFire or 0) then local delta=opponent.Character.Head.Position-b.Character.Head.Position;b.BotFire=now+1.2;b.Aim=delta.Unit;Combat.Fire(b,b.Aim,false);if b.Ammo and b.Ammo[1]==0 then Combat.Action(b,"Reload") end end
 end end end
 if acc<1 then return end;acc=0
 for mode,q in Queues do
  if mode=="1v1" then table.sort(q,function(a,b) return (Profiles.Data[a] and Profiles.Data[a].Elo or 1000)<(Profiles.Data[b] and Profiles.Data[b].Elo or 1000) end) end
  while #q>=C.Modes[mode] do local group={};for _=1,C.Modes[mode] do table.insert(group,table.remove(q,1)) end;createMatch(group,mode,false) end
 end
 for _,m in Matches do
  if m.Phase=="Live" and now>=m.Deadline then
   if m.Mode=="FFA" then local best=m.Members[1];for _,s in m.Members do if (s.Kills or 0)>(best.Kills or 0) then best=s end end;finishMatch(m,best)
   elseif not m.Training then local hp={0,0};for _,s in m.Members do if s.Character then hp[s.Team]+=s.Character.Humanoid.Health end end;roundEnd(m,hp[1]==hp[2] and 0 or hp[1]>hp[2] and 1 or 2) end
  end;broadcast(m)
 end
end)
print("[PADDLE BRAWL] Server ready — R6, authoritative combat, queues and training")
