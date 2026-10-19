#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Apply data/corrections.csv to the glossary and the native catalog sources.

Idempotent: a correction is applied only where the old wording is still
present. Native messages are matched by their glossary id, so accelerators
(_ or &) and trailing punctuation around the term are preserved.
"""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def load(path):
    with path.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

corrections={r['id']:r for r in load(ROOT/'data/corrections.csv')}
rows=load(ROOT/'data/glossary.csv')
changed=0
for row in rows:
    c=corrections.get(row['id'])
    if c and row['tetun']==c['old']:row['tetun']=c['new'];changed+=1
with (ROOT/'data/glossary.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\r\n');w.writeheader();w.writerows(rows)

def replace_term(text,old,new):
    """Replace old (ignoring one accelerator marker) keeping case of first letter."""
    plain=text.replace('_','',1) if '_' in text else text
    accel=plain!=text
    for o,n in ((old,new),(old[0].lower()+old[1:],new[0].lower()+new[1:])):
        if o in plain:
            plain=plain.replace(o,n,1)
            return ('_'+plain) if accel else plain
    return text

templates=json.loads((ROOT/'data/native-templates.json').read_text(encoding='utf-8'))
native=0
for record in templates:
    for message in record['messages']:
        c=corrections.get(message['glossary_id'])
        if not c:continue
        new=replace_term(message['translation'],c['old'],c['new'])
        if new!=message['translation']:message['translation']=new;native+=1
(ROOT/'data/native-templates.json').write_text(json.dumps(templates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'glossary: {changed} corrected; native catalogs: {native} messages corrected')
