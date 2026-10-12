# Validation — 0.2.0

Executed 2026-10-03 in Ubuntu 24.04, glibc 2.39, Python 3.12 and Qt 5.15, with a
separate temporary PyQt5 runtime. These are source/package checks, not completed
graphical desktop acceptance tests on Debian 13.

- 24 behavioral checks passed, including real QTranslator verification.
- All 432 own-domain gettext labels and the count-neutral plural phrase matched;
  all 432 own Qt messages and 31 LXQt main-menu records loaded/translated.
- All 1,553 native gettext records across 13 domains matched exact contexts and
  expected translations; wrong-context and untranslated lookups fell back.
  `msgfmt --check --check-format` passed for every PO; header language is `tet`.
- Selected native IDs/contexts were independently checked against the actual
  inspected upstream PO files; all 13 recorded source hashes matched.
- The full locale compiled without warnings; months, date output, USD, yes/no
  expressions, regeneration and temporary execution passed. Expected deliberately
  invalid test input failed without replacing previous generated data.
- Locale ownership/symlink checks preserved external data.
- Login/Plasma configuration restoration, retained unrelated edits, duplicate
  INI/block rejection, XDG paths, private journal permissions, idempotency and
  simulated write failures passed.
- AccountsService success, conflict and rollback paths passed through a simulated
  public API. The real service/GDM authorization/login path was not run here.
- Unicode normalization retained lexical distinctions and did not blindly convert
  DIT spellings to INL.
- Conventional `dpkg-buildpackage -us -uc -A` built the all-architecture package,
  buildinfo and changes files successfully. Older dpkg needs explicit binary
  Priority; it is included while source Priority uses the Policy default.
- Native Debian source (`.dsc` / `.tar.xz`) is generated without build directories,
  private configuration, PDF scans, OCR extracts or downloaded research files.
- Repeated final binary builds produced identical SHA-256 hashes; the Debian
  source was extracted and rebuilt with an identical binary result.
- Extracted binary payload MD5 sums matched; the installed-path launcher loaded
  its modules, own catalogs and doctor metadata correctly.
- A staged `/usr/local` prefix installation loaded catalogs through its installed
  launcher. This is not an acceptance test on other libc families/distributions.
- Maintainer shell scripts passed syntax checks; package payload ownership is
  root/root and there are no writable-by-all files. The locale source is provided
  at the canonical `/usr/share/i18n/locales/tet_TL` path.

The Debian Policy 4.7.4.1 manual/upgrade checklist was inspected;
Standards-Version is 4.7.4. Lintian is not installed in this execution environment.
The source's Debian 13 CI install/compile/purge job is prepared, not executed on
GitHub in this session. Full apt/dpkg install and display-manager login still
require the actual Debian/Edukasaun OS environment. No graphical GNOME, Cinnamon,
KDE, Xfce, MATE, LXDE, LXQt or other desktop session was launched here.

The optional liblxqt 2.1.0 patch was checked against pinned source in 0.1.0; its
content is unchanged. The patched library has not been compiled/launched here.
Stock Qt locale-format tables may still map `tet_TL` to `C`.

Before a school deployment: run the provided Debian CI; complete the
per-desktop X11/Wayland and upgrade/removal checks in DESKTOPS.md; obtain
native-speaker/INL approval of terms, grammar, mnemonics and locale choices.
Book/source attribution is included, but protected dictionary copying is not
licensed by those references and is deliberately excluded.

## 0.2.1 packaging update

Executed 2026-10-11 in Ubuntu 24.04 (debhelper 13.14, lintian 2.117):

- `dpkg-buildpackage -us -uc` built source and binary packages with `dh`;
  the 24-test suite ran in `dh_auto_test` (1 optional Qt test skipped).
- `lintian -I --pedantic`: no errors; only `newer-standards-version` (the
  installed lintian predates 4.7.4) and informational notices about runtime
  data under `/usr/share/eduka-language-pack-tet`.
- `apt install` compiled `/usr/lib/locale/tet_TL.utf8`; `date` printed
  `Kuarta 25 Novembru`; `eduka-tet demo` loaded the installed catalogs.
  `apt remove` and `apt purge` both removed the generated locale.
- Not yet run: the GitHub Actions job on Debian 13 and graphical desktop sessions.

## 0.3.0 Tetun corrections and LXQt

Executed 2026-10-12 (Ubuntu 24.04 container, glibc 2.39, Python 3.13):

- `scripts/check_tetun.py`: 6,187 translations (glossary, 14 native PO, own
  Qt catalog, 57 LXQt TS) — 0 problems. Before the fixes it reported the 45
  glossary errors now listed in CORRECTIONS.md and 9 native entries without
  their trailing space.
- LXQt catalogs: all 3,677 translated messages looked up through a real Qt 6.11
  `QTranslator` (PyQt6) per context, plural forms included — 0 mismatches.
- Loader patches: patched and unpatched `lxqttranslator.cpp` (master and 2.1.0),
  the lxqt-build-tools and qps loader templates and the application call form
  compiled with g++ against Qt 6.4.2. With `LANG=tet_TL.UTF-8` unpatched code
  shows `Search`, patched code `Buka`; `en_US` and `pt_PT` unchanged. Every patch
  passes `git apply --check` on master and on its Debian 13 release tag
  (liblxqt and libfm-qt have separate 2.1.0 versions; qps 2.1.0 needs only the
  lxqt-build-tools patch).
- `eduka-tet enable/disable --desktop lxqt`: session.conf keys set, LC_ALL
  removed, other settings kept, original restored exactly (unit test).
- Not run: a full LXQt session with rebuilt liblxqt, and review of the LXQt
  translations by INL/native speakers.
