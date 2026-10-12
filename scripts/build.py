#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Generate all catalogs and resources offline; no root or network needed.

Debian packages are built with dpkg-buildpackage (debian/rules uses debhelper);
this script only produces the architecture-independent build/ tree.
"""
from pathlib import Path
import shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent


def build_catalogs():
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_catalogs.py')],check=True)
    mo=ROOT/'build/locale/tet/LC_MESSAGES/edukasaun.mo';mo.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['msgfmt','--check','--check-format',str(ROOT/'po/tet.po'),'-o',str(mo)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/compile_qm.py'),str(ROOT/'qt/edukasaun_tet.ts'),str(ROOT/'build/qt/edukasaun_tet.qm')],check=True)
    for source in sorted((ROOT/'lxqt').glob('*_tet.ts')):
        subprocess.run([sys.executable,str(ROOT/'scripts/compile_qm.py'),str(source),str(ROOT/'build/lxqt'/(source.stem+'.qm'))],check=True,stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_native.py')],check=True)
    for source in sorted((ROOT/'native').glob('*.po')):
        output=ROOT/'build/locale/tet/LC_MESSAGES'/(source.stem+'.mo')
        subprocess.run(['msgfmt','--check','--check-format',str(source),'-o',str(output)],check=True)
    subprocess.run([sys.executable,str(ROOT/'scripts/generate_resources.py')],check=True)


def copy(source,destination,mode=0o644):
    destination.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,destination);destination.chmod(mode)


if __name__=='__main__':build_catalogs()
