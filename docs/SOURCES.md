# References, access results and rights

Checked 2026-10-03. References inform technical design and reviewer guidance;
they are not a license to copy the underlying database. No protected dictionary dataset was bulk-collected. Partial native UI catalogs
use compatible GNU-licensed upstream message templates. All 432 glossary entries are original AI-assisted project drafts.

| Reference | What was checked | Distribution decision |
|---|---|---|
| [Library of Congress ISO 639-2 entry](https://www.loc.gov/standards/iso639-2/php/langcodes_name.php?code_ID=442) | `tet` = Tetum; no ISO 639-1 code listed | Reference only; no ISO certification claimed |
| [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry) | Separate `tet` and `tdt` language registrations | Use `tet-TL` as this project's tag; do not treat tdt as a tet alias |
| [Jornal da República, Decree 1/2004](https://mj.gov.tl/jornal/?q=node/1070) | INL orthographic authority, written standard based on Tetun-Prasa | Reference only; no claim of INL authorship/approval |
| [Tetun Translator dictionary](https://translate.tetumdili.com/dictionary) | It provides INL and DIT spelling references | No dictionary, corpus or audio copied |
| [Tetun Translator terms](https://translate.tetumdili.com/terms) | Prohibits scraping/bulk downloading; underlying sources retain their rights | No crawler, export or copied dataset included |
| [Tetun Translator spelling comparison](https://translate.tetumdili.com/ortho) | Comparative spelling information | Reference only; does not replace review of INL's actual guide |
| [Timor Aid national dictionary](https://www.timoraid.org/cp-dictionary-b.php) and [project page](https://www.timoraid.org/tetun-dictionary.php) | Project describes collaboration with INL; no compatible dataset license established on inspected pages | No database copied; request a licensed export for future releases |
| [DIT papers](http://www.tetundit.tl/Papers.html#Articles_on_Tetun) | User-supplied page timed out/returned 502; no full content read | Link retained for reviewers; no material imported |
| [DIT publications](http://www.tetundit.tl/publications.html) and [capitalized path](https://www.tetundit.tl/Publications.html) | Page unavailable during this request; search surfaced an author publications list/bibliography | No glossary imported or claimed reviewed in full |
| [DIT bibliography](https://www.tetundit.tl/Publications/Bibliography%20of%20Tetun%20Dili%202024.pdf) | Indexed bibliography lists dictionaries and comparative literature | Bibliographic reference only; no entries imported |
| Zuzana Greksáková, *Tetun in Timor-Leste: The Role of Language Contact in Its Development*, University of Coimbra, 2018; user-supplied PDF | Section 2.10, printed pp. 66–69, especially INL/DIT orthography and Decree 1/2004 | Academic reference only; the 542-page PDF is not redistributed |
| [Debian Reference, I18N/L10N](https://www.debian.org/doc/manuals/debian-reference/ch08.en.html) | Locale generation, LANG/LANGUAGE, UTF-8 and keyboard configuration | Technical reference |
| [GNU libc locale names](https://sourceware.org/glibc/manual/latest/html_node/Locale-Names.html) | language_territory.codeset syntax, LOCPATH | Technical reference |
| [Debian maintainer-script policy](https://www.debian.org/doc/debian-policy/ch-maintainerscripts.html) | Idempotency and noninteractive installation | Technical reference; package implements ownership checks and triggers |
| [Qt QTranslator](https://doc.qt.io/qt-6/qtranslator.html) and [Qt 6.8 QLocale](https://doc.qt.io/qt-6.8/qlocale.html) | Explicit file-based catalog loading versus built-in locale tables | Technical reference; no Qt locale database modification claimed |
| [Qt translator implementation, v6.8.3](https://raw.githubusercontent.com/qt/qtbase/v6.8.3/src/corelib/kernel/qtranslator.cpp) | QM file tags/hash index for limited deterministic compiler | Format reference; original small writer, no Qt implementation bundled |
| [Debian LXQt catalog file list](https://packages.debian.org/trixie/all/lxqt-panel-l10n/filelist) | Confirmed canonical plugin path under `/usr/share/lxqt/translations/lxqt-panel/mainmenu/` | Technical reference |
| [LXQt panel 2.1.4 template](https://raw.githubusercontent.com/lxqt/lxqt-panel/2.1.4/plugin-mainmenu/translations/mainmenu_en_GB.ts) | Exact 31 message IDs/contexts for Debian 13's panel version | Derivative Tetun TS retains LGPL-2.1-or-later notices |
| [liblxqt 2.1.0 translator source](https://raw.githubusercontent.com/lxqt/liblxqt/2.1.0/lxqttranslator.cpp) | Raw locale is lost through QLocale when Tetun is unsupported | Optional LGPL-2.1-or-later patch; not applied to installed systems |

## Legal scope of GPL

The project's GPL covers original code and terminology, not someone else's
books, translations, recordings or databases. Reusing a dictionary requires
checking its exact license or obtaining compatible written permission. Attribution
alone does not create permission. LXQt-derived materials retain their LGPL
license. GNU generic locale definitions are read from the target system during
compilation; this source does not copy the system's generic locale data.

This inventory records only what was actually accessible. It is not a claim
that every requested source was exhaustively read or imported.


## Dictionaries supplied for 0.2.0

The website fetch of the Word-Finder PDF was unavailable during research; the
user-supplied PDF was inspected instead. `data/source-manifest.json` records
filename, SHA-256, bibliographic metadata and the exact PDF page bearing rights.
The manifest is shipped; none of these books/scans/OCR extracts is shipped.

| Actual book | Edition / publisher | Rights statement inspected | Use in this release |
|---|---|---|---|
| Catharina Williams-van Klinken, *Word-Finder English-Tetun / Tetun-Ingles* | 2nd edition, DIT, 2015; ISBN 978-989-8615-02-2 | PDF p. 2: prior DIT permission required for copying | Introduction/spelling/reference checks; no bulk import or redistribution |
| Geoffrey Hull, *Standard Tetum-English Dictionary* | 3rd edition, Sebastião Aparício da Silva Project in association with INL, 2002; first published 1999; ISBN 1-86508-599-5 | PDF p. 4: reproduction requires written publisher permission | Title/rights/front-matter checked; no dictionary entries redistributed |
| Geoffrey Hull, *Concise English-Tetum Dictionary / Disionáriu Inglés-Tetun* | Sebastião Aparício da Silva Publications, 2006; ISBN 978-1-74138-223-5 | PDF p. 2: integration/alteration/reproduction requires written copyright-holder permission | Title/rights/front-matter checked; no dictionary entries redistributed |

The second English-to-Tetun upload's filename calls it “standard”, but its
printed title is **Concise English-Tetum Dictionary**. Both Hull PDFs are scans;
front matter was OCR-read and visually checked. This release does not claim to
have read/reviewed every entry in either 406-page scan.

DIT's 2015 spelling notes (PDF p. 7, printed p. v) explain its use of nh/lh rather
than former ny/ly, and preservation of native sequences. They support a spelling
comparison, not a blind conversion into INL forms. Technical “file” terminology
varies by source/register; the project's original draft “Arkivu” remains a review
choice rather than a claim that DIT prescribes it. No DIT spelling database is
converted to INL and presented as a licensed original dictionary.

## Desktop / standards sources added for 0.2.0

- [User's desktop list](https://note.com/yuuya20061202/n/n52c963a94b05?hl=en):
  scope inventory only, not copied content or authoritative toolkit guidance.
- [Tetun language overview](https://en.wikipedia.org/wiki/Tetun_language):
  background requested by the user; ISO identifiers are checked against LOC and
  IANA rather than relying on Wikipedia as the registration authority.
- [Debian Policy](https://www.debian.org/doc/debian-policy/) and
  [upgrade checklist](https://www.debian.org/doc/debian-policy/upgrading-checklist.html):
  version 4.7.4.1 inspected; Standards-Version 4.7.4 in source control. Upgrades
  from 4.7.2 concern source Priority defaults and topics not used by this pack.
- [Debian systemd environment.d documentation](https://manpages.debian.org/trixie/systemd/environment.d.5.en.html):
  systemd user-service environment is distinct from every shell/display manager.
- [Plasma 6.3 startup source](https://raw.githubusercontent.com/KDE/plasma-workspace/Plasma/6.3/startkde/startplasma.cpp):
  `plasma-localerc` Formats/Translations and `plasma-workspace/env` startup scripts.
- [AccountsService 23.13.9 public interface](https://gitlab.freedesktop.org/accountsservice/accountsservice/-/raw/23.13.9/data/org.freedesktop.Accounts.User.xml):
  Language / SetLanguage, locale string, own-user PolicyKit permission and display
  manager expectations. Private AccountsService files are not edited by the tool.
- GNU GPL/LGPL texts shipped in LICENSE / LICENSES: original project licensing
  and compatible source contribution rules; they do not license the books.

`data/native-manifest.json` lists all 13 actual upstream catalog URLs, source
versions, PO hashes, GNU licenses and coverage. `native-templates.json` lists only
the selected exact IDs/contexts with original Tetun drafts; the full English
source catalogs are not included. Original upstream notices and license texts
are retained in `upstream/native-notices/`. These are the reusable software
sources for native UI integration, distinct from the permission-required books.
