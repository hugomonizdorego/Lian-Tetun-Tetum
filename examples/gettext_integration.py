#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
import gettext,locale
locale.setlocale(locale.LC_ALL,'')
translation=gettext.translation('edukasaun','/usr/share/locale',fallback=True)
_=translation.gettext
print(_('Check Update'))
print(_('Check Again'))
print(translation.ngettext('%d file','%d files',3) % 3)
