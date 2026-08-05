# -*- coding: utf-8 -*-
from pathlib import Path
import json
import subprocess

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")

# tighten option hero padding in CSS if still wide
html = (ROOT / "index.html").read_text(encoding="utf-8")
old = """        .price-item--option-hero {
            display: block;
            grid-template-columns: none;
            min-height: 0;
            padding: 1.45rem 0.5rem 1.55rem;
            margin: 0.15rem 0 0.5rem;
            border-bottom: none;
            text-align: center;
            background: #ffffff;
        }"""
new = """        .price-item--option-hero {
            display: block;
            grid-template-columns: none;
            min-height: 0;
            padding: 1.35rem 0.15rem 1.45rem;
            margin: 0.1rem 0 0.4rem;
            border-bottom: none;
            text-align: center;
            background: #ffffff;
        }"""
if old in html:
    html = html.replace(old, new)
    print("option padding ok")
else:
    print("option padding skip")

(ROOT / "index.html").write_text(html, encoding="utf-8")

steps = {
    "en": {
        "step1Badge": "Bonus perks",
        "step1Title": "Referral, student, club transfer, etc.",
        "step1Desc": "※Student discount applies when regular monthly fee starts",
        "step2Badge": "App signup",
        "step2Title": "Easy signup via app",
        "step2Desc": "As fast as 5 min — use today",
    },
    "ko": {
        "step1Badge": "추가 혜택",
        "step1Title": "소개・학생・타 클럽 이전 등",
        "step1Desc": "※학생 할인은 통상 월액 발생 시 적용",
        "step2Badge": "앱 입회",
        "step2Title": "앱으로 간편 입회",
        "step2Desc": "최단 5분・당일 바로 이용",
    },
    "zh-CN": {
        "step1Badge": "追加特典",
        "step1Title": "介绍・学生・他店移籍等",
        "step1Desc": "※学生优惠于通常月费开始时适用",
        "step2Badge": "APP入会",
        "step2Title": "APP轻松入会",
        "step2Desc": "最短5分・当日可用",
    },
    "zh-TW": {
        "step1Badge": "追加特典",
        "step1Title": "介紹・學生・他店移籍等",
        "step1Desc": "※學生優惠於通常月費開始時適用",
        "step2Badge": "APP入會",
        "step2Title": "APP輕鬆入會",
        "step2Desc": "最短5分・當日可用",
    },
}

for lang, upd in steps.items():
    path = ROOT / "locales" / "campaign" / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for k, v in upd.items():
        data["steps"][k] = v
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang)

subprocess.run(["python", str(ROOT / "build_locales.py")], check=True)

html = (ROOT / "index.html").read_text(encoding="utf-8")
aug = html
for a, b in [
    ('href="i18n.css"', 'href="../i18n.css"'),
    ('src="locales.bundle.js"', 'src="../locales.bundle.js"'),
    ('src="i18n.js"', 'src="../i18n.js"'),
    ('src="campaign-i18n.js"', 'src="../campaign-i18n.js"'),
    ('src="joylogo.jpg"', 'src="../joylogo.jpg"'),
]:
    aug = aug.replace(a, b)
(ROOT / "8月" / "index.html").write_text(aug, encoding="utf-8")
print("done")
