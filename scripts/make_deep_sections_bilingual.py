# -*- coding: utf-8 -*-
"""
make_deep_sections_bilingual.py
Adds full dual-language markup to Configuration, Security Architecture,
Zero-Day Protocol, RFC 2119 Best Practices, Running Tests, Ecosystem Tools,
and Contact sections in index.html.
"""

import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Configuration Section
    old_config = r'''        <h2 id="configuration" class="heading-anchor">
          <a href="#configuration" class="anchor-link">#</a> Configuration
        </h2>
        <p class="doc-para">
          Konfigurasi optimal sistem operasi host sebelum menjalankan instalasi
          Zimbra:
        </p>'''

    new_config = r'''        <h2 id="configuration" class="heading-anchor">
          <a href="#configuration" class="anchor-link">#</a> <span class="lang-id">Konfigurasi &amp; Optimasi Sistem</span><span class="lang-en">System Configuration &amp; OS Tuning</span>
        </h2>
        <p class="doc-para lang-id">
          Konfigurasi optimal sistem operasi host sebelum menjalankan instalasi Zimbra:
        </p>
        <p class="doc-para lang-en">
          Recommended host operating system tuning parameters before executing Zimbra installation:
        </p>'''

    if old_config in html:
        html = html.replace(old_config, new_config)

    # 2. Security Section Intro
    old_sec_intro = r'''        <h2
          id="security-architecture--comprehensive-cve-matrix-20162026"
          class="heading-anchor"
        >
          <a
            href="#security-architecture--comprehensive-cve-matrix-20162026"
            class="anchor-link"
            >#</a
          >
          Security Architecture &amp; Comprehensive CVE Matrix (2016–2026)
        </h2>
        <p class="doc-para">
          Analisis mendalam arsitektur pertahanan, taksonomi vektor serangan,
          dan katalog komprehensif
          <strong>Kerentanan Keamanan (CVE)</strong> Zimbra Collaboration Suite
          (2016–2026) yang
          <strong
            >100% tervalidasi resmi pada
            <a
              href="https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories"
              target="_blank"
              rel="noopener noreferrer"
              >Zimbra Security Advisories</a
            >
            &amp; NIST NVD</strong
          >. Dilengkapi dengan
          <strong
            >rincian versi terdampak secara spesifik dan tidak terpotong</strong
          >, skor CVSS, severity, reporter/peneliti keamanan, serta panduan
          penanganan insiden darurat (_Zero-Day Triage Protocol_).
        </p>'''

    new_sec_intro = r'''        <h2
          id="security-architecture--comprehensive-cve-matrix-20162026"
          class="heading-anchor"
        >
          <a
            href="#security-architecture--comprehensive-cve-matrix-20162026"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Arsitektur Keamanan &amp; Matriks Lengkap CVE (2016–2026)</span><span class="lang-en">Security Architecture &amp; Comprehensive CVE Matrix (2016–2026)</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Analisis mendalam arsitektur pertahanan, taksonomi vektor serangan, dan katalog komprehensif <strong>Kerentanan Keamanan (CVE)</strong> Zimbra Collaboration Suite (2016–2026) yang <strong>100% tervalidasi resmi pada <a href="https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories" target="_blank" rel="noopener noreferrer">Zimbra Security Advisories</a> &amp; NIST NVD</strong>. Dilengkapi dengan <strong>rincian versi terdampak secara spesifik dan tidak terpotong</strong>, skor CVSS, severity, reporter/peneliti keamanan, serta panduan penanganan insiden darurat (<em>Zero-Day Triage Protocol</em>).
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            In-depth defensive architecture analysis, attack vector taxonomies, and comprehensive <strong>Common Vulnerabilities and Exposures (CVE)</strong> catalog for Zimbra Collaboration Suite (2016–2026), <strong>100% verified against <a href="https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories" target="_blank" rel="noopener noreferrer">Zimbra Security Advisories</a> &amp; NIST NVD</strong>. Features complete affected version breakdowns, CVSS metrics, threat classifications, security researcher credits, and an emergency Zero-Day incident response protocol.
          </p>
        </div>'''

    if old_sec_intro in html:
        html = html.replace(old_sec_intro, new_sec_intro)

    # 3. Master Vulnerability Matrix heading & lead
    old_mvm = r'''        <h3
          id="master-vulnerability-matrix--affected-versions-20162026"
          class="heading-anchor"
        >
          <a
            href="#master-vulnerability-matrix--affected-versions-20162026"
            class="anchor-link"
            >#</a
          >
          Master Vulnerability Matrix &amp; Affected Versions (2016–2026)
        </h3>
        <p class="doc-para">
          Tabel berikut menyajikan seluruh riwayat CVE resmi yang diverifikasi
          pada sistem Zimbra Collaboration Suite:
        </p>'''

    new_mvm = r'''        <h3
          id="master-vulnerability-matrix--affected-versions-20162026"
          class="heading-anchor"
        >
          <a
            href="#master-vulnerability-matrix--affected-versions-20162026"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Matriks Kerentanan Utama &amp; Versi Terdampak Resmi (2016–2026)</span><span class="lang-en">Master Vulnerability Matrix &amp; Affected Versions (2016–2026)</span>
        </h3>
        <p class="doc-para lang-id">
          Tabel berikut menyajikan seluruh riwayat CVE resmi yang diverifikasi pada sistem Zimbra Collaboration Suite:
        </p>
        <p class="doc-para lang-en">
          The following matrix catalogues verified official CVE records for Zimbra Collaboration Suite across all historical and current releases:
        </p>'''

    if old_mvm in html:
        html = html.replace(old_mvm, new_mvm)

    # 4. Attack Surface Analysis
    old_asa = r'''        <h3
          id="deep-architecture--attack-surface-analysis"
          class="heading-anchor"
        >
          <a
            href="#deep-architecture--attack-surface-analysis"
            class="anchor-link"
            >#</a
          >
          Deep Architecture &amp; Attack Surface Analysis
        </h3>
        <p class="doc-para">
          Arsitektur Zimbra terdiri dari beberapa daemon independen yang saling
          berkomunikasi. Pemahaman batas pertahanan (_security perimeter_)
          setiap komponen sangat penting untuk mitigasi proaktif:
        </p>'''

    new_asa = r'''        <h3
          id="deep-architecture--attack-surface-analysis"
          class="heading-anchor"
        >
          <a
            href="#deep-architecture--attack-surface-analysis"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Analisis Mendalam Arsitektur &amp; Permukaan Serangan</span><span class="lang-en">Deep Architecture &amp; Attack Surface Analysis</span>
        </h3>
        <p class="doc-para lang-id">
          Arsitektur Zimbra terdiri dari beberapa daemon independen yang saling berkomunikasi. Pemahaman batas pertahanan (<em>security perimeter</em>) setiap komponen sangat penting untuk mitigasi proaktif:
        </p>
        <p class="doc-para lang-en">
          ZCS architecture comprises multiple decoupled daemons operating across dedicated network boundaries. Understanding the security perimeter of each daemon is essential for proactive threat mitigation:
        </p>'''

    if old_asa in html:
        html = html.replace(old_asa, new_asa)

    # 5. Attack Surface Daemons list
    old_daemons = r'''        <ol class="doc-list">
          <li>
            <strong>Jetty (<code>mailboxd</code>):</strong> Jantung aplikasi
            ZCS. Menjalankan servlet SOAP, REST, Zimlet runtime, dan webmail UI.
            Merupakan target utama eksploitasi JSP Webshell (seperti
            CVE-2019-9670, CVE-2022-27925, dan CVE-2025-68645).
          </li>
          <li>
            <strong>Postfix MTA &amp; Postjournal:</strong> Mengelola antrean email
            masuk/keluar. Layanan postjournal yang rentan terhadap argumen
            injection (CVE-2024-45519) wajib dimatikan jika organisasi tidak
            menggunakan compliance archiving.
          </li>
          <li>
            <strong>Amavisd &amp; Antivirus Scanners:</strong> Membedah attachment
            arsip email. Ketiadaan utilitas POSIX <code>pax</code> menyebabkan
            Amavis menggunakan fallback <code>cpio</code> yang dapat
            dieksploitasi untuk meletakkan webshell arbitrer (CVE-2022-41352).
          </li>
          <li>
            <strong>OpenLDAP (<code>slapd</code>):</strong> Menyimpan seluruh
            metadata akun, domain, dan konfigurasi server global
            (<code>localconfig.xml</code>). Kebocoran kredensial LDAP superadmin
            merupakan gerbang pengambilalihan seluruh sistem mail.
          </li>
          <li>
            <strong>Nginx Reverse Proxy:</strong> Memfilter lalu lintas IMAP,
            POP3, dan HTTP. Template Nginx wajib dikonfigurasi untuk memblokir
            akses eksternal ke endpoint sensitif dan admin port 7071.
          </li>
        </ol>'''

    new_daemons = r'''        <div class="lang-id">
          <ol class="doc-list">
            <li>
              <strong>Jetty (<code>mailboxd</code>):</strong> Jantung aplikasi ZCS. Menjalankan servlet SOAP, REST, Zimlet runtime, dan webmail UI. Merupakan target utama eksploitasi JSP Webshell (seperti CVE-2019-9670, CVE-2022-27925, dan CVE-2025-68645).
            </li>
            <li>
              <strong>Postfix MTA &amp; Postjournal:</strong> Mengelola antrean email masuk/keluar. Layanan postjournal yang rentan terhadap command injection (CVE-2024-45519) wajib dimatikan jika organisasi tidak menggunakan compliance archiving.
            </li>
            <li>
              <strong>Amavisd &amp; Antivirus Scanners:</strong> Membedah attachment arsip email. Ketiadaan utilitas POSIX <code>pax</code> menyebabkan Amavis menggunakan fallback <code>cpio</code> yang dapat dieksploitasi untuk meletakkan webshell arbitrer (CVE-2022-41352).
            </li>
            <li>
              <strong>OpenLDAP (<code>slapd</code>):</strong> Menyimpan seluruh metadata akun, domain, dan konfigurasi server global (<code>localconfig.xml</code>). Kebocoran kredensial LDAP superadmin merupakan gerbang pengambilalihan seluruh sistem mail.
            </li>
            <li>
              <strong>Nginx Reverse Proxy:</strong> Memfilter lalu lintas IMAP, POP3, dan HTTP. Template Nginx wajib dikonfigurasi untuk memblokir akses eksternal ke endpoint sensitif dan admin console port 7071.
            </li>
          </ol>
        </div>
        <div class="lang-en">
          <ol class="doc-list">
            <li>
              <strong>Jetty (<code>mailboxd</code>):</strong> Core application context executing SOAP/REST servlets, Zimlet runtimes, and user webmail. Primary target for JSP webshell injections (CVE-2019-9670, CVE-2022-27925, CVE-2025-68645).
            </li>
            <li>
              <strong>Postfix MTA &amp; Postjournal:</strong> Ingress/egress mail routing daemon. Postjournal component (vulnerable to CVE-2024-45519 command injection) must be disabled unless compliance journaling is strictly required.
            </li>
            <li>
              <strong>Amavisd &amp; Antivirus Scanners:</strong> Unpacks and analyzes inbound message attachments. Missing POSIX <code>pax</code> triggers Amavis fallback to vulnerable <code>cpio</code> handlers (CVE-2022-41352).
            </li>
            <li>
              <strong>OpenLDAP (<code>slapd</code>):</strong> Master directory containing account objects, domain trees, and <code>localconfig.xml</code> credentials. Root LDAP credential leakage enables complete infrastructure takeover.
            </li>
            <li>
              <strong>Nginx Reverse Proxy:</strong> Frontline proxy for IMAP, POP3, and HTTPS. Must be configured to restrict external reachability to sensitive servlets and admin port 7071.
            </li>
          </ol>
        </div>'''

    if old_daemons in html:
        html = html.replace(old_daemons, new_daemons)

    # 6. Zero-Day Protocol Intro
    old_zd_intro = r'''        <h3
          id="zero-day-emergency-incident-response--hardening-protocol"
          class="heading-anchor"
        >
          <a
            href="#zero-day-emergency-incident-response--hardening-protocol"
            class="anchor-link"
            >#</a
          >
          Zero-Day Emergency Incident Response &amp; Hardening Protocol
        </h3>
        <p class="doc-para">
          Jika server Anda dicurigai telah disusupi atau terdapat pengumuman
          Zero-Day baru di alam liar (_active exploitation_), jalankan prosedur
          triase dan sanitasi darurat berikut:
        </p>'''

    new_zd_intro = r'''        <h3
          id="zero-day-emergency-incident-response--hardening-protocol"
          class="heading-anchor"
        >
          <a
            href="#zero-day-emergency-incident-response--hardening-protocol"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Protokol Tanggap Darurat Insiden Zero-Day &amp; Hardening</span><span class="lang-en">Zero-Day Emergency Incident Response &amp; Hardening Protocol</span>
        </h3>
        <p class="doc-para lang-id">
          Jika server Anda dicurigai telah disusupi atau terdapat pengumuman Zero-Day baru di alam liar (<em>active exploitation</em>), jalankan prosedur triase dan sanitasi darurat berikut:
        </p>
        <p class="doc-para lang-en">
          If compromise is suspected or an unpatched Zero-Day vulnerability is actively exploited in the wild, execute the following emergency containment and triage procedure:
        </p>'''

    if old_zd_intro in html:
        html = html.replace(old_zd_intro, new_zd_intro)

    # 7. Operational Best Practices Intro
    old_rfc_intro = r'''        <h2
          id="operational-best-practices-rfc-2119"
          class="heading-anchor"
        >
          <a
            href="#operational-best-practices-rfc-2119"
            class="anchor-link"
            >#</a
          >
          Operational Best Practices (RFC 2119)
        </h2>
        <p class="doc-para">
          Panduan operasional dan tata kelola keamanan Zimbra Collaboration Suite
          mengikuti standar taksonomi <strong>RFC 2119</strong> (<em>MUST, MUST NOT, SHOULD, SHOULD NOT, MAY</em>):
        </p>'''

    new_rfc_intro = r'''        <h2
          id="operational-best-practices-rfc-2119"
          class="heading-anchor"
        >
          <a
            href="#operational-best-practices-rfc-2119"
            class="anchor-link"
            >#</a
          >
          <span class="lang-id">Praktik Operasional Terbaik (RFC 2119)</span><span class="lang-en">Operational Best Practices (RFC 2119)</span>
        </h2>
        <p class="doc-para lang-id">
          Panduan operasional dan tata kelola keamanan Zimbra Collaboration Suite mengikuti standar taksonomi <strong>RFC 2119</strong> (<em>MUST, MUST NOT, SHOULD, SHOULD NOT, MAY</em>):
        </p>
        <p class="doc-para lang-en">
          Operational governance and security baselines for Zimbra Collaboration Suite adhering to <strong>RFC 2119</strong> standard terminology (<em>MUST, MUST NOT, SHOULD, SHOULD NOT, MAY</em>):
        </p>'''

    if old_rfc_intro in html:
        html = html.replace(old_rfc_intro, new_rfc_intro)

    # 8. Running Tests Lead
    old_tests = r'''        <h2 id="running-tests" class="heading-anchor">
          <a href="#running-tests" class="anchor-link">#</a> Running Tests
        </h2>
        <p class="doc-para">
          Untuk memverifikasi ketersediaan seluruh link mirror, integritas
          biner, dan status sistem:
        </p>'''

    new_tests = r'''        <h2 id="running-tests" class="heading-anchor">
          <a href="#running-tests" class="anchor-link">#</a> <span class="lang-id">Menjalankan Pengujian &amp; Verifikasi Otomatis</span><span class="lang-en">Running Automated Tests &amp; Checksum Verification</span>
        </h2>
        <p class="doc-para lang-id">
          Untuk memverifikasi ketersediaan seluruh link mirror, integritas biner, dan status sistem:
        </p>
        <p class="doc-para lang-en">
          To continuously verify mirror availability, cryptographic hashes, and repository code health:
        </p>'''

    if old_tests in html:
        html = html.replace(old_tests, new_tests)

    # 9. Ecosystem Tools Lead
    old_eco = r'''        <h2 id="ecosystem-tools--repositories" class="heading-anchor">
          <a href="#ecosystem-tools--repositories" class="anchor-link">#</a>
          Ecosystem Tools &amp; Repositories
        </h2>
        <p class="doc-para">
          Utilitas pendukung open source untuk operasional Zimbra:
        </p>'''

    new_eco = r'''        <h2 id="ecosystem-tools--repositories" class="heading-anchor">
          <a href="#ecosystem-tools--repositories" class="anchor-link">#</a>
          <span class="lang-id">Alat Ekosistem &amp; Repositori Terkait</span><span class="lang-en">Ecosystem Tools &amp; Related Repositories</span>
        </h2>
        <p class="doc-para lang-id">
          Utilitas pendukung open source untuk operasional Zimbra:
        </p>
        <p class="doc-para lang-en">
          Open-source companion utilities and ecosystem tooling for Zimbra operations:
        </p>'''

    if old_eco in html:
        html = html.replace(old_eco, new_eco)

    # 10. Official Contact Lead
    old_contact = r'''        <h2 id="official-contact--author" class="heading-anchor">
          <a href="#official-contact--author" class="anchor-link">#</a> Official
          Contact &amp; Author
        </h2>
        <p class="doc-para">
          Repository ini dikelola dan diperbarui secara berkala oleh:
        </p>'''

    new_contact = r'''        <h2 id="official-contact--author" class="heading-anchor">
          <a href="#official-contact--author" class="anchor-link">#</a> <span class="lang-id">Kontak Resmi &amp; Penulis</span><span class="lang-en">Official Contact &amp; Author</span>
        </h2>
        <p class="doc-para lang-id">
          Repository ini dikelola dan diperbarui secara berkala oleh:
        </p>
        <p class="doc-para lang-en">
          This repository is actively developed and maintained by:
        </p>'''

    if old_contact in html:
        html = html.replace(old_contact, new_contact)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: make_deep_sections_bilingual completed!")

if __name__ == '__main__':
    main()
