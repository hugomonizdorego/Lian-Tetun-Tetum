#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate deterministic PO/POT and explicit-load Qt TS from original glossary."""
import csv,json,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
q=lambda text: json.dumps(text,ensure_ascii=False)
header=('Project-Id-Version: eduka-language-pack-tet 0.2.1\n'
        'Report-Msgid-Bugs-To: \nPOT-Creation-Date: 2026-10-03 00:00+0000\n'
        'PO-Revision-Date: 2026-10-03 00:00+0000\nLast-Translator: Edukasaun OS community\n'
        'Language-Team: Tetun (community draft; INL review pending)\nLanguage: tet\n'
        'MIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\n'
        'Content-Transfer-Encoding: 8bit\nPlural-Forms: nplurals=1; plural=0;\n')
with (ROOT/'data/glossary.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
for pot in [False,True]:
    text='# SPDX-License-Identifier: GPL-3.0-or-later\n# Original AI-assisted draft; no third-party dictionary copied.\nmsgid ""\nmsgstr '+q(header)+'\n\n'
    for row in rows:
        text+=f"#. {row['id']}: {row['review_status']}\nmsgid {q(row['english'])}\nmsgstr {q('' if pot else row['tetun'])}\n\n"
    text+='#. Count-neutral Tetun phrase; one draft gettext plural form.\n#, python-format\nmsgid "%d file"\nmsgid_plural "%d files"\nmsgstr[0] '+q('' if pot else 'Arkivu %d')+'\n'
    (ROOT/'po'/('edukasaun.pot' if pot else 'tet.po')).write_text(text,encoding='utf-8')
ts=ET.Element('TS',version='2.1',language='tet_TL',sourcelanguage='en')
ctx=ET.SubElement(ts,'context');ET.SubElement(ctx,'name').text='Edukasaun'
for row in rows:
    msg=ET.SubElement(ctx,'message');ET.SubElement(msg,'source').text=row['english']
    ET.SubElement(msg,'extracomment').text=row['id']+': draft, needs INL review'
    ET.SubElement(msg,'translation').text=row['tetun']
ET.indent(ts)
ET.ElementTree(ts).write(ROOT/'qt/edukasaun_tet.ts',encoding='utf-8',xml_declaration=True)
print(f'Generated {len(rows)} gettext strings + 1 plural entry; {len(rows)} Qt messages.')
