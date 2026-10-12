# Desktop support and coverage — 0.3.0

Every desktop can launch applications with `tet_TL.UTF-8` where its libc and
session environment support the locale. Shell translations require that shell's
own catalog and language lookup. These are separate capabilities. No full desktop
UI or graphical login has been acceptance-tested by this release.

The user's [desktop list](https://note.com/yuuya20061202/n/n52c963a94b05?hl=en)
is used to define scope, not as technical documentation. For example, modern
COSMIC's toolkit is not treated as GTK, and Hyprland configuration is not treated
as Lua. GNOME/Plasma session behavior comes from their upstream interfaces.

| Desktop / session | Activation route | Dedicated content in this release | Remaining integration |
|---|---|---|---|
| GNOME | `--desktop gnome --accounts-service`; GDM language API | Partial GNOME Shell, GTK 3/4 | Other GNOME apps, language chooser, actual GDM/Wayland login |
| KDE Plasma | `--desktop kde`; Plasma startup env and language keys | Partial Dolphin gettext catalog | Plasma shell/frameworks, KI18n lookup on target version, Qt locale formats |
| Cinnamon | `--desktop cinnamon`; Debian Xsession / login defaults | Partial Cinnamon, Nemo, GTK | Actual display-manager startup, complete shell/app translations |
| Xfce | `--desktop xfce`; Debian Xsession / login defaults | Partial xfce4-panel, Thunar, GTK | Session, other plugins/apps and graphical verification |
| MATE | `--desktop mate`; Debian Xsession / login defaults | Partial mate-panel, Caja, GTK | Other shell/apps and graphical verification |
| LXDE | `--desktop lxde`; Debian Xsession / login defaults | Partial lxpanel, PCManFM, GTK 2 | libfm, other apps and graphical verification |
| LXQt | `--desktop lxqt`; `~/.config/lxqt/session.conf` [Environment] plus login defaults | **Complete draft**: 57 Qt catalogs, 3677/3706 messages (panel + all plugins, config tools, session, runner, notifications, power, policykit, sudo, PCManFM-Qt, libfm-qt, QTerminal, LXImage-Qt, archiver, screengrab, qps, pavucontrol-qt, ObConf-Qt); Openbox gettext catalog | Loader patches in `upstream/lxqt-patches` must be applied to the distribution's liblxqt and Qt apps (stock Qt reports `tet` as `C`); `.desktop`/menu names; Qt number/date formats |
| Budgie | `--desktop budgie`; login defaults / optional `--accounts-service` | Shared locale and installed GTK/app catalogs | Dedicated Budgie catalog, session inheritance |
| Pantheon | `--desktop pantheon`; login defaults / optional `--accounts-service` | Shared locale and GTK/app catalogs | Dedicated Gala/elementary app catalogs |
| Unity | `--desktop unity`; login defaults / optional `--accounts-service` | Shared locale and GTK/app catalogs | Dedicated Unity catalogs |
| Deepin | `--desktop deepin`; login defaults | Shared locale, matching gettext apps | Dedicated DDE/Qt catalogs and locale lookup |
| COSMIC | `--desktop cosmic`; login defaults | Shared glibc locale and compatible apps | Dedicated COSMIC Fluent/toolkit resources and session inheritance |
| Sway / Hyprland | `--desktop sway` / `hyprland`; compositor's launch environment | Shared locale and compatible apps | Environment propagation from launcher/display manager; no compositor catalog |
| Openbox | Inherits the LXQt/Xsession environment | Openbox gettext catalog (93/94 messages) | Plural desktop-count message |
| i3 / Awesome | `--desktop i3` / `awesome`; Debian Xsession / launcher env | Shared locale and compatible apps | WM-specific strings/configuration |
| Other / console | `--desktop generic`; profile/system defaults | Shared locale, own/native gettext catalogs | Login shell may read a different startup file |

Run activation without sudo; log out and sign in. Backend names beyond GNOME,
KDE and LXQt select the shared profile/Xsession/environment mechanism. They do not imply
that a shell-specific catalog exists. `environment.d` supplies systemd user
services, not every login shell or display manager. A shell reading `.bash_profile`
instead of `.profile` must source `.profile` or receive LANG from its login manager.

For Wayland sessions that do not inherit these files, set the default through the
system's documented login language settings (INSTALL-ID.md), or export LANG and
LANGUAGE in the script **before starting** the compositor. Changing environment
in a late desktop autostart cannot translate already-running panels. Check
`eduka-tet doctor` from a new terminal inside the new session.

## How every desktop and window manager gets Tetun

1. **Locale** (`tet_TL.UTF-8`, compiled by `postinst`) works for every glibc
   program, so dates, months and yes/no answers are Tetun on any desktop or WM.
2. **`LANGUAGE=tet:pt:en`** is exported by `eduka-tet enable`. Any gettext
   application without a Tetun catalog falls back to **Portuguese**, then
   English. This covers GTK, GNOME, Xfce, MATE, Cinnamon, KDE (KI18n uses
   gettext), Openbox, IceWM, Fluxbox and most WMs without extra work.
3. **Qt applications** select catalogs with `QLocale`, which does not know
   `tet`. LXQt is fixed by the patches in `upstream/lxqt-patches` (see
   INTEGRATION.md); the same one-line change applies to any Qt program.
4. **Catalogs** in this package translate the shells listed below. Missing
   strings fall back as in step 2, never to an error.

## LXQt catalogs

All LXQt components (union of LXQt master and the 2.1.x releases in Debian 13)
are translated; `data/lxqt-manifest.json` lists the commit, license, install
directory and coverage of each catalog. The only untranslated entries are
keyboard/CPU identifiers that must stay unchanged and two GPL notices.

## Native catalog coverage

These counts refer to exact records in each inspected source snapshot, not a
percentage of the whole desktop. Only singular, simple labels are included;
format/plural-rich sentences and untranslated entries fall back to the app's
normal language. Mnemonics are kept in the source's `_` or `&` syntax, with draft
positions requiring native-speaker/desktop review.

| Domain | Source snapshot | Tetun records / source records | Coverage |
|---|---|---:|---:|
| `gtk20` | 2.24.33 | 121 / 867 | 13.96% |
| `gtk30` | 3.24.49 | 204 / 1696 | 12.03% |
| `gtk40` | 4.18.6 | 169 / 1733 | 9.75% |
| `gnome-shell` | 48.4 | 74 / 718 | 10.31% |
| `cinnamon` | snapshot 2026-10-03 | 173 / 1949 | 8.88% |
| `nemo` | snapshot 2026-10-03 | 186 / 1395 | 13.33% |
| `xfce4-panel` | 4.20.5 | 72 / 495 | 14.55% |
| `Thunar` | 4.20.4 | 141 / 1041 | 13.54% |
| `lxpanel` | 0.11.1 | 49 / 482 | 10.17% |
| `pcmanfm` | 1.3.2 | 52 / 297 | 17.51% |
| `mate-panel` | 1.28.4 | 64 / 652 | 9.82% |
| `caja` | 1.26.4 | 159 / 1604 | 9.91% |
| `dolphin` | 24.12.3 | 89 / 870 | 10.23% |
| `openbox` | 3.6.1+git ebfa727 | 93 / 94 | 98.94% |


Native catalog source and compiled paths:
`native/DOMAIN.po` and `/usr/share/locale/tet/LC_MESSAGES/DOMAIN.mo`.
`data/native-templates.json` records each exact context/message selection;
`native-manifest.json` records source version, hash, license and counts. Upstream
copyright/translator notices are preserved in `upstream/native-notices` and
`debian/copyright`; upstream English translations are not copied as Tetun.

Do not substitute a generic `edukasaun.mo` under another application's domain.
An identical English label can require a different context or translation.

## Acceptance on Debian / Edukasaun OS

For each shipped desktop image: install/upgrade the package; activate as a fresh
user; sign out/in on X11 and Wayland where supported; verify LANG, LANGUAGE and
locale from a new terminal. Open the actual panel and file manager and compare
specific native translated IDs against source contexts. Inspect accent rendering,
keyboard input, mnemonic collisions, fallback sentences, counts, sorting and
number/date formatting. Disable and verify previous preferences return. Exercise
remove/purge after disabling every user. Record exact desktop/toolkit versions
and screenshots. Native-speaker/INL review and application testing remain required
before a school deployment.
