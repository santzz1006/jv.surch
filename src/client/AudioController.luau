local SoundService=game:GetService('SoundService')
local A={Pools={},Next={}}
local ids={Serve='137276831802452',Hit='117466028976281',Reload='121768627213216',Super='78962580289230'}
function A.Play(kind,pitch)
 local id=ids[kind];if not id then return end
 local pool=A.Pools[kind]
 if not pool then pool={};A.Pools[kind]=pool;for i=1,4 do local s=Instance.new('Sound');s.Name='Paddle'..kind;s.SoundId='rbxassetid://'..id;s.Parent=SoundService;pool[i]=s end end
 local n=(A.Next[kind] or 0)%#pool+1;A.Next[kind]=n;local s=pool[n];s:Stop();s.Volume=(SoundService:GetAttribute('PaddleVolume') or 1)*.5;s.PlaybackSpeed=pitch or 1;s:Play()
end
return A
