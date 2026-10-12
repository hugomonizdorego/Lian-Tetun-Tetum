#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Install the language pack under a GNU/Linux prefix (FHS layout).

Used by `make install` and therefore by debhelper's dh_auto_install. Nothing is
executed on the target: locale compilation and login activation are separate.
"""
import argparse
from pathlib import Path
from build import ROOT, build_catalogs, copy

PACKAGE='eduka-language-pack-tet'
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--prefix',default='/usr/local')
p.add_argument('--destdir',default='')
p.add_argument('--no-docs',action='store_true',
               help='Skip documentation, examples, license texts and manual page '
                    '(Debian installs these with dh_installdocs/dh_installman).')
args=p.parse_args()
prefix=Path(args.prefix)
if not prefix.is_absolute():p.error('--prefix must be absolute')
target=Path(args.destdir)/str(prefix).lstrip('/') if args.destdir else prefix
if not (ROOT/'build/locale/tet/LC_MESSAGES/edukasaun.mo').is_file():build_catalogs()

share=target/'share'/PACKAGE
for folder in ('src','locale','data','po','qt','upstream','native'):
    for source in sorted((ROOT/folder).rglob('*')):
        if source.is_file() and '__pycache__' not in source.parts:
            copy(source,share/folder/source.relative_to(ROOT/folder))
for source in sorted((ROOT/'build/qt').glob('*.qm')):copy(source,share/'qt'/source.name)
copy(ROOT/'build/qt/mainmenu_tet.qm',target/'share/lxqt/translations/lxqt-panel/mainmenu/mainmenu_tet.qm')
for source in sorted((ROOT/'build/locale/tet/LC_MESSAGES').glob('*.mo')):
    copy(source,target/'share/locale/tet/LC_MESSAGES'/source.name)
copy(ROOT/'locale/tet_TL',target/'share/i18n/locales/tet_TL')
copy(ROOT/'bin/eduka-tet',target/'bin/eduka-tet',0o755)
copy(ROOT/'data/eduka-tet.desktop',target/'share/applications/eduka-tet.desktop')
copy(ROOT/'data/eduka-tet.svg',target/'share/icons/hicolor/scalable/apps/eduka-tet.svg')

if not args.no_docs:
    doc=target/'share/doc'/PACKAGE
    for source in sorted((ROOT/'docs').glob('*.md')):copy(source,doc/source.name)
    for source in sorted((ROOT/'examples').glob('*.py')):copy(source,doc/'examples'/source.name)
    for source in sorted((ROOT/'LICENSES').glob('*.txt')):copy(source,doc/'LICENSES'/source.name)
    for source in ('README.md','LICENSE'):copy(ROOT/source,doc/source)
    copy(ROOT/'debian/copyright',doc/'copyright')
    copy(ROOT/'docs/eduka-tet.1',target/'share/man/man1/eduka-tet.1')
print(f'Installed {PACKAGE} under {target}. Locale compilation and login activation are separate.')
