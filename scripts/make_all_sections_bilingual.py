# -*- coding: utf-8 -*-
"""
make_all_sections_bilingual.py
Replaces text sections in index.html with crisp, complete dual-language (ID/EN) elements.
"""

import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Quickstart Section
    old_qs_block = r'''        <h2 id="quickstart" class="heading-anchor">
          <a href="#quickstart" class="anchor-link">#</a> Quickstart
        </h2>
        <h3
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
        </p>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"
              ><i class="fa-solid fa-terminal"></i> BASH</span
            ><button type="button" class="copy-btn" onclick="copyCode(this)">
              <i class="fa-regular fa-copy"></i> Salin
            </button>
          </div>
          <pre><code class="language-bash"># Unduh dan jalankan Zimbra Link Installer secara langsung
curl -fsSL https://raw.githubusercontent.com/alsyundawy/Zimbra-Link-Installer/main/zimbra-link-installer.sh -o zimbra-link-installer.sh
chmod +x zimbra-link-installer.sh
sudo ./zimbra-link-installer.sh</code></pre>
        </div>
        <h3 id="metode-2-unduhan-manual-biner-target" class="heading-anchor">
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

    new_qs_block = r'''        <h2 id="quickstart" class="heading-anchor">
          <a href="#quickstart" class="anchor-link">#</a> <span class="lang-id">Mulai Cepat (Quickstart)</span><span class="lang-en">Quickstart Guide</span>
        </h2>
        <h3
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
        </p>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"
              ><i class="fa-solid fa-terminal"></i> BASH</span
            ><button type="button" class="copy-btn" onclick="copyCode(this)">
              <i class="fa-regular fa-copy"></i> Salin
            </button>
          </div>
          <pre><code class="language-bash"># Download and execute Zimbra Link Installer directly
curl -fsSL https://raw.githubusercontent.com/alsyundawy/Zimbra-Link-Installer/main/zimbra-link-installer.sh -o zimbra-link-installer.sh
chmod +x zimbra-link-installer.sh
sudo ./zimbra-link-installer.sh</code></pre>
        </div>
        <h3 id="metode-2-unduhan-manual-biner-target" class="heading-anchor">
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

    if old_qs_block in html:
        html = html.replace(old_qs_block, new_qs_block)

    # 2. CLI Installer Features
    old_cli_text = r'''        <p class="doc-para">
          Skrip <code>zimbra-link-installer.sh</code> (v2.6.3) menyederhanakan
          siklus pengunduhan dan instalasi ZCS di lingkungan Linux enterprise dengan dukungan penuh dwibahasa (English &amp; Bahasa Indonesia):
        </p>'''

    new_cli_text = r'''        <p class="doc-para lang-id">
          Skrip <code>zimbra-link-installer.sh</code> (v2.6.3) menyederhanakan
          siklus pengunduhan dan instalasi ZCS di lingkungan Linux enterprise dengan dukungan penuh dwibahasa (English &amp; Bahasa Indonesia):
        </p>
        <p class="doc-para lang-en">
          The <code>zimbra-link-installer.sh</code> script (v2.6.3) streamlines the download, integrity verification, and installation lifecycle of ZCS in enterprise Linux environments with full bilingual support (English &amp; Bahasa Indonesia):
        </p>'''

    if old_cli_text in html:
        html = html.replace(old_cli_text, new_cli_text)

    # 3. CLI Features List
    old_cli_feats = r'''        <h3 id="fitur-utama-cli" class="heading-anchor">
          <a href="#fitur-utama-cli" class="anchor-link">#</a> Fitur Utama CLI
        </h3>
        <ul class="doc-list">
          <li>
            <strong>Defensive Shell Architecture:</strong> Dilengkapi
            <code>set -Eeuo pipefail</code>, `IFS=$'
          </li>
        </ul>
        <p class="doc-para">
          '<code>, dan </code>umask 022` untuk perlindungan dari race-condition
          dan word splitting.
        </p>
        <ul class="doc-list">
          <li>
            <strong>Deteksi Otomatis Sistem:</strong> Mengidentifikasi
            distribusi (Ubuntu/RHEL/Rocky/Alma/Oracle Linux), arsitektur
            kernel, kapasitas RAM, dan storage <code>/opt/zimbra</code>.
          </li>
          <li>
            <strong>Pre-Flight FQDN &amp; Pax Audit:</strong> Memeriksa kesiapan
            FQDN DNS resolver (<code>hostname -f</code>) dan memastikan utilitas
            POSIX <code>pax</code> telah aktif guna menangkal CVE-2022-41352.
          </li>
          <li>
            <strong>Anti-Hotlink Header Handling:</strong> Menginjeksi header
            <code>Referer</code> secara otomatis saat mengunduh dari CDN
            komunitas TechFiles.
          </li>
          <li>
            <strong>Integritas Kriptografi Otomatis:</strong> Mengunduh hash
            <code>.sha256</code> atau <code>.md5</code> dan memvalidasi file
            arsip secara case-insensitive sebelum diekstrak.
          </li>
          <li>
            <strong>Atomic Cleanup:</strong> Menangkap sinyal <code>EXIT</code>,
            <code>INT</code>, <code>TERM</code>, <code>HUP</code> untuk
            pembersihan aman direktori temporer.
          </li>
        </ul>'''

    new_cli_feats = r'''        <h3 id="fitur-utama-cli" class="heading-anchor">
          <a href="#fitur-utama-cli" class="anchor-link">#</a> <span class="lang-id">Fitur Utama CLI</span><span class="lang-en">CLI Key Features</span>
        </h3>
        <div class="lang-id">
          <ul class="doc-list">
            <li>
              <strong>Defensive Shell Architecture:</strong> Dilengkapi <code>set -Eeuo pipefail</code>, <code>IFS=$'\n\t'</code>, dan <code>umask 022</code> untuk perlindungan maksimal dari race-condition dan word splitting.
            </li>
            <li>
              <strong>Deteksi Otomatis Sistem:</strong> Mengidentifikasi distribusi (Ubuntu/RHEL/Rocky/Alma/Oracle Linux), arsitektur kernel (x86_64), kapasitas RAM, dan storage <code>/opt/zimbra</code>.
            </li>
            <li>
              <strong>Pre-Flight FQDN &amp; Pax Audit:</strong> Memeriksa kesiapan FQDN DNS resolver (<code>hostname -f</code>) dan memastikan utilitas POSIX <code>pax</code> aktif guna menangkal CVE-2022-41352.
            </li>
            <li>
              <strong>Anti-Hotlink Header Handling:</strong> Menginjeksi header <code>Referer</code> secara otomatis saat mengunduh dari CDN komunitas TechFiles.
            </li>
            <li>
              <strong>Integritas Kriptografi Otomatis:</strong> Mengunduh hash <code>.sha256</code> atau <code>.md5</code> dan memvalidasi integritas file arsip secara case-insensitive sebelum diekstrak.
            </li>
            <li>
              <strong>Atomic Cleanup:</strong> Menangkap sinyal <code>EXIT</code>, <code>INT</code>, <code>TERM</code>, <code>HUP</code> untuk pembersihan aman direktori temporer.
            </li>
          </ul>
        </div>
        <div class="lang-en">
          <ul class="doc-list">
            <li>
              <strong>Defensive Shell Architecture:</strong> Engineered with <code>set -Eeuo pipefail</code>, <code>IFS=$'\n\t'</code>, and <code>umask 022</code> for robust protection against race conditions and word splitting.
            </li>
            <li>
              <strong>Automated OS &amp; Hardware Detection:</strong> Auto-identifies distribution (Ubuntu/RHEL/Rocky/Alma/Oracle Linux), kernel architecture (x86_64), RAM capacity, and <code>/opt/zimbra</code> storage space.
            </li>
            <li>
              <strong>Pre-Flight FQDN &amp; Pax Audit:</strong> Validates FQDN DNS resolution (<code>hostname -f</code>) and verifies POSIX <code>pax</code> utility availability to mitigate CVE-2022-41352.
            </li>
            <li>
              <strong>Anti-Hotlink Header Handling:</strong> Automatically injects required <code>Referer</code> headers when fetching from TechFiles community CDN mirrors.
            </li>
            <li>
              <strong>Automated Cryptographic Integrity:</strong> Downloads matching <code>.sha256</code> or <code>.md5</code> checksums and validates archive integrity case-insensitively before extraction.
            </li>
            <li>
              <strong>Atomic Cleanup Trap:</strong> Captures <code>EXIT</code>, <code>INT</code>, <code>TERM</code>, <code>HUP</code> signals to ensure deterministic removal of temporary working files.
            </li>
          </ul>
        </div>'''

    if old_cli_feats in html:
        html = html.replace(old_cli_feats, new_cli_feats)

    # 4. Dependencies
    old_deps = r'''        <h2 id="dependencies" class="heading-anchor">
          <a href="#dependencies" class="anchor-link">#</a> Dependencies
        </h2>
        <p class="doc-para">
          Sebelum instalasi atau kompilasi ZCS, pastikan dependensi sistem
          berikut telah terpenuhi:
        </p>
        <h3 id="sec-1-kebutuhan-runtime-minimum" class="heading-anchor">
          <a href="#sec-1-kebutuhan-runtime-minimum" class="anchor-link">#</a> 1.
          Kebutuhan Runtime Minimum
        </h3>
        <ul class="doc-list">
          <li>
            <strong>Arsitektur:</strong> <code>x86_64</code> (64-bit Linux).
          </li>
          <li>
            <strong>Memori RAM:</strong> Minimal 8 GB RAM (Direkomendasikan
            16–32 GB untuk server produksi aktif).
          </li>
          <li>
            <strong>Disk Space:</strong> Minimal 50 GB ruang kosong pada
            direktori <code>/opt/zimbra</code>.
          </li>
          <li>
            <strong>Utilitas Wajib:</strong> <code>pax</code>,
            <code>net-tools</code>, <code>sysstat</code>, <code>libaio1</code>,
            <code>perl</code>, <code>cron</code>.
          </li>
        </ul>
        <h3
          id="sec-2-kebutuhan-toolchain-kompilasi-build-environment"
          class="heading-anchor"
        >
          <a
            href="#sec-2-kebutuhan-toolchain-kompilasi-build-environment"
            class="anchor-link"
            >#</a
          >
          2. Kebutuhan Toolchain Kompilasi (Build Environment)
        </h3>
        <ul class="doc-list">
          <li>
            <strong>Java Development Kit:</strong> OpenJDK 11 / OpenJDK 17
            (<code>openjdk-11-jdk</code>, <code>openjdk-17-jdk</code>).
          </li>
          <li>
            <strong>Build Automations:</strong> Apache Ant (<code>ant</code>,
            <code>ant-optional</code>), Apache Maven (<code>mvn</code>).
          </li>
          <li>
            <strong>C/C++ Native Toolchain:</strong> <code>gcc</code>,
            <code>g++</code>, <code>make</code>, <code>cmake</code>,
            <code>libtool</code>, <code>autoconf</code>, <code>automake</code>,
            <code>pkg-config</code>, <code>libcppunit-dev</code>.
          </li>
          <li>
            <strong>Scripting &amp; Engine:</strong> Perl modules
            (<code>XML::Simple</code>, <code>Data::UUID</code>,
            <code>File::Slurp</code>, <code>JSON</code>, <code>YAML</code>),
            Ruby, Node.js, NPM.
          </li>
        </ul>'''

    new_deps = r'''        <h2 id="dependencies" class="heading-anchor">
          <a href="#dependencies" class="anchor-link">#</a> <span class="lang-id">Dependensi &amp; Persyaratan Sistem</span><span class="lang-en">System Dependencies &amp; Prerequisites</span>
        </h2>
        <p class="doc-para lang-id">
          Sebelum instalasi atau kompilasi ZCS, pastikan dependensi sistem berikut telah terpenuhi:
        </p>
        <p class="doc-para lang-en">
          Ensure the following system prerequisites and dependencies are satisfied prior to ZCS installation or compilation:
        </p>
        <h3 id="sec-1-kebutuhan-runtime-minimum" class="heading-anchor">
          <a href="#sec-1-kebutuhan-runtime-minimum" class="anchor-link">#</a> <span class="lang-id">1. Kebutuhan Runtime Minimum</span><span class="lang-en">1. Minimum Runtime Requirements</span>
        </h3>
        <div class="lang-id">
          <ul class="doc-list">
            <li><strong>Arsitektur:</strong> <code>x86_64</code> (64-bit Linux).</li>
            <li><strong>Memori RAM:</strong> Minimal 8 GB RAM (Direkomendasikan 16–32 GB untuk server produksi aktif).</li>
            <li><strong>Disk Space:</strong> Minimal 50 GB ruang kosong pada direktori <code>/opt/zimbra</code>.</li>
            <li><strong>Utilitas Wajib:</strong> <code>pax</code>, <code>net-tools</code>, <code>sysstat</code>, <code>libaio1</code>, <code>perl</code>, <code>cron</code>.</li>
          </ul>
        </div>
        <div class="lang-en">
          <ul class="doc-list">
            <li><strong>Architecture:</strong> <code>x86_64</code> (64-bit Linux).</li>
            <li><strong>Memory (RAM):</strong> Minimum 8 GB RAM (16–32 GB recommended for active production deployments).</li>
            <li><strong>Storage (Disk Space):</strong> Minimum 50 GB free space dedicated to <code>/opt/zimbra</code>.</li>
            <li><strong>Mandatory Utilities:</strong> <code>pax</code>, <code>net-tools</code>, <code>sysstat</code>, <code>libaio1</code>, <code>perl</code>, <code>cron</code>.</li>
          </ul>
        </div>
        <h3
          id="sec-2-kebutuhan-toolchain-kompilasi-build-environment"
          class="heading-anchor"
        >
          <a
            href="#sec-2-kebutuhan-toolchain-kompilasi-build-environment"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">2. Kebutuhan Toolchain Kompilasi (Build Environment)</span><span class="lang-en">2. Compilation Toolchain Requirements (Build Environment)</span>
        </h3>
        <div class="lang-id">
          <ul class="doc-list">
            <li><strong>Java Development Kit:</strong> OpenJDK 11 / OpenJDK 17 (<code>openjdk-11-jdk</code>, <code>openjdk-17-jdk</code>).</li>
            <li><strong>Build Automations:</strong> Apache Ant (<code>ant</code>, <code>ant-optional</code>), Apache Maven (<code>mvn</code>).</li>
            <li><strong>C/C++ Native Toolchain:</strong> <code>gcc</code>, <code>g++</code>, <code>make</code>, <code>cmake</code>, <code>libtool</code>, <code>autoconf</code>, <code>automake</code>, <code>pkg-config</code>, <code>libcppunit-dev</code>.</li>
            <li><strong>Scripting &amp; Engine:</strong> Perl modules (<code>XML::Simple</code>, <code>Data::UUID</code>, <code>File::Slurp</code>, <code>JSON</code>, <code>YAML</code>), Ruby, Node.js, NPM.</li>
          </ul>
        </div>
        <div class="lang-en">
          <ul class="doc-list">
            <li><strong>Java Development Kit:</strong> OpenJDK 11 / OpenJDK 17 (<code>openjdk-11-jdk</code>, <code>openjdk-17-jdk</code>).</li>
            <li><strong>Build Automation:</strong> Apache Ant (<code>ant</code>, <code>ant-optional</code>), Apache Maven (<code>mvn</code>).</li>
            <li><strong>C/C++ Native Toolchain:</strong> <code>gcc</code>, <code>g++</code>, <code>make</code>, <code>cmake</code>, <code>libtool</code>, <code>autoconf</code>, <code>automake</code>, <code>pkg-config</code>, <code>libcppunit-dev</code>.</li>
            <li><strong>Scripting &amp; Runtimes:</strong> Perl modules (<code>XML::Simple</code>, <code>Data::UUID</code>, <code>File::Slurp</code>, <code>JSON</code>, <code>YAML</code>), Ruby, Node.js, NPM.</li>
          </ul>
        </div>'''

    if old_deps in html:
        html = html.replace(old_deps, new_deps)

    # 5. Verification Legend
    old_legend = r'''        <h2 id="download-verification-status--legend" class="heading-anchor">
          <a href="#download-verification-status--legend" class="anchor-link"
            >#</a
          >
          Download Verification Status &amp; Legend
        </h2>
        <p class="doc-para">
          Setiap tautan unduhan dalam repositori ini telah diuji secara berkala
          dengan skrip telemetri HTTP. Berikut arti label status yang
          disematkan:
        </p>
        <ul class="doc-list">
          <li>
            🟢 <strong><code>[Active Direct]</code></strong> — Tautan langsung
            aktif pada server resmi <code>files.zimbra.com</code> atau GitHub
            CDN (HTTP 200 OK). Dapat diunduh secara instan tanpa header khusus.
          </li>
          <li>
            🟡 <strong><code>[Referer Req]</code></strong> — Tautan aktif pada
            mirror CDN TechFiles.online. <strong>Wajib</strong> menyertakan
            header referer <code>Referer: https://techfiles.online/</code> saat
            diunduh via CLI / automation script.
          </li>
          <li>
            🔴 <strong><code>[Need Mirror / Portal Only]</code></strong> — File
            biner telah diarsipkan oleh upstream vendor atau memerlukan akun
            berbayar Synacor Portal. Disarankan melakukan kompilasi mandiri via
            <code>zm-build</code> atau menggunakan rilis komunitas yang setara.
          </li>
        </ul>'''

    new_legend = r'''        <h2 id="download-verification-status--legend" class="heading-anchor">
          <a href="#download-verification-status--legend" class="anchor-link"
            >#</a
          >
          <span class="lang-id">Status Verifikasi Unduhan &amp; Legenda</span><span class="lang-en">Download Verification Status &amp; Legend</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Setiap tautan unduhan dalam repositori ini telah diuji secara berkala dengan skrip telemetri HTTP. Berikut arti label status yang disematkan:
          </p>
          <ul class="doc-list">
            <li>
              🟢 <strong><code>[Active Direct]</code></strong> — Tautan langsung aktif pada server resmi <code>files.zimbra.com</code> atau GitHub CDN (HTTP 200 OK). Dapat diunduh secara instan tanpa header khusus.
            </li>
            <li>
              🟡 <strong><code>[Referer Req]</code></strong> — Tautan aktif pada mirror CDN TechFiles.online. <strong>Wajib</strong> menyertakan header referer <code>Referer: https://techfiles.online/</code> saat diunduh via CLI / automation script.
            </li>
            <li>
              🔴 <strong><code>[Need Mirror / Portal Only]</code></strong> — File biner telah diarsipkan oleh upstream vendor atau memerlukan akun berbayar Synacor Portal. Disarankan melakukan kompilasi mandiri via <code>zm-build</code> atau menggunakan rilis komunitas yang setara.
            </li>
          </ul>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Every download link in this repository is continuously tested with automated HTTP telemetry suites. The status badges are defined as follows:
          </p>
          <ul class="doc-list">
            <li>
              🟢 <strong><code>[Active Direct]</code></strong> — Active direct link on official <code>files.zimbra.com</code> servers or GitHub CDN (HTTP 200 OK). Downloads instantly without special headers.
            </li>
            <li>
              🟡 <strong><code>[Referer Req]</code></strong> — Active link on TechFiles.online CDN mirror. <strong>Requires</strong> the HTTP referer header <code>Referer: https://techfiles.online/</code> when fetched via CLI or automated scripts.
            </li>
            <li>
              🔴 <strong><code>[Need Mirror / Portal Only]</code></strong> — Binary archived by upstream vendor or requires Synacor portal authentication. Community builds or self-compilation via <code>zm-build</code> is recommended.
            </li>
          </ul>
        </div>'''

    if old_legend in html:
        html = html.replace(old_legend, new_legend)

    # 6. Strategic Migration & Upgrade Methodology
    old_mig = r'''        <h2
          id="strategic-migration--upgrade-methodology"
          class="heading-anchor"
        >
          <a
            href="#strategic-migration--upgrade-methodology"
            class="anchor-link"
            >#</a
          >
          Strategic Migration &amp; Upgrade Methodology
        </h2>
        <p class="doc-para">Panduan migrasi dan upgrade sistem ZCS:</p>
        <ol class="doc-list">
          <li>
            <strong
              >Metode Rekomendasi: Clean Install &amp; Zero-Contamination
              Migration</strong
            >
          </li>
        </ol>
        <ul class="doc-list">
          <li>
            Bangun instance server baru menggunakan Ubuntu 22.04 LTS / 24.04 LTS
            atau Rocky Linux 9.
          </li>
          <li>
            Pasang ZCS 10.1.x (Network Edition atau Maldua FOSS 10.1.20+).
          </li>
          <li>
            Migrasikan seluruh domain, akun, alias, distribution list, dan isi
            mailbox menggunakan utilitas migrasi mailbox murni seperti
            <strong
              ><a
                href="https://github.com/alsyundawy/Z2C"
                target="_blank"
                rel="noopener noreferrer"
                >Z2C</a
              ></strong
            >.
          </li>
        </ul>
        <ol class="doc-list">
          <li><strong>Metode Alternatif: Rolling In-Place Upgrade</strong></li>
        </ol>
        <ul class="doc-list">
          <li>
            Jalankan audit sanitasi total sistem menggunakan toolkit IR
            <strong
              ><a
                href="https://github.com/alsyundawy/eradicate-zimbra-malware"
                target="_blank"
                rel="noopener noreferrer"
                >eradicate-zimbra-malware</a
              ></strong
            >.
          </li>
          <li>Buat backup penuh di luar server.</li>
          <li>
            Upgrade bertahap: <code>ZCS 8.8.15 P46</code> ➔
            <code>ZCS 9.0.0 P41</code> ➔ <code>ZCS 10.1.x</code>.
          </li>
          <li>
            Jalankan
            <code>/opt/zimbra/libexec/zmfixperms --extended</code>
            pasca-upgrade.
          </li>
        </ul>'''

    new_mig = r'''        <h2
          id="strategic-migration--upgrade-methodology"
          class="heading-anchor"
        >
          <a
            href="#strategic-migration--upgrade-methodology"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Metodologi Migrasi Strategis &amp; Upgrade</span><span class="lang-en">Strategic Migration &amp; Upgrade Methodology</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">Panduan migrasi dan upgrade sistem ZCS:</p>
          <ol class="doc-list">
            <li>
              <strong>Metode Rekomendasi: Clean Install &amp; Zero-Contamination Migration</strong>
            </li>
          </ol>
          <ul class="doc-list">
            <li>Bangun instance server baru menggunakan Ubuntu 22.04 LTS / 24.04 LTS atau Rocky Linux 9.</li>
            <li>Pasang ZCS 10.1.x (Network Edition atau Maldua FOSS 10.1.20+).</li>
            <li>Migrasikan seluruh domain, akun, alias, distribution list, dan isi mailbox menggunakan utilitas migrasi mailbox murni seperti <strong><a href="https://github.com/alsyundawy/Z2C" target="_blank" rel="noopener noreferrer">Z2C</a></strong>.</li>
          </ul>
          <ol class="doc-list">
            <li><strong>Metode Alternatif: Rolling In-Place Upgrade</strong></li>
          </ol>
          <ul class="doc-list">
            <li>Jalankan audit sanitasi total sistem menggunakan toolkit IR <strong><a href="https://github.com/alsyundawy/eradicate-zimbra-malware" target="_blank" rel="noopener noreferrer">eradicate-zimbra-malware</a></strong>.</li>
            <li>Buat backup penuh di luar server (off-site backup).</li>
            <li>Upgrade bertahap: <code>ZCS 8.8.15 P46</code> ➔ <code>ZCS 9.0.0 P41</code> ➔ <code>ZCS 10.1.x</code>.</li>
            <li>Jalankan <code>/opt/zimbra/libexec/zmfixperms --extended</code> pasca-upgrade.</li>
          </ul>
        </div>
        <div class="lang-en">
          <p class="doc-para">Comprehensive ZCS migration and upgrade architecture:</p>
          <ol class="doc-list">
            <li>
              <strong>Recommended Strategy: Clean Install &amp; Zero-Contamination Migration</strong>
            </li>
          </ol>
          <ul class="doc-list">
            <li>Provision a clean target server instance running Ubuntu 22.04 / 24.04 LTS or Rocky Linux 9.</li>
            <li>Install fresh ZCS 10.1.x (Network Edition or Maldua FOSS 10.1.20+).</li>
            <li>Migrate all domains, accounts, aliases, distribution lists, and mailbox contents via pure mailbox migration engines such as <strong><a href="https://github.com/alsyundawy/Z2C" target="_blank" rel="noopener noreferrer">Z2C</a></strong>.</li>
          </ul>
          <ol class="doc-list">
            <li><strong>Alternative Strategy: Rolling In-Place Upgrade</strong></li>
          </ol>
          <ul class="doc-list">
            <li>Execute an exhaustive system sanitation audit with the incident response suite <strong><a href="https://github.com/alsyundawy/eradicate-zimbra-malware" target="_blank" rel="noopener noreferrer">eradicate-zimbra-malware</a></strong>.</li>
            <li>Take complete offline server snapshots and off-site cold backups.</li>
            <li>Upgrade iteratively: <code>ZCS 8.8.15 P46</code> ➔ <code>ZCS 9.0.0 P41</code> ➔ <code>ZCS 10.1.x</code>.</li>
            <li>Execute <code>/opt/zimbra/libexec/zmfixperms --extended</code> following upgrade completion.</li>
          </ul>
        </div>'''

    if old_mig in html:
        html = html.replace(old_mig, new_mig)

    # 7. Contributing
    old_contrib = r'''        <h2 id="contributing" class="heading-anchor">
          <a href="#contributing" class="anchor-link">#</a> Contributing
        </h2>
        <p class="doc-para">
          Kontribusi berupa penambahan tautan rilis baru, pembaruan checksum,
          laporan tautan mirror rusak, atau dokumentasi keamanan sangat
          diapresiasi.
        </p>
        <ul class="doc-list">
          <li><strong>Alur Kontribusi (Pull Request Workflow):</strong></li>
        </ul>
        <ol class="doc-list">
          <li>Fork repository ini ke akun GitHub Anda.</li>
          <li>
            Buat branch fitur baru (<code
              >git checkout -b feature/tambah-versi-10.1.x</code
            >).
          </li>
          <li>Lakukan verifikasi checksum URL yang ditambahkan.</li>
          <li>
            Submit Pull Request dengan deskripsi yang jelas dan referensi rilis
            resmi.
          </li>
        </ol>'''

    new_contrib = r'''        <h2 id="contributing" class="heading-anchor">
          <a href="#contributing" class="anchor-link">#</a> <span class="lang-id">Panduan Kontribusi</span><span class="lang-en">Contribution Guidelines</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Kontribusi berupa penambahan tautan rilis baru, pembaruan checksum, laporan tautan mirror rusak, atau dokumentasi keamanan sangat diapresiasi.
          </p>
          <ul class="doc-list">
            <li><strong>Alur Kontribusi (Pull Request Workflow):</strong></li>
          </ul>
          <ol class="doc-list">
            <li>Fork repository ini ke akun GitHub Anda.</li>
            <li>Buat branch fitur baru (<code>git checkout -b feature/tambah-versi-10.1.x</code>).</li>
            <li>Lakukan verifikasi checksum URL yang ditambahkan.</li>
            <li>Submit Pull Request dengan deskripsi yang jelas dan referensi rilis resmi.</li>
          </ol>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Contributions including new release links, checksum updates, broken mirror reports, or security documentation enhancements are highly appreciated.
          </p>
          <ul class="doc-list">
            <li><strong>Pull Request Workflow:</strong></li>
          </ul>
          <ol class="doc-list">
            <li>Fork this repository to your GitHub account.</li>
            <li>Create a new feature branch (<code>git checkout -b feature/add-version-10.1.x</code>).</li>
            <li>Verify the HTTP availability and checksums of all added URLs.</li>
            <li>Submit a Pull Request with a clear description and official release references.</li>
          </ol>
        </div>'''

    if old_contrib in html:
        html = html.replace(old_contrib, new_contrib)

    # 8. License
    old_lic = r'''        <h2 id="license" class="heading-anchor">
          <a href="#license" class="anchor-link">#</a> License
        </h2>
        <p class="doc-para">
          Didistribusikan di bawah <strong>Lisensi Resmi MIT</strong>. Lihat
          berkas [LICENSE](LICENSE) untuk ketentuan hukum lengkap.
        </p>
        <p class="doc-para">
          Copyright (c) 2016-2026
          <strong>Harry Dertin Sutisna Alsyundawy</strong>. All rights reserved.
        </p>'''

    new_lic = r'''        <h2 id="license" class="heading-anchor">
          <a href="#license" class="anchor-link">#</a> <span class="lang-id">Lisensi &amp; Ketentuan Hukum</span><span class="lang-en">License &amp; Legal Terms</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Didistribusikan di bawah <strong>Lisensi Resmi MIT</strong>. Lihat berkas <a href="LICENSE" target="_blank" rel="noopener noreferrer">LICENSE</a> untuk ketentuan hukum lengkap.
          </p>
          <p class="doc-para">
            Copyright (c) 2016-2026 <strong>Harry Dertin Sutisna Alsyundawy</strong>. All rights reserved.
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Distributed under the official <strong>MIT License</strong>. Refer to the <a href="LICENSE" target="_blank" rel="noopener noreferrer">LICENSE</a> file for full legal terms.
          </p>
          <p class="doc-para">
            Copyright (c) 2016-2026 <strong>Harry Dertin Sutisna Alsyundawy</strong>. All rights reserved.
          </p>
        </div>'''

    if old_lic in html:
        html = html.replace(old_lic, new_lic)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: make_all_sections_bilingual completed!")

if __name__ == '__main__':
    main()
