local Teams={}
function Teams.SpawnOffset(m,index,s)
 if m.Mode=='FFA' then local positions={Vector3.new(-28,4,-28),Vector3.new(28,4,28),Vector3.new(28,4,-28),Vector3.new(-28,4,28)};return positions[(index-1)%#positions+1]end
 local count,ordinal=0,0
 for _,member in m.Members do if member.Team==s.Team then count+=1;if member==s then ordinal=count end end end
 local x=(ordinal-(count+1)/2)*7;return Vector3.new(s.Team==1 and x or -x,4,s.Team==1 and -28 or 28)
end
return Teams
