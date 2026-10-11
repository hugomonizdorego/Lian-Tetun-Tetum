# Application and upstream integration

## Gettext: Eduka applications

Installed catalog: `/usr/share/locale/tet/LC_MESSAGES/edukasaun.mo`.
Domain: `edukasaun`. English message IDs must match exactly, including punctuation.
Using a generic English-to-Tetun dictionary does not translate an application
whose source never calls gettext. Adapt the supplied example to your application.

```python
import gettext
tr = gettext.translation('edukasaun', '/usr/share/locale', languages=['tet'], fallback=True)
_ = tr.gettext
print(_('Check Again'))
print(tr.ngettext('%d file', '%d files', 3) % 3)
```

For system-following language selection, omit `languages=['tet']` and initialize
Python's libc locale with `locale.setlocale(locale.LC_ALL, '')`. Honor existing
LANG/LANGUAGE and retain an English fallback. Do not force Tetun on every user.
For Qt widgets built in Python, gettext is also usable directly for display text.

Own application-specific catalogs are preferable once full source/POT files are
available. Use `msgmerge` with exact extracted IDs, check placeholders with
`msgfmt --check --check-format`, and test screenshots. This release does not
invent application-specific contexts for unavailable Eduka source code.

## Qt: explicit catalog loading

Installed catalog:
`/usr/share/eduka-language-pack-tet/qt/edukasaun_tet.qm`.
All 432 generic entries have the context `Edukasaun`.

```python
from PyQt5.QtCore import QCoreApplication, QTranslator
translator = QTranslator(application)
if translator.load('/usr/share/eduka-language-pack-tet/qt/edukasaun_tet.qm'):
    application.installTranslator(translator)
label.setText(QCoreApplication.translate('Edukasaun', 'Settings'))
```

Keep the translator alive for the application's lifetime. Use the equivalent
PySide6 API for Qt 6. Recognize `tet` from LANG/LANGUAGE before choosing this file;
see `examples/qt_integration.py`. Unknown locales can map to `C` in Qt, so the
QLocale-based overload is insufficient for Tetun on the inspected versions.
The `.qm` file changes strings only; Qt number/date/calendar formatting remains
limited by its built-in locale data. Use glibc/Python locale for these formats.

The included QM writer deliberately supports only non-numerus TS messages with
explicit contexts/source text and optional disambiguation. For a general Qt
project, use Qt Linguist's `lrelease`. It can compile these non-plural TS files,
but the language may be unknown to its locale tables. Do not add numerus TS
entries to this limited writer; use count-neutral gettext wording instead.

## LXQt main menu

The draft catalog was made from the exact upstream panel 2.1.4 template:
31/31 message records have translations. This is the **main-menu plugin only**,
not all panel plugins or all LXQt applications. Catalog installation path:

`/usr/share/lxqt/translations/lxqt-panel/mainmenu/mainmenu_tet.qm`

Stock liblxqt 2.1.0 obtains its locale from `QLocale::system().name()`, which can
return `C` for `tet`. Therefore this catalog needs upstream/distro integration.
The package **does not replace liblxqt or apply a binary patch**.

For maintainers working from matching liblxqt source:

```sh
# In the liblxqt 2.1.0 source tree:
patch --dry-run -p1 < /path/to/liblxqt-2.1.0-tet-locale.patch
patch -p1 < /path/to/liblxqt-2.1.0-tet-locale.patch
# Rebuild using that project's Debian packaging/build dependencies.
```

The patch preserves raw Tetun POSIX identifiers for translation-file lookup.
It honors `LC_ALL`, then `LC_MESSAGES`, then `LANG`; every other language uses
normal QLocale selection. It does not add Tetun date/number/plural support to Qt.
Patch applicability is checked against the pinned source. This environment did
not build or launch a patched LXQt desktop; do that in a Debian 13 VM before
including a patched liblxqt in an Edukasaun OS release. Verify the installed
plugin path against the target liblxqt build's translation directory.

The provenance file records upstream URLs and hashes. Follow upstream
contribution rules and keep the LGPL notices when submitting the translation or
patch. No PR has been submitted by this release workflow.

## Wider Debian contribution

1. Review the locale with INL/native speakers and research Tetun collation and
   regional choices before proposing it upstream to glibc.
2. Propose Qt/CLDR/ICU language support separately; installing a locale on disk
   does not change those libraries' supported-language tables.
3. Translate actual POT/TS files of LXQt, libfm-qt, PCManFM-Qt, QTerminal and
   applications, preserving contexts, licensing, plural forms and accelerators.
4. Package approved data with Debian policy/DFSG-compatible rights and contact
   Debian localization/upstream teams. A local .deb is not archive acceptance.
5. Integrate into the installer/image only after fresh-install, upgrade, locale
   fallback, accessibility and removal tests on actual target machines.


## Native desktop catalogs (0.2.0)

Thirteen real GNU gettext domains are compiled into the normal
`/usr/share/locale/tet/LC_MESSAGES/DOMAIN.mo` directory. These include original
translations of selected upstream singular labels, with exact message contexts
and mnemonic syntax. They are partial and retain the app's source-compatible GNU
license. DESKTOPS.md and native-manifest.json give per-domain counts/versions.
KDE KI18n and GNOME/GTK loaders still need verification in the actual target
application; this package does not change toolkit language tables.

Edit `data/native-templates.json` (each record's messages) for selected native
translations; edit glossary.csv for own-domain terminology. Generated native PO
files are recreated by generate_native.py during build, so direct PO edits alone
will be overwritten. When adding source messages, update the corresponding
manifest count and preserve upstream notices/rights. A translated source label
must not be reassigned to a context that has a different meaning. Format strings
and native plurals require dedicated review and are excluded from these partial
native selections.
