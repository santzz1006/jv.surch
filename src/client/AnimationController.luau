-- Camera-relative hand poses. The racket is attached to the hand grip, never animated independently.
local Animation={};Animation.__index=Animation
local I=CFrame.identity
local function pose(x,y,z,rx,ry,rz) return CFrame.new(x,y,z)*CFrame.Angles(math.rad(rx),math.rad(ry),math.rad(rz)) end
local function key(t,cf,left,ball) return {Time=t,Grip=cf,Left=left or Vector3.zero,Ball=ball==nil and 1 or ball} end
local clips={
 Swing={key(0,I),key(.18,pose(.12,.08,.12,-12,28,-16),Vector3.new(.12,.22,-.12)),key(.38,pose(-.50,.13,-.36,-8,-55,22),Vector3.new(.2,.4,-.18),0),key(.60,pose(-.70,-.05,-.22,10,-80,36),Vector3.new(.08,-.1,.1),0),key(1,I)},
 Rapid={key(0,I),key(.20,pose(.02,.03,.05,-5,12,-6)),key(.5,pose(-.13,.04,-.15,-4,-20,10),Vector3.new(0,.08,0),0),key(1,I)},
 Melee={key(0,I),key(.22,pose(.25,.2,.2,-12,50,-35)),key(.5,pose(-.95,.2,-.45,4,-95,50),Vector3.zero,0),key(.72,pose(-.7,-.1,-.1,10,-70,40)),key(1,I)},
 Reload={key(0,I),key(.18,pose(.12,-.3,.1,30,20,-30),Vector3.new(.1,-.3,.05),0),key(.48,pose(-.2,-.05,-.1,80,15,-55),Vector3.new(.8,.22,-.05),0),key(.72,pose(-.1,.04,-.15,50,5,-25),Vector3.new(.4,.35,-.1)),key(1,I)},
 Inspect={key(0,I),key(.23,pose(-.35,.2,-.2,-10,50,-25)),key(.5,pose(-.35,.18,-.16,10,150,-25)),key(.76,pose(-.25,.08,-.1,0,40,15)),key(1,I)},
 Switch={key(0,I),key(.43,pose(.15,-1.5,.3,20,20,40),Vector3.new(0,-1,0),0),key(.52,pose(.15,-1.5,.3,20,20,40),Vector3.new(0,-1,0),0),key(1,I)},
 Parry={key(0,I),key(.2,pose(-.45,.5,-.2,0,-10,75),Vector3.new(.4,.3,0),0),key(.62,pose(-.4,.45,-.12,4,-8,70),Vector3.new(.4,.25,0),0),key(1,I)},
 Super={key(0,I),key(.35,pose(.25,.5,.4,-45,55,-20),Vector3.new(.1,.5,-.2)),key(.48,pose(-.7,.25,-.6,0,-70,45),Vector3.new(.2,.6,-.4),0),key(.7,pose(-.9,-.1,-.2,20,-95,50),Vector3.new(0,-.2,.1),0),key(1,I)},
 Hurt={key(0,I),key(.25,pose(.08,-.12,.18,12,8,-8)),key(1,I)},
}
clips.Precision={key(0,I),key(.16,pose(.08,.06,.18,-12,20,-8)),key(.32,pose(-.35,.1,-.5,0,-40,16),Vector3.new(.18,.4,-.25),0),key(.62,pose(-.55,-.04,-.26,12,-55,28),Vector3.zero,0),key(1,I)}
clips.Spread={key(0,I),key(.15,pose(.24,.1,.1,0,30,-20)),key(.33,pose(-.65,.13,-.3,-12,-60,32),Vector3.new(.25,.4,-.2),0),key(.7,pose(-.8,-.1,-.1,18,-80,40),Vector3.zero,0),key(1,I)}
clips.Spin={key(0,I),key(.15,pose(.12,-.08,.08,10,10,-30)),key(.32,pose(-.4,.25,-.3,-15,-35,55),Vector3.new(.1,.35,-.1),0),key(.64,pose(-.6,.3,-.2,-22,-55,75),Vector3.zero,0),key(1,I)}
clips.Homing={key(0,I),key(.15,pose(.08,.2,.1,-15,15,-15)),key(.3,pose(-.25,.3,-.42,-25,-30,12),Vector3.new(.15,.5,-.2),0),key(.6,pose(-.4,.1,-.2,-5,-45,20),Vector3.zero,0),key(1,I)}
clips.Heavy={key(0,I),key(.14,pose(.22,.22,.2,-25,35,-20)),key(.28,pose(-.65,-.1,-.5,25,-75,38),Vector3.new(.3,.5,-.25),0),key(.58,pose(-.8,-.3,-.1,35,-95,45),Vector3.zero,0),key(1,I)}
local durations={Swing=.24,Rapid=.085,Precision=.4,Spread=.45,Spin=.29,Homing=.45,Heavy=.65,Melee=.45,Reload=1.35,Inspect=1.6,Switch=.28,Parry=.4,Super=.78,Hurt=.22}
local weaponClips={RallyRapid='Rapid',Melee='Melee',LongSmash='Precision',TripleServe='Spread',SpinMaster='Spin',Homing='Homing',MegaSmash='Heavy'}
function Animation.new() return setmetatable({Grip=I,Left=Vector3.zero,At=-10,Duration=.3,Kind=nil,Sway=Vector2.zero,Walk=0},Animation) end
function Animation:Play(kind,options)
 options=options or {};if kind=='Swing' then kind=weaponClips[options.Weapon] or kind end
 self.From=self.Grip;self.FromLeft=self.Left;self.Kind=kind;self.At=os.clock();self.Duration=options.Duration or durations[kind] or .3
end
local function smooth(t) return t*t*(3-2*t) end
function Animation:Update(dt,state)
 local now=os.clock();local cf,left,ball=I,Vector3.zero,1;local age=now-self.At
 local clip=self.Kind and clips[self.Kind]
 if clip and age<self.Duration then
  local t=age/self.Duration;local a,b=clip[1],clip[#clip]
  for i=2,#clip do if clip[i].Time>=t then a=clip[i-1];b=clip[i];break end end
  local alpha=smooth(math.clamp((t-a.Time)/math.max(.001,b.Time-a.Time),0,1));cf=a.Grip:Lerp(b.Grip,alpha);left=a.Left:Lerp(b.Left,alpha);ball=a.Ball+(b.Ball-a.Ball)*alpha
  local blend=math.clamp(age/.035,0,1);cf=(self.From or I):Lerp(cf,blend);left=(self.FromLeft or Vector3.zero):Lerp(left,blend)
 else self.Kind=nil end
 self.Walk+=dt*(state.Sprint and 13 or 9)
 local speed=math.clamp(state.Speed/22,0,1.5);local bob=pose(math.sin(self.Walk)*.025*speed,math.abs(math.sin(self.Walk))*.035*speed,0,0,0,math.sin(self.Walk)*1.1*speed)
 local idle=pose(0,math.sin(now*2.2)*.012,0,math.sin(now*1.4)*.6,0,0)
 local target=state.MouseDelta or Vector2.zero;self.Sway=self.Sway:Lerp(target*.0015,1-math.exp(-16*dt))
 local sway=pose(-self.Sway.X,-self.Sway.Y,0,-self.Sway.Y*80,-self.Sway.X*100,-self.Sway.X*60)
 local stance=I
 if state.Sprint then stance=pose(.15,-.2,.12,-14,15,-20) elseif state.Crouch then stance=pose(.02,-.12,.08,0,0,8) end
 if state.Air then stance=stance*pose(0,-.08,.03,8,0,6) end
 if state.Charge then stance=stance*pose(.08,.15,.12,-18*state.Charge,22*state.Charge,-8*state.Charge) end
 self.Stance=(self.Stance or I):Lerp(stance,1-math.exp(-12*dt));stance=self.Stance
 self.Grip=cf;self.Left=left
 return {Grip=idle*bob*sway*stance*cf,Left=left,Ball=ball,Super=self.Kind=='Super',Kind=self.Kind,Progress=math.clamp(age/self.Duration,0,1)}
end
return Animation
