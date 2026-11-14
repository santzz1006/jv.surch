local Root=game.ReplicatedStorage.PaddleBrawl
local Animation=require(script.Parent.AnimationController)
local V={};V.__index=V
local function block(name,size,color,parent)
 local p=Instance.new('Part');p.Name=name;p.Size=size;p.Color=color;p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.CastShadow=false;p.Material=Enum.Material.SmoothPlastic;p.Parent=parent;return p
end
function V.new(camera)
 local self=setmetatable({Camera=camera,Animator=Animation.new(),Weapon='Classic',Color=Color3.fromRGB(8,123,255)},V)
 self.Model=Instance.new('Model');self.Model.Name='PaddleViewmodelV3';self.Model.Parent=camera
 self.Right=block('R6RightArm',Vector3.new(.57,1.4,.57),Color3.fromRGB(255,206,155),self.Model)
 self.Left=block('R6LeftArm',Vector3.new(.57,1.4,.57),Color3.fromRGB(255,206,155),self.Model)
 self.Ball=block('ServeBall',Vector3.one*.32,Color3.fromRGB(250,252,255),self.Model);self.Ball.Shape=Enum.PartType.Ball
 self:Equip('Classic',true);return self
end
function V:SetCharacter(ch)
 local arm=ch:FindFirstChild('Right Arm');local skin=arm and arm.Color or Color3.fromRGB(255,206,155);self.Right.Color=skin;self.Left.Color=skin
end
function V:SetColor(color)
 self.Color=color
 if self.Racket then for _,p in self.Racket:GetDescendants()do if p:IsA('BasePart') and p.Name=='FrontRubber' then p.Color=color end end end
end
function V:Equip(id,immediate)
 self.Weapon=id
 if not immediate then self.Pending=id;self.SwitchAt=os.clock();self.Animator:Play('Switch');return end
 if self.Racket then self.Racket:Destroy() end
 local assets=Root:FindFirstChild('WeaponAssets');local source=assets and (assets:FindFirstChild(id) or assets:FindFirstChild('Classic'))
 if not source then return end
 self.Racket=source:Clone();self.Racket.Name='Racket';self.Racket:ScaleTo(.58);self.Racket.Parent=self.Model
 for _,p in self.Racket:GetDescendants() do if p:IsA('BasePart')then p.Anchored=true;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.CastShadow=false end end
 self:SetColor(self.Color)
end
function V:Play(kind,options)
 if self.Pending and kind~='Switch' then return end
 self.Animator:Play(kind,options)
end
local function limb(part,wrist,elbow)
 local delta=wrist-elbow;part.Size=Vector3.new(.57,delta.Magnitude,.57);part.CFrame=CFrame.lookAt((wrist+elbow)/2,wrist)*CFrame.Angles(math.pi/2,0,0)
end
function V:Update(dt,state)
 self.Model.Parent=state.Visible and self.Camera or nil
 local anim=self.Animator:Update(dt,state)
 if self.Pending and os.clock()-(self.SwitchAt or 0)>=.14 then local id=self.Pending;self.Pending=nil;self:Equip(id,true) end
 local cam=self.Camera.CFrame
 local grip=cam*CFrame.new(1.12,-1.22,-2.55)*CFrame.Angles(math.rad(-9),math.rad(-13),math.rad(-12))*anim.Grip
 local leftHand=cam:PointToWorldSpace(Vector3.new(-.68,-1.05,-2.2)+anim.Left)
 limb(self.Right,grip.Position,cam:PointToWorldSpace(Vector3.new(1.47,-2.05,-1.05)))
 limb(self.Left,leftHand,cam:PointToWorldSpace(Vector3.new(-1.2,-2.0,-.95)))
 if self.Racket then self.Racket:PivotTo(grip) end
 self.Ball.Position=leftHand+cam.UpVector*(.35+math.max(0,anim.Left.Y)*.25);self.Ball.Transparency=anim.Ball>.35 and 0 or 1
 self.Ball.Size=Vector3.new(.32,.32+.08*math.max(0,anim.Left.Y),.32)
 if anim.Super and self.Racket then for _,p in self.Racket:GetDescendants()do if p:IsA('BasePart') and p.Name=='FrontRubber' then p.Material=Enum.Material.Neon end end
 elseif self.Racket then for _,p in self.Racket:GetDescendants()do if p:IsA('BasePart') and p.Name=='FrontRubber' then p.Material=Enum.Material.SmoothPlastic end end end
 return anim
end
function V:Destroy() self.Model:Destroy() end
return V
