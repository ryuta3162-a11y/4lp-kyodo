# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")
old = "background: var(--gold-light); padding: 2px 6px; border-radius: 4px;"
new = "background: #111111; color: #fff; padding: 2px 6px;"
for lang in ["en", "ko", "zh-CN", "zh-TW"]:
    p = ROOT / "locales" / "campaign" / f"{lang}.json"
    t = p.read_text(encoding="utf-8")
    p.write_text(t.replace(old, new), encoding="utf-8")
    print(lang, "ok")

subprocess.run(["python", str(ROOT / "build_locales.py")], check=True)

html = (ROOT / "index.html").read_text(encoding="utf-8")
for a, b in [
    ('href="i18n.css"', 'href="../i18n.css"'),
    ('src="locales.bundle.js"', 'src="../locales.bundle.js"'),
    ('src="i18n.js"', 'src="../i18n.js"'),
    ('src="campaign-i18n.js"', 'src="../campaign-i18n.js"'),
    ('src="joylogo.jpg"', 'src="../joylogo.jpg"'),
]:
    html = html.replace(a, b)
(ROOT / "8月" / "index.html").write_text(html, encoding="utf-8")
print("aug synced")
