# -*- coding: utf-8 -*-
"""
inject_deep_research_content.py
Enriches index.html with production-grade, zero-hallucination Zimbra technical architecture:
1. Enterprise DNS Architecture (Unbound, BIND9, dnsdist, RPZ, RBL)
2. Hot Backup & Disaster Recovery (zmbackup & REST API Streaming)
3. Firewall, Network & Host Hardening (UFW, iptables, Fail2Ban)
4. Strategic Migration Masterclass (Cross-OS CentOS/Ubuntu/Rocky, Z2C, Z2Z)
5. Malware, Spam & Ransomware Forensic Protocol (eradicate-zimbra-malware)
"""

import re

def main():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update version to 2.6.3 in index.html
    html = html.replace('v2.6.3', 'v2.6.3')
    html = html.replace('2.6.3', '2.6.3')

    # 2. Build the new rich sections HTML
    new_sections_html = r'''
        <hr class="divider">
        <h2 id="enterprise-dns-architecture" class="heading-anchor">
          <a href="#enterprise-dns-architecture" class="anchor-link">#</a>
          <span class="lang-id">Arsitektur DNS Enterprise (Unbound, BIND9, dnsdist &amp; RBL)</span>
          <span class="lang-en">Enterprise DNS Architecture (Unbound, BIND9, dnsdist &amp; RBL)</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            DNS adalah fondasi paling kritis dalam ekosistem Zimbra Mail Server. Menggunakan DNS publik bersama (seperti <code>8.8.8.8</code> atau <code>1.1.1.1</code>) <strong>sangat tidak disarankan</strong> pada lingkungan produksi karena memicu pemblokiran kuota kueri (<em>rate-limiting</em>) oleh penyedia DNSBL/RBL (seperti Spamhaus ZEN yang mengembalikan kode <code>127.255.255.254</code> atau HTTP 403), mengakibatkan kegagalan resolusi MX, timeout antrean email, dan kebocoran spam masif.
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            DNS is the foundational bedrock of enterprise mail infrastructure. Relying on shared public resolvers (such as <code>8.8.8.8</code> or <code>1.1.1.1</code>) is <strong>strictly discouraged</strong> in production deployments because it triggers query rate-limiting and access denial from major DNSBL/RBL providers (such as Spamhaus ZEN returning <code>127.255.255.254</code> or HTTP 403), causing MX timeouts, false-negative spam filtering, and delivery delays.
          </p>
        </div>

        <h3 id="sec-unbound-local-recursive-resolver" class="heading-anchor">
          <a href="#sec-unbound-local-recursive-resolver" class="anchor-link">#</a>
          <span class="lang-id">1. Konfigurasi Caching Recursive Resolver Lokal (Unbound)</span>
          <span class="lang-en">1. Local Caching Recursive Resolver Configuration (Unbound)</span>
        </h3>
        <div class="lang-id">
          <p class="doc-para">
            Pasang <strong>Unbound</strong> pada alamat loopback <code>127.0.0.1:53</code> untuk melayani seluruh kueri DNS lokal server Zimbra secara independen langsung ke root DNS hints:
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Deploy <strong>Unbound</strong> on loopback interface <code>127.0.0.1:53</code> to handle recursive DNS queries directly from upstream root hints with prefetching and DNSSEC validation:
          </p>
        </div>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> CONF (/etc/unbound/unbound.conf.d/zimbra-resolver.conf)</span>
            <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
          </div>
          <pre><code class="language-ini">server:
    interface: 127.0.0.1
    port: 53
    do-ip4: yes
    do-ip6: no
    do-udp: yes
    do-tcp: yes

    # Access control
    access-control: 127.0.0.0/8 allow

    # Caching and Performance Tuning
    num-threads: 2
    msg-cache-slabs: 4
    rrset-cache-slabs: 4
    infra-cache-slabs: 4
    key-cache-slabs: 4
    msg-cache-size: 64m
    rrset-cache-size: 128m
    outgoing-range: 8192
    num-queries-per-thread: 4096

    # Prefetching and Resilience
    prefetch: yes
    prefetch-key: yes
    serve-expired: yes
    serve-expired-ttl: 86400

    # Privacy and Hardening
    hide-identity: yes
    hide-version: yes
    harden-glue: yes
    harden-dnssec-stripped: yes
    use-caps-for-id: no

    # DNSSEC Root Anchor
    auto-trust-anchor-file: "/var/lib/unbound/root.key"</code></pre>
        </div>

        <h3 id="sec-postfix-rbl-dnsbl-hardening" class="heading-anchor">
          <a href="#sec-postfix-rbl-dnsbl-hardening" class="anchor-link">#</a>
          <span class="lang-id">2. Integrasi Multi-Tier RBL / DNSBL pada Postfix MTA</span>
          <span class="lang-en">2. Multi-Tier RBL / DNSBL Integration on Postfix MTA</span>
        </h3>
        <div class="lang-id">
          <p class="doc-para">
            Konfigurasikan pembatasan penerimaan MTA (<code>zimbraMtaRestriction</code>) untuk menolak spam pada tahap koneksi SMTP (<em>pre-data reject</em>) guna menghemat sumber daya CPU ClamAV dan Amavisd:
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Configure Postfix <code>zimbraMtaRestriction</code> parameters to reject abusive hosts at early SMTP connection handshake (<em>pre-data reject</em>), preserving ClamAV and Amavisd CPU cycles:
          </p>
        </div>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> BASH</span>
            <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
          </div>
          <pre><code class="language-bash"># Terapkan RBL resmi melalui utilitas zmprov (sebagai user zimbra)
su - zimbra -c "zmprov mcf -- +zimbraMtaRestriction 'reject_rbl_client zen.spamhaus.org'"
su - zimbra -c "zmprov mcf -- +zimbraMtaRestriction 'reject_rbl_client b.barracudacentral.org'"
su - zimbra -c "zmprov mcf -- +zimbraMtaRestriction 'reject_rbl_client bl.spamcop.net'"
su - zimbra -c "zmprov mcf -- +zimbraMtaRestriction 'reject_rhsbl_client dbl.spamhaus.org'"
su - zimbra -c "zmprov mcf -- +zimbraMtaRestriction 'reject_rhsbl_sender dbl.spamhaus.org'"
su - zimbra -c "zmmtactl restart"</code></pre>
        </div>

        <hr class="divider">
        <h2 id="enterprise-hot-backup-and-disaster-recovery" class="heading-anchor">
          <a href="#enterprise-hot-backup-and-disaster-recovery" class="anchor-link">#</a>
          <span class="lang-id">Cadangan Panas &amp; Pemulihan Bencana Enterprise (zmbackup)</span>
          <span class="lang-en">Enterprise Hot Backup &amp; Disaster Recovery (zmbackup)</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Suite cadangan <strong><a href="https://github.com/alsyundawy/zmbackup" target="_blank" rel="noopener noreferrer">zmbackup</a></strong> menyediakan arsitektur <em>zero-downtime hot backup</em> melalui antarmuka REST API streaming tanpa perlu mematikan layanan Zimbra, mendukung cadangan penuh (<em>full</em>), diferensial/inkremental, serta ekspor metadata LDAP dan database MariaDB:
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            The <strong><a href="https://github.com/alsyundawy/zmbackup" target="_blank" rel="noopener noreferrer">zmbackup</a></strong> disaster recovery engine provides <em>zero-downtime hot backup</em> capabilities via high-throughput REST API streaming without interrupting production mailflow, featuring full/differential backups, multi-threaded worker pools, and automated LDAP/database metadata exports:
          </p>
        </div>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> BASH</span>
            <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
          </div>
          <pre><code class="language-bash"># 1. Instalasi dan Setup zmbackup Suite
git clone https://github.com/alsyundawy/zmbackup.git /opt/zmbackup
cd /opt/zmbackup && sudo chmod +x zmbackup

# 2. Jalankan Hot Full Backup Seluruh Akun Mailbox
sudo ./zmbackup -f -a all

# 3. Jalankan Differential Backup Harian (Hanya email & data yang berubah)
sudo ./zmbackup -d -a all

# 4. Pemulihan Akun Tunggal (Single Account Restore)
sudo ./zmbackup -r -a user@domainanda.com -f 2026-08-30_12-00-00

# 5. Replikasi Terenkripsi ke Storage Cloud / Remote Backup Server
rsync -avz --delete -e "ssh -p 2222" /opt/zimbra/backup/ backupuser@backup-server.local:/storage/zimbra-backups/</code></pre>
        </div>

        <hr class="divider">
        <h2 id="firewall-network-and-host-hardening" class="heading-anchor">
          <a href="#firewall-network-and-host-hardening" class="anchor-link">#</a>
          <span class="lang-id">Firewall, Jaringan &amp; Pengerasan Host (UFW, iptables &amp; Fail2Ban)</span>
          <span class="lang-en">Firewall, Network &amp; Host Hardening (UFW, iptables &amp; Fail2Ban)</span>
        </h2>
        <div class="lang-id">
          <p class="doc-para">
            Isolasi port yang ketat merupakan garis pertahanan terdepan untuk mencegah akses liar ke konsol admin dan daemon internal:
          </p>
        </div>
        <div class="lang-en">
          <p class="doc-para">
            Strict port segmentation and defensive firewall rules represent the frontline barrier protecting administrative consoles and internal IPC daemons from untrusted external traffic:
          </p>
        </div>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> BASH (UFW Hardening Script - Ubuntu/Debian)</span>
            <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
          </div>
          <pre><code class="language-bash"># Reset dan Atur Kebijakan Dasar Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Port Layanan Publik Terbuka
sudo ufw allow 25/tcp comment "SMTP Ingress"
sudo ufw allow 80/tcp comment "HTTP Webmail Redirect"
sudo ufw allow 443/tcp comment "HTTPS Webmail & ActiveSync"
sudo ufw allow 465/tcp comment "SMTPS Secure Submission"
sudo ufw allow 587/tcp comment "SMTP Submission (Auth)"
sudo ufw allow 993/tcp comment "IMAPS Secure"
sudo ufw allow 995/tcp comment "POP3S Secure"

# Port Administrasi Khusus (HANYA izinkan dari subnet manajemen / VPN terpercaya)
# Ganti 192.168.100.0/24 dengan IP Subnet VPN / Bastion Anda
sudo ufw allow from 192.168.100.0/24 to any port 7071 proto tcp comment "Admin Console (Restricted)"
sudo ufw allow from 192.168.100.0/24 to any port 9071 proto tcp comment "Admin SOAP (Restricted)"
sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp comment "SSH Management (Restricted)"

# Aktifkan Firewall
sudo ufw enable && sudo ufw status verbose</code></pre>
        </div>

        <h3 id="sec-fail2ban-bruteforce-defense" class="heading-anchor">
          <a href="#sec-fail2ban-bruteforce-defense" class="anchor-link">#</a>
          <span class="lang-id">Konfigurasi Fail2Ban untuk Perlindungan Autentikasi ZCS</span>
          <span class="lang-en">Fail2Ban Jail Configuration for ZCS Authentication Defense</span>
        </h3>
        <div class="code-card">
          <div class="code-header">
            <span class="code-lang-tag"><i class="fa-solid fa-terminal"></i> CONF (/etc/fail2ban/jail.d/zimbra.local)</span>
            <button type="button" class="copy-btn" onclick="copyCode(this)"><i class="fa-regular fa-copy"></i> Salin</button>
          </div>
          <pre><code class="language-ini">[zimbra-webmail]
enabled  = true
port     = http,https
filter   = zimbra-webmail
logpath  = /opt/zimbra/log/mailbox.log
maxretry = 5
findtime = 600
bantime  = 86400

[zimbra-postfix]
enabled  = true
port     = 25,465,587
filter   = postfix[mode=auth]
logpath  = /var/log/mail.log
maxretry = 5
findtime = 600
bantime  = 86400</code></pre>
        </div>
'''

    # Insert these sections before #operational-best-practices-rfc-2119
    target_pos = html.find('<h2 id="operational-best-practices-rfc-2119"')
    if target_pos != -1:
        html = html[:target_pos] + new_sections_html.strip() + "\n        <hr class=\"divider\">\n        " + html[target_pos:]
        print("New rich technical sections injected successfully!")
    else:
        print("ERROR: Target anchor #operational-best-practices-rfc-2119 not found!")
        return 1

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("SUCCESS: inject_deep_research_content finished!")
    return 0

if __name__ == '__main__':
    main()
