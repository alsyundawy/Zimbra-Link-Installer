# [2.6.3] - Changelog

<!-- markdownlint-disable MD013 MD024 -->

All notable changes to the **Zimbra Link Installer & Telemetry Suite** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.6.3] - 2026-08-30

### Added

- **Official Zimbra Network Edition (NE 10.1, 10.0, 9.0, 8.8.15) Link Re-Verification**:
  - Live scraped and validated 100% of official Zimbra NE direct binary download links, `.md5`, and `.sha256` checksums directly from `files.zimbra.com` (confirmed HTTP 200 OK across Ubuntu 18/20/22/24 and RHEL 7/8/9).
  - Updated dataset files `scripts/data/all_historical_verified.json` (291 entries) and `scripts/data/verified_official_all.json` (529 entries).
  - Updated `zimbra-link-installer.sh`, `README.md`, and `index.html` (Tables 132, 134, 136).
- **Enterprise Deep Research & Architecture Expansion (`index.html`)**:
  - **Enterprise DNS Architecture (Unbound, BIND9, dnsdist & RBL)**: Added production configuration guides for dedicated local recursive DNS caching via Unbound (`127.0.0.1:53`), DNS threat sinkholing via BIND9 RPZ, query rate-limiting via dnsdist, and Postfix multi-tier DNSBL/RBL integration (Spamhaus ZEN, Barracuda, SpamCop) to eliminate DNS rate-limiting and MX timeout failures.
  - **Enterprise Hot Backup & Disaster Recovery (`zmbackup`)**: Added comprehensive REST API streaming hot backup architectures, multi-threaded worker pipelines, differential/incremental backup strategies, and single-mailbox/full disaster recovery workflows based on `alsyundawy/zmbackup`.
  - **Firewall, Network & Defense-in-Depth Hardening**: Added production UFW and iptables port isolation rules (restricting Admin Console ports 7071/9071 to management subnets/VPN, and binding internal IPC daemons to loopback), coupled with Fail2Ban jails for Mailboxd, Postfix SASL, and Nginx authentication brute-force protection.
  - **Cross-OS Zero-Data-Loss Migration Masterclass**: Expanded end-to-end migration methodology for migrating legacy CentOS 7 / RHEL 7 / Ubuntu 18 to modern Ubuntu 22.04 / 24.04 LTS and Rocky Linux 9 using pure mailbox streaming tools (`alsyundawy/Z2C` & `alsyundawy/Zimbra2Zimbra-Migration-Tool`).
  - **Malware, Spam, Ransomware & Webshell Forensic Protocol**: Detailed automated JSP webshell scanning, crontab persistence inspection, SSH authorized_keys audits, and permission healing using `alsyundawy/eradicate-zimbra-malware`.
- **Comprehensive Bilingual (ID/EN) i18n Engine**:
  - Implemented instant CSS visibility-driven bilingual architecture (`html[lang="id"]` / `html[lang="en"]`) combined with dynamic JavaScript translation dictionary (`i18nDict`).
  - Synchronized translations across all UI components: top navigation, sidebar, hero headers, section titles, explanatory paragraphs, step-by-step guides, RFC 2119 operational best practices, search filter placeholders, and copy buttons.
  - Added preference persistence in `localStorage` with smooth zero-layout-shift language switching.

### Changed

- Updated version identifier to `v2.6.3` across all repository files (`zimbra-link-installer.sh`, `index.html`, `README.md`, `DOCNOTE.md`, `SECURITY.md`, and `CHANGELOG.md`).
- Passed HTML5 strict validation and `htmlhint` with zero errors and zero warnings.

---

## [2.6.2] - 2026-08-28

### Added

- **Comprehensive Dual-Language Architecture (Bahasa Indonesia & English)**:
  - **CLI Suite (`zimbra-link-installer.sh`)**:
    - Built-in internationalization engine (`tr_msg`) supporting seamless switching between English and Bahasa Indonesia.
    - Added interactive language selector prompt upon startup (`[1] English / [2] Bahasa Indonesia`).
    - Added command-line flags `--lang=en` and `--lang=id` (short option: `-l <lang>`) for fully automated, non-interactive execution.
    - Added runtime language switching option directly inside the main menu (`Option 6: Switch Language / Ganti Bahasa`).
    - Translated all CLI components including banners, pre-flight audits, menus, download logs, cryptographic verification alerts, and error diagnostics.
  - **Web Portal (`index.html`)**:
    - Added interactive bilingual switcher toggle buttons (`[ ID | EN ]`) in the top navigation bar with `localStorage` preference persistence.
    - Added dynamic language-switching event handlers updating search input placeholders, copy buttons (`Salin` / `Copy`), and accessibility aria-labels.
  - **Documentation (`README.md`, `SECURITY.md`, `DOCNOTE.md`)**:
    - Added bilingual navigation badges (`[🇮🇩 Bahasa Indonesia]` / `[🇬🇧 English]`).
    - Added dedicated English overview and quickstart section in `README.md`.
    - Added complete Bahasa Indonesia version of the security policy and responsible disclosure procedure in `SECURITY.md`.
    - Updated version matrix and lifecycle references across all documentation files.

---

## [2.6.1] - 2026-08-28

### Added

- **Deep Security Research & Vulnerability Expansion**:
  - Integrated 5 newly verified Zimbra security advisories into the Master Vulnerability Matrix in `README.md` and `index.html` (totaling **37+ CVEs** spanning 2016–2026):
    - `CVE-2025-48700` (CVSS 6.1 MEDIUM - CISA KEV actively exploited, stored XSS in Classic UI via CSS `@import` / malformed tags).
    - `CVE-2024-45516` (CVSS 6.1 MEDIUM, stored XSS in Classic UI via malformed `<img>` tags).
    - `CVE-2023-48432` (CVSS 6.1 MEDIUM, reflected XSS in Classic Web Client via email link).
    - `CVE-2023-34193` (CVSS 7.2 HIGH, authenticated arbitrary file upload in `ClientUploader` servlet).
    - `CVE-2023-29382` (CVSS 7.5 HIGH, pre-auth arbitrary code execution / LFI in `sfdc_preauth.jsp`).
- **Comprehensive Lifecycle Policy (`SECURITY.md`)**:
  - Replaced generic policy with enterprise Zimbra Collaboration Suite Lifecycle Matrix detailing active support (ZCS 10.1 Daffodil) vs End-of-Life branches (ZCS 10.0 EOL 2025, ZCS 9.0 EOL 2024, ZCS 8.8.15 EOL 2023).
  - Outlined vulnerability disclosure reporting standards, response SLA, and third-party security verification process.

### Changed

- Updated version counters and metadata to `v2.6.1` across `README.md`, `DOCNOTE.md`, `index.html`, and `zimbra-link-installer.sh`.
- Re-verified all 1,215 binary and checksum URLs with automated telemetry validation (`scripts/deep_link_validator.py`), confirming all target download links actively accessible with zero broken links.

---

## [2.6.0] - 2026-08-27

### Added

- **Enterprise Security Hardening (`zimbra-link-installer.sh`)**:
  - Implemented strict defensive execution flags (`set -Eeuo pipefail`), safe IFS (`IFS=$'\n\t'`), and secure default file creation mask (`umask 022`).
  - Added atomic signal trapping (`trap cleanup EXIT INT TERM HUP`) ensuring temporary workspace `/tmp/zcs_*` cleanup without corrupting downloaded archives.
  - Implemented Privilege Abstraction Layer (`run_privileged`) to seamlessly adapt command elevation (native root vs `sudo`) for containerized (Docker/LXC) and standard host environments.
  - Hardened cryptographic checksum verification with regex extraction (`grep -oE '[a-fA-F0-9]{32|64}'`) and case-insensitive comparison (`${expected,,} == ${actual,,}`).
  - Added automated FQDN Pre-Flight Audit (`hostname -f`) validating host DNS alignment against `/etc/hosts` to prevent fatal `zmsetup.pl` MX resolution crashes.
  - Added prerequisite verification for POSIX `pax` utility to eliminate Amavis `cpio` Remote Code Execution risk (CVE-2022-41352).
  - Implemented anti-WAF / CDN Referer header bypass (`Referer: https://techfiles.online/`) for resilient fetching from community CDNs.
- **Standalone Interactive Web Application (`index.html`)**:
  - Created zero-dependency responsive single-page web dashboard with modern dark theme, glassmorphic UI, and full viewport responsiveness from VGA (640x480) to 2K (2560x1440).
  - Integrated dynamic Mermaid.js architecture and deployment topology diagrams with high-contrast theme.
  - Implemented debounced real-time client-side search across all 1,215+ binary links and CVE records to prevent layout thrashing.
  - Added responsive off-canvas mobile navigation drawer with backdrop overlay, keyboard navigation (ESC key trap), and focus management.
  - Enhanced accessibility (WCAG AA) with Skip to Main Content link, high-contrast focus rings (`:focus-visible`), and ARIA landmarks.
  - Added robust copy-to-clipboard functionality with automatic fallback for non-secure/legacy environments.
- **Security Research & Master Vulnerability Matrix**:
  - Verified official NVD CVE records (2016–2026) against NIST database with direct links, CVSS v3/v4 severity metrics, attack vectors, and discovering researchers.
  - Documented exact affected version boundaries for all 32+ critical and high-severity CVEs.
  - Added Emergency Zero-Day Hardening and Webshell Quarantine playbooks.
- **Technical Documentation Suite**:
  - Added canonical `DOCNOTE.md` and overhauled `CHANGELOG.md`.

### Changed

- Refactored working directory management in `download_and_verify` to preserve original working directory state (`$original_pwd`).
- Updated User-Agent identifier to `Zimbra-Link-Installer/2.6.0`.
- Formatted all documentation tables with compact micro-typography for optimal scannability and zero line truncation.

---

## [2.5.0] - 2026-08-27

### Added

- **Multi-Tiered CLI Architecture**:
  - Refactored `zimbra-link-installer.sh` with dedicated nested submenus:
    - *Menu 1: Official Network Edition* (10.1, 10.0, 9.0, 8.8.x, 8.7.x, 8.6.0, 8.5.x, 8.0.x, 7.x).
    - *Menu 2: Official Open Source Edition / FOSS* (8.8.x, 8.7.x, 8.6.0, 8.5.x, 8.0.x, 7.x).
    - *Menu 3: Unofficial / Community Builds* (10.1.x, 10.0.x, 9.0.0, 8.8.15) for Ubuntu & RHEL distributions.
    - *Menu 4: Pre-Flight System Audit & Prerequisite Check*.
    - *Menu 5: Deep Link Telemetry & Health Validator Launcher*.
- **Master Vulnerability Matrix**:
  - Structured 32+ CVE breakdown across ZCS components (Mailbox, Admin Console, Amavis, Postfix, OpenLDAP, Nginx, ClamAV).
  - Added Zero-Day Emergency Hardening and Webshell Quarantine operational guidelines.

### Changed

- Improved CLI menu navigation flow with clear return options and error handling.

---

## [2.4.0] - 2026-08-27

### Added

- **Complete Historical Zimbra Wiki Synchronization**:
  - Mapped and indexed all official releases directly from Zimbra Releases Wiki (`wiki.zimbra.com/wiki/Zimbra_Releases`).
  - Indexed all historical branches:
    - ZCS 4.5.x (*Franklin*)
    - ZCS 5.0.x (*Frankie*)
    - ZCS 6.0.x (*GunsNRoses*)
    - ZCS 7.0.x – 7.2.x (*Helix*)
    - ZCS 8.0.x (*IronMaiden*)
    - ZCS 8.5.x – 8.8.x (*JudasPriest*)
    - ZCS 9.0.0 (*Kepler*)
    - ZCS 10.0.x (*Lennon*)
    - ZCS 10.1.x (*MotleyCrue*)
- **1,215+ Verified Active Downloads**:
  - Scaled active binary and checksum links to 1,215+ verified download targets with zero broken links verified by telemetry validation suite.

---

## [2.3.0] - 2026-08-27

### Added

- **Archival Consolidation from `zimbra_bits` and `zimbra_direct_downloads`**:
  - Merged 235 official release entries from `alsyundawy/zimbra_bits`.
  - Incorporated direct download links and MD5/SHA checksum tables from `martbrooks/zimbra_direct_downloads`.
  - Expanded OS coverage to legacy enterprise platforms:
    - Debian GNU/Linux 4.0 (*Etch*), 5.0 (*Lenny*), 6.0 (*Squeeze*), 7.0 (*Wheezy*), 8.0 (*Jessie*)
    - RHEL / CentOS 4.x, 5.x, 6.x, 7.x
    - SUSE Linux Enterprise Server (SLES) 10, 11, 12 and openSUSE
    - Fedora Core 4/5, Fedora 7/11/13
    - Mandriva Linux and Mac OS X (x86 & PowerPC)
  - Expanded verified download archive from 945 to 1,140+, then to 1,183+ active links.

---

## [2.2.0] - 2026-08-27

### Added

- **Official Synacor Release Indexing**:
  - Indexed official Synacor / VMware archive from `files.zimbra.com` for Network Edition (NE) and Open Source Edition (FOSS) covering ZCS 7.x through ZCS 10.1.x.
  - Added official security patch archives, maintenance builds, and hotfix tarballs.
  - Increased total verified active download links to 945+.

---

## [2.1.0] - 2026-08-27

### Added

- **Community FOSS Expansion (53+ Builds)**:
  - Indexed and populated 53+ community builds across ZCS 8.8.15, 9.0.0, 10.0.x, and 10.1.x.
  - Consolidated community artifacts from `maldua/zimbra-foss` GitHub releases and `techfiles.online` CDN (Ian Walker Builds).
  - Added multi-OS support matrix: Ubuntu 24.04 LTS (Noble), 22.04 LTS (Jammy), 20.04 LTS (Focal), 18.04 LTS (Bionic), RHEL 9, and RHEL 8.
  - Increased total verified download targets to 741+ links.

---

## [2.0.0] - 2026-08-27

### Added

- **Initial Public Release**:
  - Initial public release of **Zimbra Link Installer & Telemetry Suite**.
  - Interactive Bash Installer (`zimbra-link-installer.sh`) v2.0.0.
  - Asynchronous multithreaded Deep Link Telemetry & Health Validator (`scripts/deep_link_validator.py`) with concurrent HTTP HEAD/GET range checking.
  - Automated cryptographic integrity verification engine supporting SHA-256 and MD5 checksum validation.
  - Core binary download archive consolidating official LTS and modern community builds.
