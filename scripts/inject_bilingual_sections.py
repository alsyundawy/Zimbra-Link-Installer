# -*- coding: utf-8 -*-
"""
inject_bilingual_sections.py
Transforms all content sections in index.html into dual-language ID / EN markup
with .lang-id and .lang-en classes for instant, flawless language switching.
"""

import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Overview Section
    old_overview = r'''        <h2 id="overview" class="heading-anchor">
          <a href="#overview" class="anchor-link">#</a> Overview
        </h2>
        <p class="doc-para">
          <strong>Zimbra Link Installer</strong> adalah repositori referensi
          arsitektural enterprise, indeks arsip biner lengkap, dan utilitas
          instalasi otomatis untuk
          <strong>Zimbra Collaboration Suite (ZCS)</strong> dari rilis historis
          <strong>4.5.x hingga rilis aktif 10.1.x</strong>.
        </p>
        <p class="doc-para">Repositori ini menyatukan:</p>
        <ol class="doc-list">
          <li>
            <strong
              >Interactive Bash CLI Installer (<code
                >zimbra-link-installer.sh</code
              >
              v2.6.3):</strong
            >
            Utilitas interaktif aman bilingual (English &amp; Bahasa Indonesia) dengan _pre-flight system audit_ (RAM,
            storage, FQDN DNS, POSIX pax), penanganan sinyal _atomic cleanup
            trap_, _privilege elevation helper_ (<code>run_privileged</code>),
            dan verifikasi integritas kriptografi SHA256/MD5 otomatis.
          </li>
          <li>
            <strong>Comprehensive Official &amp; Unofficial Archive:</strong>
            Mengindeks seluruh tautan unduhan langsung biner resmi (_Network
            Edition, Open Source Edition, Cumulative Security Patches_) dari
            <code>files.zimbra.com</code> serta seluruh kompilasi biner
            komunitas independen (_FOSS Edition 2018–2026_).
          </li>
          <li>
            <strong>Cryptographic Checksums:</strong> Nilai hash MD5 dan SHA256
            untuk memverifikasi integritas setiap installer secara
            case-insensitive.
          </li>
          <li>
            <strong>Compilation Masterclass:</strong> Panduan lengkap kompilasi
            mandiri kode sumber ZCS (8.8, 9.0, 10.0, 10.1) pada Ubuntu (20.04,
            22.04, 24.04) dan RHEL/Rocky/Alma/Oracle (8 &amp; 9).
          </li>
          <li>
            <strong>Security Vulnerability Dossier:</strong> Analisis 32+ CVE
            (2016–2026) dengan
            <strong
              >rincian versi terdampak secara spesifik dan terverifikasi resmi
              pada Zimbra Security Advisories &amp; NIST NVD</strong
            >, taksonomi eksploitasi, dan panduan mitigasi Zero-Day.
          </li>
        </ol>'''

    new_overview = r'''        <h2 id="overview" class="heading-anchor">
          <a href="#overview" class="anchor-link">#</a> <span class="lang-id">Ringkasan Eksekutif &amp; Arsitektur</span><span class="lang-en">Executive Summary &amp; Architecture</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            <strong>Zimbra Link Installer</strong> adalah repositori referensi
            arsitektural enterprise, indeks arsip biner lengkap, dan utilitas
            instalasi otomatis untuk
            <strong>Zimbra Collaboration Suite (ZCS)</strong> dari rilis historis
            <strong>4.5.x hingga rilis aktif 10.1.x</strong>.
          </p>
          <p class="doc-para">Repositori ini menyatukan:</p>
          <ol class="doc-list">
            <li>
              <strong>Interactive Bash CLI Installer (<code>zimbra-link-installer.sh</code> v2.6.3):</strong>
              Utilitas interaktif aman bilingual (English &amp; Bahasa Indonesia) dengan <em>pre-flight system audit</em> (RAM,
              storage, FQDN DNS, POSIX pax), penanganan sinyal <em>atomic cleanup trap</em>, <em>privilege elevation helper</em> (<code>run_privileged</code>),
              dan verifikasi integritas kriptografi SHA256/MD5 otomatis.
            </li>
            <li>
              <strong>Comprehensive Official &amp; Unofficial Archive:</strong>
              Mengindeks seluruh tautan unduhan langsung biner resmi (<em>Network Edition, Open Source Edition, Cumulative Security Patches</em>) dari
              <code>files.zimbra.com</code> serta seluruh kompilasi biner komunitas independen (<em>FOSS Edition 2018–2026</em>).
            </li>
            <li>
              <strong>Cryptographic Checksums:</strong> Nilai hash MD5 dan SHA256 untuk memverifikasi integritas setiap installer secara case-insensitive.
            </li>
            <li>
              <strong>Compilation Masterclass:</strong> Panduan lengkap kompilasi mandiri kode sumber ZCS (8.8, 9.0, 10.0, 10.1) pada Ubuntu (20.04, 22.04, 24.04) dan RHEL/Rocky/Alma/Oracle (8 &amp; 9).
            </li>
            <li>
              <strong>Security Vulnerability Dossier:</strong> Analisis 32+ CVE (2016–2026) dengan <strong>rincian versi terdampak secara spesifik dan terverifikasi resmi pada Zimbra Security Advisories &amp; NIST NVD</strong>, taksonomi eksploitasi, dan panduan mitigasi Zero-Day.
            </li>
          </ol>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            <strong>Zimbra Link Installer</strong> is an enterprise architectural reference repository, comprehensive binary archive index, and automated installation utility for <strong>Zimbra Collaboration Suite (ZCS)</strong> spanning historical releases from <strong>4.5.x up to active 10.1.x</strong>.
          </p>
          <p class="doc-para">This repository unifies:</p>
          <ol class="doc-list">
            <li>
              <strong>Interactive Bash CLI Installer (<code>zimbra-link-installer.sh</code> v2.6.3):</strong>
              A secure, bilingual (English &amp; Bahasa Indonesia) interactive utility with pre-flight system audits (RAM, storage, FQDN DNS, POSIX pax), atomic cleanup trap signal handling, privilege elevation helper (<code>run_privileged</code>), and automatic SHA256/MD5 cryptographic integrity verification.
            </li>
            <li>
              <strong>Comprehensive Official &amp; Unofficial Archive:</strong>
              Indexes all official direct binary download links (<em>Network Edition, Open Source Edition, Cumulative Security Patches</em>) from <code>files.zimbra.com</code> as well as independent community binary builds (<em>FOSS Edition 2018–2026</em>).
            </li>
            <li>
              <strong>Cryptographic Checksums:</strong> Complete MD5 and SHA256 hash values to verify the authenticity and cryptographic integrity of each installer.
            </li>
            <li>
              <strong>Compilation Masterclass:</strong> Comprehensive guide for independently compiling ZCS source code (8.8, 9.0, 10.0, 10.1) on Ubuntu (20.04, 22.04, 24.04) and RHEL/Rocky/Alma/Oracle (8 &amp; 9).
            </li>
            <li>
              <strong>Security Vulnerability Dossier:</strong> In-depth analysis of 32+ CVEs (2016–2026) with official affected version matrices verified against Zimbra Security Advisories &amp; NIST NVD, exploit taxonomy, and zero-day emergency response protocols.
            </li>
          </ol>
        </div>'''

    if old_overview in html:
        html = html.replace(old_overview, new_overview)
        print("Overview updated successfully!")
    else:
        print("WARNING: Overview block not matched exactly, checking substring...")

    # 2. Original Links Lead
    old_orig_lead = r'''        <p class="doc-para">
          Tautan resmi portal Zimbra Synacor, dokumentasi wiki, repository build system, dan rujukan biner komunitas (Unofficial FOSS / OSE):
        </p>'''

    new_orig_lead = r'''        <p class="doc-para lang-id">
          Tautan resmi portal Zimbra Synacor, dokumentasi wiki, repository build system, dan rujukan biner komunitas (Unofficial FOSS / OSE):
        </p>
        <p class="doc-para lang-en">
          Official Zimbra Synacor portals, wiki documentation, build system repositories, and community binary references (Unofficial FOSS / OSE):
        </p>'''

    if old_orig_lead in html:
        html = html.replace(old_orig_lead, new_orig_lead)
        print("Original links lead updated successfully!")

    # 3. Quickstart Lead & Steps
    old_qs = r'''        <h3
          id="metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan"
          class="heading-anchor"
        >
          <a
            href="#metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan"
            class="anchor-link"
            >#</a
          >
          Metode 1: Menggunakan Script Otomatis Interaktif (Direkomendasikan)
        </h3>
        <p class="doc-para">
          Jalankan perintah one-liner berikut pada terminal root / sudo server Linux Anda:
        </p>'''

    new_qs = r'''        <h3
          id="metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan"
          class="heading-anchor"
        >
          <a
            href="#metode-1-menggunakan-script-otomatis-interaktif-direkomendasikan"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Metode 1: Menggunakan Script Otomatis Interaktif (Direkomendasikan)</span>
          <span class="lang-en">Method 1: Using Interactive Automated Script (Recommended)</span>
        </h3>
        <p class="doc-para lang-id">
          Jalankan perintah one-liner berikut pada terminal root / sudo server Linux Anda:
        </p>
        <p class="doc-para lang-en">
          Execute the following one-liner command in your Linux server terminal with root / sudo privileges:
        </p>'''

    if old_qs in html:
        html = html.replace(old_qs, new_qs)
        print("Quickstart method 1 updated successfully!")

    old_qs2 = r'''        <h3
          id="metode-2-unduhan-manual-biner-target"
          class="heading-anchor"
        >
          <a href="#metode-2-unduhan-manual-biner-target" class="anchor-link"
            >#</a
          >
          Metode 2: Unduhan Manual Biner Target
        </h3>
        <p class="doc-para">
          Jika Anda hanya memerlukan biner tertentu, temukan versi yang sesuai pada tabel arsip di bawah, salin tautan, lalu unduh menggunakan <code>wget</code> atau <code>curl</code>:
        </p>'''

    new_qs2 = r'''        <h3
          id="metode-2-unduhan-manual-biner-target"
          class="heading-anchor"
        >
          <a href="#metode-2-unduhan-manual-biner-target" class="anchor-link"
            >#</a
          >
          <span class="lang-id">Metode 2: Unduhan Manual Biner Target</span>
          <span class="lang-en">Method 2: Target Binary Manual Download</span>
        </h3>
        <p class="doc-para lang-id">
          Jika Anda hanya memerlukan biner tertentu, temukan versi yang sesuai pada tabel arsip di bawah, salin tautan, lalu unduh menggunakan <code>wget</code> atau <code>curl</code>:
        </p>
        <p class="doc-para lang-en">
          If you only need a specific binary, find the corresponding version in the archive tables below, copy the link, and download it using <code>wget</code> or <code>curl</code>:
        </p>'''

    if old_qs2 in html:
        html = html.replace(old_qs2, new_qs2)
        print("Quickstart method 2 updated successfully!")

    # 4. Build Guide Lead
    old_build_lead = r'''        <p class="doc-para">
          Panduan kompilasi mandiri kode sumber resmi (_official upstream source
          code_) menggunakan framework <code>zm-build</code> pada
          <strong>Ubuntu 20.04–24.04 LTS</strong> dan
          <strong>RHEL / Rocky / AlmaLinux 8–9</strong>.
        </p>'''

    new_build_lead = r'''        <p class="doc-para lang-id">
          Panduan kompilasi mandiri kode sumber resmi (<em>official upstream source code</em>) menggunakan framework <code>zm-build</code> pada
          <strong>Ubuntu 20.04–24.04 LTS</strong> dan <strong>RHEL / Rocky / AlmaLinux 8–9</strong>.
        </p>
        <p class="doc-para lang-en">
          Comprehensive guide for independently building official upstream source code using the <code>zm-build</code> framework on
          <strong>Ubuntu 20.04–24.04 LTS</strong> and <strong>RHEL / Rocky / AlmaLinux 8–9</strong>.
        </p>'''

    if old_build_lead in html:
        html = html.replace(old_build_lead, new_build_lead)
        print("Build guide lead updated successfully!")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: inject_bilingual_sections finished!")

if __name__ == '__main__':
    main()
