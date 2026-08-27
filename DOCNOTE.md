<!-- markdownlint-disable MD013 MD024 MD033 -->

# TECHNICAL DOCUMENTATION NOTE (DOCNOTE)

## Zimbra Link Installer & Telemetry Suite

**Enterprise Binary Downloader, Checksum Verifier & Automated Installer (ZCS 4.5.x – 10.1.x)**  
**Maintainer:** Harry Dertin Sutisna Alsyundawy (`alsyundawy@gmail.com`)  
**Version:** `v2.6.0`  
**License:** MIT License

---

### 1. Arsitektur & Prinsip Desain Keamanan

Skrip `zimbra-link-installer.sh` dirancang dengan prinsip **Defense-in-Depth**, **Least Privilege**, **Idempotency**, dan **Zero Data Contamination**:

1. **Defensive Shell Execution (`set -Eeuo pipefail`):**

   - `-e`: Menghentikan eksekusi segera jika suatu perintah menghasilkan exit code non-zero yang tidak ditangani.
   - `-u`: Mencegah penggunaan variabel yang belum didefinisikan (_unbound variable error_).
   - `-o pipefail`: Memastikan kegagalan pada setiap pipeline command (contoh: `curl ... | tar ...`) tertangkap sebagai error.
   - `-E`: Mewariskan trap sinyal `ERR` ke fungsi-fungsi anak.
   - `IFS=$'\n\t'`: Mengamankan parsing input dan perulangan dari bahaya _word splitting_ spasi tidak disengaja.
   - `umask 022`: Memastikan berkas biner dan konfigurasi yang diunduh tidak memiliki izin write publik.

2. **Privilege Elevation Model (`run_privileged`):**

   - Mendeteksi apakah skrip dijalankan langsung sebagai `root` (`id -u == 0`) atau sebagai user biasa.
   - Jika dijalankan sebagai user biasa, perintah instalasi sistem atau paket OS didelegasikan ke `sudo`.
   - Menghindari kegagalan pada container minimalis (Docker/LXC) yang tidak memiliki utilitas `sudo` jika sudah berada di sesi root.

3. **Signal Trapping & Atomic Cleanup (`trap cleanup EXIT INT TERM HUP`):**

   - Menangkap interupsi pengguna (`Ctrl+C` / `SIGINT`), `SIGTERM`, dan `SIGHUP`.
   - Membersihkan berkas temporary `/tmp` tanpa merusak berkas unduhan biner resmi yang berhasil diselesaikan di `${WORK_DIR}`.

4. **Cryptographic Checksum Sanitization:**

   - Mengekstrak pola hash alfanumerik murni (32 karakter untuk MD5, 64 karakter untuk SHA-256) menggunakan `grep -oE` sebelum pencocokan.
   - Melakukan komparasi hash secara **case-insensitive** (`${expected_hash,,} == ${actual_hash,,}`) guna menghindari false-positive akibat format kapitalisasi yang berbeda antar penyedia mirror.

5. **WAF & CDN Referer Bypass:**

   - Menyertakan header `Referer: https://techfiles.online/` dan User-Agent enterprise `Zimbra-Link-Installer/2.6.0` untuk mencegah pemblokiran oleh Firewall CDN komunitas saat mengunduh biner TechFiles (Ian Walker Builds).

6. **Directory State Preservation:**
   - Menyimpan `$original_pwd` sebelum berpindah ke direktori unduhan `${WORK_DIR}`, dan merestorasinya setelah proses selesai untuk menjamin idempotensi working directory shell pemanggil.

---

### 2. Validasi Kesiapan Sistem (Pre-Flight Audit)

Sebelum mengunduh atau menginstal ZCS, skrip melakukan 4 tahap audit:

- **RAM Kapasitas:** Menguji `/proc/meminfo`. Peringatan jika < 8 GB RAM.
- **Ruang Disk `/opt`:** Menguji kapasitas partisi `/opt` (minimal 50 GB direkomendasikan untuk storage mailbox dan database OpenLDAP/MySQL).
- **Resolusi DNS & FQDN:** Menguji `hostname -f` dan kecocokannya pada `/etc/hosts` guna menghindari kegagalan fatal `DNS ERROR resolving MX` pada `zmsetup.pl`.
- **Paket Sistem POSIX Pax:** Menguji keberadaan `pax`, `sysstat`, `net-tools`, dan `curl`. Paket `pax` merupakan mitigasi wajib terhadap kerentanan Remote Code Execution Amavis `cpio` (CVE-2022-41352).

---

### 3. Matriks Kompatibilitas Sistem Operasi

| <small>Distribusi Host</small>         | <small>Versi OS</small>                                               |    <small>Arsitektur</small>     |  <small>Status Dukungan</small>  |
| :------------------------------------- | :-------------------------------------------------------------------- | :------------------------------: | :------------------------------: |
| <small>**Ubuntu Server**</small>       | <small>24.04, 22.04, 20.04, 18.04, 16.04, 14.04, 12.04, 10.04</small> |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**Debian GNU/Linux**</small>    | <small>12 (Bookworm), 11 (Bullseye), 10, 8, 7, 5, 4.0</small>         |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**RHEL / Rocky / Alma**</small> | <small>9.x, 8.x, 7.x, 6.x, 5.x, 4.x</small>                           |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**Oracle Linux (OL)**</small>   | <small>9.x, 8.x, 7.x, 6.x</small>                                     |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**SUSE Linux / SLES**</small>   | <small>SLES 12, SLES 11, SLES 10, openSUSE</small>                    |     <small>`x86_64`</small>      |  <small>✅ Arsip Resmi</small>   |
| <small>**Fedora Linux**</small>        | <small>Fedora 13, 11, 7, Core 5, Core 4</small>                       | <small>`x86_64` / `i386`</small> | <small>✅ Arsip Historis</small> |
