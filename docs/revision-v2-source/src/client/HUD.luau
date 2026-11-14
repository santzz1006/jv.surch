local Players=game:GetService("Players")
local UIS=game:GetService("UserInputService")
local GuiService=game:GetService("GuiService")
local Tween=game:GetService("TweenService")
local Root=game.ReplicatedStorage.PaddleBrawl
local C=require(Root.Config);local A=require(Root.Assets);local Maps=require(Root.MapData)
local H={Profile=nil,Match=nil,InMatch=false,MenuOpen=true,Slot=1,Weapons={"Classic","RallyRapid","Melee","Explosive"},Mobile={}}
local function frame(parent,name,pos,size) local f=Instance.new("Frame");f.Name=name;f.BackgroundTransparency=1;f.Position=pos;f.Size=size;f.Parent=parent;return f end
local function sprite(parent,name,pos,size,button)
 local f=Instance.new(button and "ImageButton" or "ImageLabel");f.Name=name;f.BackgroundTransparency=1;f.Image=A.Images[name] or A.Images.Panel;f.Position=pos;f.Size=size;f.ImageColor3=H.TeamColor or Color3.fromRGB(39,143,255);f:SetAttribute("TeamTint",true);f.Parent=parent;return f
end
local function text(parent,str,pos,size,fontSize,color)
 local t=Instance.new("TextLabel");t.BackgroundTransparency=1;t.Text=str;t.Position=pos;t.Size=size;t.Font=Enum.Font.FredokaOne;t.TextSize=fontSize or 22;t.TextColor3=color or Color3.fromRGB(245,248,255);t.TextWrapped=true;t.Parent=parent;return t
end
local function button(parent,label,x,y,w,h,fn)
 local b=sprite(parent,"Button",UDim2.fromOffset(x,y),UDim2.fromOffset(w,h),true);b.Selectable=true
 text(b,label,UDim2.fromScale(.06,.1),UDim2.fromScale(.88,.8),23)
 b.Activated:Connect(fn);b.MouseEnter:Connect(function() Tween:Create(b,TweenInfo.new(.12),{ImageColor3=Color3.fromRGB(178,246,255)}):Play() end);b.MouseLeave:Connect(function() Tween:Create(b,TweenInfo.new(.12),{ImageColor3=H.TeamColor or Color3.fromRGB(39,143,255)}):Play() end)
 return b
end
function H.Init(send)
 H.Send=send;local player=Players.LocalPlayer
 local gui=Instance.new("ScreenGui");gui.Name="PaddleHUD";gui.ResetOnSpawn=false;gui.IgnoreGuiInset=true;gui.DisplayOrder=10;gui.ZIndexBehavior=Enum.ZIndexBehavior.Sibling;gui.Parent=player.PlayerGui;H.Gui=gui
 local canvas=frame(gui,"Canvas",UDim2.fromScale(.5,.5),UDim2.fromOffset(1440,900));canvas.AnchorPoint=Vector2.new(.5,.5);H.Canvas=canvas
 local scale=Instance.new("UIScale");scale.Parent=canvas
 local function resize() local v=workspace.CurrentCamera.ViewportSize;scale.Scale=math.min(v.X/1440,v.Y/900) end
 resize();workspace.CurrentCamera:GetPropertyChangedSignal("ViewportSize"):Connect(resize)
 H.Top=frame(canvas,"Top",UDim2.fromOffset(430,20),UDim2.fromOffset(580,145))
 local purple=sprite(H.Top,"TeamPurple",UDim2.fromOffset(0,0),UDim2.fromOffset(200,135));H.Purple=text(purple,"0",UDim2.fromScale(.1,.16),UDim2.fromScale(.8,.45),36)
 local gold=sprite(H.Top,"TeamYellow",UDim2.fromOffset(380,0),UDim2.fromOffset(200,135));H.Gold=text(gold,"0",UDim2.fromScale(.1,.16),UDim2.fromScale(.8,.45),36)
 local clock=sprite(H.Top,"Timer",UDim2.fromOffset(205,6),UDim2.fromOffset(170,120));H.Clock=text(clock,"LOBBY",UDim2.fromScale(.12,.2),UDim2.fromScale(.76,.5),27)
 H.Mode=text(H.Top,"",UDim2.fromOffset(100,125),UDim2.fromOffset(380,32),15)
 H.TeamFrames={purple,gold};purple:SetAttribute("TeamTint",false);gold:SetAttribute("TeamTint",false);purple.ImageColor3=Color3.fromRGB(39,143,255);gold.ImageColor3=Color3.fromRGB(255,82,102);H.Avatars={}
 H.Cross=sprite(canvas,"Crosshair",UDim2.fromOffset(702,432),UDim2.fromOffset(36,36));H.Cross.Visible=false;H.Cross:SetAttribute("TeamTint",false);H.Cross.ImageColor3=Color3.new(1,1,1)
 H.Hit=text(canvas,"✕",UDim2.fromOffset(687,416),UDim2.fromOffset(66,66),40,Color3.fromRGB(255,217,77));H.Hit.Visible=false
 local health=sprite(canvas,"Health",UDim2.fromOffset(30,798),UDim2.fromOffset(300,90));H.Health=text(health,"150 / 150",UDim2.fromScale(.25,.24),UDim2.fromScale(.68,.5),25)
 sprite(canvas,"Heart",UDim2.fromOffset(33,808),UDim2.fromOffset(48,48));H.HealthSprite=health;H.HealthName=text(canvas,player.DisplayName,UDim2.fromOffset(86,773),UDim2.fromOffset(245,28),15)
 local weapon=sprite(canvas,"Panel",UDim2.fromOffset(1110,736),UDim2.fromOffset(300,148));weapon.Name="WeaponPanel";H.WeaponPanel=weapon;H.Weapon=text(weapon,"CLÁSSICA",UDim2.fromScale(.08,.13),UDim2.fromScale(.84,.25),18);H.Ammo=text(weapon,"12 / 96",UDim2.fromScale(.08,.40),UDim2.fromScale(.84,.35),30);H.Reload=text(weapon,"R • RECARREGAR",UDim2.fromScale(.08,.76),UDim2.fromScale(.84,.15),12)
 H.UltButton=button(canvas,"Q • SUPER SAQUE 0%",510,811,420,58,function() send("Ultimate") end)
 H.SlotLabels={};H.Slots={};for i,name in {"PRIMÁRIA","SECUNDÁRIA","CORPO A CORPO","UTILITÁRIO"} do
  local b=sprite(canvas,"Slot",UDim2.fromOffset(1080+(i-1)*80,174),UDim2.fromOffset(72,72),true);sprite(b,({"Paddle","Balls","Paddle","Shield"})[i],UDim2.fromScale(.24,.16),UDim2.fromScale(.52,.52));text(b,tostring(i),UDim2.fromScale(.2,.65),UDim2.fromScale(.6,.26),18);table.insert(H.SlotLabels,text(canvas,"",UDim2.fromOffset(1075+(i-1)*80,249),UDim2.fromOffset(82,30),10));b.Activated:Connect(function()send("Slot",i)end);H.Slots[i]=b
 end
 H.QuestPanel=sprite(canvas,"Quests",UDim2.fromOffset(22,244),UDim2.fromOffset(270,270));text(H.QuestPanel,"TAREFAS DIÁRIAS",UDim2.fromScale(.08,.12),UDim2.fromScale(.84,.12),16)
 H.QuestText=text(H.QuestPanel,"Carregando perfil…",UDim2.fromScale(.09,.3),UDim2.fromScale(.82,.56),15);H.QuestText.TextXAlignment=Enum.TextXAlignment.Left
 H.Notice=text(canvas,"",UDim2.fromOffset(320,190),UDim2.fromOffset(800,58),24,Color3.fromRGB(230,245,255))
 H.Feed=text(canvas,"",UDim2.fromOffset(1050,300),UDim2.fromOffset(360,90),15);H.Feed.TextYAlignment=Enum.TextYAlignment.Top
 H.Stats=text(canvas,"",UDim2.fromOffset(1160,18),UDim2.fromOffset(250,25),12,Color3.fromRGB(161,193,211))
 H.ToggleButton=button(canvas,"MENU",25,110,150,52,function() H.ToggleMenu() end)
 H.TrainToggle=button(canvas,"SPARRING: OFF",25,174,245,50,function() send("ToggleSparring") end);H.TrainToggle.Visible=false
 H.Menu=sprite(canvas,"Panel",UDim2.fromOffset(310,205),UDim2.fromOffset(820,560));H.Menu.Name="MainMenu";H.Page=frame(H.Menu,"Page",UDim2.fromOffset(45,38),UDim2.fromOffset(730,485))
 H.Vote=frame(canvas,"Vote",UDim2.fromOffset(260,250),UDim2.fromOffset(920,420));H.Vote.Visible=false
 H.Result=sprite(canvas,"Victory",UDim2.fromOffset(480,250),UDim2.fromOffset(480,400));H.Result.Visible=false;H.ResultText=text(H.Result,"VITÓRIA!",UDim2.fromScale(.1,.43),UDim2.fromScale(.8,.3),38)
 H.Death=text(canvas,"",UDim2.fromOffset(430,570),UDim2.fromOffset(580,55),26)
 H.Controls=text(canvas,"WASD mover • Shift correr • C deslizar • RMB defender • R recarregar • F inspecionar • Q super",UDim2.fromOffset(320,879),UDim2.fromOffset(800,20),11)
 if UIS.TouchEnabled then
  local controls={{"Fire","SAQUE",1260,590,110},{"Parry","DEFESA",1155,640,88},{"Reload","RECARGA",1260,495,80},{"Sprint","CORRER",175,630,80},{"Crouch","DESLIZAR",1080,725,80},{"Inspect","VER",1350,400,70}}
  for _,v in controls do local b=sprite(canvas,"Circle",UDim2.fromOffset(v[3],v[4]),UDim2.fromOffset(v[5],v[5]),true);text(b,v[2],UDim2.fromScale(.12,.33),UDim2.fromScale(.76,.3),13,Color3.fromRGB(246,250,255));H.Mobile[v[1]]=b end
  H.Controls.Text="Use o direcional para mover e arraste a tela para mirar"
 end
 H.SetTeam(1);H.SetMatch(false);H.ShowPage("Home")
 return H
end
function H.Toast(message)
 H.Notice.Text=tostring(message);H.Notice.TextTransparency=0;H.NoticeSerial=(H.NoticeSerial or 0)+1;local n=H.NoticeSerial
 task.delay(3,function() if n==H.NoticeSerial then Tween:Create(H.Notice,TweenInfo.new(.35),{TextTransparency=1}):Play() end end)
end
function H.ToggleMenu()
 H.MenuOpen=not H.MenuOpen;H.Menu.Visible=H.MenuOpen;if H.MenuOpen then H.ShowPage("Home") end
end
function H.ShowPage(page)
 H.CurrentPage=page;H.Page:ClearAllChildren();local f=H.Page;local d=H.Profile
 local title=page=="Home" and "PADDLE BRAWL" or page=="Loadout" and "EQUIPAMENTO" or page=="Shop" and "LOJA & INVENTÁRIO" or page=="Dailies" and "TAREFAS DIÁRIAS" or "PRIMEIRO SAQUE"
 text(f,title,UDim2.fromOffset(0,0),UDim2.fromOffset(730,55),32,Color3.fromRGB(225,244,255))
 if page~="Home" then button(f,"‹ VOLTAR",0,435,170,46,function()H.ShowPage("Home")end) end
 if page=="Home" then
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
 if H.MenuOpen then H.ShowPage(H.CurrentPage or "Home") end
end
function H.UpdateWeapon(d)
 H.Slot=d.Slot;H.Weapons=d.Weapons;local w=C.Weapons[d.Weapons[d.Slot]];H.Weapon.Text=w.Name;H.Ammo.Text=d.Slot==3 and "CORPO A CORPO" or tostring(d.Ammo[d.Slot]).." / "..tostring(d.Reserve[d.Slot]);H.Reload.Text=d.Reload>0 and "RECARREGANDO…" or "R / Y • RECARREGAR"
 H.UltButton:FindFirstChildOfClass("TextLabel").Text="Q • SUPER SAQUE "..math.floor(d.Ultimate).."%"
 for i,b in H.Slots do b.ImageColor3=i==d.Slot and H.TeamColor or H.TeamColor:Lerp(Color3.new(.2,.2,.2),.6) end
end
function H.UpdateMatch(m)
 H.TrainToggle.Visible=m.Training==true;H.TrainToggle:FindFirstChildOfClass("TextLabel").Text=m.Sparring and "SPARRING: ON" or "SPARRING: OFF"
 H.Match=m;H.Clock.Text=string.format("%02d:%02d",math.floor(m.Time/60),m.Time%60);H.Purple.Text=tostring(m.Scores[1]);H.Gold.Text=tostring(m.Scores[2]);H.Mode.Text=(m.Training and "TREINO" or m.Mode).." • "..(m.Map or "VOTAÇÃO")..(m.Phase=="Countdown" and " • PREPARE-SE" or "")
 H.Vote.Visible=m.Phase=="Vote";if H.Vote.Visible then
  H.Vote:ClearAllChildren();text(H.Vote,"ESCOLHA A ARENA • "..m.Time.."s",UDim2.fromOffset(0,0),UDim2.fromOffset(920,55),30)
  local total=0;for _,v in m.Votes do total+=v end
  for i,index in m.Choices do local map=Maps[index];local card=sprite(H.Vote,"MapCard",UDim2.fromOffset((i-1)*310,65),UDim2.fromOffset(295,310),true)
   local thumb=Instance.new("ImageLabel");thumb.BackgroundTransparency=1;thumb.Image=A.Thumbnails[map.Id] or "";thumb.Size=UDim2.fromScale(.82,.51);thumb.Position=UDim2.fromScale(.09,.13);thumb.ScaleType=Enum.ScaleType.Crop;thumb.Parent=card
   text(card,map.Name,UDim2.fromScale(.09,.65),UDim2.fromScale(.82,.15),21);text(card,math.floor((m.Votes[index] or 0)/math.max(1,total)*100).."%",UDim2.fromScale(.1,.82),UDim2.fromScale(.8,.11),20)
   card.Activated:Connect(function()H.Send("Vote",index)end)
  end
 end
 for _,im in H.Avatars do im:Destroy() end;H.Avatars={}
 for team=1,2 do local n=0;for _,s in m.Roster do if s.Team==team and n<4 then local im=Instance.new("ImageLabel");im.BackgroundTransparency=1;im.Size=UDim2.fromOffset(31,31);im.Position=UDim2.fromOffset(29+n*38,84);im.Image=s.UserId>0 and ("rbxthumb://type=AvatarHeadShot&id="..s.UserId.."&w=150&h=150") or "";im.ImageTransparency=s.Alive and 0 or .7;im.Parent=H.TeamFrames[team];table.insert(H.Avatars,im);n+=1 end end end
end
function H.SetTeam(team)
 H.TeamColor=team==2 and Color3.fromRGB(255,82,102) or Color3.fromRGB(39,143,255)
 for _,v in H.Gui:GetDescendants() do if v:GetAttribute("TeamTint") then v.ImageColor3=H.TeamColor end end
end
function H.SetMatch(on)
 H.InMatch=on;H.MenuOpen=not on;H.TrainToggle.Visible=false;H.Top.Visible=on;H.HealthSprite.Visible=on;H.HealthName.Visible=on;local heart=H.Canvas:FindFirstChild("Heart");if heart then heart.Visible=on end;H.WeaponPanel.Visible=on;H.UltButton.Visible=on;for _,v in H.Slots do v.Visible=on end;for _,v in H.SlotLabels do v.Visible=on end;H.Menu.Visible=not on;H.Cross.Visible=on;H.Result.Visible=false;H.Death.Text="";H.Vote.Visible=false
 if not on then H.Clock.Text="LOBBY";H.Mode.Text="";H.ShowPage("Home") end
end
function H.ShowResult(d)
 H.Result.Visible=true;H.Result.Image=A.Images.Panel;H.ResultText.Text=d.Training and "TREINO CONCLUÍDO" or d.Draw and "EMPATE" or d.Won and "VITÓRIA!" or "DERROTA"
end
return H
