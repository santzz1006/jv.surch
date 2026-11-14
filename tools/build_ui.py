import asyncio,json,os
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
async def main():
 server=StdioServerParameters(command='C:/Users/neila/.codex/tools/blender-mcp/Scripts/mcp-for-blender.exe',env=dict(os.environ,BLENDER_PORT='9877',DISABLE_TELEMETRY='true'))
 async with stdio_client(server) as (r,w):
  async with ClientSession(r,w) as s:
   await s.initialize()
   await s.call_tool('execute_blender_code',{'code':"exec(compile(open('C:/Users/neila/OneDrive/Desktop/roblox/tools/blender_ui.py',encoding='utf-8').read(),'blender_ui.py','exec'))",'user_prompt':'refaça todos os icones e coisas'})
   for key in ['Panel','Button','Slot','Health','Score','MapCard','Heart','Crosshair','Paddle','Balls','Shield','Sprint','Reload','Crate','Trophy','Star']:
    result=await s.call_tool('execute_blender_code',{'code':f"import bpy;bpy.app.driver_namespace['pb_ui_render']('{key}')",'user_prompt':'refaça todos os icones e coisas'})
    Path(f'docs/ui-{key}.json').write_text(result.model_dump_json(),encoding='utf-8');print(key,flush=True)
asyncio.run(main())
