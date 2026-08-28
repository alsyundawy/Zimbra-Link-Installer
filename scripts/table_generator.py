import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "grouped_maldua.json")

DISTRO_LABELS = {
    "zimbra-foss-build-ubuntu-24.04": "Ubuntu 24.04",
    "zimbra-foss-build-ubuntu-22.04": "Ubuntu 22.04",
    "zimbra-foss-build-ubuntu-20.04": "Ubuntu 20.04",
    "zimbra-foss-build-ubuntu-18.04": "Ubuntu 18.04",
    "zimbra-foss-build-rhel-9": "RHEL / Rocky / Alma 9",
    "zimbra-foss-build-rhel-8": "RHEL / Rocky / Alma 8",
    "zimbra-foss-build-rhel-7": "RHEL 7 / CentOS 7"
}

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        grouped_maldua = json.load(f)
else:
    grouped_maldua = {}


def _extract_asset_links(assets):
    """Helper to extract direct, md5, and sha256 links from release assets."""
    tgz = "-"
    md5 = "-"
    sha = "-"
    for name, url in assets.items():
        if name.endswith(".tgz"):
            tgz = f"[Download]({url})"
        elif name.endswith(".md5"):
            md5 = f"[MD5]({url})"
        elif name.endswith(".sha256"):
            sha = f"[SHA256]({url})"
    return tgz, md5, sha


def _format_distro_rows(version, distros):
    """Helper to generate rows for a single version across all target distros."""
    rows = []
    for d_key, d_label in DISTRO_LABELS.items():
        if d_key not in distros:
            continue
        assets = distros[d_key].get("assets", {})
        tgz, md5, sha = _extract_asset_links(assets)
        rows.append(f"| **`{version}`** | {d_label} | {tgz} | {md5} | {sha} |")
    return rows


def format_foss_table(version_list, title):
    """
    Format Markdown table for FOSS Zimbra Community builds
    """
    lines = [
        f"### {title}\n",
        "| Version | Target OS | Direct Archive (.tgz) | MD5 | SHA256 |",
        "| :--- | :--- | :---: | :---: | :---: |"
    ]

    for v in version_list:
        if v in grouped_maldua:
            lines.extend(_format_distro_rows(v, grouped_maldua[v]))

    return "\n".join(lines)
