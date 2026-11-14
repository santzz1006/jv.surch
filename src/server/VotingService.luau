local Voting={}
function Voting.Cast(match,player,value)
 if match.Phase~='Vote' or type(value)~='number' or value%1~=0 or value<0 or value>10 then return false end
 match.Votes[player]=value -- Replaces the previous choice; one vote per member.
 return true
end
function Voting.Winner(match,random)
 random=random or Random.new();local counts={};local high=0;local candidates={}
 for _,index in match.Votes do counts[index]=(counts[index] or 0)+1;high=math.max(high,counts[index])end
 for index,n in counts do if n==high then table.insert(candidates,index)end end
 local selected=#candidates>0 and candidates[random:NextInteger(1,#candidates)] or 0
 if selected==0 then selected=match.Choices[random:NextInteger(1,#match.Choices)]end
 return selected
end
return Voting
