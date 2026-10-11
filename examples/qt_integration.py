# SPDX-License-Identifier: GPL-3.0-or-later
"""Call load_tetun(application) after creating your Qt application.

Return/retain the translator to preserve its lifetime. PySide6 also works by
changing this import. This does not modify the Qt QLocale data tables.
"""
import os,re
from PyQt5.QtCore import QTranslator

def wants_tetun():
    # LC_ALL/LC_MESSAGES have the usual locale precedence; LANGUAGE is gettext's
    # explicit translation preference when neither category override is set.
    category=os.environ.get('LC_ALL') or os.environ.get('LC_MESSAGES')
    raw=category or os.environ.get('LANGUAGE') or os.environ.get('LANG','')
    first=raw.split(':',1)[0]
    return bool(re.match(r'^tet(?:$|[_.@-])',first))

def load_tetun(application):
    if not wants_tetun():return None
    translator=QTranslator(application)
    if translator.load('/usr/share/eduka-language-pack-tet/qt/edukasaun_tet.qm'):
        application.installTranslator(translator)
        return translator
    return None
