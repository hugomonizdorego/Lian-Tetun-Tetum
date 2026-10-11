# Review and release gate

Every row in `data/glossary.csv` is currently `needs-INL-review`, including
common-looking words. No row is marked INL-approved merely because it appears
on a dictionary website or was proposed by an AI tool.

1. Have native-speaking translators review meaning in real screenshots of
   EUS, Eduka-Desktop, Eduka-Block and Eduka-Konekta. Record terminology changes.
2. Ask INL to review spelling, approved technical vocabulary, date/month names,
   regional formats, plural wording, and the project's choice of `tet` for
   written Tetun-Prasa. Obtain a written scope and version for any endorsement.
3. Record reviewer, organization, date, evidence/reference and decision in a
   separate signed-off review record. Keep language approval distinct from
   copyright permission to reuse a dictionary/corpus.
4. Change approved glossary rows only after that evidence exists. Regenerate
   PO/TS with `python3 scripts/generate_catalogs.py`; review real UI context,
   placeholders, keyboard shortcuts, wrapping and screen-reader labels.
5. Publish a new version with a changelog describing the actual review scope.
   Do not flip `inl_approved` for the entire package on partial term review.

Licensing gate for any future imported dataset:

| Required field | Purpose |
|---|---|
| Publisher and exact source/version | Establish provenance |
| Explicit license or permission letter | Establish redistribution rights |
| Allowed adaptation and redistribution | Confirm PO/dictionary conversion is allowed |
| GPL/DFSG compatibility and notices | Preserve the original obligations |
| Imported entries and review status | Keep copied data separate from original drafts |

No automated crawler is included. Obtain a compatible licensed export from
INL/Timor Aid/DIT before adding their database. Do not relicense an entire
third-party dictionary by placing a GPL notice on it.
