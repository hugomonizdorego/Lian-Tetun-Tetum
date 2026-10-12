# Edukasaun OS — Tetun language pack

**0.2.1 — community draft; linguistic review by INL/native speakers is pending.**

A desktop-independent Tetun locale and GNU-licensed translation foundation for
Edukasaun OS and Debian. This release contains 432 original draft UI terms,
13 partial native gettext catalogs (1,553 translated message records), own
gettext/Qt catalogs, an LXQt main-menu contribution, and reversible login tools.
The source can be uploaded directly to a new GitHub repository.

It is not an official INL, ISO-certified or Debian archive language pack.
Installing it does not translate every application or complete any desktop UI.
The dictionaries supplied by the user remain references; their entries, scans
and datasets are not redistributed. See [sources](docs/SOURCES.md) and
[per-file licensing](docs/LICENSING.md).

## Install on Debian / Edukasaun OS

```sh
sudo apt install ./eduka-language-pack-tet_0.2.1_all.deb
eduka-tet demo
eduka-tet doctor
eduka-tet enable --user
```

Run activation as the desktop user without sudo, then log out and sign in again.
Desktop detection uses `XDG_CURRENT_DESKTOP` / `DESKTOP_SESSION`. Explicit modes:

```sh
eduka-tet enable --user --desktop kde
eduka-tet enable --user --desktop gnome --accounts-service
eduka-tet disable --user
```

Disable a previous activation before switching its desktop backend. GNOME/GDM
uses the public AccountsService language API when available; Plasma also uses
`plasma-localerc` and its environment startup script. Other sessions use login
profiles, Debian Xsession and systemd user environment settings. See the
[installation guide](docs/INSTALL-ID.md) and [desktop matrix](docs/DESKTOPS.md).

```sh
eduka-tet run -- date '+%A, %d %B %Y'
eduka-tet glossary Settings
eduka-tet resources
```

Missing native translations fall back through `LANGUAGE=tet:pt:en` where the
application honors GNU gettext. Locale, language chooser availability, toolkit
formatting and UI translations are distinct integration tasks.

## Language identifiers and formats

| Use | Identifier / choice |
|---|---|
| ISO 639-2 and ISO 639-3 registered language code | `tet` (Tetum); no ISO 639-1 two-letter code |
| BCP 47 regional language tag | `tet-TL` |
| GNU libc locale | `tet_TL.UTF-8` / generated `tet_TL.utf8` |
| Separate Tetun Dili identifier | `tdt`; not silently aliased to `tet` |
| Text | UTF-8, NFC; original INL-oriented spelling drafts |
| Plurals | One draft gettext form, count-neutral wording; native plural messages not supplied |
| Collation | Generic glibc ISO 14651; no claimed INL-specific tailoring |
| Regional formats | Project defaults: DD/MM/YYYY, 24-hour, USD, A4, metric |

The ISO language code identifies a language; it does not certify these
translations. [Orthography](docs/ORTHOGRAPHY.md) explains the INL/DIT distinction.

## What is included

| Component | Coverage |
|---|---|
| Shared glibc locale | 12 categories, compiled using the target computer's libc |
| Eduka gettext / Qt | 432 original labels + one gettext plural entry; Qt context `Edukasaun` |
| GTK 2 / 3 / 4 | Partial `gtk20`, `gtk30`, `gtk40` catalogs |
| GNOME / Cinnamon | Partial `gnome-shell`, `cinnamon`, `nemo` catalogs |
| Xfce / MATE / LXDE | Partial panel and file-manager catalogs for each |
| KDE | Partial Dolphin catalog; full Plasma/framework translations remain future work |
| LXQt | 31/31 main-menu template records; optional liblxqt source patch, not applied by installer |
| Other desktops / window managers | Shared locale and compatible application catalogs; no dedicated shell catalogs |

Exact source versions, hashes and coverage are in
[data/native-manifest.json](data/native-manifest.json). Qt locale lookup can
fall back to `C` for `tet`; explicit loading and upstream support are documented
in [INTEGRATION.md](docs/INTEGRATION.md). No complete GUI session has been
validated here.

## Build and develop

The package follows the usual GNU and Debian conventions: `make` /
`make check` / `make install PREFIX=... DESTDIR=...`, and a standard
debhelper (`dh`, compat 13) `debian/` directory. On Debian / Edukasaun OS:

```sh
sudo apt install build-essential debhelper gettext locales python3 lintian
make check                     # generate catalogs and run the test suite
dpkg-buildpackage -us -uc      # .deb, .dsc and .tar.xz in the parent directory
lintian ../eduka-language-pack-tet_*.changes
sudo apt install ../eduka-language-pack-tet_0.2.1_all.deb
```

`make deb` is a shortcut for an unsigned binary build. Without dpkg, install
under any prefix with `sudo make install PREFIX=/usr/local`, then run
`sudo eduka-tet compile-locale`.

Optional real Qt runtime checks need `python3-pyqt5`. Builds are offline and do
not require root (`Rules-Requires-Root: no`). The package is `Architecture: all`,
source format `3.0 (native)`, version `0.2.1`. Generated locale binaries are
produced on the target system by `postinst`, not shipped across libc versions,
and are removed again on `apt remove`/`apt purge`. [Portability](docs/PORTABILITY.md)
explains source installation on other glibc-based GNU/Linux systems.

Canonical editable data: `data/glossary.csv`, `data/native-templates.json` and
`locale/tet_TL`. PO/TS files are generated; edit the canonical data before running
`make build`. Preserve message contexts, source notices, placeholders and
per-file licenses. For complete desktop translations, import compatible actual
POT/TS source templates and review every new string. The supplied book references
do not provide permission to bulk-import dictionaries.

## GitHub

Source: <https://github.com/hugomonizdorego/Lian-Tetun-Tetum>. The
`.github/workflows/deb.yml` workflow builds the package in Debian 13 (trixie),
runs the tests and lintian, performs an install/remove/purge check and uploads
the `.deb` as a build artifact. See [VALIDATION.md](docs/VALIDATION.md) for
actual tests and remaining acceptance work.

## License

Code and original terminology: GNU GPL version 3 or later (see `LICENSE`).
Native application catalogs keep their upstream GNU GPL/LGPL licenses; see
`debian/copyright` and [per-file licensing](docs/LICENSING.md).
