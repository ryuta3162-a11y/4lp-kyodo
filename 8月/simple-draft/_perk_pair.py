# -*- coding: utf-8 -*-
from pathlib import Path
import json
import subprocess

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")

updates = {
    "en": {
        "monthsList": "Aug · Sep · Oct · Nov · Dec · Jan",
        "optionCatch": "August options",
        "optionLabel": "8 free options",
        "joinAmountLabel": "Amount due at signup",
        "joinAmountAt": "(<span class=\"join-date\">{m}/{d}</span>) Amount due at signup",
    },
    "ko": {
        "monthsList": "8월 · 9월 · 10월 · 11월 · 12월 · 1월",
        "optionCatch": "8월 옵션",
        "optionLabel": "무료 옵션 8개",
        "joinAmountLabel": "입회 시 결제 금액",
        "joinAmountAt": "(<span class=\"join-date\">{m}/{d}</span>) 입회 시 결제 금액",
    },
    "zh-CN": {
        "monthsList": "8月 · 9月 · 10月 · 11月 · 12月 · 1月",
        "optionCatch": "8月选项",
        "optionLabel": "8项免费选项",
        "joinAmountLabel": "入会时应付金额",
        "joinAmountAt": "(<span class=\"join-date\">{m}/{d}</span>)入会时应付金额",
    },
    "zh-TW": {
        "monthsList": "8月 · 9月 · 10月 · 11月 · 12月 · 1月",
        "optionCatch": "8月選項",
        "optionLabel": "8項免費選項",
        "joinAmountLabel": "入會時應付金額",
        "joinAmountAt": "(<span class=\"join-date\">{m}/{d}</span>)入會時應付金額",
    },
}

for lang, upd in updates.items():
    path = ROOT / "locales" / "campaign" / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["pricing"]["monthsList"] = upd["monthsList"]
    data["pricing"]["optionCatch"] = upd["optionCatch"]
    data["pricing"]["optionLabel"] = upd["optionLabel"]
    data["pricing"]["joinAmountLabel"] = upd["joinAmountLabel"]
    data["pricing"]["joinAmountAt"] = upd["joinAmountAt"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(lang)

subprocess.run(["python", str(ROOT / "build_locales.py")], check=True)

# sync aug
html = (ROOT / "index.html").read_text(encoding="utf-8")
# also fix JS fallback for join label if present
html = html.replace(
    "dateLabelEl.innerHTML = `(<span class=\"join-date\">${month}/${date}</span>)ご入会時金額`;",
    "dateLabelEl.innerHTML = `(<span class=\"join-date\">${month}/${date}</span>)ご入会時のお支払い金額`;",
)
html = html.replace(
    "JoyfitI18n.t('pricing.joinAmountAt', '(<span class=\"join-date\">{m}/{d}</span>)ご入会時金額')",
    "JoyfitI18n.t('pricing.joinAmountAt', '(<span class=\"join-date\">{m}/{d}</span>)ご入会時のお支払い金額')",
)
html = html.replace(
    "setText('dynamic-date-label', 'pricing.joinAmountLabel', 'ご入会時金額');",
    "setText('dynamic-date-label', 'pricing.joinAmountLabel', 'ご入会時のお支払い金額');",
)
(ROOT / "index.html").write_text(html, encoding="utf-8")

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
