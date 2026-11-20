"""Create a reproducible public ZIP, excluding the private collector configuration."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import json

ROOT = Path(__file__).parent
SOURCE = ROOT / 'extension-shop'
FILES = ['manifest.json','background.js','cloud.js','dashboard.html','dashboard.css','dashboard.js','core.js','reader.js','page-tools.js','popup.html','popup.css','popup.js','privacy.html','LEIA-ME.md','icons/16.png','icons/48.png','icons/128.png']

def build():
    version=json.loads((SOURCE/'manifest.json').read_text(encoding='utf-8'))['version']
    dest=ROOT/'public'/'downloads'/f'goofish-br-extensao-{version}.zip'
    dest.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(dest,'w',ZIP_DEFLATED) as archive:
        for filename in FILES:
            archive.write(SOURCE/filename,filename)
    print(dest)
    cloud=ROOT/'cloudflare'
    cloud_dest=dest.parent/f'goofish-br-cloudflare-{version}.zip'
    cloud_files=['package.json','package-lock.json','wrangler.jsonc','LEIA-ME.md','.gitignore','migrations/0001_initial.sql','src/model.mjs','src/worker.mjs','test/worker.test.mjs']
    with ZipFile(cloud_dest,'w',ZIP_DEFLATED) as archive:
        for filename in cloud_files:
            archive.write(cloud/filename,filename)
    print(cloud_dest)
    return dest

if __name__=='__main__':build()
