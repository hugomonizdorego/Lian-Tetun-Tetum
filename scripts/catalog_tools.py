# SPDX-License-Identifier: GPL-3.0-or-later
"""Read conventional gettext PO files for offline validation (not a full editor)."""
import ast


def parse_po(text):
    entries, entry, field = [], {'comments': []}, None
    for line in text.splitlines() + ['']:
        if not line.strip():
            if 'msgid' in entry: entries.append(entry)
            entry, field = {'comments': []}, None
        elif line.startswith('#~'):
            continue  # Obsolete entries are not installed.
        elif line.startswith('#'):
            entry['comments'].append(line)
        elif line.startswith(('msgctxt ', 'msgid ', 'msgid_plural ', 'msgstr ')) or line.startswith('msgstr['):
            field, literal = line.split(' ', 1)
            entry[field] = ast.literal_eval(literal)
        elif line.startswith('"') and field:
            entry[field] += ast.literal_eval(line)
        else:
            raise ValueError('Unsupported PO syntax: ' + line[:100])
    return entries
