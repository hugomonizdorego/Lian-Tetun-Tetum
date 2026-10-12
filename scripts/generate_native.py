#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Emit partial, exact-domain catalogs from the checked-in source selections."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
q = lambda value: json.dumps(value, ensure_ascii=False)
directory = ROOT/'native'
directory.mkdir(exist_ok=True)
for record in json.loads((ROOT/'data/native-templates.json').read_text()):
    domain = record['domain']
    header = (f'Project-Id-Version: {domain} Tetun 0.3.0\n'
              'Report-Msgid-Bugs-To: \nPOT-Creation-Date: 2026-10-03 00:00+0000\n'
              'PO-Revision-Date: 2026-10-03 00:00+0000\n'
              'Last-Translator: Edukasaun OS community draft\n'
              'Language-Team: Tetun (INL review pending)\nLanguage: tet\n'
              'MIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\n'
              'Content-Transfer-Encoding: 8bit\nPlural-Forms: nplurals=1; plural=0;\n')
    text = (f"# SPDX-License-Identifier: {record['catalog_license']}\n"
            '# Copyright (C) 2026 Edukasaun OS contributors (original Tetun translations)\n'
            '# Partial draft; exact upstream IDs/contexts. Not endorsed by INL.\n'
            '# Original upstream notices and license: upstream/native-notices/' + domain + '.txt\n'
            + '\n'.join(line for line in record['original_header'].splitlines() if not line.startswith('#,')) + '\nmsgid ""\nmsgstr ' + q(header) + '\n\n')
    for message in record['messages']:
        text += '\n'.join(message['comments']) + '\n'
        text += f"#. {message['glossary_id']}; needs-INL-review\n"
        if message['msgctxt'] is not None: text += 'msgctxt ' + q(message['msgctxt']) + '\n'
        text += 'msgid ' + q(message['msgid']) + '\nmsgstr ' + q(message['translation']) + '\n\n'
    (directory/(domain + '.po')).write_text(text, encoding='utf-8')
    print(f"{domain}: {record['translated_count']}/{record['source_message_count']} messages (partial)")
