# -*- coding: utf-8 -*-
"""
build_full_i18n.py
Constructs an exhaustive, full-document bilingual (ID / EN) i18n engine
for index.html and injects it.
"""

import re

def build_js_engine():
    return r'''
        // =====================================================================
        // 7. Comprehensive Full-Document Bilingual i18n Engine (ID <-> EN)
        // =====================================================================
        const btnLangId = document.getElementById('btnLangId');
        const btnLangEn = document.getElementById('btnLangEn');

        const i18nDict = {
          id: {
            title: "Zimbra Link Installer — Binary Archive & CVE Matrix",
            skipLink: "Lewati ke Konten Utama",
            navLinks: [
              '<i class="fa-solid fa-compass" aria-hidden="true"></i> Ringkasan',
              '<i class="fa-solid fa-bolt" aria-hidden="true"></i> Mulai Cepat',
              '<i class="fa-solid fa-box-archive" aria-hidden="true"></i> Arsip Resmi',
              '<i class="fa-solid fa-users-gear" aria-hidden="true"></i> FOSS Komunitas',
              '<i class="fa-solid fa-shield-halved" aria-hidden="true"></i> Keamanan & CVE'
            ],
            sidebarTitles: [
              "Navigasi Utama",
              "Arsip Resmi Official",
              "Arsip Komunitas (FOSS)",
              "Kompilasi & Panduan",
              "Keamanan & Operasional"
            ],
            sidebarLinks: {
              "#overview": '<i class="fa-solid fa-info-circle"></i> Ringkasan Eksekutif',
              "#original-links--references": '<i class="fa-solid fa-link"></i> Tautan Asli & Rujukan',
              "#quickstart": '<i class="fa-solid fa-play"></i> Mulai Cepat (Quickstart)',
              "#automated-cli-installer-zimbra-link-installersh": '<i class="fa-solid fa-terminal"></i> Installer CLI',
              "#dependencies": '<i class="fa-solid fa-cubes"></i> Dependensi Sistem',
              "#download-verification-status--legend": '<i class="fa-solid fa-circle-check"></i> Legenda Verifikasi',
              "#zcs-101x-series-official-releases-daffodil": '<i class="fa-solid fa-box"></i> ZCS 10.1.x Daffodil',
              "#zcs-100x-series-official-releases-daffodil": '<i class="fa-solid fa-box"></i> ZCS 10.0.x Daffodil',
              "#zcs-900x-series-official-releases-kepler": '<i class="fa-solid fa-box"></i> ZCS 9.0.0 Kepler',
              "#zcs-88x-series-official-releases-joule": '<i class="fa-solid fa-box"></i> ZCS 8.8.x Joule',
              "#zcs-87x-series-official-releases-judaspriest": '<i class="fa-solid fa-box"></i> ZCS 8.7.x JudasPriest',
              "#zcs-860-series-official-releases--cumulative-security-patches": '<i class="fa-solid fa-box"></i> ZCS 8.6.0 & Security Patch',
              "#zcs-85x-series-official-releases-851-ga--850-ga": '<i class="fa-solid fa-box"></i> ZCS 8.5.x Official',
              "#zcs-80x-series-official-releases-809-ga-down-to-803-ga": '<i class="fa-solid fa-box"></i> ZCS 8.0.x Official',
              "#zcs-7x-legacy-official-releases-727-ga-720-ga-713-ga-701-ga": '<i class="fa-solid fa-box"></i> ZCS 7.x Legacy',
              "#zcs-6x-legacy-official-releases-6010-ga-609-ga-607-ga": '<i class="fa-solid fa-box"></i> ZCS 6.x Legacy',
              "#zcs-5x-legacy-official-releases-5010-ga-down-to-500-ga": '<i class="fa-solid fa-box"></i> ZCS 5.x Legacy',
              "#zcs-45x-historical-archive-4510-ga-down-to-455-ga": '<i class="fa-solid fa-box"></i> ZCS 4.5.x Historical',
              "#techfilesonline-zimbra-foss-101x-ian-walker-builds": '<i class="fa-solid fa-cube"></i> TechFiles 10.1.20',
              "#zcs-foss-101x-series-all-26-community-releases-20242026": '<i class="fa-solid fa-cube"></i> Maldua FOSS 10.1.x',
              "#zcs-foss-100x-series-all-17-community-releases-20232026": '<i class="fa-solid fa-cube"></i> Maldua FOSS 10.0.x',
              "#zcs-foss-900x-series-all-8-kepler-community-releases-20202025": '<i class="fa-solid fa-cube"></i> Maldua FOSS 9.0.0',
              "#zcs-foss-8815x-series-all-joule-community-releases-20182024": '<i class="fa-solid fa-cube"></i> Maldua FOSS 8.8.15',
              "#build-systems--source-compilation-guide": '<i class="fa-solid fa-wrench"></i> Panduan Kompilasi Source',
              "#configuration": '<i class="fa-solid fa-sliders"></i> Konfigurasi Sistem',
              "#security-architecture--comprehensive-cve-matrix-20162026": '<i class="fa-solid fa-shield-virus"></i> Matriks CVE & Keamanan',
              "#zero-day-emergency-incident-response--hardening-protocol": '<i class="fa-solid fa-triangle-exclamation"></i> Mitigasi Zero-Day',
              "#operational-best-practices-rfc-2119": '<i class="fa-solid fa-clipboard-check"></i> Praktik Terbaik (RFC 2119)',
              "#strategic-migration--upgrade-methodology": '<i class="fa-solid fa-arrow-right-arrow-left"></i> Metodologi Migrasi',
              "#official-contact--author": '<i class="fa-solid fa-address-card"></i> Kontak & Penulis'
            },
            heroTitle: '<a href="#zimbra-link-installer--the-complete-zimbra-collaboration-archive--installer-suite" class="anchor-link">#</a> ZIMBRA LINK INSTALLER — ARSIP LENGKAP & SUITE PEMASANG ZIMBRA COLLABORATION',
            heroSubtitle: "Unduhan Langsung Binary Enterprise, Rilis Resmi & Komunitas FOSS, Checksum Kriptografi (MD5/SHA256), Matriks Keamanan CVE, dan Skrip Otomatisasi Instalasi CLI untuk Zimbra Collaboration Suite (ZCS 4.5.x – 10.1.x).",
            copyBtnText: '<i class="fa-regular fa-copy"></i> Salin',
            copiedBtnText: '<i class="fa-solid fa-check"></i> Tersalin!',
            filterPlaceholder: "Cari versi, OS, tanggal rilis, atau checksum di tabel ini...",
            headings: {
              "table-of-contents": '<a href="#table-of-contents" class="anchor-link">#</a> Daftar Isi',
              "overview": '<a href="#overview" class="anchor-link">#</a> Ringkasan Eksekutif & Arsitektur',
              "original-links--references": '<a href="#original-links--references" class="anchor-link">#</a> Tautan Asli & Rujukan Resmi',
              "portal-resmi--dokumentasi-zimbra-synacor": '<a href="#portal-resmi--dokumentasi-zimbra-synacor" class="anchor-link">#</a> <i class="fa-solid fa-globe text-primary"></i> Portal Resmi & Dokumentasi Zimbra Synacor',
              "unduhan-biner-komunitas-unofficial-foss--ose--mirror": '<a href="#unduhan-biner-komunitas-unofficial-foss--ose--mirror" class="anchor-link">#</a> <i class="fa-solid fa-box-archive text-warning"></i> Unduhan Biner Komunitas Unofficial FOSS / OSE & Mirror',
              "script-builder-incident-response--toolkits": '<a href="#script-builder-incident-response--toolkits" class="anchor-link">#</a> <i class="fa-solid fa-screwdriver-wrench text-success"></i> Script Builder, Incident Response & Toolkits',
              "quickstart": '<a href="#quickstart" class="anchor-link">#</a> Mulai Cepat (Quickstart)',
              "metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan": '<a href="#metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan" class="anchor-link">#</a> Metode 1: Menggunakan Script Otomatis Interaktif (Direkomendasikan)',
              "metode-2-unduhan-manual-biner-target": '<a href="#metode-2-unduhan-manual-biner-target" class="anchor-link">#</a> Metode 2: Unduhan Manual Biner Target',
              "automated-cli-installer-zimbra-link-installersh": '<a href="#automated-cli-installer-zimbra-link-installersh" class="anchor-link">#</a> Automated CLI Installer (<code>zimbra-link-installer.sh</code>)',
              "fitur-utama-cli": '<a href="#fitur-utama-cli" class="anchor-link">#</a> Fitur Utama CLI',
              "dependencies": '<a href="#dependencies" class="anchor-link">#</a> Dependensi & Persyaratan Sistem',
              "sec-1-kebutuhan-runtime-minimum": '<a href="#sec-1-kebutuhan-runtime-minimum" class="anchor-link">#</a> 1. Kebutuhan Runtime Minimum',
              "sec-2-kebutuhan-toolchain-kompilasi-build-environment": '<a href="#sec-2-kebutuhan-toolchain-kompilasi-build-environment" class="anchor-link">#</a> 2. Kebutuhan Toolchain Kompilasi (Build Environment)',
              "download-verification-status--legend": '<a href="#download-verification-status--legend" class="anchor-link">#</a> Status Verifikasi Unduhan & Legenda',
              "official-zimbra-release-archive-45x--101x": '<a href="#official-zimbra-release-archive-45x--101x" class="anchor-link">#</a> Arsip Rilis Resmi Zimbra (4.5.x – 10.1.x)',
              "unofficial--community-foss-archive-20182026": '<a href="#unofficial--community-foss-archive-20182026" class="anchor-link">#</a> Arsip FOSS Komunitas & Unofficial (2018–2026)',
              "build-systems--source-compilation-guide": '<a href="#build-systems--source-compilation-guide" class="anchor-link">#</a> Sistem Kompilasi & Panduan Kode Sumber',
              "os--zcs-build-compatibility-matrix": '<a href="#os--zcs-build-compatibility-matrix" class="anchor-link">#</a> Matriks Kompatibilitas Kompilasi OS & ZCS',
              "step-by-step-native-compilation": '<a href="#step-by-step-native-compilation" class="anchor-link">#</a> Langkah Kompilasi Native Mandiri',
              "automated-docker--helper-methods": '<a href="#automated-docker--helper-methods" class="anchor-link">#</a> Metode Otomatisasi Docker & Helper',
              "configuration": '<a href="#configuration" class="anchor-link">#</a> Konfigurasi & Optimasi Sistem',
              "sec-1-file-descriptor--security-limits-etcsecuritylimitsconf": '<a href="#sec-1-file-descriptor--security-limits-etcsecuritylimitsconf" class="anchor-link">#</a> 1. File Descriptor & Security Limits (/etc/security/limits.conf)',
              "sec-2-kernel-tuning-etcsysctld99-zimbraconf": '<a href="#sec-2-kernel-tuning-etcsysctld99-zimbraconf" class="anchor-link">#</a> 2. Kernel Tuning (/etc/sysctl.d/99-zimbra.conf)',
              "sec-3-konfigurasi-fqdn--local-dns-etchosts": '<a href="#sec-3-konfigurasi-fqdn--local-dns-etchosts" class="anchor-link">#</a> 3. Konfigurasi FQDN & Local DNS (/etc/hosts)',
              "security-architecture--comprehensive-cve-matrix-20162026": '<a href="#security-architecture--comprehensive-cve-matrix-20162026" class="anchor-link">#</a> Arsitektur Keamanan & Matriks Lengkap CVE (2016–2026)',
              "master-vulnerability-matrix--affected-versions-20162026": '<a href="#master-vulnerability-matrix--affected-versions-20162026" class="anchor-link">#</a> Matriks Kerentanan Utama & Versi Terdampak Resmi (2016–2026)',
              "deep-architecture--attack-surface-analysis": '<a href="#deep-architecture--attack-surface-analysis" class="anchor-link">#</a> Analisis Mendalam Arsitektur & Permukaan Serangan',
              "taxonomy-of-zimbra-threat-vectors--exploit-chains": '<a href="#taxonomy-of-zimbra-threat-vectors--exploit-chains" class="anchor-link">#</a> Taksonomi Vektor Ancaman & Rantai Eksploitasi Zimbra',
              "zero-day-emergency-incident-response--hardening-protocol": '<a href="#zero-day-emergency-incident-response--hardening-protocol" class="anchor-link">#</a> Protokol Tanggap Darurat Insiden Zero-Day & Hardening',
              "sec-1-isolasi-dan-nonaktifkan-vektor-rce-umum": '<a href="#sec-1-isolasi-dan-nonaktifkan-vektor-rce-umum" class="anchor-link">#</a> 1. Isolasi dan Nonaktifkan Vektor RCE Umum',
              "sec-2-audit-dan-karantina-jsp-webshell-di-webroot-jetty": '<a href="#sec-2-audit-dan-karantina-jsp-webshell-di-webroot-jetty" class="anchor-link">#</a> 2. Audit dan Karantina JSP Webshell di Webroot Jetty',
              "sec-3-audit-persistensi-crontab--ssh-keys": '<a href="#sec-3-audit-persistensi-crontab--ssh-keys" class="anchor-link">#</a> 3. Audit Persistensi Crontab & SSH Keys',
              "sec-4-rotasi-kredensial-ldap--kunci-enkripsi": '<a href="#sec-4-rotasi-kredensial-ldap--kunci-enkripsi" class="anchor-link">#</a> 4. Rotasi Kredensial LDAP & Kunci Enkripsi',
              "operational-best-practices-rfc-2119": '<a href="#operational-best-practices-rfc-2119" class="anchor-link">#</a> Praktik Operasional Terbaik (RFC 2119)',
              "strategic-migration--upgrade-methodology": '<a href="#strategic-migration--upgrade-methodology" class="anchor-link">#</a> Metodologi Migrasi Strategis & Upgrade',
              "running-tests": '<a href="#running-tests" class="anchor-link">#</a> Menjalankan Pengujian & Verifikasi Otomatis',
              "ecosystem-tools--repositories": '<a href="#ecosystem-tools--repositories" class="anchor-link">#</a> Alat Ekosistem & Repositori Terkait',
              "contributing": '<a href="#contributing" class="anchor-link">#</a> Panduan Kontribusi',
              "official-contact--author": '<a href="#official-contact--author" class="anchor-link">#</a> Kontak Resmi & Penulis',
              "license": '<a href="#license" class="anchor-link">#</a> Lisensi & Ketentuan Hukum'
            }
          },
          en: {
            title: "Zimbra Link Installer — Binary Archive & CVE Matrix",
            skipLink: "Skip to Main Content",
            navLinks: [
              '<i class="fa-solid fa-compass" aria-hidden="true"></i> Overview',
              '<i class="fa-solid fa-bolt" aria-hidden="true"></i> Quickstart',
              '<i class="fa-solid fa-box-archive" aria-hidden="true"></i> Official Archive',
              '<i class="fa-solid fa-users-gear" aria-hidden="true"></i> Community FOSS',
              '<i class="fa-solid fa-shield-halved" aria-hidden="true"></i> Security & CVEs'
            ],
            sidebarTitles: [
              "Main Navigation",
              "Official Release Archive",
              "Community Archive (FOSS)",
              "Build Systems & Guides",
              "Security & Operations"
            ],
            sidebarLinks: {
              "#overview": '<i class="fa-solid fa-info-circle"></i> Executive Summary',
              "#original-links--references": '<i class="fa-solid fa-link"></i> Original Links & References',
              "#quickstart": '<i class="fa-solid fa-play"></i> Quickstart Guide',
              "#automated-cli-installer-zimbra-link-installersh": '<i class="fa-solid fa-terminal"></i> CLI Installer',
              "#dependencies": '<i class="fa-solid fa-cubes"></i> System Dependencies',
              "#download-verification-status--legend": '<i class="fa-solid fa-circle-check"></i> Verification Legend',
              "#zcs-101x-series-official-releases-daffodil": '<i class="fa-solid fa-box"></i> ZCS 10.1.x Daffodil',
              "#zcs-100x-series-official-releases-daffodil": '<i class="fa-solid fa-box"></i> ZCS 10.0.x Daffodil',
              "#zcs-900x-series-official-releases-kepler": '<i class="fa-solid fa-box"></i> ZCS 9.0.0 Kepler',
              "#zcs-88x-series-official-releases-joule": '<i class="fa-solid fa-box"></i> ZCS 8.8.x Joule',
              "#zcs-87x-series-official-releases-judaspriest": '<i class="fa-solid fa-box"></i> ZCS 8.7.x JudasPriest',
              "#zcs-860-series-official-releases--cumulative-security-patches": '<i class="fa-solid fa-box"></i> ZCS 8.6.0 & Security Patches',
              "#zcs-85x-series-official-releases-851-ga--850-ga": '<i class="fa-solid fa-box"></i> ZCS 8.5.x Official',
              "#zcs-80x-series-official-releases-809-ga-down-to-803-ga": '<i class="fa-solid fa-box"></i> ZCS 8.0.x Official',
              "#zcs-7x-legacy-official-releases-727-ga-720-ga-713-ga-701-ga": '<i class="fa-solid fa-box"></i> ZCS 7.x Legacy',
              "#zcs-6x-legacy-official-releases-6010-ga-609-ga-607-ga": '<i class="fa-solid fa-box"></i> ZCS 6.x Legacy',
              "#zcs-5x-legacy-official-releases-5010-ga-down-to-500-ga": '<i class="fa-solid fa-box"></i> ZCS 5.x Legacy',
              "#zcs-45x-historical-archive-4510-ga-down-to-455-ga": '<i class="fa-solid fa-box"></i> ZCS 4.5.x Historical',
              "#techfilesonline-zimbra-foss-101x-ian-walker-builds": '<i class="fa-solid fa-cube"></i> TechFiles 10.1.20',
              "#zcs-foss-101x-series-all-26-community-releases-20242026": '<i class="fa-solid fa-cube"></i> Maldua FOSS 10.1.x',
              "#zcs-foss-100x-series-all-17-community-releases-20232026": '<i class="fa-solid fa-cube"></i> Maldua FOSS 10.0.x',
              "#zcs-foss-900x-series-all-8-kepler-community-releases-20202025": '<i class="fa-solid fa-cube"></i> Maldua FOSS 9.0.0',
              "#zcs-foss-8815x-series-all-joule-community-releases-20182024": '<i class="fa-solid fa-cube"></i> Maldua FOSS 8.8.15',
              "#build-systems--source-compilation-guide": '<i class="fa-solid fa-wrench"></i> Source Build Guide',
              "#configuration": '<i class="fa-solid fa-sliders"></i> System Configuration',
              "#security-architecture--comprehensive-cve-matrix-20162026": '<i class="fa-solid fa-shield-virus"></i> CVE & Security Matrix',
              "#zero-day-emergency-incident-response--hardening-protocol": '<i class="fa-solid fa-triangle-exclamation"></i> Zero-Day Mitigation',
              "#operational-best-practices-rfc-2119": '<i class="fa-solid fa-clipboard-check"></i> Best Practices (RFC 2119)',
              "#strategic-migration--upgrade-methodology": '<i class="fa-solid fa-arrow-right-arrow-left"></i> Migration Methodology',
              "#official-contact--author": '<i class="fa-solid fa-address-card"></i> Contact & Author'
            },
            heroTitle: '<a href="#zimbra-link-installer--the-complete-zimbra-collaboration-archive--installer-suite" class="anchor-link">#</a> ZIMBRA LINK INSTALLER — THE COMPLETE ZIMBRA COLLABORATION ARCHIVE & INSTALLER SUITE',
            heroSubtitle: "Enterprise Direct Binary Downloads, Official & Unofficial Community Builds, Cryptographic Checksums (MD5/SHA256), CVE Security Advisory Matrix, and Automated CLI Installer Script for Zimbra Collaboration Suite (ZCS 4.5.x – 10.1.x).",
            copyBtnText: '<i class="fa-regular fa-copy"></i> Copy',
            copiedBtnText: '<i class="fa-solid fa-check"></i> Copied!',
            filterPlaceholder: "Search version, OS, build date, or checksum in this table...",
            headings: {
              "table-of-contents": '<a href="#table-of-contents" class="anchor-link">#</a> Table of Contents',
              "overview": '<a href="#overview" class="anchor-link">#</a> Executive Summary & Architecture',
              "original-links--references": '<a href="#original-links--references" class="anchor-link">#</a> Original Links & Official References',
              "portal-resmi--dokumentasi-zimbra-synacor": '<a href="#portal-resmi--dokumentasi-zimbra-synacor" class="anchor-link">#</a> <i class="fa-solid fa-globe text-primary"></i> Official Zimbra Synacor Portals & Documentation',
              "unduhan-biner-komunitas-unofficial-foss--ose--mirror": '<a href="#unduhan-biner-komunitas-unofficial-foss--ose--mirror" class="anchor-link">#</a> <i class="fa-solid fa-box-archive text-warning"></i> Unofficial Community FOSS / OSE Binaries & Mirrors',
              "script-builder-incident-response--toolkits": '<a href="#script-builder-incident-response--toolkits" class="anchor-link">#</a> <i class="fa-solid fa-screwdriver-wrench text-success"></i> Script Builder, Incident Response & Toolkits',
              "quickstart": '<a href="#quickstart" class="anchor-link">#</a> Quickstart Guide',
              "metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan": '<a href="#metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan" class="anchor-link">#</a> Method 1: Using Interactive Automated Script (Recommended)',
              "metode-2-unduhan-manual-biner-target": '<a href="#metode-2-unduhan-manual-biner-target" class="anchor-link">#</a> Method 2: Target Binary Manual Download',
              "automated-cli-installer-zimbra-link-installersh": '<a href="#automated-cli-installer-zimbra-link-installersh" class="anchor-link">#</a> Automated CLI Installer (<code>zimbra-link-installer.sh</code>)',
              "fitur-utama-cli": '<a href="#fitur-utama-cli" class="anchor-link">#</a> CLI Key Features',
              "dependencies": '<a href="#dependencies" class="anchor-link">#</a> System Dependencies & Prerequisites',
              "sec-1-kebutuhan-runtime-minimum": '<a href="#sec-1-kebutuhan-runtime-minimum" class="anchor-link">#</a> 1. Minimum Runtime Requirements',
              "sec-2-kebutuhan-toolchain-kompilasi-build-environment": '<a href="#sec-2-kebutuhan-toolchain-kompilasi-build-environment" class="anchor-link">#</a> 2. Compilation Toolchain Requirements (Build Environment)',
              "download-verification-status--legend": '<a href="#download-verification-status--legend" class="anchor-link">#</a> Download Verification Status & Legend',
              "official-zimbra-release-archive-45x--101x": '<a href="#official-zimbra-release-archive-45x--101x" class="anchor-link">#</a> Official Zimbra Release Archive (4.5.x – 10.1.x)',
              "unofficial--community-foss-archive-20182026": '<a href="#unofficial--community-foss-archive-20182026" class="anchor-link">#</a> Unofficial & Community FOSS Archive (2018–2026)',
              "build-systems--source-compilation-guide": '<a href="#build-systems--source-compilation-guide" class="anchor-link">#</a> Build Systems & Source Compilation Guide',
              "os--zcs-build-compatibility-matrix": '<a href="#os--zcs-build-compatibility-matrix" class="anchor-link">#</a> OS & ZCS Build Compatibility Matrix',
              "step-by-step-native-compilation": '<a href="#step-by-step-native-compilation" class="anchor-link">#</a> Step-by-Step Native Compilation',
              "automated-docker--helper-methods": '<a href="#automated-docker--helper-methods" class="anchor-link">#</a> Automated Docker & Helper Methods',
              "configuration": '<a href="#configuration" class="anchor-link">#</a> System Configuration & OS Tuning',
              "sec-1-file-descriptor--security-limits-etcsecuritylimitsconf": '<a href="#sec-1-file-descriptor--security-limits-etcsecuritylimitsconf" class="anchor-link">#</a> 1. File Descriptor & Security Limits (/etc/security/limits.conf)',
              "sec-2-kernel-tuning-etcsysctld99-zimbraconf": '<a href="#sec-2-kernel-tuning-etcsysctld99-zimbraconf" class="anchor-link">#</a> 2. Kernel Tuning (/etc/sysctl.d/99-zimbra.conf)',
              "sec-3-konfigurasi-fqdn--local-dns-etchosts": '<a href="#sec-3-konfigurasi-fqdn--local-dns-etchosts" class="anchor-link">#</a> 3. FQDN & Local DNS Configuration (/etc/hosts)',
              "security-architecture--comprehensive-cve-matrix-20162026": '<a href="#security-architecture--comprehensive-cve-matrix-20162026" class="anchor-link">#</a> Security Architecture & Comprehensive CVE Matrix (2016–2026)',
              "master-vulnerability-matrix--affected-versions-20162026": '<a href="#master-vulnerability-matrix--affected-versions-20162026" class="anchor-link">#</a> Master Vulnerability Matrix & Official Affected Versions (2016–2026)',
              "deep-architecture--attack-surface-analysis": '<a href="#deep-architecture--attack-surface-analysis" class="anchor-link">#</a> Deep Architecture & Attack Surface Analysis',
              "taxonomy-of-zimbra-threat-vectors--exploit-chains": '<a href="#taxonomy-of-zimbra-threat-vectors--exploit-chains" class="anchor-link">#</a> Taxonomy of Zimbra Threat Vectors & Exploit Chains',
              "zero-day-emergency-incident-response--hardening-protocol": '<a href="#zero-day-emergency-incident-response--hardening-protocol" class="anchor-link">#</a> Zero-Day Emergency Incident Response & Hardening Protocol',
              "sec-1-isolasi-dan-nonaktifkan-vektor-rce-umum": '<a href="#sec-1-isolasi-dan-nonaktifkan-vektor-rce-umum" class="anchor-link">#</a> 1. Isolate and Disable Common RCE Attack Vectors',
              "sec-2-audit-dan-karantina-jsp-webshell-di-webroot-jetty": '<a href="#sec-2-audit-dan-karantina-jsp-webshell-di-webroot-jetty" class="anchor-link">#</a> 2. Audit and Quarantine JSP Webshells in Jetty Webroot',
              "sec-3-audit-persistensi-crontab--ssh-keys": '<a href="#sec-3-audit-persistensi-crontab--ssh-keys" class="anchor-link">#</a> 3. Audit Crontab & SSH Keys Persistence',
              "sec-4-rotasi-kredensial-ldap--kunci-enkripsi": '<a href="#sec-4-rotasi-kredensial-ldap--kunci-enkripsi" class="anchor-link">#</a> 4. Rotate LDAP Credentials & Encryption Keys',
              "operational-best-practices-rfc-2119": '<a href="#operational-best-practices-rfc-2119" class="anchor-link">#</a> Operational Best Practices (RFC 2119)',
              "strategic-migration--upgrade-methodology": '<a href="#strategic-migration--upgrade-methodology" class="anchor-link">#</a> Strategic Migration & Upgrade Methodology',
              "running-tests": '<a href="#running-tests" class="anchor-link">#</a> Running Automated Tests & Checksum Verification',
              "ecosystem-tools--repositories": '<a href="#ecosystem-tools--repositories" class="anchor-link">#</a> Ecosystem Tools & Related Repositories',
              "contributing": '<a href="#contributing" class="anchor-link">#</a> Contribution Guidelines',
              "official-contact--author": '<a href="#official-contact--author" class="anchor-link">#</a> Official Contact & Author',
              "license": '<a href="#license" class="anchor-link">#</a> License & Legal Terms'
            }
          }
        };

        function setLanguage(lang) {
          localStorage.setItem('zimbra_docs_lang', lang);
          document.documentElement.lang = lang;
          const dict = i18nDict[lang] || i18nDict['id'];

          // 1. Toggle button active states
          if (lang === 'en') {
            btnLangEn?.classList.add('active');
            btnLangId?.classList.remove('active');
          } else {
            btnLangId?.classList.add('active');
            btnLangEn?.classList.remove('active');
          }

          // 2. Update Document Title & Skip to Content
          if (dict.title) document.title = dict.title;
          const skipLink = document.querySelector('.skip-to-content');
          if (skipLink) skipLink.textContent = dict.skipLink;

          // 3. Update Navbar Navigation Links
          const navLinks = document.querySelectorAll('.nav-links .nav-link');
          dict.navLinks.forEach((html, i) => {
            if (navLinks[i]) navLinks[i].innerHTML = html;
          });

          // 4. Update Sidebar Section Titles
          const sidebarTitles = document.querySelectorAll('.sidebar-title');
          dict.sidebarTitles.forEach((txt, i) => {
            if (sidebarTitles[i]) sidebarTitles[i].textContent = txt;
          });

          // 5. Update Sidebar Menu Links
          Object.keys(dict.sidebarLinks).forEach(href => {
            const el = document.querySelector(`.sidebar-link[href="${href}"]`);
            if (el) el.innerHTML = dict.sidebarLinks[href];
          });

          // 6. Update Hero Header and Lead Subtitle
          const heroH1 = document.getElementById('zimbra-link-installer--the-complete-zimbra-collaboration-archive--installer-suite');
          if (heroH1) heroH1.innerHTML = dict.heroTitle;

          const heroSub = document.querySelector('.main-wrapper > p.doc-para:nth-of-type(1)');
          if (heroSub) heroSub.textContent = dict.heroSubtitle;

          // 7. Update All Headings (H2, H3, H4)
          Object.keys(dict.headings).forEach(hid => {
            const el = document.getElementById(hid);
            if (el) el.innerHTML = dict.headings[hid];
          });

          // 8. Update Copy Buttons
          document.querySelectorAll('.copy-btn').forEach(b => {
            if (!b.innerHTML.includes('Tersalin') && !b.innerHTML.includes('Copied')) {
              b.innerHTML = dict.copyBtnText;
            }
          });

          // 9. Update Table Filter Search Placeholders
          document.querySelectorAll('.table-filter').forEach(f => {
            f.placeholder = dict.filterPlaceholder;
          });
        }

        btnLangId?.addEventListener('click', () => setLanguage('id'));
        btnLangEn?.addEventListener('click', () => setLanguage('en'));

        // Initialize saved language on DOM load
        const savedLang = localStorage.getItem('zimbra_docs_lang') || 'id';
        setLanguage(savedLang);
    '''

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    js_code = build_js_engine().strip()

    old_block_regex = r'// 7\. Bilingual Language Switcher \(ID / EN\)[\s\S]*?const savedLang = localStorage\.getItem\(\'zimbra_docs_lang\'\) \|\| \'id\';\s*setLanguage\(savedLang\);'
    
    match = re.search(old_block_regex, html)
    if not match:
        print("ERROR: old language switcher block not found!")
        return 1

    new_html = html[:match.start()] + js_code + html[match.end():]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("SUCCESS: index.html fully updated with comprehensive bilingual engine!")
    return 0

if __name__ == '__main__':
    main()
