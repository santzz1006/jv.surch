"""Start an isolated Blender scene with the official MCP add-on on port 9877."""
import bpy,importlib.util,sys
from pathlib import Path
path='C:/Users/neila/.codex/tools/blender-mcp/Lib/site-packages/blender_mcp/bundled/addon.py'
spec=importlib.util.spec_from_file_location('paddle_mcp_addon',path)
addon=importlib.util.module_from_spec(spec);sys.modules[spec.name]=addon;spec.loader.exec_module(addon)
addon.register()
bpy.context.scene.blendermcp_port=9877
bpy.types.paddle_mcp_server=addon.BlenderMCPServer(port=9877)
bpy.types.paddle_mcp_server.start()
bpy.context.scene.name='PADDLE BRAWL Assets'
Path('C:/Users/neila/OneDrive/Desktop/roblox/docs/blender-ready.txt').write_text(str(bpy.app.version_string))
