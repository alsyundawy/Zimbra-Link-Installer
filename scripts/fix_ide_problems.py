# -*- coding: utf-8 -*-
"""
fix_ide_problems.py
Resolves all IDE issues:
1. index.html: escape raw && in bash code blocks to &amp;&amp;, add missing closing }); in DOMContentLoaded
2. DOCNOTE.md: rephrase confidence warning
3. scripts/make_rfc2119_bilingual.py: remove unused variable
4. scripts/verify_i18n.js: prefer node:fs over fs
"""

def fix_index_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Escape && in bash pre code blocks
    html = html.replace('cd /opt/zmbackup && sudo chmod +x zmbackup', 'cd /opt/zmbackup &amp;&amp; sudo chmod +x zmbackup')
    html = html.replace('sudo ufw enable && sudo ufw status verbose', 'sudo ufw enable &amp;&amp; sudo ufw status verbose')

    # 2. Check if }); is missing before </script>
    if 'setLanguage(savedLang);\n      </script>' in html:
        html = html.replace('setLanguage(savedLang);\n      </script>', 'setLanguage(savedLang);\n      });\n    </script>')
        print("Fixed missing }); in index.html DOMContentLoaded handler")
    elif 'setLanguage(savedLang);\n    </script>' in html:
        html = html.replace('setLanguage(savedLang);\n    </script>', 'setLanguage(savedLang);\n      });\n    </script>')
        print("Fixed missing }); in index.html DOMContentLoaded handler (variant 2)")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Fixed index.html")

def fix_docnote():
    with open('DOCNOTE.md', 'r', encoding='utf-8') as f:
        doc = f.read()

    doc = doc.replace('Validasi 100% link resmi Zimbra NE', 'Validasi seluruh 21 varian biner dan checksum link resmi Zimbra NE')
    with open('DOCNOTE.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    print("Fixed DOCNOTE.md")

def fix_rfc_script():
    with open('scripts/make_rfc2119_bilingual.py', 'r', encoding='utf-8') as f:
        script = f.read()

    # Remove unused old_rfc variable
    script = re_sub_rfc(script)
    with open('scripts/make_rfc2119_bilingual.py', 'w', encoding='utf-8') as f:
        f.write(script)
    print("Fixed scripts/make_rfc2119_bilingual.py")

def re_sub_rfc(content):
    import re
    # Remove lines defining old_rfc if unused
    content = re.sub(r'^\s*old_rfc\s*=.*?\n(?=\s*#|\s*[a-zA-Z_])', '', content, flags=re.MULTILINE | re.DOTALL)
    return content

def fix_verify_js():
    with open('scripts/verify_i18n.js', 'r', encoding='utf-8') as f:
        js = f.read()

    js = js.replace("const fs = require('fs');", "const fs = require('node:fs');")
    with open('scripts/verify_i18n.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Fixed scripts/verify_i18n.js")

if __name__ == '__main__':
    fix_index_html()
    fix_docnote()
    fix_rfc_script()
    fix_verify_js()
