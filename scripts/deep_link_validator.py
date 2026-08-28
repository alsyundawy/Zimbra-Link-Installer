import re
import urllib.request
import concurrent.futures
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
README_FILE = os.path.join(SCRIPT_DIR, "..", "README.md")

if not os.path.exists(README_FILE):
    print(f"Error: README.md not found at {README_FILE}")
    sys.exit(1)

with open(README_FILE, "r") as f:
    content = f.read()

# Extract all URLs
urls = re.findall(r'https?://[^\s\>\)\"]+', content)
cleaned_urls = list({u.rstrip(".,;`')") for u in urls})

print(f"Total extracted links from README.md: {len(urls)}")
print(f"Total unique URLs to validate: {len(cleaned_urls)}")

# Filter binary and checksum targets
binary_urls = [u for u in cleaned_urls if any(u.endswith(ext) for ext in [".tgz", ".sha256", ".md5", ".zip", ".tar.gz"])]
non_binary_urls = [u for u in cleaned_urls if u not in binary_urls]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://techfiles.online/"
}

verified_active = 0
failed_urls = []

def check_binary_url(url):
    req = urllib.request.Request(url, headers=headers)
    req.get_method = lambda: "HEAD"
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status in [200, 301, 302, 307, 308]:
                return True, url, resp.status
    except Exception:
        # Fallback to GET range
        try:
            req_get = urllib.request.Request(url, headers={**headers, "Range": "bytes=0-10"})
            with urllib.request.urlopen(req_get, timeout=10) as resp:
                if resp.status in [200, 206, 301, 302]:
                    return True, url, resp.status
        except Exception as e:
            return False, url, str(e)
    return False, url, "Unknown error"

print(f"Validating {len(binary_urls)} binary and checksum download links...")

with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    results = list(executor.map(check_binary_url, binary_urls))

for success, url, status in results:
    if success:
        verified_active += 1
    else:
        failed_urls.append((url, status))

print("\n=== VALIDATION SUMMARY ===")
print(f"Verified Active Downloads : {verified_active}")
print(f"Non-Binary / Skipped URLs : {len(non_binary_urls)}")
print(f"Failed / Unavailable URLs : {len(failed_urls)}")

if failed_urls:
    print("\n[!] The following URLs failed validation:")
    for url, err in failed_urls:
        print(f"  - {url} ({err})")
    sys.exit(1)
else:
    print("\n[SUCCESS] All binary and checksum URLs are 100% active and healthy!")
