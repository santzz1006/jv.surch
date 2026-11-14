local source=game.ServerScriptService.PaddleBrawl.Combat:Clone();source.Name='QACombat';source.Parent=game.ServerScriptService
local Combat=require(source);local C=require(game.ReplicatedStorage.PaddleBrawl.Config);local folder=Instance.new('Folder');folder.Name='IsolatedCombatQA';folder.Parent=workspace
local match={Mode='1v1',Phase='Live'};local events={};local kills=0
local function char(name,pos)
 local ch=game.ServerStorage.PaddleR6:Clone();ch.Name=name;ch.PrimaryPart=ch.HumanoidRootPart;ch:PivotTo(CFrame.new(pos));ch.Parent=folder
 for _,p in ch:GetDescendants()do if p:IsA('BasePart')then p.Anchored=true;p.CanQuery=true;p.CanCollide=false end end
 ch.Humanoid.MaxHealth=150;ch.Humanoid.Health=150;return ch
end
local a={Player={UserId=-101},Team=1,Match=match,Character=char('Shooter',Vector3.new(5000,1000,0)),Weapons={'Classic','RallyRapid','Melee','Explosive'},Ultimate=0}
local b={Player={UserId=-102},Team=2,Match=match,Character=char('Target',Vector3.new(5000,1000,-20)),Weapons={'Classic','RallyRapid','Melee','Explosive'},Ultimate=0}
local targets={a,b};Combat.Init({},function(p,k,d)table.insert(events,{Kind=k,Data=d})end,function()return targets end,function()kills+=1 end)
local results={};local function check(name,ok,detail)table.insert(results,{name=name,passed=ok,detail=detail})end
local function reset(id)
 Combat.Clear(match);events={};a.Weapons[1]=id or 'Classic';Combat.Reset(a);b.Character.Humanoid.Health=150;a.Character.Humanoid.Health=150;b.KillCredited=false;b.Team=2;b.ParryUntil=0;b.Character:PivotTo(CFrame.new(5000,1000,-20));a.NextFire=0
end
local function aim()return (b.Character.Head.Position-a.Character.Head.Position).Unit end
reset();Combat.Fire(a,aim());task.wait(.45);check('Classic headshot',math.abs(b.Character.Humanoid.Health-98.8)<.1,b.Character.Humanoid.Health)
reset();Combat.Fire(a,aim());Combat.Fire(a,aim());check('Cooldown consumes one round',a.Ammo[1]==11,a.Ammo[1]);task.wait(.1)
reset();Combat.Fire(a,Vector3.new(0/0,0,0));check('Reject NaN aim',a.Ammo[1]==12,a.Ammo[1])
reset();b.Team=1;Combat.Fire(a,aim());task.wait(.4);check('No friendly fire',b.Character.Humanoid.Health==150,b.Character.Humanoid.Health)
reset();a.Ammo[1]=0;Combat.Action(a,'Reload');task.wait(1.5);check('Reload moves reserve',a.Ammo[1]==12 and a.Reserve[1]==84,{a.Ammo[1],a.Reserve[1]})
for _,id in {'LongSmash','TripleServe','RallyRapid','SpinMaster','Homing','MegaSmash'}do reset(id);a.Charge=os.clock()-1;Combat.Fire(a,aim());task.wait(.5);check(id..' damages target',b.Character.Humanoid.Health<150,b.Character.Humanoid.Health)end
reset();b.Character:PivotTo(CFrame.new(5000,1000,-20)*CFrame.Angles(0,math.pi,0));b.ParryUntil=os.clock()+1;b.Aim=(a.Character.Head.Position-b.Character.Head.Position).Unit;Combat.Fire(a,aim());task.wait(.6);check('Parry reflects onto attacker',b.Character.Humanoid.Health==150 and a.Character.Humanoid.Health<150,{attacker=a.Character.Humanoid.Health,defender=b.Character.Humanoid.Health})
reset();a.Ultimate=100;Combat.Fire(a,aim(),true);task.wait(.4);check('Ultimate consumes charge and kills',a.Ultimate<100 and b.Character.Humanoid.Health==0,{charge=a.Ultimate,health=b.Character.Humanoid.Health})
Combat.Clear(match);match.Phase='Finished';folder:Destroy();source:Destroy();return results
