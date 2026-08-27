import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "grouped_maldua.json")

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        grouped_maldua = json.load(f)
else:
    grouped_maldua = {}

def format_foss_table(version_list, title):
    """
    Format Markdown table for FOSS Zimbra Community builds
    """
    distro_labels = {
        "zimbra-foss-build-ubuntu-24.04": "Ubuntu 24.04",
        "zimbra-foss-build-ubuntu-22.04": "Ubuntu 22.04",
        "zimbra-foss-build-ubuntu-20.04": "Ubuntu 20.04",
        "zimbra-foss-build-ubuntu-18.04": "Ubuntu 18.04",
        "zimbra-foss-build-rhel-9": "RHEL / Rocky / Alma 9",
        "zimbra-foss-build-rhel-8": "RHEL / Rocky / Alma 8",
        "zimbra-foss-build-rhel-7": "RHEL 7 / CentOS 7"
    }

    lines = []
    lines.append(f"### {title}\n")
    lines.append("| Version | Target OS | Direct Archive (.tgz) | MD5 | SHA256 |")
    lines.append("| :--- | :--- | :---: | :---: | :---: |")

    for v in version_list:
        if v not in grouped_maldua:
            continue
        distros = grouped_maldua[v]
        for d_key, d_label in distro_labels.items():
            if d_key in distros:
                assets = distros[d_key].get("assets", {})
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
                lines.append(f"| **`{v}`** | {d_label} | {tgz} | {md5} | {sha} |")
    lines.append("")
    return "\n".join(lines)
