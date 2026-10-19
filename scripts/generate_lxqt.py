#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate Tetun Qt catalogs for LXQt from upstream templates and a TM.

    generate_lxqt.py --import DIR [DIR ...]   # refresh message lists
    generate_lxqt.py                          # refill translations only

Message lists are the union of every imported upstream checkout (for example
LXQt master and the 2.1.x release in Debian 13), so one catalog serves both.
Translations come from data/lxqt-tm.json: "source" keys apply everywhere,
"context\\u0004source" keys override one context and
"catalog\\u0004context\\u0004source" keys override one catalog's context.
Missing entries stay unfinished and fall back to English at run time.
"""
import argparse,json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'lxqt'
MANIFEST=ROOT/'data/lxqt-manifest.json'
TM=ROOT/'data/lxqt-tm.json'
LXQT='/usr/share/lxqt/translations'
# Repositories whose catalogs are not installed under LXQT_TRANSLATIONS_DIR.
APP_DIRS={'pcmanfm-qt':'/usr/share/pcmanfm-qt/translations',
          'libfm-qt':'/usr/share/libfm-qt6/translations',
          'lximage-qt':'/usr/share/lximage-qt/translations',
          'lxqt-archiver':'/usr/share/lxqt-archiver/translations',
          'obconf-qt':'/usr/share/obconf-qt/translations',
          'pavucontrol-qt':'/usr/share/pavucontrol-qt/translations',
          'qps':'/usr/share/qps/translations',
          'qterminal':'/usr/share/qterminal/translations',
          'qtermwidget':'/usr/share/qtermwidget6/translations',
          'screengrab':'/usr/share/screengrab/translations'}
GPL={'pcmanfm-qt','lximage-qt','lxqt-archiver','obconf-qt','pavucontrol-qt',
     'qps','qterminal','qtermwidget','screengrab'}
LANG_SUFFIX=re.compile(r'_[a-z]{2,3}(_[A-Z]{2}|@\w+|_[A-Za-z]+)?\.ts$')


def install_dir(repo,template):
    name=template.stem
    if repo in APP_DIRS:return APP_DIRS[repo]
    if repo=='lxqt-panel' and template.parts[-3].startswith('plugin-'):return f'{LXQT}/lxqt-panel/{name}'
    if repo=='lxqt-policykit':return f'{LXQT}/lxqt-policykit'
    return f'{LXQT}/{name}'


def read_template(path):
    messages=[]
    for ctx in ET.parse(path).getroot().findall('context'):
        context=ctx.findtext('name','')
        for m in ctx.findall('message'):
            t=m.find('translation')
            if t is not None and t.get('type') in ('vanished','obsolete'):continue
            messages.append({'context':context,'source':m.findtext('source',''),
                             'comment':m.findtext('comment'),'numerus':m.get('numerus')=='yes'})
    return messages


def import_upstream(dirs):
    catalogs={}
    for base in map(Path,dirs):
        for repo_dir in sorted(p for p in base.iterdir() if (p/'.git').exists()):
            repo=repo_dir.name
            head=subprocess.run(['git','-C',str(repo_dir),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
            ref=subprocess.run(['git','-C',str(repo_dir),'describe','--tags','--exact-match'],capture_output=True,text=True).stdout.strip() or 'master'
            for template in sorted(repo_dir.glob('**/translations/*.ts')):
                if LANG_SUFFIX.search(template.name):continue
                key=template.stem
                cat=catalogs.setdefault(key,{'catalog':key,'repo':repo,
                    'template':str(template.relative_to(repo_dir)),
                    'install_dir':install_dir(repo,template.relative_to(repo_dir)),
                    'license':'GPL-2.0-or-later' if repo in GPL else 'LGPL-2.1-or-later',
                    'upstream':[],'messages':[]})
                cat['upstream'].append({'url':f'https://github.com/lxqt/{repo}','ref':ref,'commit':head})
                seen={(m['context'],m['source'],m['comment']) for m in cat['messages']}
                for m in read_template(template):
                    if (m['context'],m['source'],m['comment']) not in seen:
                        cat['messages'].append(m);seen.add((m['context'],m['source'],m['comment']))
    for cat in catalogs.values():
        cat['messages'].sort(key=lambda m:(m['context'],m['source'],m['comment'] or ''))
    return [catalogs[k] for k in sorted(catalogs)]


def write_ts(cat,tm):
    ts=ET.Element('TS',version='2.1',language='tet_TL',sourcelanguage='en')
    done=0;contexts={}
    for m in cat['messages']:
        ctx=contexts.get(m['context'])
        if ctx is None:
            ctx=contexts[m['context']]=ET.SubElement(ts,'context');ET.SubElement(ctx,'name').text=m['context']
        msg=ET.SubElement(ctx,'message')
        if m['numerus']:msg.set('numerus','yes')
        ET.SubElement(msg,'source').text=m['source']
        if m['comment'] is not None:ET.SubElement(msg,'comment').text=m['comment']
        key=m['context']+'\u0004'+m['source']
        text=tm.get(cat['catalog']+'\u0004'+key,tm.get(key,tm.get(m['source'])))
        tr=ET.SubElement(msg,'translation')
        if not text:tr.set('type','unfinished');continue
        done+=1
        if m['numerus']:ET.SubElement(tr,'numerusform').text=text
        else:tr.text=text
    ET.indent(ts)
    path=OUT/(cat['catalog']+'_tet.ts')
    body=ET.tostring(ts,encoding='unicode')
    header=('<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n'
            f"<!-- SPDX-License-Identifier: {cat['license']} -->\n"
            f"<!-- Tetun translation of LXQt {cat['repo']} ({cat['catalog']}); "
            'Edukasaun OS community draft, INL review pending. -->\n')
    path.write_text(header+body+'\n',encoding='utf-8')
    return done


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--import',dest='dirs',nargs='+',metavar='DIR')
    args=p.parse_args()
    if args.dirs:
        catalogs=import_upstream(args.dirs)
    else:
        catalogs=json.loads(MANIFEST.read_text(encoding='utf-8'))
        for cat in catalogs:cat['messages']=read_template(OUT/(cat['catalog']+'_tet.ts'))
    tm=json.loads(TM.read_text(encoding='utf-8')) if TM.exists() else {}
    OUT.mkdir(exist_ok=True)
    total=translated=0
    for cat in catalogs:
        n=write_ts(cat,tm);translated+=n;total+=len(cat['messages'])
        cat['messages_total']=len(cat['messages']);cat['translated']=n
    meta=[{k:v for k,v in cat.items() if k!='messages'} for cat in catalogs]
    MANIFEST.write_text(json.dumps(meta,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    print(f'LXQt: {len(catalogs)} catalogs, {translated}/{total} messages translated')

if __name__=='__main__':main()
