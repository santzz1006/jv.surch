"""Translate all collected text locally and persist it for static navigation."""
import json
import re
import time
from pathlib import Path
import ctranslate2
import argostranslate.package as packages
import catalog

ROOT=Path(__file__).parent
CACHE=ROOT/'translations.json'

def models():
    installed=packages.get_installed_packages();result=[]
    for source,target in [('zh','en'),('en','pt')]:
        model=next(p for p in installed if p.from_code==source and p.to_code==target)
        result.append((model,ctranslate2.Translator(str(model.package_path/'model'),device='cpu',compute_type='int8',inter_threads=1,intra_threads=4)))
    return result

def translate_many(texts,loaded):
    values=texts
    for model,translator in loaded:
        tokens=[model.tokenizer.encode(s) for s in values]
        translated=translator.translate_batch(tokens,beam_size=2,max_batch_size=32,max_decoding_length=512,target_prefix=[[model.target_prefix]]*len(tokens) if model.target_prefix else None)
        values=[model.tokenizer.decode(r.hypotheses[0]).removeprefix(model.target_prefix).strip() if model.target_prefix else model.tokenizer.decode(r.hypotheses[0]) for r in translated]
    return values

def run():
    cache=json.loads(CACHE.read_text(encoding='utf-8')) if CACHE.exists() else {}
    texts=set()
    data=catalog.export()
    for item in data['items']:
        texts.update(x for x in [item.get('title'),item.get('description'),item.get('area'),item.get('seller',{}).get('creditLabel'),*item.get('tags',[])] if isinstance(x,str) and x.strip() and re.search('[\u3400-\u9fff]',x))
    pending=[s for s in texts if s not in cache]
    print(f'{len(pending)} textos para traduzir; {len(cache)} em cache.',flush=True)
    loaded=models()
    for offset in range(0,len(pending),16):
        batch=pending[offset:offset+16]
        segments=[];mapping=[]
        for text in batch:
            pieces=re.split(r'(?<=[。！？!?\n])',text);chunks=[]
            for piece in pieces:
                for start in range(0,len(piece),180):chunks.append(piece[start:start+180])
            mapping.append(len(chunks));segments.extend(chunks)
        output=translate_many(segments,loaded);cursor=0
        for text,count in zip(batch,mapping):cache[text]=' '.join(output[cursor:cursor+count]);cursor+=count
        temp=CACHE.with_suffix('.tmp');temp.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf-8');temp.replace(CACHE)
        catalog.export()
        print(f'Traduzidos {min(offset+16,len(pending))}/{len(pending)} textos',flush=True)
    print('Tradução concluída.',flush=True)

if __name__=='__main__':run()
