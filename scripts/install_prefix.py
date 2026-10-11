#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install sources/catalogs under a GNU/Linux prefix; no dpkg or root in DESTDIR."""
import argparse
from pathlib import Path
from build import ROOT, build_catalogs, copy

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--prefix',default='/usr/local')
p.add_argument('--destdir',default='')
args=p.parse_args()
prefix=Path(args.prefix)
if not prefix.is_absolute():p.error('--prefix must be absolute')
target=Path(args.destdir)/str(prefix).lstrip('/') if args.destdir else prefix
build_catalogs()
share=target/'share/eduka-language-pack-tet'
for folder in ('src','locale','data','po','qt','upstream','native','examples'):
    for source in (ROOT/folder).rglob('*'):
        if source.is_file() and '__pycache__' not in source.parts:
            copy(source,share/folder/source.relative_to(ROOT/folder))
for source in (ROOT/'build/qt').glob('*.qm'):copy(source,share/'qt'/source.name)
for source in (ROOT/'build/locale/tet/LC_MESSAGES').glob('*.mo'):
    copy(source,target/'share/locale/tet/LC_MESSAGES'/source.name)
copy(ROOT/'locale/tet_TL',target/'share/i18n/locales/tet_TL')
copy(ROOT/'bin/eduka-tet',target/'bin/eduka-tet',0o755)
doc=target/'share/doc/eduka-language-pack-tet'
for source in (ROOT/'docs').glob('*'):copy(source,doc/source.name)
for source in (ROOT/'LICENSES').glob('*.txt'):copy(source,doc/'LICENSES'/source.name)
for source in ('README.md','LICENSE'):copy(ROOT/source,doc/source)
copy(ROOT/'debian/copyright',doc/'copyright')
print(f'Installed sources/catalogs under {target}. Locale compilation and login activation are separate.')
