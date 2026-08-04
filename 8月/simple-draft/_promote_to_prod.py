# -*- coding: utf-8 -*-
"""Apply simple white/black/red theme to production index.html and sync 8月 copy."""
from pathlib import Path
import shutil
import re

ROOT = Path(__file__).resolve().parents[2]
PROD = ROOT / "index.html"
AUG = ROOT / "8月" / "index.html"

html = PROD.read_text(encoding="utf-8")

old_root = """        :root { 
            --brand: #C21632;
            --brand-red: #C21632;
            --brand-dark: #8a0e20;
            --lp-frame: #1a1a1a;
            --lp-frame-shadow: 0 5px 0 #1a1a1a;
            --gold-main: #D4AF37; 
            --gold-light: #F8E71C; 
            --gold-dark: #B48811; 
            --gold-gradient: linear-gradient(135deg, #B48811 0%, #F8E71C 25%, #D4AF37 50%, #F8E71C 75%, #B48811 100%);
            --summer-sun: rgba(255, 196, 87, 0.22);
            --summer-sky: rgba(126, 200, 227, 0.07);
            
            --color-dark: #1a1a2e;
            --color-text: #2C2C2C;
            --bg-body: #fffdf0; /* 全体の背景色を統一して明るく */
            --radius-lg: 20px;
            --radius-md: 12px;
            --shadow-soft: 0 12px 40px rgba(0, 0, 0, 0.06);
            
            --container-max-width: 600px;
        }"""

new_root = """        :root { 
            --brand: #C21632;
            --brand-red: #C21632;
            --brand-dark: #C21632;
            --lp-frame: #111111;
            --lp-frame-shadow: 0 4px 0 #111111;
            /* シンプル配色: 白 / 黒 / 濃い赤のみ（ゴールド廃止） */
            --gold-main: #111111; 
            --gold-light: #ffffff; 
            --gold-dark: #111111; 
            --gold-gradient: #111111;
            --summer-sun: transparent;
            --summer-sky: transparent;
            
            --color-dark: #111111;
            --color-text: #111111;
            --bg-body: #ffffff;
            --radius-lg: 12px;
            --radius-md: 8px;
            --shadow-soft: 0 8px 24px rgba(0, 0, 0, 0.06);
            
            --container-max-width: 600px;
        }"""

if old_root not in html:
    raise SystemExit("root block not found")
html = html.replace(old_root, new_root)

# Replace mid-list-total-block and monthly-fee base styles with simple theme
old_mid = """        .mid-list-total-block {
            padding: 1.75rem 1.25rem;
            text-align: center;
            background: var(--brand-red);
            border: 1px solid rgba(255, 255, 255, 0.22);
            border-radius: var(--radius-md);
            margin: 1.5rem 0;
            box-shadow: 0 4px 16px rgba(194, 22, 50, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }
        .mid-list-total-block .label {
            font-size: 1.12rem;
            font-weight: 900;
            margin-bottom: 0.65rem;
            color: #fff;
            letter-spacing: 0.06em;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        .mid-list-total-block .label i {
            font-size: 1.25rem;
            vertical-align: -0.12em;
            margin-right: 2px;
        }
        .mid-list-total-block .total-price-row {
            display: flex;
            align-items: baseline;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.15rem 0.35rem;
        }
        .mid-list-total-block .price-large,
        .mid-list-total-block .text-value-accent,
        .mid-list-total-block .featured-price {
            font-size: 2.9rem !important;
            font-weight: 900;
            color: #fff !important;
            line-height: 1;
            text-shadow: 0 2px 6px rgba(0, 0, 0, 0.22);
        }
        .mid-list-total-block .unit-large {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1.15rem;
            font-weight: 900;
            color: #fff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
        }
        .mid-list-total-block .join-date {
            color: #fff !important;
            font-weight: 900;
        }
        .mid-list-total-block .total-prorate-note {
            margin: 0.55rem 0 0;
            font-size: 0.72rem;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.88);
            letter-spacing: 0.02em;
            line-height: 1.45;
        }
        .monthly-fee {
            padding: 1.5rem 1.25rem;
            text-align: center;
            background: linear-gradient(180deg, #fafafa 0%, #fff5f6 100%);
            border-top: 2px solid rgba(194, 22, 50, 0.12);
        }
        .monthly-fee-label {
            font-size: 0.88rem;
            font-weight: 800;
            color: var(--brand);
            margin-bottom: 0.55rem;
            letter-spacing: 0.04em;
        }
        .monthly-fee-row {
            display: flex;
            align-items: baseline;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.25rem 0.5rem;
        }
        .monthly-fee .price-large {
            font-size: 1.65rem;
            font-weight: 900;
            color: #333;
        }
        .monthly-fee .unit-large {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1rem;
            font-weight: 800;
        }
        .monthly-fee-plus {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 1.15rem;
            font-weight: 900;
            color: var(--brand);
            margin: 0 0.15rem;
        }
        .monthly-fee-option {
            font-weight: 800;
            font-size: 0.95rem;
            color: #444;
        }"""

new_mid = """        .mid-list-total-block {
            padding: 1.1rem 1rem;
            text-align: center;
            background: #ffffff;
            border: 2px solid #111111;
            border-radius: 0;
            margin: 1.1rem 0;
            box-shadow: none;
        }
        .mid-list-total-block .label {
            font-size: 0.95rem;
            font-weight: 900;
            margin-bottom: 0.4rem;
            color: #111111;
            letter-spacing: 0.02em;
            text-shadow: none;
        }
        .mid-list-total-block .label i {
            font-size: 1.05rem;
            vertical-align: -0.12em;
            margin-right: 2px;
        }
        .mid-list-total-block .total-price-row {
            display: flex;
            align-items: baseline;
            justify-content: center;
            flex-wrap: wrap;
            gap: 0.15rem 0.35rem;
        }
        .mid-list-total-block .price-large,
        .mid-list-total-block .text-value-accent,
        .mid-list-total-block .featured-price {
            font-size: 2.35rem !important;
            font-weight: 900;
            color: #C21632 !important;
            line-height: 1;
            text-shadow: none;
        }
        .mid-list-total-block .unit-large {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 0.95rem;
            font-weight: 800;
            color: #111111;
            text-shadow: none;
        }
        .mid-list-total-block .join-date {
            color: #111111 !important;
            font-weight: 900;
        }
        .mid-list-total-block .total-prorate-note {
            margin: 0.55rem 0 0;
            font-size: 0.68rem;
            font-weight: 600;
            color: #111111;
            opacity: 0.75;
            letter-spacing: 0.02em;
            line-height: 1.45;
        }
        .monthly-fee {
            padding: 0.85rem 1rem 1.1rem;
            text-align: center;
            background: #ffffff;
            border-top: 1px solid #111111;
        }
        .monthly-fee-simple {
            margin: 0;
            font-size: 0.82rem;
            font-weight: 700;
            color: #111111;
            letter-spacing: 0.02em;
            line-height: 1.5;
        }
        .monthly-fee-amount {
            margin-left: 0.35em;
            font-size: 1.05rem;
            font-weight: 900;
            color: #C21632;
        }
        .monthly-fee-unit {
            font-size: 0.78rem;
            font-weight: 700;
            color: #111111;
        }"""

if old_mid not in html:
    raise SystemExit("mid-list / monthly-fee block not found")
html = html.replace(old_mid, new_mid)

# half-year price block → white card with red price
old_half = """        .price-item--half-year {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            gap: 1.05rem;
            grid-template-columns: none;
            min-height: 0;
            margin: 0.55rem 0 0.9rem;
            padding: 1.55rem 0.85rem 1.7rem;
            border: none;
            border-radius: 0;
            border-bottom: none;
            background: transparent;
            box-shadow: none;
            color: #fff;
        }
        .price-item--half-year::before {
            content: '';
            position: absolute;
            inset: 0;
            z-index: 0;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background:
                radial-gradient(ellipse 85% 70% at 50% -10%, rgba(255, 255, 255, 0.18), transparent 55%),
                linear-gradient(165deg, #e02542 0%, var(--brand-red) 42%, #9e1026 100%);
            box-shadow:
                0 1px 0 rgba(255, 255, 255, 0.22) inset,
                0 14px 36px rgba(194, 22, 50, 0.28);
        }"""

new_half = """        .price-item--half-year {
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
        }"""

if old_half not in html:
    raise SystemExit("half-year block not found")
html = html.replace(old_half, new_half)

replacements_css = [
    (
        """        .price-item--half-year .perk-badge,
        .price-item--half-year .perk-badge.perk-badge-accent {
            margin-top: 0;
            background-color: #fff !important;
            color: var(--brand-red) !important;
            border: none;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
        }
        .price-item--half-year .half-year-catch {
            margin: 0;
            font-size: clamp(1.08rem, 4.3vw, 1.32rem);
            font-weight: 900;
            letter-spacing: 0.06em;
            color: #fff;
            line-height: 1.3;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
        }""",
        """        .price-item--half-year .perk-badge,
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
        }""",
    ),
    (
        """        .price-item--half-year .half-year-price {
            display: inline;
            font-size: clamp(2.55rem, 12.5vw, 3.35rem);
            font-weight: 900;
            letter-spacing: -0.03em;
            line-height: 1;
            color: #fff;
            text-shadow: 0 2px 14px rgba(0, 0, 0, 0.18);
        }
        .price-item--half-year .half-year-unit {
            display: inline;
            margin: 0;
            font-size: clamp(0.92rem, 3.6vw, 1.12rem);
            font-weight: 800;
            color: #fff;
            letter-spacing: 0.02em;
            white-space: nowrap;
        }
        .half-year-months {
            margin: 0.15rem 0 0;
            width: 100%;
            font-size: clamp(0.9rem, 3.5vw, 1.05rem);
            font-weight: 900;
            line-height: 1.5;
            letter-spacing: 0.03em;
            color: #fff;
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
            color: rgba(255, 255, 255, 0.82);
            white-space: nowrap;
        }""",
        """        .price-item--half-year .half-year-price {
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
        }""",
    ),
]

for a, b in replacements_css:
    if a not in html:
        raise SystemExit("css chunk missing")
    html = html.replace(a, b)

# Header flat red
old_header = """        .campaign-header-enhanced {
            position: relative;
            margin-top: 10px;
            padding: 2.1rem 1.25rem 1.85rem;
            border-radius: 14px 14px 0 0;
            text-align: center;
            overflow: hidden;
            background:
                radial-gradient(ellipse 90% 70% at 50% -20%, rgba(255, 220, 140, 0.28), transparent 55%),
                linear-gradient(180deg, #d41f3c 0%, var(--brand-red) 48%, #a81228 100%);
            border-bottom: none;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.18);
        }"""

new_header = """        .campaign-header-enhanced {
            position: relative;
            margin-top: 10px;
            padding: 2.1rem 1.25rem 1.85rem;
            border-radius: 0;
            text-align: center;
            overflow: hidden;
            background: #C21632;
            border-bottom: none;
            box-shadow: none;
        }"""

if old_header not in html:
    raise SystemExit("header block not found")
html = html.replace(old_header, new_header)

# Insert production theme overrides before </style>
theme = """
        /* =======================================================
           ■ シンプル配色（白 / 黒 / 濃い赤 #C21632）
           ======================================================= */
        .ambient-bg,
        .bg-noise { display: none !important; }

        .campaign-header-enhanced::before,
        .campaign-header-enhanced::after { display: none !important; }
        .campaign-header-enhanced h2::after {
            background: #ffffff !important;
            box-shadow: none !important;
        }
        .campaign-title-summer { text-shadow: none !important; }
        .campaign-app-badge {
            background: #ffffff !important;
            color: #C21632 !important;
            border: 2px solid #ffffff !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border-radius: 4px !important;
        }
        .campaign-app-badge span { color: #C21632 !important; }

        .text-value-hero,
        .text-value-accent {
            color: #C21632 !important;
            -webkit-text-stroke: 0 !important;
            text-shadow: none !important;
        }

        .btn-gold-flat,
        .lp-frame-badge--gold,
        .step-badge.gold {
            background: #111111 !important;
            color: #ffffff !important;
            border-color: #111111 !important;
        }
        .btn-red-flat,
        .lp-frame-badge--brand,
        .step-badge.red {
            background: #C21632 !important;
            color: #ffffff !important;
        }
        .cta-emphasis { box-shadow: none !important; }

        .lp-framed,
        .digital-step-card,
        .condition-card,
        .option-card-3d {
            border-radius: 0 !important;
            box-shadow: none !important;
        }
        .lp-framed { border: 2px solid #111111 !important; }
        .lp-frame-badge { border-radius: 0 !important; }

        .campaign-price-chip {
            border-radius: 4px !important;
            background: #ffffff !important;
            color: #C21632 !important;
            border: 2px solid #C21632 !important;
        }

        .fixed-banner .banner-btn.trial {
            background: #111111 !important;
            color: #ffffff !important;
        }
        .fixed-banner .banner-btn.app {
            background: #C21632 !important;
            color: #ffffff !important;
        }

        .lp-opening { background: #C21632 !important; }
        .lp-o-intro-box,
        .lp-opening-badge { color: #ffffff !important; }

"""

marker = "    </style>"
idx = html.find(marker)
if idx < 0:
    raise SystemExit("style close not found")
if "シンプル配色（白 / 黒 / 濃い赤" not in html:
    html = html[:idx] + theme + "\n" + html[idx:]

old_fee_html = """                 <!-- 2027年2月以降 -->
                <div class="monthly-fee">
                    <div class="monthly-fee-label" data-i18n="pricing.afterFeb2027">2027年2月以降の通常月額</div>
                    <div class="monthly-fee-row">
                        <span class="price-large font-impact">9,350<span class="unit-large" data-i18n="pricing.yenTaxIncl">円(税込)</span></span>
                        <span class="monthly-fee-plus">+</span>
                        <span class="monthly-fee-option" data-i18n="pricing.optionFees">オプション料金</span>
                    </div>
                </div>"""

new_fee_html = """                 <!-- 2027年2月以降 -->
                <div class="monthly-fee">
                    <p class="monthly-fee-simple">
                        <span data-i18n="pricing.afterFeb2027">2027年2月以降通常月額</span>
                        <strong class="monthly-fee-amount">9,350</strong><span class="monthly-fee-unit" data-i18n="pricing.yenTaxIncl">円(税込)</span>
                    </p>
                </div>"""

if old_fee_html not in html:
    raise SystemExit("monthly fee html not found")
html = html.replace(old_fee_html, new_fee_html)

PROD.write_text(html, encoding="utf-8")
print("updated", PROD)

# Sync August archive copy with relative asset paths
aug = html
aug = aug.replace('href="i18n.css"', 'href="../i18n.css"')
aug = aug.replace('src="locales.bundle.js"', 'src="../locales.bundle.js"')
aug = aug.replace('src="i18n.js"', 'src="../i18n.js"')
aug = aug.replace('src="campaign-i18n.js"', 'src="../campaign-i18n.js"')
aug = aug.replace('src="joylogo.jpg"', 'src="../joylogo.jpg"')
AUG.write_text(aug, encoding="utf-8")
print("synced", AUG)
