#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Check every Tetun catalog for technical errors and known spelling mistakes.

Technical checks (source vs. translation): printf/Qt placeholders, keyboard
accelerators, HTML/XML tags, trailing colon/ellipsis and edge whitespace.
Spelling/grammar checks implement docs/ORTHOGRAPHY.md (0.3.0 rules); words that
also occur in the English source (names, commands) are never flagged.
Exit status is non-zero when any error is found.
"""
import csv,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'scripts'))
from catalog_tools import parse_po

PLACEHOLDER=re.compile(r'%(?:L?\d+|Ln|n|[-+ #0]*\d*(?:\.\d+)?[sdifuxXcp%]|[FUu])')
HTML=('a b i u p br hr html head body span small strong nobr ul ol li table tbody '
      'tr td th h1 h2 h3 center font qt pre em').split()
TAG=re.compile(r'</?(' + '|'.join(HTML) + r')\b',re.I)
ACCEL=re.compile(r'(?<!&)&(?![&#\w]+;)(?!&)(?=\S)')
WORD=re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*")
# Wrong form -> rule (see docs/ORTHOGRAPHY.md).
WRONG={
 'traballu':'Portuguese word; use servisu',
 'sem':'Portuguese "sem"; use laho','com':'Portuguese "com"; use ho',
 'rejeitada':'no feminine agreement; use rejeitadu or rephrase',
 'másima':'no feminine agreement; use másimu',
 'disponivel':'accent required: disponível','vizivel':'accent required: vizível',
 'kompativel':'accent required: kompatível','posivel':'accent required: posível',
 'reinísia':'no accent: reinisia','mikrofóne':'no accent: mikrofone',
 'sítio':'-io becomes -iu: sítiu','botaun':'spelling: butaun',
 'largura':'Portuguese; use luan',
}
PROGRESSIVE=re.compile(r'(Applying|Checking|Connecting|Copying|Creating|Deleting|Detecting|'
  r'Downloading|Extracting|Installing|Loading|Moving|Preparing|Processing|Removing|'
  r'Renaming|Saving|Searching|Updating|Uploading)\b.*(\.\.\.|…)')
DES=re.compile(r"^des(liga|monta|ativa|instala|bloke|konekta|kompresa|enkripta)",re.I)


def technical(source,target):
    errors=[]
    if sorted(PLACEHOLDER.findall(source))!=sorted(PLACEHOLDER.findall(target)):
        errors.append('placeholders differ')
    if len(ACCEL.findall(source))!=len(ACCEL.findall(target)):
        errors.append('accelerator (&) count differs')
    if sorted(t.lower() for t in TAG.findall(source))!=sorted(t.lower() for t in TAG.findall(target)):
        errors.append('HTML tags differ')
    for suffix in (':','...','…'):
        if source.rstrip().endswith(suffix)!=target.rstrip().endswith(suffix):
            errors.append(f'trailing "{suffix}" differs');break
    if source[:1].isspace()!=target[:1].isspace() or source[-1:].isspace()!=target[-1:].isspace():
        errors.append('leading/trailing whitespace differs')
    return errors


def spelling(source,target):
    errors=[]
    known={w.lower() for w in WORD.findall(source)}
    for word in WORD.findall(target):
        low=word.lower()
        if low in known:continue
        if low in WRONG:errors.append(f'"{word}": {WRONG[low]}')
        elif DES.match(low):errors.append(f'"{word}": negative prefix is dez-')
    if PROGRESSIVE.fullmatch(source) and ' hela' not in target:
        errors.append('ongoing action needs "hela"')
    return errors


def pairs():
    with (ROOT/'data/glossary.csv').open(encoding='utf-8',newline='') as f:
        for r in csv.DictReader(f):yield 'data/glossary.csv',r['english'],r['tetun']
    for po in sorted((ROOT/'native').glob('*.po')):
        for e in parse_po(po.read_text(encoding='utf-8')):
            if e.get('msgid') and e.get('msgstr'):yield str(po.relative_to(ROOT)),e['msgid'],e['msgstr']
    for ts in [ROOT/'qt/edukasaun_tet.ts',*sorted((ROOT/'lxqt').glob('*.ts'))]:
        if not ts.exists():continue
        for m in ET.parse(ts).getroot().iter('message'):
            tr=m.find('translation')
            if tr is None or tr.get('type')=='unfinished':continue
            text=tr.findtext('numerusform') if m.get('numerus')=='yes' else tr.text
            if text:yield str(ts.relative_to(ROOT)),m.findtext('source'),text


def main():
    count=0;bad=0
    for where,source,target in pairs():
        count+=1
        for problem in technical(source,target)+spelling(source,target):
            bad+=1;print(f'{where}: {problem}\n  en:  {source!r}\n  tet: {target!r}',file=sys.stderr)
    print(f'check_tetun: {count} translations checked, {bad} problems')
    return 1 if bad else 0

if __name__=='__main__':sys.exit(main())
