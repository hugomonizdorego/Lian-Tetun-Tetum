# Written-language policy — community proposal

The target is written Official Tetun with INL orthographic conventions, based
on Tetun-Prasa. Government Decree 1/2004 identifies INL as the scientific
custodian. This package is not itself an INL publication or approval.

- UTF-8, normalized to NFC. Preserve vowel distinctions, acute accents and
  meaningful apostrophes. Do not strip accents to simplify identifiers.
- Prefer INL-oriented loanword forms using ñ and ll where appropriate. Native
  sequences containing n+h/l+h must not be changed by a blanket replacement.
- Preserve native long-vowel distinctions such as `hare` and `haree`.
- Use one ASCII apostrophe U+0027 in machine-readable project strings.
  Typographic apostrophes can be normalized deliberately by the text tool.
- Keep brand names, file extensions, command names, IP addresses, placeholders
  and technical identifiers unchanged. Translatable display names can differ
  from immutable code identifiers.
- The technical register is a proposal. Terms such as `arkivu`, `seña`,
  `ambiente servisu`, `atallu` and borrowed IT terminology need INL and
  user review. Do not describe them as verified national glossary entries.
- The gettext plural expression is a draft one-form policy using count-neutral
  Tetun wording, e.g. `Arkivu %d`. It is not asserted to be a CLDR plural rule.
- ISO 14651 generic collation is inherited at compile time. Tetun-specific
  ordering of digraphs has not been researched or certified here.
- Date format, decimal/group separators, Monday as first weekday, USD and A4
  are project defaults, separately reviewable from spelling.

DIT materials are useful comparative references. Do not silently merge a DIT
word list into an INL glossary. Keep alternative forms, source/license and a
review decision before adopting an entry. `tet` and `tdt` are separate registered
language identifiers; this project uses `tet` as requested, not as a claim that
all Tetun varieties are the same.

The normalizer deliberately does not add accents, change all nh/lh, translate
arbitrary text, or claim to be a spell checker. Those operations need licensed,
reviewed lexical data and word-specific rules.


## 0.2.0 reference comparison

The supplied DIT Word-Finder, second edition (2015), explicitly discusses nh/lh
in its spelling notes (PDF p. 7). INL-oriented ñ/ll forms in this draft must still
be reviewed word by word: native sequences such as bainhira must not be replaced
by a global search-and-replace. The Hull books' printed titles/editions and rights
are recorded in SOURCES.md; their association with INL does not grant this
project INL approval or copyright permission. Proposed computer terminology,
mnemonics, invariant count wording, collation and regional defaults remain
review items. Dictionaries are references, not an automatically merged corpus.


## 0.3.0 spelling and grammar rules

The 0.3.0 review applied these rules to every catalog. Each change is listed
with its reason in `data/corrections.csv` and summarized in
[CORRECTIONS.md](CORRECTIONS.md). `scripts/check_tetun.py` (run by `make check`)
rejects regressions.

1. **Negative prefix `dez-`**: `dezliga`, `dezmonta`, `dezativa`, `dezinstala`
   (never `des-`).
2. **Accents follow stress, not Portuguese spelling**: a vowel-final word with
   penultimate stress has no accent (`reinisia`, `mikrofone`); a
   consonant-final word with penultimate stress keeps it (`disponível`,
   `vizível`, `ezekutável`).
3. **Portuguese `-io` endings become `-iu`**: `sítiu`, `relójiu`, `kalendáriu`.
4. **No Portuguese function words** inside Tetun phrases: no `de`, `sem`,
   `com`; use `laho` (without), `ho` (with) and Tetun word order
   (`ambiente servisu`, `rede laho fiu`).
5. **No gender agreement** on loans: adjectives take the masculine `-u` form
   (`másimu`, `blokeadu`); `rejeitada`, `másima` are not used.
6. **Ongoing actions use `hela`** after the verb: `Deskarrega hela...`,
   `Instala hela...`, `Hala'o hela`. A bare verb reads as a command.
7. **Word order is subject–verb–object**: `La hetan arkivu` (not
   `Arkivu la hetan`).
8. **Native Tetun words are preferred** when they are established and
   unambiguous: `fahe` (share), `laho` (without), `servisu` (work).
9. **`lian` means language**; sound is `áudiu` to avoid ambiguity.
10. **Kept international labels**: `OK`, brand and protocol names (`Wi-Fi`,
    `Bluetooth`, `VPN`, `Proxy`), units and keyboard key names.
