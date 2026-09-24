#!/usr/bin/env python3
"""Overlay the October campaign onto production root files."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OCT = Path(__file__).resolve().parent
MARKER = "2026-10-16T23:59:59+09:00"


def already_switched() -> bool:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    return MARKER in html and 'href="i18n.css"' in html


def main() -> int:
    if already_switched():
        print("already switched")
        return 0

    html = (OCT / "campaign.html").read_text(encoding="utf-8")
    html = html.replace('href="../i18n.css"', 'href="i18n.css"')
    html = html.replace('src="../i18n.js"', 'src="i18n.js"')
    # 日付ゲートは本番では使わない
    html = html.replace(
        """    <script>
    (function () {
      if (Date.now() < Date.parse('2026-09-25T00:00:00+09:00')) {
        location.replace('./');
      }
    })();
    </script>
""",
        "",
    )
    (ROOT / "index.html").write_text(html, encoding="utf-8")

    shutil.copy2(OCT / "campaign-i18n.js", ROOT / "campaign-i18n.js")

    dest = ROOT / "locales" / "campaign"
    dest.mkdir(parents=True, exist_ok=True)
    for src in (OCT / "locales-for-switch").glob("*.json"):
        shutil.copy2(src, dest / src.name)

    subprocess.check_call([sys.executable, str(ROOT / "build_locales.py")], cwd=ROOT)
    print("switched to October LP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
