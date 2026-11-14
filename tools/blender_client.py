"""Official MCP Python SDK client for the project's isolated Blender server."""
import asyncio,json,os,sys
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
 env=dict(os.environ,BLENDER_PORT='9877',DISABLE_TELEMETRY='true')
 server=StdioServerParameters(command='C:/Users/neila/.codex/tools/blender-mcp/Scripts/mcp-for-blender.exe',env=env)
 async with stdio_client(server) as (read,write):
  async with ClientSession(read,write) as session:
   await session.initialize()
   if len(sys.argv)<2:
    result=await session.list_tools()
   else:
    name=sys.argv[1]
    args=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8-sig')) if len(sys.argv)>2 else {}
    result=await session.call_tool(name,args)
   text=result.model_dump_json(indent=2)
   if len(sys.argv)>3:Path(sys.argv[3]).write_text(text,encoding='utf-8')
   print(text,flush=True)

asyncio.run(main())
