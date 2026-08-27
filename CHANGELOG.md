<!-- markdownlint-disable MD013 MD024 -->

# CHANGELOG

All notable changes to the **Zimbra Link Installer & Telemetry Suite** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.6.0] - 2026-08-27

### Added

- **Enterprise Security Hardening**: Added defensive execution flags (`set -Eeuo pipefail`), strict `IFS=$'\n\t'`, and default `umask 022`.
- **Atomic Cleanup Trap**: Added signal handler trapping `EXIT`, `INT`, `TERM`, and `HUP` to ensure temporary directories are destroyed without polluting the host.
- **Privilege Abstraction Layer (`run_privileged`)**: Dynamically invokes commands as root or via `sudo` based on current UID (`id -u`), ensuring compatibility with minimal containerized environments.
- **Advanced Checksum Parsing**: Checksum parser now uses regex extraction (`grep -oE '[a-fA-F0-9]{32|64}'`) and case-insensitive comparison (`${expected,,} == ${actual,,}`).
- **FQDN Pre-Flight Audit**: Added automated FQDN verification (`hostname -f`) to prevent DNS resolution errors during `zmsetup.pl`.
- **Technical Documentation & Notes**: Added canonical `DOCNOTE.md` and `CHANGELOG.md`.

### Changed

- Refactored directory navigation in `download_and_verify` to preserve original working directory `$original_pwd`.
- Updated User-Agent string to enterprise identifier `Zimbra-Link-Installer/2.6.0`.

---

## [2.5.0] - 2026-08-27

### Added

- **Multi-Tiered CLI Architecture**: Dedicated submenus for:
  - Menu 1: Official Network Edition (10.1, 10.0, 9.0, 8.8.x, 8.7.x, 8.6.0, 8.5.x, 8.0.x, 7.x)
  - Menu 2: Official Open Source Edition / FOSS (8.8.x, 8.7.x, 8.6.0, 8.5.x, 8.0.x, 7.x)
  - Menu 3: Unofficial / Community FOSS Builds (10.1.x, 10.0.x, 9.0.0, 8.8.15)
- **Deep Affected Version Matrix**: Enriched CVE security analysis in `README.md` with exact affected versions for 32+ CVEs (2016–2026).
- **Incident Response Playbook**: Added Zero-Day Emergency Hardening and Webshell Quarantine protocol.

---

## [2.1.0] - 2026-08-27

### Added

- **Complete Historical Index**: Mapped and indexed all releases from Zimbra Releases Wiki (ZCS 4.5.x, 5.0.x, 6.0.x, 7.x, 8.x, 9.x, 10.x).
- **1,215 Active Verified Downloads**: Automated telemetry validation guaranteeing 0 broken links on `files.zimbra.com` and community CDNs.

---

## [2.0.0] - 2026-08-27

### Added

- Initial public release of **Zimbra Link Installer** repository.
- Consolidates `alsyundawy/zimbra_bits`, `martbrooks/zimbra_direct_downloads`, `maldua/zimbra-foss`, and `techfiles.online`.
