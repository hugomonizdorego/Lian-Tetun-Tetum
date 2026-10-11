# GNU/Linux, POSIX and UNIX portability

The `.deb` is for dpkg/apt distributions such as Debian and Debian-based
Edukasaun OS. It is architecture-independent because it ships text, Python and
translation catalogs; libc locale data is compiled on the target. It does not
make a Debian package installable through Arch's pacman or Fedora's rpm.

The source supports GNU gettext, UTF-8, Python 3.9+, GNU libc `localedef`, POSIX
shell startup syntax and XDG paths. systemd is optional for the shared tools;
`environment.d` is used only by sessions that support it. Qt translators require
explicit loading for the inspected Qt versions. GNU is a software/licensing
family, Linux is the kernel, and UNIX/POSIX describe other interfaces and systems;
none is a translation certification.

## Other glibc-based GNU/Linux systems

Install Python 3, gettext's `msgfmt`, GNU libc locale/charmap source data and make
through the distribution's package manager, then stage a prefix installation:

```sh
make test
python3 scripts/install_prefix.py --prefix /usr/local --destdir /tmp/tet-stage
/tmp/tet-stage/usr/local/bin/eduka-tet demo
```

For an administrator-managed real install, omit `--destdir` and use suitable
permissions. This script does not change login defaults or compile a global
locale. After inspecting files, compile the installed source with the system's
GNU `localedef` or the installed `eduka-tet compile-locale` (requires root and
writes the package-owned directory under `/usr/lib/locale`). GNU libc searches
this canonical locale directory even when the data/tools use `/usr/local`.
A package maintainer should adapt filesystem paths and removal handling for that
distribution rather than overlay files owned by its native package manager.

GNU libc's normal `-i tet_TL` lookup uses its configured locale source directory;
a custom prefix may require an explicit absolute input source. The package's
helper already uses the absolute source path. Validate locale availability and
application catalog search paths on each target distro.

This installer does not install Debian maintainer scripts or apply the LXQt
patch. It is a source/developer route, not a replacement for a reviewed distro
package. For removal, use the native package manifest or remove only this
installation's files after disabling language settings.

## Other UNIX / libc families

musl-based Alpine, BSD, macOS and non-glibc systems do not use the same glibc
locale database/compiler semantics. Gettext catalogs and original terminology
may be reused under their licenses, but locale compilation, login integration,
formatting and packaging need a separate port. This release neither ships a
working native package for those systems nor claims UNIX/POSIX certification.

Actual validation here used Ubuntu 24.04/glibc 2.39; Debian 13 CI is supplied but
has not been executed on GitHub in this session. See VALIDATION.md and DESKTOPS.md.
