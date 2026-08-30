# -*- coding: utf-8 -*-
"""
make_rfc2119_bilingual.py
Provides bilingual translations for RFC 2119 Best Practices in index.html.
"""

import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the rfc-grid block
    p1 = html.find('<div class="rfc-grid">')
    p2 = html.find('id="strategic-migration--upgrade-methodology"')
    if p1 == -1 or p2 == -1:
        print("ERROR: RFC 2119 grid not found!")
        return 1

    rfc_bilingual = r'''<div class="rfc-grid">
          <!-- 1. MUST / REQUIRED -->
          <div class="rfc-card must">
            <div class="rfc-card-header">
              <div class="rfc-card-title">
                <i class="fa-solid fa-circle-exclamation text-danger"></i> <span class="lang-id">1. MUST / REQUIRED (Wajib Mutlak)</span><span class="lang-en">1. MUST / REQUIRED (Mandatory Baseline)</span>
              </div>
              <span class="rfc-badge"><i class="fa-solid fa-shield-halved"></i> Absolute Requirement</span>
            </div>
            <div class="rfc-card-body">
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-box-archive text-danger"></i> MUST Install POSIX <code>pax</code> Utility
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Host OS <strong>wajib</strong> memiliki paket <code>pax</code> terinstal (<code>apt-get install -y pax</code> / <code>dnf install -y pax</code>). Amavisd menggunakan utilitas ini untuk dekompresi arsip email; ketiadaannya memicu <em>fallback</em> ke <code>cpio</code> yang rentan terhadap eksekusi kode arbitrer jarak jauh (RCE) (<a href="https://nvd.nist.gov/vuln/detail/CVE-2022-41352" target="_blank" rel="noopener noreferrer"><strong>CVE-2022-41352</strong></a>).</span>
                  <span class="lang-en">The host OS <strong>MUST</strong> have the <code>pax</code> package installed (<code>apt-get install -y pax</code> / <code>dnf install -y pax</code>). Amavisd relies on this utility for archive decompression; its absence triggers an unauthenticated RCE fallback via vulnerable <code>cpio</code> unpackers (<a href="https://nvd.nist.gov/vuln/detail/CVE-2022-41352" target="_blank" rel="noopener noreferrer"><strong>CVE-2022-41352</strong></a>).</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-lock text-danger"></i> MUST Isolate Admin Port (<code>7071</code> / <code>9071</code>)
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Port administrasi ZCS (<code>7071</code> untuk Admin Web Console &amp; SOAP Admin Servlet) <strong>wajib diisolasi</strong> dari internet publik (<code>0.0.0.0/0</code>) dan hanya boleh diakses melalui VPN korporat terenkripsi, IP bastion/manajemen khusus, atau SSH tunneling lokal (<code>127.0.0.1</code>).</span>
                  <span class="lang-en">ZCS administration ports (<code>7071</code> for Admin Web Console &amp; SOAP Admin Servlets) <strong>MUST</strong> be isolated from public WAN reachability (<code>0.0.0.0/0</code>) and restricted exclusively to corporate VPNs, dedicated bastion hosts, or local SSH tunnels (<code>127.0.0.1</code>).</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-ban text-danger"></i> MUST Disable Postjournal When Not in Use
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Bagi sistem yang tidak menggunakan audit compliance journaling eksternal, layanan postjournal <strong>wajib dinonaktifkan</strong> untuk menutup celah RCE unauthenticated recipient injection (<a href="https://nvd.nist.gov/vuln/detail/CVE-2024-45519" target="_blank" rel="noopener noreferrer"><strong>CVE-2024-45519</strong></a>):</span>
                  <span class="lang-en">For environments not utilizing external compliance archiving, the postjournal service <strong>MUST</strong> be disabled to eliminate unauthenticated command injection attack surfaces (<a href="https://nvd.nist.gov/vuln/detail/CVE-2024-45519" target="_blank" rel="noopener noreferrer"><strong>CVE-2024-45519</strong></a>):</span>
                </p>
                <div class="code-card rfc-code-card">
                  <div class="code-header">
                    <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> BASH</span>
                    <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
                  </div>
                  <pre><code class="language-bash">su - zimbra -c "zmlocalconfig -e postjournal_enabled=false &amp;&amp; zmcontrol restart"</code></pre>
                </div>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-network-wired text-danger"></i> MUST Bind Internal Daemons to Loopback (<code>127.0.0.1</code>)
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Layanan internal seperti Memcached (<code>port 11211</code>), MySQL (<code>port 7306</code>), dan LDAP replica <strong>wajib di-bind</strong> hanya pada interface loopback lokal guna mencegah eksploitasi route cache poisoning (<a href="https://nvd.nist.gov/vuln/detail/CVE-2022-27924" target="_blank" rel="noopener noreferrer"><strong>CVE-2022-27924</strong></a>) dan ekstraksi basis data langsung.</span>
                  <span class="lang-en">Internal daemons including Memcached (<code>port 11211</code>), MySQL (<code>port 7306</code>), and LDAP replica listeners <strong>MUST</strong> bind strictly to the loopback interface (<code>127.0.0.1</code>) to prevent cache poisoning attacks (<a href="https://nvd.nist.gov/vuln/detail/CVE-2022-27924" target="_blank" rel="noopener noreferrer"><strong>CVE-2022-27924</strong></a>) and direct unauthorized database probing.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-key text-danger"></i> MUST Enforce Cryptographic Checksum Validation
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Setiap arsip rilis biner ZCS yang diunduh dari repositori mirror <strong>wajib diverifikasi</strong> menggunakan hash kriptografis <code>SHA256</code> atau <code>MD5</code> resmi sebelum diekstraksi ke direktori sistem.</span>
                  <span class="lang-en">All ZCS release binary packages retrieved from remote mirrors <strong>MUST</strong> undergo cryptographic integrity verification via official <code>SHA256</code> or <code>MD5</code> checksum digests before unpacking.</span>
                </p>
              </div>
            </div>
          </div>

          <!-- 2. MUST NOT / SHALL NOT -->
          <div class="rfc-card must-not">
            <div class="rfc-card-header">
              <div class="rfc-card-title">
                <i class="fa-solid fa-circle-xmark text-danger"></i> <span class="lang-id">2. MUST NOT / SHALL NOT (Dilarang Keras)</span><span class="lang-en">2. MUST NOT / SHALL NOT (Strictly Prohibited)</span>
              </div>
              <span class="rfc-badge"><i class="fa-solid fa-hand"></i> Strictly Prohibited</span>
            </div>
            <div class="rfc-card-body">
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-globe text-danger"></i> MUST NOT Expose Admin Console to Public WAN
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dilarang memetakan port <code>7071</code> atau direktori <code>/zimbraAdmin</code> secara langsung ke alamat IP publik, karena merupakan sasaran utama pemindaian otomatis botnet, CSRF, dan kerentanan Zimlet UI (<a href="https://nvd.nist.gov/vuln/detail/CVE-2023-34192" target="_blank" rel="noopener noreferrer"><strong>CVE-2023-34192</strong></a>, <a href="https://nvd.nist.gov/vuln/detail/CVE-2024-33535" target="_blank" rel="noopener noreferrer"><strong>CVE-2024-33535</strong></a>).</span>
                  <span class="lang-en">Administrators <strong>MUST NOT</strong> expose port <code>7071</code> or the <code>/zimbraAdmin</code> webroot directly to public WAN subnets due to automated botnet scanning, CSRF vectors, and Zimlet UI vulnerabilities (<a href="https://nvd.nist.gov/vuln/detail/CVE-2023-34192" target="_blank" rel="noopener noreferrer"><strong>CVE-2023-34192</strong></a>, <a href="https://nvd.nist.gov/vuln/detail/CVE-2024-33535" target="_blank" rel="noopener noreferrer"><strong>CVE-2024-33535</strong></a>).</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-user-shield text-danger"></i> MUST NOT Run Core Zimbra Processes as <code>root</code>
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dilarang menjalankan daemon aplikasi (<code>mailboxd</code>, <code>slapd</code>, <code>postfix</code>, <code>amavisd</code>, <code>nginx</code>) langsung di bawah hak pengguna <code>root</code>. Seluruh tugas pemeliharaan harian wajib didelegasikan ke user sistem unprivileged <code>zimbra</code>.</span>
                  <span class="lang-en">Application daemons (<code>mailboxd</code>, <code>slapd</code>, <code>postfix</code>, <code>amavisd</code>, <code>nginx</code>) <strong>MUST NOT</strong> execute directly with <code>root</code> user privileges. All routine operations must remain constrained under the unprivileged <code>zimbra</code> service account.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-clock-rotate-left text-danger"></i> MUST NOT Defer Cumulative Security Patches
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dilarang menunda penerapan Patch / Security Advisory resmi melebihi 14 hari kalender sejak tanggal pengumuman rilis oleh tim keamanan Zimbra / Synacor.</span>
                  <span class="lang-en">Security teams <strong>MUST NOT</strong> defer the application of critical Zimbra security patches or cumulative updates beyond 14 calendar days from official vendor disclosure.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-triangle-exclamation text-danger"></i> MUST NOT Enable Deprecated Protocols &amp; Weak Ciphers
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dilarang mengaktifkan protokol usang SSLv2, SSLv3, TLSv1.0, TLSv1.1 serta cipher lemah (RC4, 3DES, CBC, EXPORT) pada Mail Proxy Nginx maupun Postfix MTA.</span>
                  <span class="lang-en">Configurations <strong>MUST NOT</strong> enable deprecated cryptographic protocols (SSLv2, SSLv3, TLSv1.0, TLSv1.1) or insecure ciphers (RC4, 3DES, CBC, EXPORT) on Nginx reverse proxy or Postfix MTA.</span>
                </p>
              </div>
            </div>
          </div>

          <!-- 3. SHOULD / RECOMMENDED -->
          <div class="rfc-card should">
            <div class="rfc-card-header">
              <div class="rfc-card-title">
                <i class="fa-solid fa-triangle-exclamation text-warning"></i> <span class="lang-id">3. SHOULD / RECOMMENDED (Sangat Disarankan)</span><span class="lang-en">3. SHOULD / RECOMMENDED (Strongly Recommended)</span>
              </div>
              <span class="rfc-badge"><i class="fa-solid fa-thumbs-up"></i> Best Practice</span>
            </div>
            <div class="rfc-card-body">
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-bolt text-warning"></i> SHOULD Deploy Dedicated Local Caching DNS Resolver
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Sangat disarankan memasang <strong>Unbound</strong> atau BIND9 pada <code>127.0.0.1</code> sebagai recursive resolver lokal. Hal ini secara signifikan memangkas latensi lookup SpamAssassin / DNSBL serta mencegah kegagalan resolusi MX timeout akibat <em>public DNS rate-limiting</em>.</span>
                  <span class="lang-en">Deploying <strong>Unbound</strong> or BIND9 on <code>127.0.0.1</code> as a local recursive caching resolver is <strong>STRONGLY RECOMMENDED</strong>. This drastically mitigates DNSBL lookup latencies and prevents MX query dropouts caused by public DNS rate limits.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-envelope-circle-check text-warning"></i> SHOULD Enforce Strict DMARC Policy (<code>p=reject</code>)
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Domain pengirim email harus menerapkan catatan DMARC dengan kebijakan penolakan tegas (<code>p=reject</code>), penyelarasan SPF <code>strict</code> (<code>aspf=s</code>), DKIM <code>strict</code> (<code>adkim=s</code>), serta mengonfigurasi pelaporan agregat harian (<code>rua=mailto:dmarc-rua@domain.com</code>).</span>
                  <span class="lang-en">Sending domains <strong>SHOULD</strong> publish strict DMARC enforcement policies (<code>p=reject</code>), strict SPF alignment (<code>aspf=s</code>), strict DKIM alignment (<code>adkim=s</code>), and aggregate reporting URIs (<code>rua=mailto:dmarc-rua@domain.com</code>).</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-shield-virus text-warning"></i> SHOULD Implement Dynamic Brute-Force Defense (Fail2Ban)
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Konfigurasikan Fail2Ban dengan filter regex khusus pada <code>/opt/zimbra/log/mailbox.log</code> dan <code>/var/log/mail.log</code> untuk mendeteksi serta memblokir otomatis alamat IP penyerang pada port Webmail, SMTP Submission (587), dan IMAPS (993).</span>
                  <span class="lang-en">Systems <strong>SHOULD</strong> deploy Fail2Ban with tailored regex filters parsing <code>/opt/zimbra/log/mailbox.log</code> and <code>/var/log/mail.log</code> to automatically ban abusive IPs across Webmail, Submission (587), and IMAPS (993).</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-mobile-screen-button text-warning"></i> SHOULD Mandate Multi-Factor Authentication (2FA / TOTP)
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Wajibkan autentikasi dua faktor berbasis waktu (RFC 6238 TOTP) bagi seluruh akun berhak istimewa (<em>Global Administrator</em>, <em>Delegated Admin</em>) dan disarankan untuk seluruh akun mailbox pengguna.</span>
                  <span class="lang-en">Multi-factor authentication (RFC 6238 TOTP) <strong>SHOULD</strong> be strictly mandated for all administrative roles and strongly encouraged for all standard mailbox users.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-gauge-high text-warning"></i> SHOULD Implement CBPolicyD Rate-Limiting
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Aktifkan modul Cluebringer (CBPolicyD) untuk membatasi kuota pengiriman email keluar per jam/per akun (misal maks. 100-200 email/jam/user) guna mencegah domain masuk daftar hitam (<em>blacklist</em>) jika terdapat akun pengguna yang terkompromi.</span>
                  <span class="lang-en">Deploying Cluebringer (CBPolicyD) egress rate-limiting per account (e.g., 100-200 messages/hour) <strong>SHOULD</strong> be implemented to prevent IP reputation tarnishing from compromised user credentials.</span>
                </p>
              </div>
            </div>
          </div>

          <!-- 4. SHOULD NOT / NOT RECOMMENDED -->
          <div class="rfc-card should-not">
            <div class="rfc-card-header">
              <div class="rfc-card-title">
                <i class="fa-solid fa-circle-pause text-orange"></i> <span class="lang-id">4. SHOULD NOT / NOT RECOMMENDED (Sebaiknya Dihindari)</span><span class="lang-en">4. SHOULD NOT / NOT RECOMMENDED (Discouraged)</span>
              </div>
              <span class="rfc-badge"><i class="fa-solid fa-triangle-exclamation"></i> Discouraged</span>
            </div>
            <div class="rfc-card-body">
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-display text-orange"></i> SHOULD NOT Rely Solely on Web Interface for Configuration
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Hindari melakukan perubahan parameter arsitektur kritis hanya melalui antarmuka grafis Webmail/Admin UI; prioritaskan penggunaan CLI resmi (<code>zmprov</code>, <code>zmlocalconfig</code>, <code>zmcontrol</code>) yang dapat terdokumentasi dan terrekam dalam audit log.</span>
                  <span class="lang-en">Operators <strong>SHOULD NOT</strong> make core architectural adjustments exclusively through the Admin UI; audited CLI operations (<code>zmprov</code>, <code>zmlocalconfig</code>, <code>zmcontrol</code>) provide reliable configuration traceability.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-hard-drive text-orange"></i> SHOULD NOT Retain Unencrypted Backups on Same Storage Node
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Hindari menyimpan berkas cadangan mailbox hanya pada volume lokal atau storage server yang sama tanpa replikasi terenkripsi ke lokasi fisik / cloud terpisah (<em>off-site disaster recovery</em>).</span>
                  <span class="lang-en">Organizations <strong>SHOULD NOT</strong> store unencrypted backup snapshots solely on the local server volume without off-site, immutable cloud replication.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-certificate text-orange"></i> SHOULD NOT Use Self-Signed Certificates in Production
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Hindari membiarkan sertifikat SSL/TLS bawaan (<em>self-signed</em>) terpasang pada lingkungan produksi publik; selalu gunakan sertifikat valid terpercaya publik (Let's Encrypt / Commercial CA).</span>
                  <span class="lang-en">Public deployments <strong>SHOULD NOT</strong> maintain default self-signed SSL/TLS certificates; valid certificates signed by trusted public Certificate Authorities (Let's Encrypt / Commercial CA) are essential.</span>
                </p>
              </div>
            </div>
          </div>

          <!-- 5. MAY / OPTIONAL -->
          <div class="rfc-card may">
            <div class="rfc-card-header">
              <div class="rfc-card-title">
                <i class="fa-solid fa-circle-check text-success"></i> <span class="lang-id">5. MAY / OPTIONAL (Pilihan Tambahan)</span><span class="lang-en">5. MAY / OPTIONAL (Discretionary Enhancements)</span>
              </div>
              <span class="rfc-badge"><i class="fa-solid fa-sliders"></i> Discretionary</span>
            </div>
            <div class="rfc-card-body">
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-chart-line text-success"></i> MAY Integrate Centralized SIEM / Syslog Forwarding
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Administrator dapat memforward log audit ZCS (<code>/opt/zimbra/log/audit.log</code>, <code>mailbox.log</code>, <code>nginx.access.log</code>) ke platform SIEM terpusat (Wazuh, Elastic SIEM, Graylog, Splunk) via rsyslog TLS terenkripsi.</span>
                  <span class="lang-en">Administrators <strong>MAY</strong> forward ZCS security audit logs (<code>/opt/zimbra/log/audit.log</code>, <code>mailbox.log</code>, <code>nginx.access.log</code>) to centralized SIEM platforms (Wazuh, Elastic, Graylog, Splunk) over TLS-encrypted rsyslog pipelines.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-earth-americas text-success"></i> MAY Implement GeoIP Ingress Filtering on Reverse Proxy
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dapat menerapkan modul Nginx GeoIP2 untuk membatasi atau menolak akses autentikasi Webmail dari wilayah geografis di luar jangkauan operasional bisnis.</span>
                  <span class="lang-en">Infrastructure teams <strong>MAY</strong> leverage Nginx GeoIP2 modules to restrict webmail authentication attempts originating from untrusted geographic territories outside normal operational zones.</span>
                </p>
              </div>
              <div class="rfc-item">
                <div class="rfc-item-title">
                  <i class="fa-solid fa-wand-magic-sparkles text-success"></i> MAY Deploy Automated Forensic &amp; Webshell Scanners
                </div>
                <p class="rfc-item-desc">
                  <span class="lang-id">Dapat menjadwalkan pemeriksaan berkala berkas sistem dan webroot Jetty menggunakan toolkit pemulihan insiden seperti <a href="https://github.com/alsyundawy/eradicate-zimbra-malware" target="_blank" rel="noopener noreferrer"><strong>eradicate-zimbra-malware</strong></a>.</span>
                  <span class="lang-en">Security teams <strong>MAY</strong> schedule periodic forensic integrity audits on Jetty webroots using automated incident response suites such as <a href="https://github.com/alsyundawy/eradicate-zimbra-malware" target="_blank" rel="noopener noreferrer"><strong>eradicate-zimbra-malware</strong></a>.</span>
                </p>
              </div>
            </div>
          </div>
        </div>
        <hr class="divider">
        '''

    new_html = html[:p1] + rfc_bilingual + html[p2:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    print("SUCCESS: RFC 2119 Best Practices fully converted to bilingual!")
    return 0

if __name__ == '__main__':
    main()
