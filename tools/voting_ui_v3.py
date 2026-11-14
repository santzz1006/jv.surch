from pathlib import Path
p=Path(__file__).resolve().parents[1]/'src/client/HUD.luau';s=p.read_text(encoding='utf-8');start=s.index(' H.Vote.Visible=m.Phase==');end=s.index(' for _,im in H.Avatars',start)
s=s[:start]+''' H.Vote.Visible=m.Phase=="Vote";if H.Vote.Visible then
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
''' +s[end:];s=s.replace('page=="Ranking" and "RANKING DO SERVIDOR"','page=="Ranking" and "RANKING DO SERVIDOR" or page=="History" and "HISTÓRICO"');p.write_text(s,encoding='utf-8')
print('Stable vote cards and voter avatars added')
