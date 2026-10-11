#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Reproducible architecture-independent .deb build; no root or network needed."""
from pathlib import Path
import argparse,gzip,hashlib,os,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parent.parent
VERSION='0.2.0'
EPOCH=int(os.environ.get('SOURCE_DATE_EPOCH','1790985600'))


def build_catalogs():
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_catalogs.py')],check=True)
    mo=ROOT/'build/locale/tet/LC_MESSAGES/edukasaun.mo';mo.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['msgfmt','--check','--check-format',str(ROOT/'po/tet.po'),'-o',str(mo)],check=True)
    for source,name in [(ROOT/'qt/edukasaun_tet.ts','edukasaun_tet.qm'),(ROOT/'upstream/mainmenu_tet.ts','mainmenu_tet.qm')]:
        subprocess.run([sys.executable,str(ROOT/'scripts/compile_qm.py'),str(source),str(ROOT/'build/qt'/name)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_native.py')],check=True)
    for source in sorted((ROOT/'native').glob('*.po')):
        output=ROOT/'build/locale/tet/LC_MESSAGES'/(source.stem+'.mo')
        subprocess.run(['msgfmt','--check','--check-format',str(source),'-o',str(output)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_resources.py')],check=True)


def copy(source,destination,mode=0o644):
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,destination);destination.chmod(mode)


def build_deb(output):
    build_catalogs()
    stage=ROOT/'build/package';shutil.rmtree(stage,ignore_errors=True);stage.mkdir(parents=True)
    share=stage/'usr/share/eduka-language-pack-tet'
    for folder in ['src','locale','data','po','qt','upstream','examples','native']:
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                copy(p,share/folder/p.relative_to(ROOT/folder))
    for p in (ROOT/'build/qt').glob('*.qm'):copy(p,share/'qt'/p.name)
    copy(ROOT/'build/qt/mainmenu_tet.qm',stage/'usr/share/lxqt/translations/lxqt-panel/mainmenu/mainmenu_tet.qm')
    for p in (ROOT/'build/locale/tet/LC_MESSAGES').glob('*.mo'):
        copy(p,stage/'usr/share/locale/tet/LC_MESSAGES'/p.name)
    copy(ROOT/'bin/eduka-tet',stage/'usr/bin/eduka-tet',0o755)
    copy(ROOT/'locale/tet_TL',stage/'usr/share/i18n/locales/tet_TL')
    doc=stage/'usr/share/doc/eduka-language-pack-tet'
    for p in (ROOT/'docs').glob('*'):copy(p,doc/p.name)
    for name in ['README.md','LICENSE']:copy(ROOT/name,doc/name)
    copy(ROOT/'debian/copyright',doc/'copyright')
    for p in (ROOT/'LICENSES').glob('*.txt'):copy(p,doc/'LICENSES'/p.name)
    for source,dest in [(ROOT/'debian/changelog',doc/'changelog.gz'),(ROOT/'docs/eduka-tet.1',stage/'usr/share/man/man1/eduka-tet.1.gz')]:
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(gzip.compress(source.read_bytes(),mtime=EPOCH))
    copy(ROOT/'data/eduka-tet.desktop',stage/'usr/share/applications/eduka-tet.desktop')
    copy(ROOT/'data/eduka-tet.svg',stage/'usr/share/icons/hicolor/scalable/apps/eduka-tet.svg')
    control=stage/'DEBIAN';control.mkdir()
    installed=sum(p.stat().st_size for p in stage.rglob('*') if p.is_file())
    (control/'control').write_text(f'''Package: eduka-language-pack-tet
Version: {VERSION}
Architecture: all
Section: localization
Priority: optional
Maintainer: Hugo Moniz do Rego <ideaofficial@fdsl.tl>
Installed-Size: {(installed+1023)//1024}
Depends: python3 (>= 3.9), locales, libc-bin
Recommends: xdg-utils
Suggests: accountsservice, dbus
Homepage: https://www.edukasaunos.tl
Description: Tetun locale and community language resources for Edukasaun OS
 Provides a target-compiled tet_TL.UTF-8 locale, original draft gettext and
 Qt catalogs, partial native desktop catalogs and reversible user tools.
 Orthography targets INL conventions but has not been approved by INL.
 Supports desktop-independent locale use; full UI coverage is not provided.
''')
    for name in ['postinst','postrm','triggers']:copy(ROOT/'debian'/name,control/name,0o755 if name!='triggers' else 0o644)
    sums=[]
    for p in sorted(stage.rglob('*')):
        if p.is_file() and 'DEBIAN' not in p.relative_to(stage).parts:
            sums.append(hashlib.md5(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(stage)))
    (control/'md5sums').write_text('\n'.join(sums)+'\n')
    for p in stage.rglob('*'):os.utime(p,(EPOCH,EPOCH),follow_symlinks=False)
    os.utime(stage,(EPOCH,EPOCH))
    output=Path(output).resolve();output.mkdir(parents=True,exist_ok=True)
    deb=output/f'eduka-language-pack-tet_{VERSION}_all.deb'
    env=dict(os.environ,SOURCE_DATE_EPOCH=str(EPOCH))
    subprocess.run(['dpkg-deb','--root-owner-group','-Zxz','-z9','--build',str(stage),str(deb)],check=True,env=env)
    print(deb)
    return deb

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'dist'));p.add_argument('--catalogs-only',action='store_true')
    args=p.parse_args()
    if args.catalogs_only:build_catalogs()
    else:build_deb(args.output)
