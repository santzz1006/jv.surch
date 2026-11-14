local Root=game.ReplicatedStorage.PaddleBrawl
local W={}
function W.Equip(state)
 local ch=state.Character;local arm=ch and ch:FindFirstChild('Right Arm');if not arm then return end
 local old=ch:FindFirstChild('EquippedPaddle');if old then old:Destroy() end
 local assets=Root:FindFirstChild('WeaponAssets');local id=state.Weapons[state.Slot or 1]
 local source=assets and (assets:FindFirstChild(id) or assets:FindFirstChild('Classic'));if not source then return end
 local model=source:Clone();model.Name='EquippedPaddle';model:ScaleTo(.62)
 model:PivotTo(arm.CFrame*CFrame.new(0,-.95,-.15)*CFrame.Angles(math.pi/2,0,0));model.Parent=ch
 for _,p in model:GetDescendants()do if p:IsA('BasePart')then
  p.Anchored=false;p.CanCollide=false;p.CanTouch=false;p.CanQuery=false;p.Massless=true
  if p.Name=='FrontRubber' then p.Color=state.Team==2 and Color3.fromRGB(255,48,75) or Color3.fromRGB(8,123,255)end
  local weld=Instance.new('WeldConstraint');weld.Part0=arm;weld.Part1=p;weld.Parent=p
 end end
end
return W
