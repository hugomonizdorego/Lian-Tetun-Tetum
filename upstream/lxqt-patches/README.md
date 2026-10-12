# LXQt loader patches for Tetun (and other languages unknown to Qt)

Qt's `QLocale` has no Tetun data, so `QLocale::system().name()` is `C` under
`LANG=tet_TL.UTF-8` and LXQt never opens `*_tet.qm`. These patches replace
`QLocale::system().name()`-based file names with the QLocale overload of
`QTranslator::load()`, which follows `QLocale::uiLanguages()` (`LANGUAGE`,
`LC_ALL`, `LC_MESSAGES`, `LANG`) and its fallbacks. Languages Qt already knows
behave exactly as before.

| File | Upstream base |
|---|---|
| `liblxqt-tet-locale.patch` | liblxqt master |
| `liblxqt-2.1.0-tet-locale.patch` | liblxqt 2.1.0 (Debian 13) |
| `libfm-qt-tet-locale.patch` | libfm-qt master |
| `libfm-qt-2.1.0-tet-locale.patch` | libfm-qt 2.1.0 (Debian 13) |
| `lxqt-build-tools-tet-locale.patch` | master; also applies to 2.1.0 and 2.4.0 |
| `pcmanfm-qt`, `lximage-qt`, `qterminal` | master; also apply to their 2.1 tags |
| `pavucontrol-qt-tet-locale.patch` | master; also applies to 2.1.0 |
| `qps-tet-locale.patch` | qps master bundles its own loader template; qps 2.1.0 uses lxqt-build-tools' |
| `lxqt-archiver`, `obconf-qt` | master; also apply to 1.4.0 / 0.16.6 |

In a Debian source package: copy the patch to `debian/patches/`, append its
name to `debian/patches/series`, bump the version (e.g. `+edukasaun1`) and
rebuild. LXQt core apps load through liblxqt and need only the liblxqt patch
(no rebuild). screengrab (and qps 2.1.0) generate their loader from
lxqt-build-tools and pick up the change when rebuilt against the patched
lxqt-build-tools. QTermWidget already uses the QLocale overload.
