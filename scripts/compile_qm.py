#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Small deterministic QM writer for this project's non-plural Qt TS catalog.

This is not a general replacement for Qt Linguist. Context, source text and
optional disambiguation are preserved; numerus/id-based entries are rejected.
File format reference: Qt qtbase v6.8.3 src/corelib/kernel/qtranslator.cpp.
No Qt implementation is bundled in this source file.
"""
import struct,sys,xml.etree.ElementTree as ET
from pathlib import Path
MAGIC=bytes.fromhex('3cb86418caef9c95cd211cbf60a1bddd')

def integer(n): return struct.pack('>I',n)
def field(tag,value): return bytes([tag])+integer(len(value))+value

def hash_text(text):
    result=0
    for byte in text:
        result=(result<<4)+byte
        high=result & 0xf0000000
        if high: result ^= high>>24
        result &= ~high
    return result or 1

def compile_ts(source,output):
    ts=ET.parse(source).getroot(); records=[]; seen=set()
    for ctx in ts.findall('context'):
        context=ctx.findtext('name','')
        for message in ctx.findall('message'):
            if message.get('numerus') or message.get('id'):
                raise ValueError('Use Qt Linguist for numerus/id-based catalogs.')
            translation=message.find('translation')
            if translation is None or translation.get('type') in ['unfinished','vanished','obsolete']: continue
            text=message.findtext('source',''); translated=translation.text or ''
            comment=message.findtext('comment','')
            key=(context,text,comment)
            if key in seen: raise ValueError(f'Duplicate Qt key: {key}')
            seen.add(key)
            if not translated: continue
            records.append((context.encode(),text.encode(),comment.encode(),translated.encode('utf-16-be')))
    messages=bytearray(); offsets=[]
    for context,text,comment,translated in records:
        offsets.append((hash_text(text+comment),len(messages)))
        messages.extend(field(7,context)+field(6,text)+field(8,comment+b'\0')+field(3,translated)+b'\x01')
    hashes=b''.join(integer(h)+integer(off) for h,off in sorted(offsets))
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    Path(output).write_bytes(MAGIC+field(0xa7,ts.get('language','tet').encode())+field(0x42,hashes)+field(0x69,messages))
    return len(records)

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: compile_qm.py INPUT.ts OUTPUT.qm')
    print('Qt messages:',compile_ts(sys.argv[1],sys.argv[2]))
