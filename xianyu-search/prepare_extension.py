"""Pairs the local extension without printing the local secret."""
import json
from pathlib import Path
import bridge
dest=Path(__file__).parent/'extension'/'config.js'
dest.write_text('const ALPHA_BRIDGE_KEY = '+json.dumps(bridge.KEY)+';\n',encoding='utf-8')
print('Extensão preparada em:',dest.parent)
