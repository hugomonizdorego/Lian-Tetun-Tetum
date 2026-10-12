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

## LXQt (complete draft)

`lxqt/*_tet.ts` holds 57 catalogs (3677/3706 messages) generated from
the upstream templates of LXQt master **and** the 2.1.x releases shipped by
Debian 13, so one catalog serves both. They compile to QM files installed where
each component looks, for example:

| Component | Installed catalog |
|---|---|
| liblxqt, lxqt-panel, lxqt-config-*, lxqt-session, … | `/usr/share/lxqt/translations/NAME/NAME_tet.qm` |
| Panel plugins | `/usr/share/lxqt/translations/lxqt-panel/PLUGIN/PLUGIN_tet.qm` |
| PCManFM-Qt, LXImage-Qt, QTerminal, qps, … | `/usr/share/APP/translations/APP_tet.qm` |
| libfm-qt, QTermWidget | `/usr/share/libfm-qt6/translations/`, `/usr/share/qtermwidget6/translations/` |

To update after a new LXQt release: clone the LXQt repositories (master and the
release tag) into two directories and run
`python3 scripts/generate_lxqt.py --import DIR1 DIR2`. Edit translations only in
`data/lxqt-tm.json` (source text → Tetun; `context\u0004source` or
`catalog\u0004context\u0004source` keys override a single place), then
`make check`.

### Why LXQt needs a loader patch

Qt has no Tetun entry in its CLDR-derived `QLocale` tables. Under
`LANG=tet_TL.UTF-8`, `QLocale::system().name()` returns `C`, and liblxqt and the
LXQt applications build file names from `name()` (`lxqt-panel_C.qm`). liblxqt
also treats `C` as English and stops searching. The catalogs are therefore
installed but not loaded by stock LXQt.

`QLocale::system().uiLanguages()` does contain `tet` (and honours `LANGUAGE`),
and the QLocale overload of `QTranslator::load()` walks that list with the usual
fallbacks (`tet_TL` → `tet`). The patches in `upstream/lxqt-patches/` switch
every loader to that overload:

| Patch | Applies to |
|---|---|
| `liblxqt-tet-locale.patch` / `liblxqt-2.1.0-tet-locale.patch` | Translator for all LXQt core apps, panel plugins and libraries |
| `lxqt-build-tools-tet-locale.patch` | Generated loader used by screengrab and qps 2.1 (rebuild those apps) |
| `qps-tet-locale.patch` | The loader template bundled in qps master |
| `pcmanfm-qt`, `libfm-qt` (master and 2.1.0), `lximage-qt`, `lxqt-archiver`, `obconf-qt`, `qterminal`, `pavucontrol-qt` | Their own `QTranslator` calls |

QTermWidget already uses the QLocale overload and needs no patch. Behaviour for
languages Qt knows is unchanged. Verified here by compiling the patched
`lxqttranslator.cpp` (master and 2.1.0) and the build-tools loader against
Qt 6.4: unpatched code shows English under `LANG=tet_TL.UTF-8`, patched code
loads the Tetun catalog; `en_US` and `pt_PT` behave as before. Each patch was
checked with `git apply --check` against the Debian 13 release tag.

For Edukasaun OS, add the patch to each source package (`debian/patches/` +
`series`, DEP-3 header already included) and rebuild, or forward them upstream
to LXQt; no LXQt binary is replaced by this package. The patches do not add
Tetun number/date formats to Qt; those come from glibc for non-Qt programs.

## Wider Debian contribution

1. Review the locale with INL/native speakers and research Tetun collation and
   regional choices before proposing it upstream to glibc.
2. Propose Qt/CLDR/ICU language support separately; installing a locale on disk
   does not change those libraries' supported-language tables.
3. Submit the LXQt catalogs to LXQt Weblate after INL review, and forward the
   loader patches to the LXQt projects.
4. Package approved data with Debian policy/DFSG-compatible rights and contact
   Debian localization/upstream teams. A local .deb is not archive acceptance.
5. Integrate into the installer/image only after fresh-install, upgrade, locale
   fallback, accessibility and removal tests on actual target machines.


## Native desktop catalogs

Fourteen real GNU gettext domains are compiled into the normal
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
must not be reassigned to a context that has a different meaning. Format strings are allowed only with their `c-format` flag, so `msgfmt
--check-format` and `scripts/check_tetun.py` verify every placeholder. Native
plurals are still excluded.
