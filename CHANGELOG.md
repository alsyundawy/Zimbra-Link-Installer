<!-- markdownlint-disable MD013 MD024 -->

# CHANGELOG

All notable changes to the **Zimbra Link Installer & Telemetry Suite** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
