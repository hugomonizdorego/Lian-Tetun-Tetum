# SPDX-License-Identifier: GPL-3.0-or-later
"""Reversible login settings, with a journal and preflight conflict checks."""
import json, os, re, shlex, subprocess, tempfile
from pathlib import Path

LANG = 'tet_TL.UTF-8'
LANGUAGE = 'tet:pt:en'
BEGIN = '# BEGIN EDUKA TETUN LANGUAGE PACK'
END = '# END EDUKA TETUN LANGUAGE PACK'
CATEGORIES = ('CTYPE NUMERIC TIME COLLATE MONETARY MESSAGES PAPER NAME ADDRESS '
              'TELEPHONE MEASUREMENT IDENTIFICATION').split()
BLOCK = (BEGIN + '\n# Login language; log out and sign in again after changing.\n'
         + 'unset LC_ALL ' + ' '.join('LC_' + c for c in CATEGORIES) + '\n'
         + f'export LANG={LANG}\nexport LANGUAGE={LANGUAGE}\n' + END + '\n')
LEGACY_ENV = '# Managed by eduka-language-pack-tet\nLANG=tet_TL.UTF-8\nLANGUAGE=tet:pt:en\n'
ENV = LEGACY_ENV + 'LC_ALL=\n' + ''.join(f'LC_{c}={LANG}\n' for c in CATEGORIES)
DESKTOPS = ('auto', 'generic', 'gnome', 'kde', 'cinnamon', 'xfce', 'mate',
            'lxde', 'lxqt', 'budgie', 'pantheon', 'deepin', 'unity', 'cosmic',
            'sway', 'hyprland', 'i3', 'awesome')


def detect_desktop(env=None):
    env = os.environ if env is None else env
    names = (env.get('XDG_CURRENT_DESKTOP', '') + ':' + env.get('DESKTOP_SESSION', '')).lower()
    for name in DESKTOPS[2:]:
        if name in names or (name == 'kde' and 'plasma' in names): return name
    return 'generic'


def locations(home):
    home = Path(home).absolute()
    # Respect XDG base directories for the actual user's home, not test fixtures.
    def base(variable, default):
        candidate = os.environ.get(variable, '') if home == Path.home().absolute() else ''
        return Path(candidate) if candidate and Path(candidate).is_absolute() else home/default
    config, state = base('XDG_CONFIG_HOME', '.config'), base('XDG_STATE_HOME', '.local/state')
    return {'profile': home/'.profile', 'xsession': home/'.xsessionrc',
            'env': config/'environment.d/60-eduka-tet.conf',
            'plasma_env': config/'plasma-workspace/env/eduka-tet.sh',
            'plasma': config/'plasma-localerc',
            'journal': state/'eduka-tet/session.json'}


def safe_path(path):
    for item in (path, *path.parents):
        if item.is_symlink(): raise RuntimeError(f'Refusing to change a symbolic link: {item}')
    if path.exists() and not path.is_file(): raise RuntimeError(f'Not a regular file: {path}')


def read(path):
    safe_path(path)
    return path.read_text(encoding='utf-8') if path.exists() else None


def write(path, content):
    safe_path(path)
    if content is None:
        if path.exists(): path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
    fd, name = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f: f.write(content)
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name): os.unlink(name)


def strip_block(text):
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise RuntimeError('Malformed managed block; repair the login file before continuing.')
    if BEGIN not in text: return text
    first = text.index(BEGIN)
    try: last = text.index(END, first) + len(END)
    except ValueError as exc: raise RuntimeError('Managed block markers are out of order.') from exc
    if last < len(text) and text[last] == '\n': last += 1
    return text[:first] + text[last:]


def ini_value(text, section, key):
    current, values, sections = None, [], 0
    for line in text.splitlines():
        m = re.fullmatch(r'\s*\[([^]]+)\]\s*', line)
        if m:
            current = m[1]
            if current == section:
                sections += 1
                if sections > 1: raise RuntimeError(f'Duplicate [{section}] sections; resolve them first.')
        elif current == section:
            m = re.match(r'^\s*' + re.escape(key) + r'\s*=(.*)$', line)
            if m: values.append(m[1].strip())
    if len(values) > 1: raise RuntimeError(f'Duplicate {section}/{key} settings; resolve them first.')
    return values[0] if values else None


def ini_set(text, section, key, value):
    ini_value(text, section, key)  # Reject ambiguous duplicate keys before editing.
    lines = text.splitlines(keepends=True)
    start, end = None, len(lines)
    for i, line in enumerate(lines):
        m = re.fullmatch(r'\s*\[([^]]+)\]\s*', line.rstrip('\r\n'))
        if m:
            if start is not None: end = i; break
            if m[1] == section: start = i + 1
    if start is None:
        if value is None: return text
        return text + ('' if not text or text.endswith('\n') else '\n') + f'[{section}]\n{key}={value}\n'
    for i in range(start, end):
        if re.match(r'^\s*' + re.escape(key) + r'\s*=', lines[i]):
            lines[i:i+1] = [] if value is None else [f'{key}={value}\n']
            return ''.join(lines)
    if value is not None:
        if end and not lines[end-1].endswith('\n'): lines[end-1] += '\n'
        lines.insert(end, f'{key}={value}\n')
    return ''.join(lines)


def accounts_language(value=None):
    """Use the public AccountsService interface; never edit its private database."""
    prefix = ['busctl', '--system', '--timeout=10s']
    object_path = f'/org/freedesktop/Accounts/User{os.getuid()}'
    dest = ['org.freedesktop.Accounts', object_path, 'org.freedesktop.Accounts.User']
    if value is None:
        result = subprocess.run(prefix + ['get-property'] + dest + ['Language'],
                                check=True, text=True, capture_output=True, timeout=15)
        words = shlex.split(result.stdout)
        if len(words) != 2 or words[0] != 's': raise RuntimeError('Unexpected AccountsService language response.')
        return words[1]
    subprocess.run(prefix + ['call'] + dest + ['SetLanguage', 's', value],
                   check=True, text=True, capture_output=True, timeout=15)


def undo_entry(entry, current):
    if current == entry['after']: return entry['before']
    if entry['kind'] == 'block':
        if current is None or BLOCK not in current:
            raise RuntimeError('A managed login block has been edited; preserve those edits before disabling.')
        return strip_block(current)
    if entry['kind'] == 'ini':
        text = current or ''
        for item in entry['keys']:
            if ini_value(text, item['section'], item['key']) != item['after']:
                raise RuntimeError('A managed desktop language setting has been edited; resolve it before disabling.')
        for item in entry['keys']: text = ini_set(text, item['section'], item['key'], item['before'])
        return text
    raise RuntimeError('A managed environment file has been edited; preserve it before disabling.')


def change_user(home, enable, desktop='auto', use_accounts=False, account_api=accounts_language):
    paths = locations(home)
    journal_text = read(paths['journal'])
    state = json.loads(journal_text) if journal_text else None
    if state:
        if state.get('schema') != 1: raise RuntimeError('Unsupported session journal version.')
        for name in state['files']:
            if name not in paths or name == 'journal': raise RuntimeError('Invalid session journal entry.')
    desktop = detect_desktop() if desktop == 'auto' else desktop
    warnings = []
    if enable and state:
        if desktop != state['desktop'] or (use_accounts and not state.get('accounts')):
            raise RuntimeError('Disable the previous activation before selecting a different session backend.')
        for name, entry in state['files'].items():
            if read(paths[name]) != entry['after']:
                # Editing outside a block or language key is allowed for disable,
                # but repeat enable never overwrites such changes.
                raise RuntimeError(f'{paths[name]} changed after activation; disable first.')
        if state.get('accounts') and account_api() != state['accounts']['after']:
            raise RuntimeError('AccountsService language changed outside this tool; disable or preserve that choice first.')
        return warnings
    changes, newstate = {}, {'schema': 1, 'desktop': desktop, 'files': {}}
    if enable:
        for name in ('profile', 'xsession'):
            before = read(paths[name]); original = strip_block(before or '')
            after = original + ('\n' if original and not original.endswith('\n') else '') + BLOCK
            # v0.1 block migration: treat the removed old block as package data.
            baseline = original if before and BEGIN in before else before
            newstate['files'][name] = {'kind': 'block', 'before': baseline, 'after': after}
            changes[name] = (before, after)
        for name, value in [('env', ENV)] + ([('plasma_env', BLOCK)] if desktop == 'kde' else []):
            before = read(paths[name])
            if before is not None and before not in (value, LEGACY_ENV):
                raise RuntimeError(f'The environment file has been edited: {paths[name]}')
            changes[name] = (before, value)
            newstate['files'][name] = {'kind': 'owned', 'before': None, 'after': value}
        if desktop == 'kde':
            before = read(paths['plasma']); after = before or ''; keys = []
            for section, key, value in ([('Formats', 'LANG', LANG), ('Translations', 'LANGUAGE', LANGUAGE)]
                                       + [('Formats', 'LC_' + c, LANG) for c in CATEGORIES]
                                       + [('Formats', 'LC_ALL', '')]):
                keys.append({'section': section, 'key': key, 'before': ini_value(after, section, key), 'after': value})
                after = ini_set(after, section, key, value)
            changes['plasma'] = (before, after)
            newstate['files']['plasma'] = {'kind': 'ini', 'before': before, 'after': after, 'keys': keys}
        if use_accounts or desktop == 'gnome':
            try: newstate['accounts'] = {'before': account_api(), 'after': LANG}
            except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                if use_accounts: raise RuntimeError('AccountsService unavailable or denied; use the documented system default method.') from exc
                warnings.append('AccountsService unavailable: GNOME/GDM may require --accounts-service or a system language default.')
    elif state:
        for name, entry in state['files'].items():
            current = read(paths[name])
            changes[name] = (current, undo_entry(entry, current))
        if state.get('accounts') and account_api() != state['accounts']['after']:
            raise RuntimeError('AccountsService language changed outside this tool; preserve that choice before disabling.')
    else:
        # v0.1 installations had no journal. Undo only their exact owned content.
        for name in ('profile', 'xsession'):
            current = read(paths[name])
            if current and BEGIN in current: changes[name] = (current, strip_block(current))
        current = read(paths['env'])
        if current is not None:
            if current not in (ENV, LEGACY_ENV): raise RuntimeError('Environment file was edited; preserve it first.')
            changes['env'] = (current, None)
    account_change = newstate.get('accounts') if enable else (state or {}).get('accounts')
    applied, account_applied = [], False
    try:
        for name, (_, after) in changes.items(): write(paths[name], after); applied.append(name)
        if account_change:
            account_api(account_change['after'] if enable else account_change['before']); account_applied = True
        if enable:
            paths['journal'].parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            write(paths['journal'], json.dumps(newstate, ensure_ascii=False, indent=2) + '\n')
            paths['journal'].chmod(0o600)
        else: write(paths['journal'], None)
    except BaseException:
        for name in reversed(applied): write(paths[name], changes[name][0])
        if account_applied: account_api(account_change['before'] if enable else account_change['after'])
        write(paths['journal'], journal_text)
        raise
    return warnings
