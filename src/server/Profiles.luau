-- Server-only profiles, daily claims and cosmetic economy. Never trust client balances.
local Players=game:GetService("Players")
local DSS=game:GetService("DataStoreService")
local Http=game:GetService("HttpService")
local C=require(game.ReplicatedStorage.PaddleBrawl.Config)
local P={Data={},Writable={},Locks={}}
local store=DSS:GetDataStore(C.DataStoreName)
local session=game.JobId~="" and game.JobId or Http:GenerateGUID(false)
local function day() return os.date("!%Y-%m-%d") end
local function fresh()
 return {Coins=300,Keys=2,Elo=1000,XP=0,Wins=0,Kills=0,History={},Owned={Default=true},Skin="Default",Primary="Classic",Secondary="RallyRapid",Utility="Explosive",Day=day(),Daily={duels=0,kills=0,wins=0},Claimed={},SeasonClaims={}}
end
local function normalize(d)
 local f=fresh();if type(d)~="table" then return f end
 for k,v in f do if d[k]==nil or typeof(d[k])~=typeof(v) then d[k]=v end end
 while #d.History>20 do table.remove(d.History)end
 d.Coins=math.max(0,math.floor(d.Coins));d.Keys=math.max(0,math.floor(d.Keys));d.Elo=math.clamp(d.Elo,0,4000)
 if d.Day~=day() then d.Day=day();d.Daily={duels=0,kills=0,wins=0};d.Claimed={} end
 if not C.Cosmetics[d.Skin] then d.Skin="Default" end
 if not C.Weapons[d.Primary] then d.Primary="Classic" end
 if not C.Weapons[d.Secondary] then d.Secondary="RallyRapid" end
 return d
end
function P.Load(player)
 local d=fresh();P.Writable[player]=false
 if C.PersistenceEnabled and game.GameId>0 then
  local ok,result=pcall(function()
   return store:UpdateAsync("u"..player.UserId,function(old)
    old=normalize(old)
    if old.Lock and old.Lock.Id~=session and old.Lock.Expires>os.time() then return nil end
    old.Lock={Id=session,Expires=os.time()+C.ProfileLockSeconds};return old
   end)
  end)
  if ok and result then d=normalize(result);P.Writable[player]=true
  elseif ok then player:Kick("Seu perfil ainda está aberto em outro servidor. Tente novamente em alguns segundos.");return
  else warn("[PADDLE BRAWL] Profile unavailable; session-only progression:",result) end
 end
 P.Data[player]=d;player:SetAttribute("PersistenceReady",P.Writable[player]);return d
end
function P.Save(player,release)
 local d=P.Data[player];if not d or not P.Writable[player] then return end
 local snapshot=Http:JSONDecode(Http:JSONEncode(d))
 local ok,err=pcall(function() store:UpdateAsync("u"..player.UserId,function(old)
  if old and old.Lock and old.Lock.Id~=session then return nil end
  snapshot.Lock=not release and {Id=session,Expires=os.time()+C.ProfileLockSeconds} or nil;return snapshot
 end) end)
 if not ok then warn("[PADDLE BRAWL] Save failed",player.UserId,err) end
end
function P.Public(player)
 local d=P.Data[player];if not d then return nil end;normalize(d)
 local out={};for _,k in {"Coins","Keys","Elo","XP","Wins","Kills","History","Owned","Skin","Primary","Secondary","Utility","Daily","Claimed","SeasonClaims"} do out[k]=d[k] end
 out.Persistent=P.Writable[player];return out
end
function P.Add(player,key,n)
 local d=P.Data[player];if not d then return end;normalize(d)
 if d.Daily[key]~=nil then d.Daily[key]+=n end
end
function P.Claim(player,id)
 local d=P.Data[player];if not d then return false,"Perfil carregando" end;normalize(d)
 for _,q in C.Dailies do if q.Id==id then
  if d.Claimed[id] or (d.Daily[id] or 0)<q.Target then return false,"Tarefa ainda não disponível" end
  d.Claimed[id]=true;d.Coins+=q.Coins;d.Keys+=q.Keys;return true,"Recompensa recebida!"
 end end
 return false,"Tarefa inválida"
end
function P.Buy(player,id)
 local d=P.Data[player];local item=C.Cosmetics[id]
 if not d or not item or d.Owned[id] then return false,"Item indisponível" end
 if d.Coins<item.Price then return false,"Moedas insuficientes" end
 d.Coins-=item.Price;d.Owned[id]=true;return true,item.Name.." desbloqueado"
end
function P.Crate(player)
 local d=P.Data[player];if not d or d.Keys<1 then return false,"Você precisa de uma chave" end
 d.Keys-=1;local roll=Random.new():NextNumber(0,100);local sum=0;local id="Citrus"
 for _,item in C.Crate do sum+=item.Weight;if roll<=sum then id=item.Id;break end end
 if d.Owned[id] then d.Coins+=75;return true,C.Cosmetics[id].Name.." repetido: +75 moedas" end
 d.Owned[id]=true;return true,C.Cosmetics[id].Name.." desbloqueado!"
end
function P.SeasonClaim(player,level)
 local d=P.Data[player];if not d or type(level)~="number" or level%1~=0 or level<1 or level>C.Season.MaxLevel then return false,"Nível inválido" end
 local key=tostring(level)
 if d.XP<level*C.Season.XPPerLevel or d.SeasonClaims[key] then return false,"Recompensa indisponível" end
 d.SeasonClaims[key]=true;d.Coins+=C.Season.CoinsPerLevel;return true,"Recompensa da temporada recebida"
end
task.spawn(function() while true do task.wait(C.AutoSaveSeconds);for p in P.Data do task.spawn(P.Save,p,false) end end end)
Players.PlayerRemoving:Connect(function(p) P.Save(p,true);P.Data[p]=nil;P.Writable[p]=nil end)
game:BindToClose(function() local pending=0;for p in P.Data do pending+=1;task.spawn(function() P.Save(p,true);pending-=1 end) end;local deadline=os.clock()+25;while pending>0 and os.clock()<deadline do task.wait(.1) end end)
return P
