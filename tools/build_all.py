import asyncio,json,os
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
ROOT=Path('C:/Users/neila/OneDrive/Desktop/roblox')
async def main():
 server=StdioServerParameters(command='C:/Users/neila/.codex/tools/blender-mcp/Scripts/mcp-for-blender.exe',env=dict(os.environ,BLENDER_PORT='9877',DISABLE_TELEMETRY='true'))
 async with stdio_client(server) as (r,w):
  async with ClientSession(r,w) as session:
   await session.initialize()
   code="exec(compile(open('C:/Users/neila/OneDrive/Desktop/roblox/tools/blender_assets.py',encoding='utf-8').read(),'blender_assets.py','exec'))"
   await session.call_tool('execute_blender_code',{'code':code,'user_prompt':'se conecte ao blender e ao roblox studio e faça o jogo seguindo o prompt abaixo'})
   for key in ['Arena','Ponte','Westown','Cemiterio','Backrooms','Campo','Xadrez','Portao','Parquinho','Experimento']:
    result=await session.call_tool('execute_blender_code',{'code':f"import bpy; bpy.app.driver_namespace['pb_build_map']('{key}')",'user_prompt':'se conecte ao blender e ao roblox studio e faça o jogo seguindo o prompt abaixo'})
    (ROOT/'docs'/f'build-{key}.json').write_text(result.model_dump_json(),encoding='utf-8')
    print(key,result.isError,flush=True)
asyncio.run(main())
