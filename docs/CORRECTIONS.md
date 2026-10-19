# Tetun corrections — 0.3.0

Corrections applied to the glossary and propagated to every native, Qt and
LXQt catalog. The machine-readable source is `data/corrections.csv`;
`scripts/apply_corrections.py` applies it idempotently. All entries remain
community drafts pending INL / native-speaker review.

References consulted: the MediaWiki Tetun interface (translatewiki.net,
`languages/i18n/tet.json`), the Tetun alphabet and orthography summaries
(INL standard, Government Decree 1/2004), the GNU Tetum project, and the
project's own consistency rules in [ORTHOGRAPHY.md](ORTHOGRAPHY.md).
Dictionary content was not copied.

| ID | English | Before | After | Reason |
|---|---|---|---|---|
| TET-0007 | OK | Di'ak | **OK** | UI convention: button label OK is kept; "di'ak" means "good". |
| TET-0018 | Refresh | Karga fali | **Karrega fali** | Consistency: pt "carregar" is spelled karrega elsewhere (Upload, Charging). |
| TET-0432 | Reload | Karga fali | **Karrega fali** | Consistency with Refresh. |
| TET-0037 | Preview | Pré-vizualizasaun | **Previzualizasaun** | Tetun spelling does not keep the Portuguese hyphenated prefix pré-. |
| TET-0045 | Download | Deskarga | **Deskarrega** | Verb (action) is deskarrega (pt descarregar); deskarga is the noun. |
| TET-0073 | Website | Sítio web | **Sítiu web** | Portuguese final -io becomes -iu in Tetun spelling. |
| TET-0271 | Block Website | Blokeia sítio web | **Blokeia sítiu web** | Same rule as Website. |
| TET-0272 | Unblock Website | Hasai blokeiu sítio web | **Hasai blokeiu sítiu web** | Same rule as Website. |
| TET-0273 | Blocked Websites | Sítio web blokeadu | **Sítiu web blokeadu** | Same rule as Website. |
| TET-0087 | Desktop | Ambiente de traballu | **Ambiente servisu** | "traballu" and "de" are Portuguese; Tetun uses servisu (work) and no linking "de". |
| TET-0126 | Add to Desktop | Aumenta ba ambiente de traballu | **Aumenta ba ambiente servisu** | Same rule as Desktop. |
| TET-0157 | Show Desktop | Hatudu ambiente de traballu | **Hatudu ambiente servisu** | Same rule as Desktop. |
| TET-0333 | Workspace | Espasu traballu | **Espasu servisu** | Same rule as Desktop. |
| TET-0334 | Workspaces | Espasu traballu sira | **Espasu servisu sira** | Same rule as Desktop. |
| TET-0335 | Workspace Switcher | Troka espasu traballu | **Troka espasu servisu** | Same rule as Desktop. |
| TET-0109 | Unmount | Desmonta | **Dezmonta** | Negative prefix is spelled dez- (dezativa, dezinstala, dezliga). |
| TET-0161 | Shut Down | Desliga | **Dezliga** | Same dez- rule; Power Off already used Dezliga. |
| TET-0219 | Disconnect | Desliga ligasaun | **Dezliga** | Same dez- rule; "ligasaun" was redundant. |
| TET-0114 | Used Space | Espasu uza | **Espasu uzadu** | Participle needed: "espasu uza" reads as "space uses". |
| TET-0118 | File not found | Arkivu la hetan | **La hetan arkivu** | Word order: "arkivu la hetan" makes the file the finder. |
| TET-0119 | Permission denied | Permisaun rejeitada | **La iha permisaun** | Tetun loans have no feminine agreement; natural phrasing is "la iha permisaun". |
| TET-0133 | Sound & Video | Som no Vídeu | **Áudiu no Vídeu** | "som" is Portuguese; áudiu is the assimilated loan. |
| TET-0398 | Sound | Lian | **Áudiu** | "lian" also means Language (TET-0068); avoid the ambiguity in settings. |
| TET-0326 | Muted | La iha lian | **Silensiadu** | Matches Mute = Silensia; avoids lian (language) ambiguity. |
| TET-0327 | Unmute | Ativa lian | **Ativa áudiu** | Avoids lian (language) ambiguity. |
| TET-0160 | Restart | Reinísia | **Reinisia** | Stress is on the penultimate syllable of a vowel-final word, so no accent is written. |
| TET-0192 | Restart Required | Presiza reinísia | **Presiza reinisia** | Same accent rule as Restart. |
| TET-0193 | Restart Now | Reinísia agora | **Reinisia agora** | Same accent rule as Restart. |
| TET-0194 | Restart Later | Reinísia depois | **Reinisia depois** | Same accent rule as Restart. |
| TET-0255 | Microphone | Mikrofóne | **Mikrofone** | Penultimate stress on a vowel-final word: no accent. |
| TET-0183 | Updates Available | Atualizasaun disponivel | **Atualizasaun disponível** | Penultimate stress on a consonant-final word requires the accent. |
| TET-0184 | No Updates Available | La iha atualizasaun disponivel | **La iha atualizasaun disponível** | Same accent rule. |
| TET-0166 | Charging | Karrega bateria | **Karrega hela** | Ongoing action uses the progressive marker hela. |
| TET-0185 | Checking for updates... | Verifika atualizasaun... | **Verifika hela atualizasaun...** | Ongoing action needs hela; the bare verb reads as a command. |
| TET-0186 | Downloading... | Deskarga... | **Deskarrega hela...** | Progressive hela and verb form deskarrega. |
| TET-0187 | Installing... | Instala... | **Instala hela...** | Progressive hela. |
| TET-0188 | Updating... | Atualiza... | **Atualiza hela...** | Progressive hela. |
| TET-0213 | Running | Hala'o | **Hala'o hela** | Status of an ongoing process uses hela. |
| TET-0224 | Wireless | Rede sem fiu | **Rede laho fiu** | "sem" is Portuguese; Tetun uses laho (without). |
| TET-0230 | Share | Partilla | **Fahe** | Native Tetun verb fahe (to share/divide) is preferred over a loan. |
| TET-0231 | Sharing | Partilla | **Fahe** | Same as Share. |
| TET-0306 | Translated Text | Testu tradús | **Testu tradusidu** | "tradús" is not a participle; use tradusidu. |
| TET-0312 | Welcome to Edukasaun OS | Benvindu ba Edukasaun OS | **Bemvindu ba Edukasaun OS** | Common Tetun spelling is bemvindu (pt bem-vindo). |
| TET-0313 | Free and open-source software | Software livre no ho kódigu fonte nakloke | **Software livre no kódigu nakloke** | Removes the doubled conjunction "no ho". |
| TET-0372 | Formatting | Formata | **Formatasaun** | Noun required, not the verb. |
