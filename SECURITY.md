<!-- markdownlint-disable MD013 MD024 MD033 -->

# Security Policy & Vulnerability Management

## 1. Supported Versions

### Repository & CLI Suite Support

| Component / Version | Supported | Maintenance Status |
| :--- | :---: | :--- |
| **Zimbra Link Installer & Telemetry Suite `v2.6.x`** | ✅ | **Active Support** (Continuous vulnerability patching & binary telemetry) |
| **Zimbra Link Installer & Telemetry Suite `< v2.6.0`** | ❌ | **End of Life** (Users must upgrade to latest script release) |

### Zimbra Collaboration Suite (ZCS) Lifecycle Matrix

| ZCS Major Series | Official Status | Lifecycle Notes |
| :--- | :---: | :--- |
| **ZCS 10.1.x (Daffodil)** | ✅ | **Active General Support** (Latest security patch: `10.1.20`) |
| **ZCS 10.0.x (Daffodil)** | ❌ | **End of General Support** (EOL: June 30, 2025; Upgrade to 10.1.x required) |
| **ZCS 9.0.0 (Kepler)** | ❌ | **End of General Support** (EOL: December 31, 2024; Legacy archive only) |
| **ZCS 8.8.15 (Joule)** | ❌ | **End of General Support** (EOL: December 31, 2023; Cumulative P47 available) |
| **ZCS < 8.8.15 (Legacy)** | ❌ | **End of Life** (Historical archival reference only) |

---

## 2. Reporting a Vulnerability

Security is a fundamental priority for the **Zimbra Link Installer & Telemetry Suite**. If you discover a security vulnerability in this repository, the installer script (`zimbra-link-installer.sh`), telemetry modules, or discover newly confirmed Zimbra zero-day exploits / CVEs that need to be documented, please report them responsibly.

### How to Report

1. **Direct Maintainer Contact:**
   - **Email:** `alsyundawy@gmail.com`
   - **Subject Line:** `[SECURITY DISCLOSURE] Zimbra Link Installer - <Short Description>`
   - **PGP / Secure Messaging:** Available upon request or via direct contact.

2. **Information to Include:**
   - Detailed description of the vulnerability or newly discovered exploit vector.
   - Affected script version, OS environment, or ZCS target version.
   - Proof of Concept (PoC) or reproduction steps.
   - Potential impact (RCE, LFI, SSRF, XSS, PrivEsc, etc.).

### Response Timeline

- **Initial Acknowledgment:** Within **24 hours**.
- **Triage & Reproduction:** Within **48 hours**.
- **Fix & Advisory Release:** Critical security fixes will be published within **72 hours** of confirmation.

---

## 3. Official Upstream Vulnerability Disclosures

For vulnerabilities discovered directly in upstream **Zimbra Collaboration Suite (ZCS)** software:

- Report to Synacor / Zimbra Security Team: `security@zimbra.com` or via the [Zimbra Security Center](https://wiki.zimbra.com/wiki/Security_Center).
- Review the official [Zimbra Security Advisories](https://wiki.zimbra.com/wiki/Zimbra_Security_Advisories) and the [CISA Known Exploited Vulnerabilities (KEV) Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog).
