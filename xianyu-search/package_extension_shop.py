"""Create a reproducible public ZIP, excluding the private collector configuration."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).parent
SOURCE = ROOT / 'extension-shop'
FILES = ['manifest.json','core.js','reader.js','page-tools.js','popup.html','popup.css','popup.js','privacy.html','LEIA-ME.md','icons/16.png','icons/48.png','icons/128.png']

def build():
    version=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))['version']
    dest=ROOT/'public'/'downloads'/f'goofish-br-extensao-{version}.zip'
    dest.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(dest,'w',ZIP_DEFLATED) as archive:
        for filename in FILES:
            archive.write(SOURCE/filename,filename)
    print(dest)
    return dest

if __name__=='__main__':build()
