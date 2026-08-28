<!-- markdownlint-disable MD013 MD024 MD033 -->

# TECHNICAL DOCUMENTATION NOTE (DOCNOTE)

## Zimbra Link Installer & Telemetry Suite

**Enterprise Binary Downloader, Checksum Verifier, Interactive CLI & Automated Installer (ZCS 4.5.x – 10.1.x)**<br>
**Maintainer:** Harry Dertin Sutisna Alsyundawy (`alsyundawy@gmail.com`)<br>
**Current Version:** `v2.6.2`<br>
**License:** MIT License<br>
**Last Updated:** 2026-08-28

---

### 1. Arsitektur & Prinsip Desain Keamanan (Security Engineering)

Skrip `zimbra-link-installer.sh` dirancang dengan standar enterprise yang menerapkan prinsip **Defense-in-Depth**, **Least Privilege**, **Idempotency**, dan **Zero Data Contamination**:

1. **Defensive Shell Execution (`set -Eeuo pipefail`):**
   - `-e`: Menghentikan eksekusi segera jika suatu sub-proses menghasilkan exit code non-zero tanpa penanganan eksplisit.
   - `-u`: Mencegah penggunaan variabel yang belum didefinisikan (*unbound variable error*), mengeliminasi risiko variabel kosong yang tidak sengaja merusak direktori sistem.
   - `-o pipefail`: Memastikan kegagalan pada setiap segmen pipeline command (seperti `curl ... | tar ...`) tertangkap sebagai error fatal.
   - `-E`: Mewariskan trap sinyal `ERR` ke fungsi-fungsi internal skrip.
   - `IFS=$'\n\t'`: Mengamankan pemisahan kata (*word splitting*) pada perulangan array dan pembacaan berkas.
   - `umask 022`: Memastikan berkas biner dan direktori kerja tidak memiliki izin tulis publik (*world-writable*).

2. **Internationalization (i18n) Engine (`tr_msg` & `--lang` Flag):**
   - Mesin penerjemah terintegrasi yang mendukung **Bahasa Indonesia** dan **English**.
   - Otomatis menyediakan pemilih bahasa interaktif saat startup, opsi CLI `--lang=en` / `--lang=id` untuk mode automasi/skrip nir-interaktif, serta opsi ganti bahasa (*runtime language switcher*) langsung di menu utama.

3. **Privilege Abstraction Layer (`run_privileged`):**
   - Mendeteksi privilege sesi aktif melalui `id -u`.
   - Jika dijalankan sebagai user reguler non-root, perintah instalasi sistem atau manajemen paket secara otomatis didelegasikan melalui `sudo`.
   - Menjamin portabilitas pada container minimalis (Docker, LXC, Podman) yang berjalan sebagai root murni tanpa utilitas `sudo` terpasang.

4. **Signal Trapping & Atomic Cleanup (`trap cleanup EXIT INT TERM HUP`):**
   - Menangkap interupsi sinyal interaktif pengguna (`Ctrl+C` / `SIGINT`), pemutusan koneksi SSH (`SIGHUP`), dan terminasi proses (`SIGTERM`, `EXIT`).
   - Membersihkan berkas sementara (`/tmp/zcs_*`) secara atomik tanpa merusak arsip instalasi resmi yang telah selesai diunduh pada `${WORK_DIR}`.

5. **Cryptographic Checksum Sanitization & Matching:**
   - Mengekstrak pola string hash murni (32 karakter untuk MD5, 64 karakter untuk SHA-256) menggunakan regex alfanumerik (`grep -oE '[a-fA-F0-9]{32|64}'`).
   - Melakukan komparasi hash secara **case-insensitive** (`${expected_hash,,} == ${actual_hash,,}`) guna menghindari kegagalan verifikasi akibat perbedaan kapitalisasi karakter heksadesimal antar penyedia mirror.

6. **WAF & Community CDN Referer Bypass:**
   - Menyertakan header HTTP `Referer: https://techfiles.online/` dan User-Agent enterprise `Zimbra-Link-Installer/2.6.2` guna mencegah pemblokiran Cloudflare WAF pada mirror biner komunitas (Ian Walker Builds).

7. **Directory State Preservation:**
   - Menyimpan variabel `$original_pwd` sebelum berpindah ke working directory `${WORK_DIR}`, dan mengembalikannya ke posisi awal saat skrip selesai untuk menjaga konsistensi state shell pemanggil.

---

### 2. Validasi Kesiapan Sistem (Pre-Flight Audit Engine)

Sebelum proses pengunduhan dan instalasi biner ZCS dijalankan, modul audit melakukan inspeksi 4 pilar kesiapan server:

- **Audit Kapasitas Memori (RAM):** Membaca data `/proc/meminfo`. Menampilkan peringatan tegas jika RAM terdeteksi kurang dari 8 GB (minimum rekomendasi Zimbra MTA + Mailbox + ClamAV + Amavis).
- **Audit Ruang Penyimpanan (`/opt` Partition):** Menguji ketersediaan disk space partisi `/opt` (minimum 50 GB disarankan untuk struktur database OpenLDAP, MariaDB/MySQL, dan mailbox store).
- **Audit Resolusi DNS & FQDN:** Memeriksa `hostname -f` dan memverifikasi keselarasan FQDN pada `/etc/hosts` untuk mencegah kegagalan fatal `DNS ERROR resolving MX` saat eksekusi `zmsetup.pl`.
- **Audit Paket Prasyarat POSIX (`pax`):** Menguji keberadaan dependensi `pax`, `sysstat`, `net-tools`, dan `curl`. Paket `pax` merupakan mitigasi wajib terhadap kerentanan Remote Code Execution Amavis `cpio` (CVE-2022-41352).

---

### 3. Matriks Kompatibilitas Sistem Operasi & Arsitektur

| <small>Distribusi Host</small>         | <small>Versi OS</small>                                               |    <small>Arsitektur</small>     |  <small>Status Dukungan</small>  |
| :------------------------------------- | :-------------------------------------------------------------------- | :------------------------------: | :------------------------------: |
| <small>**Ubuntu Server**</small>       | <small>24.04, 22.04, 20.04, 18.04, 16.04, 14.04, 12.04, 10.04</small> |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**Debian GNU/Linux**</small>    | <small>12 (Bookworm), 11 (Bullseye), 10, 8, 7, 5, 4.0</small>         |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**RHEL / Rocky / Alma**</small> | <small>9.x, 8.x, 7.x, 6.x, 5.x, 4.x</small>                           |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**Oracle Linux (OL)**</small>   | <small>9.x, 8.x, 7.x, 6.x</small>                                     |     <small>`x86_64`</small>      |     <small>✅ Penuh</small>      |
| <small>**SUSE Linux / SLES**</small>   | <small>SLES 12, SLES 11, SLES 10, openSUSE</small>                    |     <small>`x86_64`</small>      |  <small>✅ Arsip Resmi</small>   |
| <small>**Fedora Linux**</small>        | <small>Fedora 13, 11, 7, Core 5, Core 4</small>                       | <small>`x86_64` / `i386`</small> | <small>✅ Arsip Historis</small> |

---

### 4. Struktur CLI Menu & Alur Eksekusi Skrip

Skrip `zimbra-link-installer.sh` mengimplementasikan arsitektur menu bertingkat yang intuitif dan dwibahasa:

```text
[Main Menu / Menu Utama]
  ├── 1) Zimbra Network Edition (Official Synacor Releases)
  │      ├── ZCS NE 10.1.x (Ubuntu 22.04 / 20.04, RHEL 9 / 8)
  │      ├── ZCS NE 10.0.x (Ubuntu 20.04 / 18.04, RHEL 8)
  │      ├── ZCS NE 9.0.0 (Ubuntu 20.04 / 18.04, RHEL 8 / 7)
  │      ├── ZCS NE 8.8.15 / 8.8.x LTS
  │      └── ZCS NE Legacy (8.7.x, 8.6.0, 8.5.x, 8.0.x, 7.x)
  ├── 2) Zimbra Open Source Edition / FOSS (Official Synacor)
  │      ├── ZCS FOSS 8.8.15 GA (Ubuntu 20.04 / 18.04, RHEL 8 / 7)
  │      ├── ZCS FOSS 8.7.x / 8.6.0 / 8.5.x GA
  │      └── ZCS FOSS 8.0.x / 7.x GA
  ├── 3) Zimbra FOSS Unofficial / Community Builds
  │      ├── ZCS 10.1.x Modern Builds (TechFiles / Ian Walker & Maldua)
  │      ├── ZCS 10.0.x Community FOSS (Ubuntu 20.04 / 22.04, RHEL 8 / 9)
  │      ├── ZCS 9.0.0 Community FOSS (Ubuntu 20.04 / 18.04, RHEL 8 / 7)
  │      └── ZCS 8.8.15 Community Rebuilds (Ubuntu 20.04, RHEL 8)
  ├── 4) Pre-Flight System Audit & Prerequisite Checks
  ├── 5) Deep Link Telemetry & Health Validator
  ├── 6) Switch Language / Ganti Bahasa [Current: English / ID]
  └── 0) Exit / Keluar
```

---

### 5. Mesin Validasi Telemetri Biner (`deep_link_validator.py`)

Utilitas `scripts/deep_link_validator.py` merupakan modul telemetri asynchronous berbasis Python:

- **Concurrent ThreadPool:** Menjalankan hingga 20 thread paralel untuk memverifikasi ketersediaan seluruh URL biner.
- **Dua Tahap Pengujian HTTP:**
  1. *Primary Check:* Mengirimkan request `HEAD` dengan custom User-Agent dan Referer.
  2. *Secondary Fallback:* Jika server menolak metode `HEAD` (HTTP 405/403), script otomatis beralih ke request `GET` dengan header `Range: bytes=0-10` untuk meminimalisir konsumsi bandwidth.
- **Hasil Telemetri:** Menjamin seluruh 1,215+ direct download link terverifikasi aktif tanpa tautan rusak (*zero broken links*).

---

### 6. Arsitektur Portal Web Interaktif (`index.html`)

Aplikasi web standalone `index.html` dibangun dengan teknologi web modern tanpa dependensi berat (*zero external framework*) yang sepenuhnya responsif dari layar VGA (640x480) hingga monitor 2K (2560x1440):

- **Bilingual Interface Switcher:** Dilengkapi tombol toggle dwibahasa interaktif `[ ID | EN ]` pada navbar dengan persistensi `localStorage` untuk memfasilitasi pengguna global dan lokal.
- **Interactive Architecture Visualizer:** Mengintegrasikan pustaka Mermaid.js untuk merender diagram topologi dan alur kerja instalasi Zimbra secara dinamis dengan tema gelap (*dark theme*) berkontras tinggi.
- **Debounced Real-Time Client-Side Search:** Fitur pencarian instan dengan proteksi *debouncing* (120ms) untuk menyaring 1,215+ tautan biner dan matriks CVE secara efisien tanpa *layout thrashing*.
- **Responsive Mobile Navigation & Offcanvas Drawer:** Dilengkapi tombol menu hamburger dan *slide-in offcanvas drawer* dengan *backdrop blur* serta navigasi keyboard (*ESC key & focus trapping*).
- **Aksesibilitas & Standar WCAG AA:** Menyediakan *Skip to Main Content link*, kontras warna teks optimal, styling `:focus-visible` untuk keyboard user, dan atribut ARIA (`aria-label`, `aria-expanded`, `aria-controls`).
- **Quick Copy Utility with Fallback:** Tombol salin satu klik untuk perintah unduh `wget`/`curl` dan hash verifikasi dengan fallback otomatis jika Clipboard API dibatasi oleh browser.

---

### 7. Matriks Evolusi & Riwayat Versi (v2.0.0 – v2.6.2)

| Versi | Tanggal Rilis | Fokus Perubahan Utama |
| :---: | :---: | :--- |
| **`v2.6.2`** | 2026-08-28 | Implementasi penuh arsitektur dwibahasa (Bahasa Indonesia & English) lintas platform: mesin i18n interaktif pada CLI (`zimbra-link-installer.sh` dengan flag `--lang=en`/`--lang=id` dan runtime switch), tombol pengalih bahasa pada navbar web portal (`index.html`), navigasi dwibahasa pada `README.md` dan `SECURITY.md`. |
| **`v2.6.1`** | 2026-08-28 | Sinkronisasi Deep Research rilis biner & CVE terbaru (2023–2026): penambahan CVE-2025-48700 (CISA KEV), CVE-2024-45516, CVE-2023-48432, CVE-2023-34193, CVE-2023-29382 ke Master Vulnerability Matrix (total 37+ CVE), peremajaan kebijakan `SECURITY.md` enterprise, dan verifikasi telemetri 1,215 link aktif secara menyeluruh. |
| **`v2.6.0`** | 2026-08-27 | Enterprise Security Hardening (`set -Eeuo pipefail`, cleanup traps, privilege abstraction, regex checksum sanitization, FQDN audit), standalone web portal (`index.html`) responsif (VGA s.d. 2K) dengan diagram Mermaid & WCAG AA accessibility, verifikasi NVD CVE terkonfirmasi resmi, dan micro-typography formatting. |
| **`v2.5.0`** | 2026-08-27 | Implementasi arsitektur CLI submenu bertingkat (NE 7-10.1, Official FOSS 7-8.8, Community FOSS 8.8-10.1), penyusunan Master Vulnerability Matrix 32+ CVE (2016–2026), dan Zero-Day Emergency Hardening Playbook. |
| **`v2.4.0`** | 2026-08-27 | Sinkronisasi penuh dengan Zimbra Releases Wiki (`wiki.zimbra.com/wiki/Zimbra_Releases`), menambahkan cabang legacy ZCS 4.5.x s.d. 10.1.x, total link terverifikasi mencapai 1,215+. |
| **`v2.3.0`** | 2026-08-27 | Penggabungan 235 rilis resmi dari `alsyundawy/zimbra_bits` dan arsip download langsung dari `martbrooks/zimbra_direct_downloads` (Debian 4-8, RHEL 4-7, SLES 10-12, Fedora, Mac OS X), total link 1,183+. |
| **`v2.2.0`** | 2026-08-27 | Ekspansi arsip resmi Synacor `files.zimbra.com` untuk Network Edition & FOSS (ZCS 7.x s.d. 10.1.x) dan arsip patch, total link mencapai 945+. |
| **`v2.1.0`** | 2026-08-27 | Penambahan 53+ rilis komunitas Zimbra FOSS (ZCS 8.8.15, 9.0.0, 10.0.x, 10.1.x) dari `maldua/zimbra-foss` dan `techfiles.online` CDN untuk Ubuntu 18.04–24.04 dan RHEL 8–9 (741+ link). |
| **`v2.0.0`** | 2026-08-27 | Rilis perdana repositori Zimbra Link Installer & Telemetry Suite, skrip CLI `zimbra-link-installer.sh`, modul Python `deep_link_validator.py`, verifikasi checksum otomatis SHA-256/MD5. |
