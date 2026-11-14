-- PADDLE BRAWL tuning. All authoritative values are read by the server.
local C = {}
C.Version = "0.1.0"
C.Health = 150
C.WalkSpeed = 22
C.SprintSpeed = 30
C.CrouchSpeed = 12
C.SlideSpeed = 42
C.SlideDuration = 0.65
C.SlideCooldown = 1.4
C.JumpPower = 48
C.BunnyHopBonus = 2
C.BunnyHopCap = 34
C.BaseFOV = 76
C.AimFOV = 65
C.RoundSeconds = 90
C.RoundCountdown = 3
C.RoundsToWin = 5
C.VoteSeconds = 8
C.FFASeconds = 180
C.FFATarget = 20
C.RespawnSeconds = 3
C.MaxMatches = 6
C.ArenaSpacing = 650
C.ParryWindow = 0.24
C.ParryCooldown = 0.9
C.ProjectileLife = 4
C.RicochetGain = 1.12
C.MaxBallSpeed = 420
C.MaxProjectiles = 256
C.UltimateRequired = 100
C.UltimateHitCharge = 8
C.UltimateKillCharge = 22
C.UltimateDamage = 120
C.HeadshotMultiplier = 1.6
C.EloK = 28
C.PersistenceEnabled = true -- uses session locking when the experience has API access
C.DataStoreName = "PaddleBrawl_v1"
C.ProfileLockSeconds = 180
C.AutoSaveSeconds = 55
C.RemoteRate = 32
C.RemoteBurst = 52
C.Modes = { ["1v1"] = 2, ["2v2"] = 4, ["3v3"] = 6, FFA = 4 }
C.WeaponOrder = {"Classic","LongSmash","TripleServe","RallyRapid","SpinMaster","Homing","MegaSmash"}
C.Weapons = {
 Classic={Name="Raquete Clássica",Damage=32,Interval=.22,Speed=260,Magazine=12,Reserve=96,Reload=1.35,Bounces=3,Color=Color3.fromRGB(109,87,255)},
 LongSmash={Name="Long Smash",Damage=76,Interval=1,Charge=.65,Speed=400,Magazine=4,Reserve=28,Reload=2.1,Bounces=1,Pierce=2,Color=Color3.fromRGB(43,215,247)},
 TripleServe={Name="Triple Serve",Damage=24,Interval=.7,Speed=235,Magazine=6,Reserve=42,Reload=1.9,Bounces=2,Pellets=3,Spread=.095,Range=85,Color=Color3.fromRGB(255,151,54)},
 RallyRapid={Name="Rally Rapid",Damage=13,Interval=.085,Speed=255,Magazine=32,Reserve=192,Reload=1.65,Bounces=2,Color=Color3.fromRGB(255,83,151)},
 SpinMaster={Name="Spin Master",Damage=30,Interval=.30,Speed=220,Magazine=10,Reserve=70,Reload=1.5,Bounces=4,Curve=.55,Color=Color3.fromRGB(91,239,141)},
 Homing={Name="Homing",Damage=26,Interval=.55,Speed=155,Magazine=6,Reserve=36,Reload=1.8,Bounces=1,Homing=2,TurnRate=2.1,Color=Color3.fromRGB(223,105,255)},
 MegaSmash={Name="Mega Smash",Damage=62,Interval=1.25,Speed=140,Magazine=2,Reserve=14,Reload=2.6,Bounces=1,Radius=9,BallSize=2.3,Color=Color3.fromRGB(255,211,70)},
 Melee={Name="Golpe Curto",Damage=48,Interval=.55,Range=8,Knockback=34,Magazine=1,Reserve=0,Reload=0,Color=Color3.fromRGB(234,244,255)},
 Explosive={Name="Bolinha Explosiva",Damage=48,Interval=.9,Speed=100,Magazine=3,Reserve=0,Reload=0,Bounces=1,Radius=10,BallSize=.9,Color=Color3.fromRGB(255,105,59)},
 Freeze={Name="Bolinha Congelante",Damage=14,Interval=.9,Speed=120,Magazine=3,Reserve=0,Reload=0,Bounces=1,Radius=8,Freeze=2.0,BallSize=.9,Color=Color3.fromRGB(100,232,255)},
}
C.Dailies = {
 {Id="duels",Name="Jogar duelos",Target=5,Coins=120,Keys=1},
 {Id="kills",Name="Eliminações",Target=15,Coins=150,Keys=1},
 {Id="wins",Name="Vença duelos",Target=3,Coins=200,Keys=2},
}
C.Cosmetics = {
 Default={Name="Original",Color=Color3.fromRGB(116,89,255),Rarity="Comum",Price=0},
 Citrus={Name="Citrus",Color=Color3.fromRGB(188,255,51),Rarity="Comum",Price=150},
 Bubblegum={Name="Bubblegum",Color=Color3.fromRGB(255,96,179),Rarity="Raro",Price=350},
 Glacier={Name="Glacier",Color=Color3.fromRGB(72,229,255),Rarity="Raro",Price=350},
 Solar={Name="Solar",Color=Color3.fromRGB(255,193,48),Rarity="Épico",Price=700},
 Nova={Name="Nova",Color=Color3.fromRGB(224,129,255),Rarity="Lendário",Price=1200},
}
C.Crate = {{Id="Citrus",Weight=40},{Id="Bubblegum",Weight=25},{Id="Glacier",Weight=25},{Id="Solar",Weight=8},{Id="Nova",Weight=2}}
C.Season = {Name="Primeiro Saque",XPPerLevel=150,MaxLevel=20,CoinsPerLevel=75}
C.Ranks = {{0,"Bronze"},{1100,"Prata"},{1250,"Ouro"},{1450,"Platina"},{1700,"Diamante"}}
return C
