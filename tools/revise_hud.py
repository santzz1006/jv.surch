from pathlib import Path
r=Path(__file__).resolve().parents[1];p=r/'src/client/HUD.luau';s=p.read_text(encoding='utf-8')
s=s.replace('MenuOpen=true','MenuOpen=false',1)
s=s.replace('f.ImageColor3=H.TeamColor or Color3.fromRGB(39,143,255);f:SetAttribute("TeamTint",true)', 'f.ImageColor3=Color3.new(1,1,1);f:SetAttribute("TeamTint",false)')
s=s.replace('ImageColor3=Color3.fromRGB(178,246,255)', 'ImageColor3=Color3.fromRGB(210,235,255)').replace('ImageColor3=H.TeamColor or Color3.fromRGB(39,143,255)', 'ImageColor3=Color3.new(1,1,1)')
start=s.index(' H.Top=frame');end=s.index(' H.Cross=sprite',start)
s=s[:start]+''' H.Top=frame(canvas,"Top",UDim2.fromOffset(375,22),UDim2.fromOffset(690,110))
 local blue=sprite(H.Top,"ScoreBlue",UDim2.fromOffset(0,0),UDim2.fromOffset(255,86));H.Purple=text(blue,"0",UDim2.fromOffset(195,6),UDim2.fromOffset(50,65),48)
 local red=sprite(H.Top,"ScoreRed",UDim2.fromOffset(435,0),UDim2.fromOffset(255,86));H.Gold=text(red,"0",UDim2.fromOffset(8,6),UDim2.fromOffset(50,65),48)
 local clock=sprite(H.Top,"Panel",UDim2.fromOffset(264,0),UDim2.fromOffset(162,86));sprite(clock,"Hourglass",UDim2.fromOffset(12,24),UDim2.fromOffset(35,39));H.Clock=text(clock,"00:00",UDim2.fromOffset(48,12),UDim2.fromOffset(105,60),33)
 H.Mode=text(H.Top,"",UDim2.fromOffset(80,90),UDim2.fromOffset(530,26),14)
 H.TeamFrames={blue,red};H.Avatars={}
''' +s[end:]
start=s.index(' local health=sprite');end=s.index(' H.Notice=text',start)
s=s[:start]+''' local health=sprite(canvas,"Health",UDim2.fromOffset(28,804),UDim2.fromOffset(326,63));H.Health=text(health,"150",UDim2.fromScale(.22,.08),UDim2.fromScale(.7,.82),43)
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
''' +s[end:]
s=s.replace('UDim2.fromOffset(1160,18),UDim2.fromOffset(250,25)','UDim2.fromOffset(1230,12),UDim2.fromOffset(180,25)')
s=s.replace('H.ToggleButton=button(canvas,"MENU",25,110,150,52', 'H.ToggleButton=button(canvas,"MENU",25,110,135,50')
s=s.replace('25,174,245,50','25,490,245,44')
s=s.replace('H.Menu.Name="MainMenu";', 'H.Menu.Name="PauseMenu";')
pos=s.index(' H.SetTeam(1);')
s=s[:pos]+''' H.LobbyBar=frame(canvas,"LobbyBar",UDim2.fromOffset(0,0),UDim2.fromOffset(1440,900))
 local play=button(H.LobbyBar,"JOGAR",550,776,340,100,function()H.MenuOpen=true;H.ShowPage("Modes")end);play.Image=A.Images.Health
 sprite(play,"Play",UDim2.fromOffset(30,23),UDim2.fromOffset(52,52))
 button(H.LobbyBar,"RANKING",385,791,150,74,function()H.MenuOpen=true;H.ShowPage("Ranking")end)
 button(H.LobbyBar,"INVENTÁRIO",910,791,155,74,function()H.MenuOpen=true;H.ShowPage("Loadout")end)
 button(H.LobbyBar,"TREINAR",1100,791,245,74,function()H.Send("Train")end)
 H.Currency=text(H.LobbyBar,"",UDim2.fromOffset(1100,35),UDim2.fromOffset(310,45),24)
 H.ProfileLabel=text(H.LobbyBar,"",UDim2.fromOffset(30,795),UDim2.fromOffset(335,75),22)
 H.MenuBlur=Instance.new("BlurEffect");H.MenuBlur.Name="PaddleMenuBlur";H.MenuBlur.Size=0;H.MenuBlur.Parent=workspace.CurrentCamera
 H.Settings={FOV=C.BaseFOV,Volume=1,Sensitivity=1}
''' +s[pos:]
s=s.replace('if H.MenuOpen then H.ShowPage("Home") end','if H.MenuOpen then H.ShowPage("Home") end\n Tween:Create(H.MenuBlur,TweenInfo.new(.18),{Size=H.MenuOpen and 8 or 0}):Play()')
# Insert actual functional pause grid and settings before legacy modes page.
s=s.replace('local title=page=="Home" and "PADDLE BRAWL"', 'local title=page=="Home" and "Menu do Jogo" or page=="Modes" and "MODOS DE JOGO" or page=="Settings" and "CONFIGURAÇÕES" or page=="Ranking" and "RANKING DO SERVIDOR"')
s=s.replace(' if page=="Home" then\n  text(f,d and', ''' if page=="Home" then
  local entries={{"Voltar ao Jogo","Play",function()H.ToggleMenu()end},{"Loja","Shop",function()H.ShowPage("Shop")end},{"Inventário","Inventory",function()H.ShowPage("Loadout")end},{"Tarefas","Tasks",function()H.ShowPage("Dailies")end},{"Configurações","Settings",function()H.ShowPage("Settings")end},{H.InMatch and "Sair da Partida" or "Modos de Jogo","Exit",function()if H.InMatch then H.Send("Leave") else H.ShowPage("Modes")end end}}
  for i,v in entries do local b=button(f,"",((i-1)%3)*245,90+math.floor((i-1)/3)*165,235,150,v[3]);sprite(b,v[2],UDim2.fromOffset(86,18),UDim2.fromOffset(64,64));text(b,v[1],UDim2.fromOffset(10,99),UDim2.fromOffset(215,36),22) end
  button(f,"×",670,0,60,50,function()H.ToggleMenu()end)
 elseif page=="Settings" then
  for i,row in {{"Campo de visão","FOV",60,100,5},{"Volume","Volume",0,1,.1},{"Sensibilidade","Sensitivity",.2,2,.1}} do
   local value=H.Settings[row[2]];text(f,row[1]..": "..string.format("%.1f",value),UDim2.fromOffset(20,90+(i-1)*95),UDim2.fromOffset(430,55),25)
   for j,delta in {-1,1} do button(f,j==1 and "−" or "+",485+(j-1)*110,90+(i-1)*95,95,55,function()H.Settings[row[2]]=math.clamp(value+delta*row[5],row[3],row[4]);UIS.MouseDeltaSensitivity=H.Settings.Sensitivity;game:GetService("SoundService"):SetAttribute("PaddleVolume",H.Settings.Volume);H.ShowPage("Settings")end) end
  end
 elseif page=="Ranking" then
  local list=Players:GetPlayers();table.sort(list,function(a,b)return (a:GetAttribute("PaddleElo") or 0)>(b:GetAttribute("PaddleElo") or 0)end)
  for i,p in list do if i>6 then break end;text(f,i..". "..p.DisplayName.." • "..(p:GetAttribute("PaddleElo") or "carregando").." ELO",UDim2.fromOffset(15,75+i*43),UDim2.fromOffset(700,38),23)end
 elseif page=="Modes" then
  text(f,d and''')
s=s.replace('if H.MenuOpen then H.ShowPage(H.CurrentPage or "Home") end', '''for i,q in C.Dailies do local n=math.min(d.Daily[q.Id] or 0,q.Target);local row=H.QuestRows[i];row.Count.Text=n.." / "..q.Target;row.Bar.Size=UDim2.fromOffset(math.max(3,142*n/q.Target),12);row.Bar.ImageColor3=n>=q.Target and Color3.new(1,1,1) or Color3.fromRGB(55,170,255)end
 H.Currency.Text=d.Coins.." moedas   •   "..d.Keys.." chaves"
 H.ProfileLabel.Text=Players.LocalPlayer.DisplayName.."\\nNível "..(1+math.floor(d.XP/150)).." • "..d.Elo.." ELO"
 if H.MenuOpen then H.ShowPage(H.CurrentPage or "Home") end''')
s=s.replace('for i,b in H.Slots do b.ImageColor3=i==d.Slot and H.TeamColor or H.TeamColor:Lerp(Color3.new(.2,.2,.2),.6) end', '''for i,b in H.Slots do b.ImageColor3=i==d.Slot and H.TeamColor or Color3.new(1,1,1);H.SlotIcons[i].Image=A.Images[d.Weapons[i]] or A.Images.Paddle end''')
s=s.replace('UDim2.fromOffset(31,31)','UDim2.fromOffset(47,47)').replace('UDim2.fromOffset(29+n*38,84)','UDim2.fromOffset((team==1 and 14 or 66)+n*53,9)')
s=s.replace('table.insert(H.Avatars,im);n+=1', '''table.insert(H.Avatars,im);local bar=sprite(im,"Health",UDim2.fromOffset(0,47),UDim2.fromOffset(47*math.clamp((s.Health or (s.Alive and 150 or 0))/150,0,1),7));text(im,tostring(s.Level or 1),UDim2.fromOffset(30,31),UDim2.fromOffset(18,16),11);n+=1''')
s=s.replace('H.MenuOpen=not on;', 'H.MenuOpen=false;H.LobbyBar.Visible=not on;H.Ammo.Visible=on;H.Reload.Visible=on;H.MenuBlur.Size=0;')
s=s.replace('H.Menu.Visible=not on;', 'H.Menu.Visible=false;')
s=s.replace('H.Result.Image=A.Images.Panel', 'H.Result.Image=A.Images.Panel')
p.write_text(s,encoding='utf-8')
print('HUD v3 source updated')
