# Instalasi Tetun 0.3.0

Paket ini ditujukan untuk Edukasaun OS berbasis Debian dan Debian dengan glibc.
Paket menyediakan locale bersama serta katalog aplikasi parsial; terjemahan
masih memerlukan pemeriksaan INL dan penutur Tetun. Tidak ada kamus berhak cipta
yang dibundel. Rincian hak penggunaan ada di SOURCES.md dan LICENSING.md.

## Pasang dan periksa

```sh
sudo apt install ./eduka-language-pack-tet_0.3.0_all.deb
eduka-tet demo
eduka-tet doctor
```

Locale `tet_TL.utf8` dikompilasi oleh `localedef` komputer tujuan, dengan sumber
standar di `/usr/share/i18n/locales/tet_TL`. Salinan sumber, glosarium dan manifest
ada di `/usr/share/eduka-language-pack-tet`; dokumentasi/referensi ada di
`/usr/share/doc/eduka-language-pack-tet`.

Pemasangan tidak menetapkan bahasa login secara otomatis. Locale hasil kompilasi
ada di `/usr/lib/locale/tet_TL.utf8`; direktori milik pengelola lain tidak akan
ditimpa. Paket tidak mengubah `/etc/locale.gen`, `SUPPORTED`, keyboard atau zona
waktu. Katalog native ada di `/usr/share/locale/tet/LC_MESSAGES`.

## Aktifkan untuk pengguna desktop

Jalankan tanpa sudo, sebagai pengguna yang akan memakai Tetun:

```sh
eduka-tet enable --user
```

Deteksi otomatis memilih backend sesi. Untuk Plasma dan GNOME/GDM:

```sh
eduka-tet enable --user --desktop kde
eduka-tet enable --user --desktop gnome --accounts-service
```

**Keluar dan masuk kembali.** Aplikasi yang telah berjalan menyimpan lingkungan
bahasa lama. `LANGUAGE=tet:pt:en` memilih Tetun, Portugis, lalu Inggris jika
aplikasi memakai mekanisme gettext tersebut. Aplikasi tanpa katalog/loader
Tetun tetap memakai bahasa alternatif.

Alat menyimpan blok di `.profile` dan `.xsessionrc`, konfigurasi
`environment.d/60-eduka-tet.conf`, serta jurnal pemulihan privat. Direktori
`XDG_CONFIG_HOME` / `XDG_STATE_HOME` absolut dihormati; default `.config` /
`.local/state`. Plasma menambahkan skrip `plasma-workspace/env/eduka-tet.sh`
dan mengatur kunci bahasa dalam `plasma-localerc`, sambil menyimpan nilai lama.
GNOME mencoba AccountsService; opsi `--accounts-service` mewajibkan keberhasilan
API. Jika layanan tidak tersedia/akses ditolak, gunakan default sistem yang
dijelaskan di bawah. Alat tidak mengedit database AccountsService secara langsung.

Konfigurasi `LC_*` yang bertentangan dibersihkan di blok shell; environment.d dan
Plasma diberi kategori locale Tetun. `LC_ALL` tidak ditetapkan permanen ke suatu
locale. Session manager tetap dapat menimpa pengaturan ini; periksa `eduka-tet
doctor` setelah login. Pemilih bahasa dapat tidak menampilkan Tetun meskipun
locale tersedia karena memakai tabel bahasa internalnya sendiri.

Untuk membatalkan sebelum mengganti backend atau melepas paket:

```sh
eduka-tet disable --user
```

Alat mengembalikan nilai lama dan mempertahankan perubahan di luar blok/kunci
bahasa. Jika blok atau kunci bahasa milik paket telah diedit, alat berhenti
sebelum mengubah berkas lainnya. Pulihkan nilai yang tersimpan di jurnal atau
simpan perubahan Anda secara manual, lalu ulangi. Jangan menghapus jurnal
pemulihan selama aktivasi. Migrasi pengaturan versi 0.1.0 didukung.

## Sistem atau image Edukasaun OS

Administrator dapat menetapkan bahasa default login baru setelah locale diuji:

```sh
# Jalankan cp hanya jika /etc/default/locale sudah ada:
sudo cp -a /etc/default/locale /etc/default/locale.before-eduka-tet
sudo update-locale --reset LANG=tet_TL.UTF-8 LANGUAGE=tet:pt:en
```

`--reset` membersihkan kategori lama di berkas ini; periksa hasilnya. Preferensi
bahasa pengguna/display manager dapat tetap menimpa default sistem. Kembalikan
cadangan untuk memulihkan pilihan lama. Jangan menimpa `/etc/environment` untuk
mengatur bahasa. Lihat DESKTOPS.md untuk jalur sesi yang sesuai.

Untuk mencoba satu aplikasi tanpa perubahan login:

```sh
eduka-tet run -- date '+%A, %d %B %Y'
eduka-tet run -- your-application
```

## Huruf, keyboard, dan ejaan

Gunakan UTF-8 dan font dengan á, é, í, ó, ú, ñ. Pilih Portuguese atau US
international melalui pengaturan desktop; Compose key juga bisa dipakai.
Paket tidak mengganti layout keyboard pengguna.

```sh
printf "ha’u ne’e\n" | eduka-tet normalize
```

Normalisasi hanya NFC/apostrof ASCII. Ini tidak mengubah seluruh ejaan DIT ke INL
atau mengesahkan tata bahasa. Sumber DIT memakai konvensi yang berbeda pada
beberapa bentuk; lihat ORTHOGRAPHY.md.

## Pembaruan dan pelepasan

Pembaruan data `locales` memicu kompilasi ulang. Kompilasi ulang manual:

```sh
sudo eduka-tet compile-locale
```

Sebelum purge, batalkan pilihan bahasa tiap pengguna dan pulihkan default
sistem/compositor. `remove` mempertahankan locale yang dihasilkan; `purge` hanya
menghapus direktori dengan penanda milik paket. Berkas pengguna tidak disentuh
oleh maintainer script.

```sh
eduka-tet disable --user
sudo apt purge eduka-language-pack-tet
```

Terminal pemulihan dapat memakai `LANG=C.UTF-8 LC_ALL=C.UTF-8`. Jika paket locale
Tetun resmi suatu saat tersedia, bereskan aktivasi ini dan lepaskan paket komunitas
terlebih dahulu agar tidak terjadi kepemilikan berkas yang bertabrakan.
