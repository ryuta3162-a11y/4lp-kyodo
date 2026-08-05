# -*- coding: utf-8 -*-
"""Impact + simplify: price hero, remove frames/underlines, option copy."""
from pathlib import Path
import re
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "index.html"
AUG = ROOT / "8月" / "index.html"

html = PROD.read_text(encoding="utf-8")

# --- HTML: half-year price block ---
old_half_html = """                    <div class="price-item price-item--half-year">
                        <div class="label-group">
                            <span class="perk-badge perk-badge-accent" data-i18n="pricing.perkBadge">キャンペーン特典</span>
                            <p class="half-year-catch" data-i18n="hero.halfYearCatch">6ヶ月間ずーっとお得</p>
                        </div>
                        <div class="half-year-main">
                            <div class="half-year-price-hero">
                                <span class="half-year-price font-impact">3,740</span>
                                <span class="half-year-unit" data-i18n="pricing.perMonthUnit">円(税込)/月</span>
                            </div>
                            <p class="half-year-months" data-i18n="pricing.monthsList">8月、9月、10月、11月、12月、1月</p>
                            <p class="half-year-period-note" data-i18n="pricing.monthsNote">2026年8月から2027年1月までの半年間</p>
                        </div>
                    </div>"""

new_half_html = """                    <div class="price-item price-item--half-year">
                        <div class="half-year-main">
                            <p class="half-year-catch" data-i18n="hero.halfYearCatch">半年間ずーっと値引き</p>
                            <p class="half-year-period" data-i18n="pricing.halfYearPeriod">8月〜1月</p>
                            <div class="half-year-price-hero">
                                <span class="half-year-price font-impact">3,740</span><span class="half-year-yen font-impact" data-i18n="pricing.yen">円</span>
                            </div>
                            <p class="half-year-unit" data-i18n="pricing.perMonthUnitTax">(税込)/月</p>
                        </div>
                    </div>"""

if old_half_html not in html:
    raise SystemExit("half-year html not found")
html = html.replace(old_half_html, new_half_html)

old_opt_html = """                    <div class="price-item">
                        <div class="label-group">
                            <span class="perk-badge perk-badge-accent" data-i18n="pricing.perkBadge">キャンペーン特典</span>
                            <div class="label"><span id="campaign-option-label">8月オプション</span><span class="label-sub" id="campaign-option-label-sub">無料オプション8つ自動契約</span></div>
                        </div>
                        <div class="divider-dot"></div>
                        <div class="price-display-center">
                            <span class="price-value zero-yen font-impact featured-price text-value-accent">0<span class="unit" data-i18n="pricing.yen">円</span></span>
                        </div>
                    </div>"""

new_opt_html = """                    <div class="price-item price-item--option-simple">
                        <p class="option-simple-line" id="campaign-option-label" data-i18n="pricing.optionLabel">8月オプション8つが0円</p>
                    </div>"""

if old_opt_html not in html:
    raise SystemExit("option html not found")
html = html.replace(old_opt_html, new_opt_html)

old_item3 = 'data-i18n="conditions.item3">無料オプションは入会時、全て自動契約となります</span>'
new_item3 = 'data-i18n="conditions.item3">8つの無料オプションは入会時全て自動契約となります</span>'
if old_item3 not in html:
    raise SystemExit("item3 not found")
html = html.replace(old_item3, new_item3)

# --- CSS: half-year redesign ---
old_half_css = """        .price-item--half-year {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 1.05rem;
            grid-template-columns: none;
            min-height: 0;
            margin: 0.4rem 0 1rem;
            padding: 1.8rem 0.85rem 2rem;
            border: none;
            border-radius: 0;
            border-bottom: none;
            background: transparent;
            box-shadow: none;
            color: #111111;
        }
        .price-item--half-year::before {
            content: '';
            position: absolute;
            inset: 0;
            z-index: 0;
            border-radius: 0;
            border: 2px solid #111111;
            background: #ffffff;
            box-shadow: none;
        }
        .price-item--half-year > * {
            position: relative;
            z-index: 1;
        }
        .price-item--half-year .label-group {
            align-items: center;
            width: 100%;
            max-width: none;
        }
        .price-item--half-year .perk-badge,
        .price-item--half-year .perk-badge.perk-badge-accent {
            margin-top: 0;
            background-color: #C21632 !important;
            color: #ffffff !important;
            border: none;
            border-radius: 4px;
            box-shadow: none;
        }
        .price-item--half-year .half-year-catch {
            margin: 0;
            font-size: clamp(1.08rem, 4.3vw, 1.32rem);
            font-weight: 900;
            letter-spacing: 0.04em;
            color: #111111;
            line-height: 1.3;
            text-shadow: none;
        }
        .half-year-main {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 0.65rem;
            width: 100%;
            padding: 0.15rem 0 0;
        }
        .half-year-price-hero {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: baseline;
            justify-content: center;
            gap: 0.12em;
            white-space: nowrap;
            padding: 0.15rem 0 0.05rem;
        }
        .price-item--half-year .half-year-price {
            display: inline;
            font-size: clamp(3.2rem, 16vw, 4.4rem);
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1;
            color: #C21632;
            text-shadow: none;
            -webkit-text-stroke: 0;
        }
        .price-item--half-year .half-year-unit {
            display: inline;
            margin: 0;
            font-size: clamp(1.1rem, 4.5vw, 1.45rem);
            font-weight: 800;
            color: #C21632;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }
        .half-year-months {
            margin: 0.15rem 0 0;
            width: 100%;
            font-size: clamp(1rem, 4vw, 1.2rem);
            font-weight: 900;
            line-height: 1.5;
            letter-spacing: 0.03em;
            color: #111111;
            word-break: keep-all;
        }
        .half-year-period-note {
            margin: 0;
            width: 100%;
            max-width: none;
            padding: 0 0.15rem;
            font-size: clamp(0.7rem, 2.7vw, 0.82rem);
            font-weight: 700;
            line-height: 1.45;
            color: #111111;
            opacity: 0.75;
            white-space: normal;
        }"""

new_half_css = """        .price-item--half-year {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 0;
            grid-template-columns: none;
            min-height: 0;
            margin: 0.25rem 0 0.75rem;
            padding: 1.6rem 0.5rem 1.75rem;
            border: none;
            border-radius: 0;
            border-bottom: none;
            background: #ffffff;
            box-shadow: none;
            color: #111111;
        }
        .price-item--half-year::before {
            display: none;
        }
        .price-item--half-year > * {
            position: relative;
            z-index: 1;
        }
        .half-year-main {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 0.35rem;
            width: 100%;
            padding: 0;
        }
        .price-item--half-year .half-year-catch {
            margin: 0;
            order: 1;
            font-size: clamp(1.15rem, 4.8vw, 1.45rem);
            font-weight: 900;
            letter-spacing: 0.08em;
            color: #111111;
            line-height: 1.25;
            text-shadow: none;
        }
        .half-year-period {
            margin: 0 0 0.35rem;
            order: 2;
            font-size: clamp(0.95rem, 3.8vw, 1.15rem);
            font-weight: 800;
            letter-spacing: 0.12em;
            color: #111111;
            line-height: 1.3;
        }
        .half-year-price-hero {
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            align-items: baseline;
            justify-content: center;
            gap: 0.02em;
            white-space: nowrap;
            padding: 0.2rem 0 0;
            order: 3;
        }
        .price-item--half-year .half-year-price {
            display: inline;
            font-size: clamp(4.2rem, 22vw, 5.8rem);
            font-weight: 900;
            letter-spacing: -0.04em;
            line-height: 0.95;
            color: #C21632;
            text-shadow: none;
            -webkit-text-stroke: 0;
        }
        .price-item--half-year .half-year-yen {
            display: inline;
            font-size: clamp(1.6rem, 7vw, 2.2rem);
            font-weight: 900;
            color: #C21632;
            letter-spacing: 0;
            line-height: 1;
            margin-left: 0.05em;
        }
        .price-item--half-year .half-year-unit {
            display: block;
            order: 4;
            margin: 0.15rem 0 0;
            font-size: clamp(0.95rem, 3.6vw, 1.15rem);
            font-weight: 800;
            color: #111111;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }
        .price-item--option-simple {
            display: block;
            grid-template-columns: none;
            min-height: 0;
            padding: 0.85rem 0.5rem 1rem;
            border-bottom: none;
            text-align: center;
        }
        .option-simple-line {
            margin: 0;
            font-size: clamp(1rem, 4vw, 1.2rem);
            font-weight: 900;
            color: #111111;
            letter-spacing: 0.04em;
            line-height: 1.4;
        }"""

if old_half_css not in html:
    raise SystemExit("half-year css not found")
html = html.replace(old_half_css, new_half_css)

# Remove responsive overrides that reference removed classes / old sizes
old_mq = """            .price-item--half-year {
                padding: 1.35rem 0.7rem 1.5rem;
            }
            .price-item--half-year .half-year-price {
                font-size: clamp(2.2rem, 11vw, 2.85rem);
            }
            .half-year-period-note {
                font-size: 0.68rem;
            }"""
# may have different content - search flexibly
mq_pat = re.compile(
    r"\s*\.price-item--half-year \{\s*padding: 1\.35rem[^}]+\}\s*"
    r"\.price-item--half-year \.half-year-price \{\s*font-size:[^}]+\}\s*"
    r"\.half-year-period-note \{\s*font-size:[^}]+\}",
    re.M,
)
html, n = mq_pat.subn("\n", html, count=1)
print("mq removed", n)

# Header underline off
html = html.replace(
    """        .campaign-header-enhanced h2::after {
            content: '';
            display: block;
            width: 2.6rem;
            height: 2px;
            margin: 0.7rem auto 0;
            background: linear-gradient(90deg, transparent, #F8E71C, transparent);
            border-radius: 1px;
            box-shadow: none;
        }""",
    """        .campaign-header-enhanced h2::after {
            display: none !important;
        }""",
)

# Remove black frames
html = html.replace(
    """        .lp-framed {
            background: #fff;
            border: 2px solid var(--lp-frame);
            border-radius: 14px;
            box-shadow: var(--lp-frame-shadow);
            position: relative;
        }""",
    """        .lp-framed {
            background: #fff;
            border: none;
            border-radius: 0;
            box-shadow: none;
            position: relative;
        }""",
)
html = html.replace(
    """        .lp-framed { border: 2px solid #111111 !important; }""",
    """        .lp-framed { border: none !important; box-shadow: none !important; }""",
)
html = html.replace(
    """        .campaign-header-enhanced h2::after {
            background: #ffffff !important;
            box-shadow: none !important;
        }""",
    """        .campaign-header-enhanced h2::after {
            display: none !important;
        }""",
)

# Options carousel: white bg, black text, no underline, larger cards
old_carousel_text = """        .options-carousel-section .text-box {
            margin: 0 auto 1.35rem auto;
            max-width: 92%;
            text-align: center;
            background: var(--brand-red);
            border: 2px solid var(--lp-frame);
            border-radius: 12px;
            padding: 20px 16px;
            box-shadow: 0 4px 0 rgba(0, 0, 0, 0.15);
            color: #fff;
        }
        .options-carousel-section .section-title {
            font-size: 1.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            position: relative;
            display: inline-block;
            padding-bottom: 0.5rem;
            color: #fff;
        }
        .options-carousel-section .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 3px;
            background: var(--gold-gradient);
            border-radius: 2px;
        }
        .options-carousel-section .section-title .highlight {
            color: var(--gold-light);
            font-size: 2.5rem;
            margin-right: 4px;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
        }
        .options-carousel-section .text-box p {
            font-size: 0.85rem;
            line-height: 1.65;
            font-weight: 700;
            color: #fff;
            margin: 0;
        }
        .options-carousel-section .text-box .highlight-text {
            color: #fff;
            font-size: 1.15rem;
            font-weight: 900;
        }
        .options-carousel-section .text-box .text-box-note {
            font-size: 0.75rem;
            color: rgba(255, 255, 255, 0.88);
            display: inline-block;
            margin-top: 8px;
            font-weight: 700;
        }"""

new_carousel_text = """        .options-carousel-section .text-box {
            margin: 0 auto 1.35rem auto;
            max-width: 92%;
            text-align: center;
            background: #ffffff;
            border: none;
            border-radius: 0;
            padding: 16px 12px;
            box-shadow: none;
            color: #111111;
        }
        .options-carousel-section .section-title {
            font-size: 1.45rem;
            font-weight: 900;
            margin-bottom: 0.75rem;
            position: relative;
            display: inline-block;
            padding-bottom: 0;
            color: #111111;
        }
        .options-carousel-section .section-title::after {
            display: none !important;
        }
        .options-carousel-section .section-title .highlight {
            color: #C21632;
            font-size: 2.35rem;
            margin-right: 4px;
            text-shadow: none;
        }
        .options-carousel-section .text-box p {
            font-size: 0.85rem;
            line-height: 1.65;
            font-weight: 700;
            color: #111111;
            margin: 0;
        }
        .options-carousel-section .text-box .highlight-text {
            color: #C21632;
            font-size: 1.15rem;
            font-weight: 900;
        }
        .options-carousel-section .text-box .text-box-note {
            font-size: 0.75rem;
            color: #111111;
            opacity: 0.75;
            display: inline-block;
            margin-top: 8px;
            font-weight: 700;
        }"""

if old_carousel_text not in html:
    raise SystemExit("carousel text css not found")
html = html.replace(old_carousel_text, new_carousel_text)

html = html.replace(
    """.scene { width: 100%; height: 450px; display: flex; justify-content: center; align-items: center; position: relative; overflow: hidden; }
        .card-carousel { width: 280px; height: 340px; position: relative; cursor: grab; }
        .option-card-3d { position: absolute; width: 280px; height: 340px; border-radius: 20px; background-color: #fff; border: 4px solid var(--brand-red); display: flex; flex-direction: column; padding: 1.5rem 1rem; left: 50%; top: 0; transform: translateX(-50%); transition: 0.5s; }
        .card-icon { max-width: 140px; max-height: 140px; margin: auto; }""",
    """.scene { width: 100%; height: 520px; display: flex; justify-content: center; align-items: center; position: relative; overflow: hidden; }
        .card-carousel { width: 320px; height: 400px; position: relative; cursor: grab; }
        .option-card-3d { position: absolute; width: 320px; height: 400px; border-radius: 0; background-color: #fff; border: 2px solid #111111; display: flex; flex-direction: column; padding: 1.35rem 1rem; left: 50%; top: 0; transform: translateX(-50%); transition: 0.5s; }
        .card-icon { max-width: 190px; max-height: 190px; margin: auto; width: 100%; object-fit: contain; }""",
)

# mid-list and monthly fee: remove black borders for consistency
html = html.replace(
    """        .mid-list-total-block {
            padding: 1.1rem 1rem;
            text-align: center;
            background: #ffffff;
            border: 2px solid #111111;
            border-radius: 0;
            margin: 1.1rem 0;
            box-shadow: none;
        }""",
    """        .mid-list-total-block {
            padding: 1.1rem 1rem;
            text-align: center;
            background: #ffffff;
            border: none;
            border-radius: 0;
            margin: 1.1rem 0;
            box-shadow: none;
        }""",
)

PROD.write_text(html, encoding="utf-8")
print("updated", PROD)

# Sync August copy
aug = html
for a, b in [
    ('href="i18n.css"', 'href="../i18n.css"'),
    ('src="locales.bundle.js"', 'src="../locales.bundle.js"'),
    ('src="i18n.js"', 'src="../i18n.js"'),
    ('src="campaign-i18n.js"', 'src="../campaign-i18n.js"'),
    ('src="joylogo.jpg"', 'src="../joylogo.jpg"'),
]:
    aug = aug.replace(a, b)
AUG.write_text(aug, encoding="utf-8")
print("synced", AUG)

# campaign-i18n.js
ci = (ROOT / "campaign-i18n.js").read_text(encoding="utf-8")
ci = ci.replace(
    "setText('campaign-option-label', 'pricing.optionLabel', '8月オプション');\n    setText('campaign-option-label-sub', 'pricing.optionLabelSub', '無料オプション8つ自動契約');",
    "setText('campaign-option-label', 'pricing.optionLabel', '8月オプション8つが0円');",
)
(ROOT / "campaign-i18n.js").write_text(ci, encoding="utf-8")
print("updated campaign-i18n.js")

# locales
locale_updates = {
    "en": {
        "halfYearCatch": "Half-year fee discount",
        "halfYearPeriod": "Aug–Jan",
        "perMonthUnitTax": "(tax incl.)/mo",
        "optionLabel": "August: 8 options for ¥0",
        "item3": "All 8 free options are auto-enrolled at signup",
    },
    "ko": {
        "halfYearCatch": "반년 내내 회비 할인",
        "halfYearPeriod": "8월〜1월",
        "perMonthUnitTax": "(세금 포함)/월",
        "optionLabel": "8월 옵션 8개가 0원",
        "item3": "무료 옵션 8개는 입회 시 모두 자동 가입됩니다",
    },
    "zh-CN": {
        "halfYearCatch": "半年会费持续优惠",
        "halfYearPeriod": "8月〜1月",
        "perMonthUnitTax": "(含税)/月",
        "optionLabel": "8月8项选项0元",
        "item3": "8项免费选项在入会时全部自动签约",
    },
    "zh-TW": {
        "halfYearCatch": "半年會費持續優惠",
        "halfYearPeriod": "8月〜1月",
        "perMonthUnitTax": "(含稅)/月",
        "optionLabel": "8月8項選項0元",
        "item3": "8項免費選項在入會時全部自動簽約",
    },
}

for lang, upd in locale_updates.items():
    path = ROOT / "locales" / "campaign" / f"{lang}.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["hero"]["halfYearCatch"] = upd["halfYearCatch"]
    data["pricing"]["halfYearPeriod"] = upd["halfYearPeriod"]
    data["pricing"]["perMonthUnitTax"] = upd["perMonthUnitTax"]
    data["pricing"]["optionLabel"] = upd["optionLabel"]
    data["conditions"]["item3"] = upd["item3"]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("locale", lang)

subprocess.run(["python", str(ROOT / "build_locales.py")], check=True)
print("bundle rebuilt")
