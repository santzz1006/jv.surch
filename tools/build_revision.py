import asyncio,os
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path(__file__).resolve().parents[1]
async def main():
 server=StdioServerParameters(command='C:/Users/neila/.codex/tools/blender-mcp/Scripts/mcp-for-blender.exe',env=dict(os.environ,BLENDER_PORT='9877',DISABLE_TELEMETRY='true'))
 async with stdio_client(server) as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   async def run(code,label):
    result=await s.call_tool('execute_blender_code',{'code':code,'user_prompt':'os icones que vc gerou estão sem cores, melhorar as animações e os mapas a interface, seguindo o prompt que mandei'})
    (ROOT/'docs'/('v3-'+label+'.json')).write_text(result.model_dump_json(),encoding='utf-8');print(label,'ERROR' if result.isError else 'OK',flush=True)
    if result.isError:raise RuntimeError(str(result))
   await run(f"exec(compile(open('{ROOT.as_posix()}/tools/blender_ui_v3.py',encoding='utf-8').read(),'ui_v3','exec'))",'ui-load')
   for key in ['Panel','Button','Slot','Health','ScoreBlue','ScoreRed','MapCard','Heart','Crosshair','Paddle','Balls','Shield','Sprint','Reload','Crate','Trophy','Star','Play','Shop','Inventory','Settings','Exit','Hourglass','Tasks','Chart','Coin','Key']:
    await run(f"bpy.app.driver_namespace['pb_ui_render']('{key}')",key)
   await run(f"exec(compile(open('{ROOT.as_posix()}/tools/blender_paddles_v3.py',encoding='utf-8').read(),'paddles_v3','exec'))",'weapons-load')
   for key in ['Classic','LongSmash','TripleServe','RallyRapid','SpinMaster','Homing','MegaSmash','Melee']:
    await run(f"bpy.app.driver_namespace['pb_paddle_v3']('{key}')",key)
asyncio.run(main())
