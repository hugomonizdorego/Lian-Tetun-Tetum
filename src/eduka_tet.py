# SPDX-License-Identifier: GPL-3.0-or-later
"""Tetun locale and user-session helpers. Python standard library only."""
from __future__ import annotations
import argparse, csv, datetime, gettext, json, locale, os, re, shutil
import subprocess, sys, tempfile, unicodedata
from pathlib import Path

VERSION = '0.2.0'
DOMAIN = 'edukasaun'
SHARE = Path('/usr/share/eduka-language-pack-tet')
LOCALE_DIR = Path('/usr/share/locale')
LOCALE_NAME = 'tet_TL.UTF-8'
BEGIN = '# BEGIN EDUKA TETUN LANGUAGE PACK'
END = '# END EDUKA TETUN LANGUAGE PACK'


def data_root() -> Path:
    # Source-tree use never changes installed runtime paths.
    source = Path(__file__).resolve().parent.parent
    return source if (source / 'data/metadata.json').is_file() else SHARE


def translations(language='tet'):
    base = data_root()
    directory=base/'build/locale'
    if not (directory/'tet/LC_MESSAGES/edukasaun.mo').is_file(): directory=base.parent/'locale'
    return gettext.translation(DOMAIN, localedir=directory, languages=[language], fallback=True)


def tet_environment(base=None):
    env = dict(os.environ if base is None else base)
    for key in list(env):
        if key == 'LC_ALL' or key.startswith('LC_'):
            env.pop(key)
    env['LANG'] = LOCALE_NAME
    env['LANGUAGE'] = 'tet:pt:en'
    return env


def compile_locale(source: Path, parent: Path):
    """Compile with the target libc; replace only package-owned generated data."""
    parent.mkdir(parents=True, exist_ok=True)
    target = parent / 'tet_TL.utf8'
    marker = target / '.eduka-tet-owner'
    if target.is_symlink() or (target.exists() and (marker.is_symlink() or not marker.is_file() or marker.read_text(encoding='ascii') != 'eduka-language-pack-tet\n')):
        raise RuntimeError(f'Refusing to replace an existing locale not owned by this package: {target}')
    with tempfile.TemporaryDirectory(prefix='.eduka-tet-', dir=parent) as temp:
        compiled = Path(temp) / 'tet_TL.utf8'
        subprocess.run(['localedef', '--no-archive', '-i', str(source), '-f', 'UTF-8', str(compiled)], check=True)
        (compiled / '.eduka-tet-owner').write_text('eduka-language-pack-tet\n', encoding='ascii')
        # Generation is complete before the existing locale is touched.
        backup = Path(temp) / 'old'
        if target.exists():
            target.rename(backup)
        try:
            compiled.rename(target)
        except BaseException:
            if backup.exists(): backup.rename(target)
            raise
    return target


from session import strip_block, write as atomic_write, change_user as change_session, detect_desktop, DESKTOPS, locations


def change_user(home: Path, enable: bool, check_locale=True, desktop='auto', use_accounts=False):
    if enable and check_locale:
        old=locale.setlocale(locale.LC_ALL)
        try: locale.setlocale(locale.LC_ALL,LOCALE_NAME)
        finally: locale.setlocale(locale.LC_ALL,old)
    return change_session(home,enable,desktop,use_accounts)


def normalize(text):
    """Normalize Unicode only. Do not invent accent/dialect conversions."""
    return unicodedata.normalize('NFC',text).translate(str.maketrans({'\u2019':"'",'\u2018':"'",'\u02bc':"'"}))


def load_glossary():
    with (data_root()/'data/glossary.csv').open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))


def main(argv=None):
    parser=argparse.ArgumentParser(description='Tetun language tools for Edukasaun OS and Debian (community draft).')
    parser.add_argument('--version',action='version',version=VERSION)
    sub=parser.add_subparsers(dest='command',required=True)
    sub.add_parser('status',help='Show installed locale, metadata and session environment.')
    sub.add_parser('doctor',help='Check locale, desktop backend and native catalog coverage.')
    sub.add_parser('demo',help='Show an explicitly loaded Tetun translation and date sample.')
    for name in ('enable','disable'):
        p=sub.add_parser(name,help=f'{name.capitalize()} Tetun for the current user; reversible.')
        p.add_argument('--user',action='store_true',required=True)
        if name=='enable':
            p.add_argument('--desktop',choices=DESKTOPS,default='auto')
            p.add_argument('--accounts-service',action='store_true',help='Require the public AccountsService language API (GNOME/GDM).')
    p=sub.add_parser('run',help='Run a command with Tetun locale without changing defaults.')
    p.add_argument('program',nargs=argparse.REMAINDER)
    p=sub.add_parser('glossary',help='Search the original draft terminology list.')
    p.add_argument('query',nargs='?',default='')
    sub.add_parser('normalize',help='Read stdin; NFC and canonical ASCII apostrophes only.')
    sub.add_parser('resources',help='Open the offline searchable glossary and installation guide.')
    p=sub.add_parser('compile-locale',help='Compile locale on the target libc (root required).')
    args=parser.parse_args(argv)
    try:
        if args.command in ('status','doctor'):
            metadata=json.loads((data_root()/'data/metadata.json').read_text())
            old=locale.setlocale(locale.LC_ALL)
            try: locale.setlocale(locale.LC_ALL,LOCALE_NAME); available=True
            except locale.Error: available=False
            finally: locale.setlocale(locale.LC_ALL,old)
            print(json.dumps({'metadata':metadata,'locale_available':available,
                             'environment':{x:os.environ.get(x) for x in ['LANG','LANGUAGE','LC_ALL','LC_MESSAGES']},
                             'desktop_detected':detect_desktop(),
                             'native_catalogs':json.loads((data_root()/'data/native-manifest.json').read_text()),
                             'session_journal':locations(Path.home())['journal'].exists(),
                             'qt_note':'Use explicit filename loading for tet; QLocale may fall back to C.',
                             'coverage_note':'Partial application catalogs; full desktop UI and session startup require target-machine verification.'},ensure_ascii=False,indent=2))
        elif args.command=='demo':
            _=translations().gettext
            print(_('Tetun Language Pack')+' '+VERSION)
            print(_('Community draft; INL review pending.'))
            for label in ['Open','Save','Cancel','Settings','Check Update','Check Again','Restart Required']:
                print(label+' → '+_(label))
            try:
                locale.setlocale(locale.LC_TIME,LOCALE_NAME)
                print(datetime.datetime(2026,11,25,13).strftime('%A, %d %B %Y %T'))
            except locale.Error:
                print('Locale unavailable. Install the .deb package or compile the locale first.')
        elif args.command in ('enable','disable'):
            if os.geteuid()==0:
                raise RuntimeError('Run this command as your normal desktop user, without sudo.')
            warnings=change_user(Path.home(),args.command=='enable',desktop=getattr(args,'desktop','auto'),use_accounts=getattr(args,'accounts_service',False))
            for warning in warnings: print('eduka-tet: '+warning,file=sys.stderr)
            print('Saved. Log out and log in again. See docs/INSTALL-ID.md for session-specific limitations.')
        elif args.command=='run':
            program=args.program
            if program and program[0]=='--': program=program[1:]
            if not program: parser.error('run requires a command after --')
            locale.setlocale(locale.LC_ALL,LOCALE_NAME)
            os.execvpe(program[0],program,tet_environment())
        elif args.command=='glossary':
            query=normalize(args.query).casefold()
            for row in load_glossary():
                if query in (row['english']+' '+row['tetun']).casefold():
                    print(f"{row['english']}\t{row['tetun']}\t[{row['review_status']}]")
        elif args.command=='normalize': print(normalize(sys.stdin.read()),end='')
        elif args.command=='resources':
            subprocess.run(['xdg-open',str(data_root()/'data/resources.html')],check=True)
        elif args.command=='compile-locale':
            if os.geteuid()!=0: raise RuntimeError('compile-locale requires root.')
            print(compile_locale(data_root()/'locale/tet_TL',Path('/usr/lib/locale')))
    except (OSError,ValueError,RuntimeError,locale.Error,subprocess.SubprocessError) as exc:
        print('eduka-tet: '+str(exc),file=sys.stderr);return 1
    return 0

if __name__=='__main__': sys.exit(main())
