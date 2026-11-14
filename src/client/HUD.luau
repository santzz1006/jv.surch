local Players=game:GetService("Players")
local UIS=game:GetService("UserInputService")
local GuiService=game:GetService("GuiService")
local Tween=game:GetService("TweenService")
local Root=game.ReplicatedStorage.PaddleBrawl
local C=require(Root.Config);local A=require(Root.Assets);local Maps=require(Root.MapData)
local H={Profile=nil,Match=nil,InMatch=false,MenuOpen=false,Slot=1,Weapons={"Classic","RallyRapid","Melee","Explosive"},Mobile={}}
local function frame(parent,name,pos,size) local f=Instance.new("Frame");f.Name=name;f.BackgroundTransparency=1;f.Position=pos;f.Size=size;f.Parent=parent;return f end
local function sprite(parent,name,pos,size,button)
 local f=Instance.new(button and "ImageButton" or "ImageLabel");f.Name=name;f.BackgroundTransparency=1;f.Image=A.Images[name] or A.Images.Panel;f.Position=pos;f.Size=size;f.ImageColor3=Color3.new(1,1,1);f:SetAttribute("TeamTint",false);f.Parent=parent;return f
end
local function text(parent,str,pos,size,fontSize,color)
 local t=Instance.new("TextLabel");t.BackgroundTransparency=1;t.Text=str;t.Position=pos;t.Size=size;t.Font=Enum.Font.FredokaOne;t.TextSize=fontSize or 22;t.TextColor3=color or Color3.fromRGB(245,248,255);t.TextWrapped=true;t.Parent=parent;return t
end
local function button(parent,label,x,y,w,h,fn)
 local b=sprite(parent,"Button",UDim2.fromOffset(x,y),UDim2.fromOffset(w,h),true);b.Selectable=true
 text(b,label,UDim2.fromScale(.06,.1),UDim2.fromScale(.88,.8),23)
 b.Activated:Connect(fn);b.MouseEnter:Connect(function() Tween:Create(b,TweenInfo.new(.12),{ImageColor3=Color3.fromRGB(210,235,255)}):Play() end);b.MouseLeave:Connect(function() Tween:Create(b,TweenInfo.new(.12),{ImageColor3=Color3.new(1,1,1)}):Play() end)
 return b
end
function H.Init(send)
 H.Send=send;local player=Players.LocalPlayer
 local gui=Instance.new("ScreenGui");gui.Name="PaddleHUD";gui.ResetOnSpawn=false;gui.IgnoreGuiInset=true;gui.DisplayOrder=10;gui.ZIndexBehavior=Enum.ZIndexBehavior.Sibling;gui.Parent=player.PlayerGui;H.Gui=gui
 local canvas=frame(gui,"Canvas",UDim2.fromScale(.5,.5),UDim2.fromOffset(1440,900));canvas.AnchorPoint=Vector2.new(.5,.5);H.Canvas=canvas
 local scale=Instance.new("UIScale");scale.Parent=canvas
 local function resize() local v=workspace.CurrentCamera.ViewportSize;scale.Scale=math.min(v.X/1440,v.Y/900) end
 resize();workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"):Connect(resize)
 H.Top=frame(canvas,"Top",UDim2.fromOffset(375,22),UDim2.fromOffset(690,110))
 local blue=sprite(H.Top,"ScoreBlue",UDim2.fromOffset(0,0),UDim2.fromOffset(255,86));H.Purple=text(blue,"0",UDim2.fromOffset(195,6),UDim2.fromOffset(50,65),48)
 local red=sprite(H.Top,"ScoreRed",UDim2.fromOffset(435,0),UDim2.fromOffset(255,86));H.Gold=text(red,"0",UDim2.fromOffset(8,6),UDim2.fromOffset(50,65),48)
 local clock=sprite(H.Top,"Panel",UDim2.fromOffset(264,0),UDim2.fromOffset(162,86));sprite(clock,"Hourglass",UDim2.fromOffset(12,24),UDim2.fromOffset(35,39));H.Clock=text(clock,"00:00",UDim2.fromOffset(48,12),UDim2.fromOffset(105,60),33)
 H.Mode=text(H.Top,"",UDim2.fromOffset(80,90),UDim2.fromOffset(530,26),14)
 H.TeamFrames={blue,red};H.Avatars={}
 H.Cross=sprite(canvas,"Crosshair",UDim2.fromOffset(702,432),UDim2.fromOffset(36,36));H.Cross.Visible=false;H.Cross:SetAttribute("TeamTint",false);H.Cross.ImageColor3=Color3.new(1,1,1)
 H.Hit=text(canvas,"✕",UDim2.fromOffset(687,416),UDim2.fromOffset(66,66),40,Color3.fromRGB(255,217,77));H.Hit.Visible=false
 local health=sprite(canvas,"Panel",UDim2.fromOffset(28,804),UDim2.fromOffset(326,63));H.HealthFill=sprite(health,"Health",UDim2.fromScale(0,0),UDim2.fromScale(1,1));H.Health=text(health,"150",UDim2.fromScale(.22,.08),UDim2.fromScale(.7,.82),43)
 H.Heart=sprite(canvas,"Heart",UDim2.fromOffset(28,798),UDim2.fromOffset(67,67));H.HealthSprite=health;H.HealthName=text(canvas,player.DisplayName,UDim2.fromOffset(48,775),UDim2.fromOffset(280,28),16)
 local weapon=sprite(canvas,"Panel",UDim2.fromOffset(1140,813),UDim2.fromOffset(275,60));weapon.Name="WeaponPanel";H.WeaponPanel=weapon;H.Weapon=text(weapon,"Raquete Clássica",UDim2.fromScale(.06,.12),UDim2.fromScale(.88,.76),20)
 H.Ammo=text(canvas,"12 / 96",UDim2.fromOffset(1120,125),UDim2.fromOffset(140,32),23);H.Reload=text(canvas,"",UDim2.fromOffset(1080,160),UDim2.fromOffset(330,25),13)
 H.UltButton=button(canvas,"Q • SUPER SAQUE 0%",540,826,360,44,function()send("Ultimate")end)
 H.SlotLabels={};H.Slots={};H.SlotIcons={}
 for i in {1,2,3,4} do
  local b=sprite(canvas,"Slot",UDim2.fromOffset(1094+(i-1)*77,48),UDim2.fromOffset(74,74),true);b.Name="EquipmentSlot"..i
  H.SlotIcons[i]=sprite(b,({"Paddle","Balls","Paddle","Shield"})[i],UDim2.fromScale(.17,.14),UDim2.fromScale(.66,.66));text(b,tostring(i),UDim2.fromOffset(26,-17),UDim2.fromOffset(24,28),22);b.Activated:Connect(function()send("Slot",i)end);H.Slots[i]=b
 end
 H.QuestPanel=sprite(canvas,"Panel",UDim2.fromOffset(22,208),UDim2.fromOffset(278,264));sprite(H.QuestPanel,"Tasks",UDim2.fromOffset(15,13),UDim2.fromOffset(36,36));text(H.QuestPanel,"Tarefas Diárias",UDim2.fromOffset(55,12),UDim2.fromOffset(205,36),22)
 H.QuestRows={}
 for i,q in C.Dailies do
  local y=58+(i-1)*66;sprite(H.QuestPanel,({"Paddle","Balls","Trophy"})[i],UDim2.fromOffset(15,y+5),UDim2.fromOffset(36,36))
  text(H.QuestPanel,q.Name,UDim2.fromOffset(57,y),UDim2.fromOffset(180,23),15)
  local bar=sprite(H.QuestPanel,"Health",UDim2.fromOffset(58,y+29),UDim2.fromOffset(142,12));local count=text(H.QuestPanel,"0 / "..q.Target,UDim2.fromOffset(195,y+23),UDim2.fromOffset(70,26),14)
  H.QuestRows[i]={Bar=bar,Count=count}
 end
 H.QuestText=text(H.QuestPanel,"",UDim2.fromOffset(0,0),UDim2.fromOffset(0,0),1);H.QuestText.Visible=false
 H.Notice=text(canvas,"",UDim2.fromOffset(320,190),UDim2.fromOffset(800,58),24,Color3.fromRGB(230,245,255))
 H.Feed=text(canvas,"",UDim2.fromOffset(1050,300),UDim2.fromOffset(360,90),15);H.Feed.TextYAlignment=Enum.TextYAlignment.Top
 H.Stats=text(canvas,"",UDim2.fromOffset(1230,12),UDim2.fromOffset(180,25),12,Color3.fromRGB(161,193,211))
 H.ToggleButton=button(canvas,"MENU",25,110,135,50,function() H.ToggleMenu() end)
 H.TrainToggle=button(canvas,"SPARRING: OFF",25,490,245,44,function() send("ToggleSparring") end);H.TrainToggle.Visible=false
 H.Menu=sprite(canvas,"Panel",UDim2.fromOffset(310,205),UDim2.fromOffset(820,560));H.Menu.Name="PauseMenu";H.Page=frame(H.Menu,"Page",UDim2.fromOffset(45,38),UDim2.fromOffset(730,485))
 H.Vote=frame(canvas,"Vote",UDim2.fromOffset(260,250),UDim2.fromOffset(920,420));H.Vote.Visible=false
 H.Result=sprite(canvas,"Victory",UDim2.fromOffset(480,250),UDim2.fromOffset(480,400));H.Result.Visible=false;H.ResultText=text(H.Result,"VITÓRIA!",UDim2.fromScale(.1,.43),UDim2.fromScale(.8,.3),38)
 H.Death=text(canvas,"",UDim2.fromOffset(430,570),UDim2.fromOffset(580,55),26)
 H.DamageFlash=frame(gui,"DamageFlash",UDim2.fromScale(0,0),UDim2.fromScale(1,1));H.DamageFlash.BackgroundColor3=Color3.fromRGB(255,35,65);H.DamageFlash.ZIndex=30
 H.Controls=text(canvas,"WASD mover • Shift correr • C deslizar • RMB defender • R recarregar • F inspecionar • Q super",UDim2.fromOffset(320,879),UDim2.fromOffset(800,20),11)
 if UIS.TouchEnabled then
  H.TouchLayer=frame(gui,"TouchControls",UDim2.fromScale(0,0),UDim2.fromScale(1,1))
  local controls={{"Fire","SAQUE",.89,.62,94},{"Parry","MIRAR",.77,.7,76},{"Reload","RECARGA",.89,.44,68},{"Sprint","CORRER",.13,.49,70},{"Crouch","SLIDE",.7,.84,70},{"Inspect","VER",.96,.32,58},{"CycleNext","TROCAR",.72,.5,64},{"Ultimate","SUPER",.59,.84,68}}
  for _,v in controls do local b=sprite(H.TouchLayer,"Slot",UDim2.fromScale(v[3],v[4]),UDim2.fromOffset(v[5],v[5]),true);b.AnchorPoint=Vector2.new(.5,.5);b.ImageTransparency=.25;text(b,v[2],UDim2.fromScale(.08,.33),UDim2.fromScale(.84,.3),13,Color3.fromRGB(246,250,255));H.Mobile[v[1]]=b end
  H.Controls.Text="Use o direcional para mover e arraste a tela para mirar"
 end
 H.LobbyBar=frame(canvas,"LobbyBar",UDim2.fromOffset(0,0),UDim2.fromOffset(1440,900))
 local play=button(H.LobbyBar,"JOGAR",550,776,340,100,function()H.MenuOpen=true;H.ShowPage("Modes")end);play.Image=A.Images.Health
 sprite(play,"Play",UDim2.fromOffset(30,23),UDim2.fromOffset(52,52))
 button(H.LobbyBar,"RANKING",385,791,150,74,function()H.MenuOpen=true;H.ShowPage("Ranking")end)
 button(H.LobbyBar,"INVENTÁRIO",910,791,155,74,function()H.MenuOpen=true;H.ShowPage("Loadout")end)
 button(H.LobbyBar,"TREINAR",1100,791,245,74,function()H.Send("Train")end)
 H.Currency=text(H.LobbyBar,"",UDim2.fromOffset(1100,35),UDim2.fromOffset(310,45),24)
 H.ProfileLabel=text(H.LobbyBar,"",UDim2.fromOffset(30,795),UDim2.fromOffset(335,75),22)
 H.MenuBlur=Instance.new("BlurEffect");H.MenuBlur.Name="PaddleMenuBlur";H.MenuBlur.Size=0;H.MenuBlur.Parent=workspace.CurrentCamera
 H.Settings={FOV=C.BaseFOV,Volume=1,Sensitivity=1}
 H.SetTeam(1);H.SetMatch(false);H.ShowPage("Home")
 return H
end
function H.Toast(message)
 H.Notice.Text=tostring(message);H.Notice.TextTransparency=0;H.NoticeSerial=(H.NoticeSerial or 0)+1;local n=H.NoticeSerial
 task.delay(3,function() if n==H.NoticeSerial then Tween:Create(H.Notice,TweenInfo.new(.35),{TextTransparency=1}):Play() end end)
end
function H.UpdateHealth(value,max)
 H.Health.Text=tostring(math.ceil(value));Tween:Create(H.HealthFill,TweenInfo.new(.18),{Size=UDim2.fromScale(math.clamp(value/max,0,1),1)}):Play()
 if H.LastHealth and value<H.LastHealth then H.DamageFlash.BackgroundTransparency=.8;Tween:Create(H.DamageFlash,TweenInfo.new(.3),{BackgroundTransparency=1}):Play()end
 H.LastHealth=value
end
function H.ToggleMenu()
 H.MenuOpen=not H.MenuOpen;H.Menu.Visible=H.MenuOpen;if H.MenuOpen then H.ShowPage("Home") end
 Tween:Create(H.MenuBlur,TweenInfo.new(.18),{Size=H.MenuOpen and 8 or 0}):Play()
end
function H.ShowPage(page)
 H.CurrentPage=page;H.Page:ClearAllChildren();local f=H.Page;local d=H.Profile
 local title=page=="Home" and "Menu do Jogo" or page=="Modes" and "MODOS DE JOGO" or page=="Settings" and "CONFIGURAÇÕES" or page=="Ranking" and "RANKING DO SERVIDOR" or page=="History" and "HISTÓRICO" or page=="Loadout" and "EQUIPAMENTO" or page=="Shop" and "LOJA & INVENTÁRIO" or page=="Dailies" and "TAREFAS DIÁRIAS" or "PRIMEIRO SAQUE"
 text(f,title,UDim2.fromOffset(0,0),UDim2.fromOffset(730,55),32,Color3.fromRGB(225,244,255))
 if page~="Home" then button(f,"‹ VOLTAR",0,435,170,46,function()H.ShowPage("Home")end) end
 if page=="Home" then
  local entries={{"Voltar ao Jogo","Play",function()H.ToggleMenu()end},{"Loja","Shop",function()H.ShowPage("Shop")end},{"Inventário","Inventory",function()H.ShowPage("Loadout")end},{"Tarefas","Tasks",function()H.ShowPage("Dailies")end},{"Configurações","Settings",function()H.ShowPage("Settings")end},{H.InMatch and "Sair da Partida" or "Modos de Jogo","Exit",function()if H.InMatch then H.Send("Leave") else H.ShowPage("Modes")end end}}
  for i,v in entries do local b=button(f,"",((i-1)%3)*245,90+math.floor((i-1)/3)*165,235,150,v[3]);sprite(b,v[2],UDim2.fromOffset(86,18),UDim2.fromOffset(64,64));text(b,v[1],UDim2.fromOffset(10,99),UDim2.fromOffset(215,36),22) end
  button(f,"×",670,0,60,50,function()H.ToggleMenu()end)
 elseif page=="Settings" then
  for i,row in {{"Campo de visão","FOV",60,100,5},{"Volume","Volume",0,1,.1},{"Sensibilidade","Sensitivity",.2,2,.1}} do
   local value=H.Settings[row[2]];text(f,row[1]..": "..string.format("%.1f",value),UDim2.fromOffset(20,90+(i-1)*95),UDim2.fromOffset(430,55),25)
   for j,delta in {-1,1} do button(f,j==1 and "−" or "+",485+(j-1)*110,90+(i-1)*95,95,55,function()H.Settings[row[2]]=math.clamp(value+delta*row[5],row[3],row[4]);UIS.MouseDeltaSensitivity=H.Settings.Sensitivity;game:GetService("SoundService"):SetAttribute("PaddleVolume",H.Settings.Volume);H.ShowPage("Settings")end) end
  end
 elseif page=="Ranking" then
  button(f,"MEU HISTÓRICO",450,62,270,45,function()H.ShowPage("History")end)
  local list=Players:GetPlayers();table.sort(list,function(a,b)return (a:GetAttribute("PaddleElo") or 0)>(b:GetAttribute("PaddleElo") or 0)end)
  for i,p in list do if i>6 then break end;text(f,i..". "..p.DisplayName.." • "..(p:GetAttribute("PaddleElo") or "carregando").." ELO",UDim2.fromOffset(15,75+i*43),UDim2.fromOffset(700,38),23)end
 elseif page=="History" then
  local list=d and d.History or {};if #list==0 then text(f,"Suas partidas concluídas aparecem aqui.",UDim2.fromOffset(30,150),UDim2.fromOffset(670,100),25)end
  for i,m in list do if i>6 then break end;text(f,(m.Draw and "EMPATE" or m.Won and "VITÓRIA" or "DERROTA").." • "..m.Mode.." • "..(m.Map or "").." • "..m.Elo.." ELO",UDim2.fromOffset(10,75+i*45),UDim2.fromOffset(710,40),20)end
 elseif page=="Modes" then
  text(f,d and (d.Coins.." MOEDAS    •    "..d.Keys.." CHAVES    •    "..d.Elo.." ELO") or "Carregando perfil…",UDim2.fromOffset(0,55),UDim2.fromOffset(730,35),17)
  for i,mode in {"1v1","2v2","3v3","FFA"} do button(f,mode..(i==1 and " RANQUEADO" or ""),(i-1)*182,110,175,64,function()H.Send("Queue",mode);H.Toast("Buscando partida "..mode)end) end
  button(f,"CAMPO DE TREINO",0,190,355,62,function()H.Send("Train")end)
  button(f,"EQUIPAMENTO",375,190,355,62,function()H.ShowPage("Loadout")end)
  button(f,"LOJA & INVENTÁRIO",0,270,355,62,function()H.ShowPage("Shop")end)
  button(f,"TAREFAS",375,270,170,62,function()H.ShowPage("Dailies")end)
  button(f,"TEMPORADA",560,270,170,62,function()H.ShowPage("Season")end)
  if H.InMatch then button(f,"VOLTAR À PARTIDA",0,350,355,60,function()H.ToggleMenu()end);button(f,"SAIR DO DUELO",375,350,355,60,function()H.Send("Leave")end)
  else button(f,"CANCELAR BUSCA",0,350,355,60,function()H.Send("CancelQueue")end);button(f,"EMOTE",375,350,355,60,function()H.Send("Emote")end) end
  text(f,d and (d.Persistent and "Progressão salva • Sem vantagens pagas" or "Progressão desta sessão • Salvamento indisponível") or "",UDim2.fromOffset(0,424),UDim2.fromOffset(730,35),13)
 elseif page=="Loadout" then
  H.LoadoutSlot=H.LoadoutSlot or "Primary"
  for i,v in {"Primary","Secondary","Utility"} do button(f,({"PRIMÁRIA","SECUNDÁRIA","UTILITÁRIO"})[i],(i-1)*242,62,230,47,function()H.LoadoutSlot=v;H.ShowPage("Loadout")end) end
  local list=H.LoadoutSlot=="Utility" and {"Explosive","Freeze"} or C.WeaponOrder
  for i,id in list do local w=C.Weapons[id];local equipped=d and d[H.LoadoutSlot]==id
   button(f,(equipped and "✓ " or "")..w.Name,((i-1)%2)*365,126+math.floor((i-1)/2)*71,350,62,function()H.Send("Loadout",id,H.LoadoutSlot)end)
  end
 elseif page=="Shop" then
  local ids={"Default","Citrus","Bubblegum","Glacier","Solar","Nova"}
  for i,id in ids do local item=C.Cosmetics[id];local owned=d and d.Owned[id];local b=button(f,item.Name.." • "..item.Rarity.."\n"..(d and d.Skin==id and "EQUIPADA" or owned and "EQUIPAR" or item.Price.." moedas"),((i-1)%3)*243,72+math.floor((i-1)/3)*115,232,100,function()H.Send(owned and "Skin" or "Buy",id)end);b.ImageColor3=item.Color end
  button(f,"ABRIR CAIXA • 1 CHAVE",195,321,350,58,function()H.Send("Crate")end)
  text(f,"Chances: Citrus 40% • Bubblegum 25% • Glacier 25% • Solar 8% • Nova 2%\nRepetido = 75 moedas. Chaves são obtidas jogando.",UDim2.fromOffset(10,386),UDim2.fromOffset(710,45),12)
 elseif page=="Dailies" then
  for i,q in C.Dailies do local n=d and d.Daily[q.Id] or 0
   text(f,q.Name.."  "..math.min(n,q.Target).."/"..q.Target.."  •  "..q.Coins.." moedas + "..q.Keys.." chave(s)",UDim2.fromOffset(0,90+(i-1)*105),UDim2.fromOffset(480,64),19)
   button(f,d and d.Claimed[q.Id] and "RECEBIDA" or "RESGATAR",490,96+(i-1)*105,230,60,function()H.Send("Claim",q.Id)end)
  end
 elseif page=="Season" then
  local level=math.min(C.Season.MaxLevel,math.floor((d and d.XP or 0)/C.Season.XPPerLevel));text(f,"NÍVEL "..level.." / 20   •   "..(d and d.XP or 0).." XP",UDim2.fromOffset(0,60),UDim2.fromOffset(730,40),23)
  for i=1,20 do button(f,tostring(i)..(d and d.SeasonClaims[tostring(i)] and " ✓" or ""),((i-1)%5)*145,120+math.floor((i-1)/5)*68,135,55,function()H.Send("Season",i)end) end
  text(f,"75 moedas por nível • 150 XP por nível • Passe gratuito",UDim2.fromOffset(180,440),UDim2.fromOffset(550,35),14)
 end
 if UIS.GamepadEnabled then for _,v in f:GetChildren() do if v:IsA("GuiButton") then GuiService.SelectedObject=v;break end end end
end
function H.UpdateProfile(d)
 if not d then return end;H.Profile=d
 local lines={};for _,q in C.Dailies do table.insert(lines,q.Name.."\n"..math.min(d.Daily[q.Id] or 0,q.Target).." / "..q.Target..(d.Claimed[q.Id] and " ✓" or "")) end;H.QuestText.Text=table.concat(lines,"\n\n")
 for i,q in C.Dailies do local n=math.min(d.Daily[q.Id] or 0,q.Target);local row=H.QuestRows[i];row.Count.Text=n.." / "..q.Target;row.Bar.Size=UDim2.fromOffset(math.max(3,142*n/q.Target),12);row.Bar.ImageColor3=n>=q.Target and Color3.new(1,1,1) or Color3.fromRGB(55,170,255)end
 H.Currency.Text=d.Coins.." moedas   •   "..d.Keys.." chaves"
 H.ProfileLabel.Text=Players.LocalPlayer.DisplayName.."\nNível "..(1+math.floor(d.XP/150)).." • "..d.Elo.." ELO"
 if H.MenuOpen then H.ShowPage(H.CurrentPage or "Home") end
end
function H.UpdateWeapon(d)
 H.Ultimate=d.Ultimate;H.AmmoCounts=d.Ammo
 H.Slot=d.Slot;H.Weapons=d.Weapons;local w=C.Weapons[d.Weapons[d.Slot]];H.Weapon.Text=w.Name;H.Ammo.Text=d.Slot==3 and "MELEE" or tostring(d.Ammo[d.Slot]).." / "..tostring(d.Reserve[d.Slot]);H.Reload.Text=d.Slot==3 and "" or d.Reload>0 and "RECARREGANDO…" or "R / Y • RECARREGAR"
 H.UltButton:FindFirstChildOfClass("TextLabel").Text="Q • SUPER SAQUE "..math.floor(d.Ultimate).."%"
 for i,b in H.Slots do b.ImageColor3=i==d.Slot and H.TeamColor or Color3.new(1,1,1);H.SlotIcons[i].Image=A.Images[d.Weapons[i]] or A.Images.Balls end
end
function H.UpdateMatch(m)
 H.TrainToggle.Visible=m.Training==true;H.TrainToggle:FindFirstChildOfClass("TextLabel").Text=m.Sparring and "SPARRING: ON" or "SPARRING: OFF"
 H.Match=m;H.Clock.Text=string.format("%02d:%02d",math.floor(m.Time/60),m.Time%60);H.Purple.Text=tostring(m.Scores[1]);H.Gold.Text=tostring(m.Scores[2]);H.Mode.Text=(m.Training and "TREINO" or m.Mode).." • "..(m.Map or "VOTAÇÃO")..(m.Phase=="Countdown" and " • PREPARE-SE" or "")
 H.Vote.Visible=m.Phase=="Vote";if H.Vote.Visible then
  if H.VoteMatch~=m.Id then
   H.VoteMatch=m.Id;H.Vote:ClearAllChildren();H.VoteCards={}
   local bg=sprite(H.Vote,"Panel",UDim2.fromOffset(-15,-15),UDim2.fromOffset(950,470));bg.ImageColor3=Color3.fromRGB(100,225,150)
   H.VoteTitle=text(H.Vote,"",UDim2.fromOffset(0,0),UDim2.fromOffset(920,55),30)
   for i,index in m.Choices do local map=Maps[index];local card=sprite(H.Vote,"MapCard",UDim2.fromOffset((i-1)*310,65),UDim2.fromOffset(295,280),true)
    local thumb=Instance.new("ImageLabel");thumb.BackgroundTransparency=1;thumb.Image=A.Thumbnails[map.Id] or "";thumb.Size=UDim2.fromScale(.86,.5);thumb.Position=UDim2.fromScale(.07,.07);thumb.ScaleType=Enum.ScaleType.Crop;thumb.Parent=card
    text(card,map.Name,UDim2.fromScale(.07,.58),UDim2.fromScale(.86,.14),21)
    local percent=text(card,"",UDim2.fromScale(.1,.74),UDim2.fromScale(.8,.12),20)
    local voters=frame(card,"Voters",UDim2.fromScale(.1,.87),UDim2.fromScale(.8,.1));H.VoteCards[index]={Percent=percent,Voters=voters}
    if map.Id=="Portao"then text(card,"EXPERIMENTAL",UDim2.fromScale(.1,.05),UDim2.fromScale(.8,.1),12,Color3.fromRGB(255,214,51))end
    card.Activated:Connect(function()H.Send("Vote",index)end)
   end
   button(H.Vote,"ALEATÓRIO",0,365,140,60,function()H.Send("Vote",0)end)
   local n=0;for index=1,10 do if not table.find(m.Choices,index)then n+=1;button(H.Vote,Maps[index].Name,150+(n-1)*109,365,104,60,function()H.Send("Vote",index)end)end end
  end
  H.VoteTitle.Text="ESCOLHA A ARENA • "..m.Time.."s"
  local total=0;for _,n in m.Votes do total+=n end
  for index,card in H.VoteCards do
   card.Percent.Text=math.floor((m.Votes[index] or 0)/math.max(1,total)*100).."%";card.Voters:ClearAllChildren();local n=0
   for _,v in m.Voters or {}do if v.Choice==index and n<6 then local im=Instance.new("ImageLabel");im.BackgroundTransparency=1;im.Size=UDim2.fromOffset(28,28);im.Position=UDim2.fromOffset(n*31,0);im.Image="rbxthumb://type=AvatarHeadShot&id="..v.UserId.."&w=150&h=150";im.Parent=card.Voters;n+=1 end end
  end
 end
 for _,im in H.Avatars do im:Destroy() end;H.Avatars={}
 for team=1,2 do local n=0;for _,s in m.Roster do if s.Team==team and n<4 then local im=Instance.new("ImageLabel");im.BackgroundTransparency=1;im.Size=UDim2.fromOffset(47,47);im.Position=UDim2.fromOffset((team==1 and 14 or 66)+n*53,9);im.Image=s.UserId>0 and ("rbxthumb://type=AvatarHeadShot&id="..s.UserId.."&w=150&h=150") or "";im.ImageTransparency=s.Alive and 0 or .7;im.Parent=H.TeamFrames[team];table.insert(H.Avatars,im);local bar=sprite(im,"Health",UDim2.fromOffset(0,47),UDim2.fromOffset(47*math.clamp((s.Health or (s.Alive and 150 or 0))/150,0,1),7));text(im,tostring(s.Level or 1),UDim2.fromOffset(30,31),UDim2.fromOffset(18,16),11);n+=1 end end end
end
function H.SetTeam(team)
 H.TeamColor=team==2 and Color3.fromRGB(255,82,102) or Color3.fromRGB(39,143,255)
 for _,v in H.Gui:GetDescendants() do if v:GetAttribute("TeamTint") then v.ImageColor3=H.TeamColor end end
end
function H.SetMatch(on)
 H.InMatch=on;H.MenuOpen=false;H.LobbyBar.Visible=not on;H.Ammo.Visible=on;H.Reload.Visible=on;H.MenuBlur.Size=0;H.TrainToggle.Visible=false;H.Top.Visible=on;H.HealthSprite.Visible=on;H.HealthName.Visible=on;local heart=H.Canvas:FindFirstChild("Heart");if heart then heart.Visible=on end;H.WeaponPanel.Visible=on;H.UltButton.Visible=on;for _,v in H.Slots do v.Visible=on end;for _,v in H.SlotLabels do v.Visible=on end;H.Menu.Visible=false;H.Cross.Visible=on;H.Result.Visible=false;H.Death.Text="";H.Vote.Visible=false
 if not on then H.Clock.Text="LOBBY";H.Mode.Text="";H.ShowPage("Home") end
end
function H.ShowResult(d)
 H.Result.Visible=true;H.Result.Image=A.Images.Panel;H.ResultText.Text=d.Training and "TREINO CONCLUÍDO" or d.Draw and "EMPATE" or d.Won and "VITÓRIA!" or "DERROTA"
end
return H
