-- Bounded local presentation pools. Authoritative projectile simulation stays on the server.
local Pool={};Pool.__index=Pool
function Pool.new(parent,max)
 return setmetatable({Parent=parent,Free={},Live={},Count=0,Max=max or 256},Pool)
end
function Pool:Acquire(size,color)
 local p=table.remove(self.Free)
 if not p then
  if self.Count>=self.Max then return nil end
  p=Instance.new('Part');p.Name='PooledEffect';p.Shape=Enum.PartType.Ball;p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.CastShadow=false;p.Material=Enum.Material.Neon
  local a=Instance.new('Attachment');a.Name='TrailA';a.Position=Vector3.new(0,.14,0);a.Parent=p
  local b=Instance.new('Attachment');b.Name='TrailB';b.Position=Vector3.new(0,-.14,0);b.Parent=p
  local t=Instance.new('Trail');t.Attachment0=a;t.Attachment1=b;t.FaceCamera=true;t.LightEmission=1;t.Lifetime=.14;t.Parent=p;self.Count+=1
 end
 p.Size=Vector3.one*size;p.Color=color;p.Transparency=0;p.Trail.Color=ColorSequence.new(color);p.Trail.Enabled=true;p.Trail:Clear();p.Parent=self.Parent;self.Live[p]=true;return p
end
function Pool:Release(p)
 if not self.Live[p] then return end
 self.Live[p]=nil;p.Trail.Enabled=false;p.Trail:Clear();p.Parent=nil;table.insert(self.Free,p)
end
function Pool:Destroy()
 for p in self.Live do p:Destroy()end;for _,p in self.Free do p:Destroy()end;table.clear(self.Live);table.clear(self.Free)
end
return Pool
