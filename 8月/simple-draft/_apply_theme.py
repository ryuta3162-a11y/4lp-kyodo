# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(__file__).with_name("index.html")
html = p.read_text(encoding="utf-8")

replacements = [
    ('href="i18n.css"', 'href="../../i18n.css"'),
    ('src="locales.bundle.js"', 'src="../../locales.bundle.js"'),
    ('src="i18n.js"', 'src="../../i18n.js"'),
    ('src="campaign-i18n.js"', 'src="../../campaign-i18n.js"'),
    ('src="joylogo.jpg"', 'src="../../joylogo.jpg"'),
    (
        "JOYFIT24経堂 夏得キャンペーン｜8/16(日)まで",
        "【デザイン仮版】JOYFIT24経堂 夏得キャンペーン｜白黒赤シンプル",
    ),
]
for a, b in replacements:
    html = html.replace(a, b)

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
            /* ゴールド廃止 → 黒・白・赤のみ */
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

override = """
        /* =======================================================
           ■ デザイン仮版: 白 / 黒 / 濃い赤(#C21632) のみ
           本番 index.html には未反映。確認用クローン。
           ======================================================= */
        .ambient-bg,
        .bg-noise {
            display: none !important;
        }
        body {
            background-color: #ffffff !important;
            color: #111111 !important;
        }

        /* ヘッダー: 単色赤フラット */
        .campaign-header-enhanced {
            background: #C21632 !important;
            box-shadow: none !important;
            border-radius: 0 !important;
        }
        .campaign-header-enhanced::before,
        .campaign-header-enhanced::after {
            display: none !important;
        }
        .campaign-header-enhanced h2::after {
            background: #ffffff !important;
            box-shadow: none !important;
        }
        .campaign-title-summer {
            text-shadow: none !important;
        }
        .campaign-app-badge {
            background: #ffffff !important;
            color: #C21632 !important;
            border: 2px solid #ffffff !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border-radius: 4px !important;
        }
        .campaign-app-badge span {
            color: #C21632 !important;
        }

        /* 価格訴求ブロック: 白地に赤価格（イメージ準拠） */
        .price-item--half-year {
            color: #111111 !important;
            padding: 1.8rem 0.85rem 2rem !important;
            margin: 0.4rem 0 1rem !important;
        }
        .price-item--half-year::before {
            border: 2px solid #111111 !important;
            border-radius: 0 !important;
            background: #ffffff !important;
            box-shadow: none !important;
        }
        .price-item--half-year .perk-badge,
        .price-item--half-year .perk-badge.perk-badge-accent {
            background-color: #C21632 !important;
            color: #ffffff !important;
            border-radius: 4px !important;
            box-shadow: none !important;
        }
        .price-item--half-year .half-year-catch {
            color: #111111 !important;
            text-shadow: none !important;
            letter-spacing: 0.04em !important;
        }
        .price-item--half-year .half-year-price {
            color: #C21632 !important;
            font-size: clamp(3.2rem, 16vw, 4.4rem) !important;
            text-shadow: none !important;
            -webkit-text-stroke: 0 !important;
        }
        .price-item--half-year .half-year-unit {
            color: #C21632 !important;
            font-size: clamp(1.1rem, 4.5vw, 1.45rem) !important;
        }
        .half-year-months {
            color: #111111 !important;
            font-size: clamp(1rem, 4vw, 1.2rem) !important;
        }
        .half-year-period-note {
            color: #111111 !important;
            opacity: 0.75;
            white-space: normal !important;
        }

        .text-value-hero,
        .text-value-accent {
            color: #C21632 !important;
            -webkit-text-stroke: 0 !important;
            text-shadow: none !important;
        }

        /* ゴールド系ボタン・バッジ → 黒 or 赤 */
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
        .cta-emphasis {
            box-shadow: none !important;
        }

        /* 枠・カードをフラットに */
        .lp-framed,
        .digital-step-card,
        .condition-card,
        .option-card-3d {
            border-radius: 0 !important;
            box-shadow: none !important;
        }
        .lp-framed {
            border: 2px solid #111111 !important;
        }
        .lp-frame-badge {
            border-radius: 0 !important;
        }

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

        .lp-opening {
            background: #C21632 !important;
        }
        .lp-o-intro-box,
        .lp-opening-badge {
            color: #ffffff !important;
        }

        .simple-draft-banner {
            position: sticky;
            top: 0;
            z-index: 9999;
            background: #111111;
            color: #ffffff;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            padding: 8px 12px;
            text-align: center;
        }
        .simple-draft-banner a {
            color: #ffffff;
            text-decoration: underline;
            margin-left: 8px;
        }
"""

marker = "    </style>"
idx = html.find(marker)
if idx < 0:
    raise SystemExit("style close not found")
html = html[:idx] + override + "\n" + html[idx:]

bi = html.find("<body")
be = html.find(">", bi)
if bi < 0:
    raise SystemExit("body not found")
banner = (
    '\n    <div class="simple-draft-banner">'
    "デザイン仮版（白・黒・濃い赤）／本番未反映 "
    '<a href="../../index.html">本番LPへ戻る</a></div>\n'
)
html = html[: be + 1] + banner + html[be + 1 :]

html = html.replace(
    "<!-- キャンペーンLP本体: kyodo-lp-deta の index.html をここに貼り付け可（貼り替え後は i18n 用の追記を再適用） -->",
    "<!-- デザイン仮版クローン: 文面は本番と同じ。配色のみ白/黒/#C21632。本番反映前の確認用。 -->",
    1,
)

p.write_text(html, encoding="utf-8")
print("patched", p)
print("size", p.stat().st_size)
