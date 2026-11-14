"""Short original procedural game sounds; no third-party recordings."""
import math,random,wave,struct
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'assets/audio';r.mkdir(exist_ok=True)
random.seed(731);rate=44100
for name,duration,freq in [('Serve',.15,800),('Hit',.21,1350),('Reload',.4,420),('Super',.7,180)]:
 values=[]
 for i in range(int(rate*duration)):
  t=i/rate;envelope=min(1,t/.002)*math.exp(-t/(duration*.2));pitch=freq*(1-.4*t/duration)
  noise=(random.random()*2-1)*(.28 if name=='Serve' else .10)
  sample=(math.sin(2*math.pi*pitch*t)*.7+noise)*envelope*.7
  values.append(struct.pack('<h',round(max(-1,min(1,sample))*32760)))
 with wave.open(str(r/(name+'.wav')),'wb')as f:f.setnchannels(1);f.setsampwidth(2);f.setframerate(rate);f.writeframes(b''.join(values))
print('4 original sound effects generated')
