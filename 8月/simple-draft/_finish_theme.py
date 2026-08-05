# -*- coding: utf-8 -*-
"""Finish simple theme: banners, CTAs, dividers, flatten radii."""
from pathlib import Path

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")
PROD = ROOT / "index.html"
html = PROD.read_text(encoding="utf-8")

replacements = [
    # Fixed bottom banner
    (
        """        .fixed-banner {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            display: flex;
            gap: 12px;
            padding: 14px 16px calc(14px + env(safe-area-inset-bottom, 0px));
            max-width: 100%;
            margin: 0 auto;
            background: linear-gradient(180deg, rgba(255, 253, 248, 0.96) 0%, rgba(255, 255, 255, 0.9) 55%, rgba(255, 250, 240, 0.94) 100%);
            backdrop-filter: blur(16px) saturate(1.15);
            -webkit-backdrop-filter: blur(16px) saturate(1.15);
            border-top: 1px solid rgba(212, 175, 55, 0.55);
            box-shadow: 0 -10px 36px rgba(26, 26, 46, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.75);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .fixed-banner .banner-btn {
            flex: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 12px;
            font-weight: 900;
            font-size: 0.88rem;
            letter-spacing: 0.03em;
            border-radius: 9999px;
            text-decoration: none;
            border: 1px solid rgba(255, 255, 255, 0.35);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12), inset 0 1px 0 rgba(255, 255, 255, 0.35);
            transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.2s ease;
        }
        .fixed-banner .banner-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16), inset 0 1px 0 rgba(255, 255, 255, 0.45);
            filter: brightness(1.04);
        }
        .fixed-banner .banner-btn i { font-size: 1.15rem; flex-shrink: 0; }
        /* 見学：ゴールド系で「特別感」／APP：ブランド赤の深みグラデ */
        .fixed-banner .trial {
            background: linear-gradient(155deg, #fdf6d5 0%, #e8c547 38%, #c9a227 72%, #8a6b1a 100%);
            color: #1a1100;
            text-shadow: 0 1px 0 rgba(255, 255, 255, 0.45);
            border-color: rgba(255, 255, 255, 0.65);
        }
        .fixed-banner .app {
            background: var(--brand-red);
            color: #fff;
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 255, 255, 0.22);
        }""",
        """        .fixed-banner {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            display: flex;
            gap: 10px;
            padding: 12px 14px calc(12px + env(safe-area-inset-bottom, 0px));
            max-width: 100%;
            margin: 0 auto;
            background: #ffffff;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            border-top: 2px solid #111111;
            box-shadow: none;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .fixed-banner .banner-btn {
            flex: 1;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            padding: 14px 12px;
            font-weight: 900;
            font-size: 0.88rem;
            letter-spacing: 0.03em;
            border-radius: 0;
            text-decoration: none;
            border: none;
            box-shadow: none;
            transition: filter 0.2s ease;
        }
        .fixed-banner .banner-btn:hover {
            transform: none;
            box-shadow: none;
            filter: brightness(1.06);
        }
        .fixed-banner .banner-btn i { font-size: 1.15rem; flex-shrink: 0; }
        .fixed-banner .trial {
            background: #111111;
            color: #ffffff;
            text-shadow: none;
            border-color: #111111;
        }
        .fixed-banner .app {
            background: #C21632;
            color: #fff;
            text-shadow: none;
            border-color: #C21632;
        }""",
    ),
    # Video CTA yellow → black
    (
        """        .cta-button-video { display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(45deg, #ffea00, #ffd600); color: #333; font-weight: 900; padding: 12px 25px; border-radius: 50px; text-decoration: none; margin-top: 25px; transition: 0.3s; font-size: 0.9rem; }""",
        """        .cta-button-video { display: inline-flex; align-items: center; gap: 8px; background: #111111; color: #ffffff; font-weight: 900; padding: 14px 28px; border-radius: 0; text-decoration: none; margin-top: 25px; transition: filter 0.2s; font-size: 0.95rem; }""",
    ),
    # Top banner → black
    (
        """        /* =======================================================
           ■ トップ固定バナー（既定カラー：赤・ゴールド・白）
           ======================================================= */
        .gold-metallic-banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            background: var(--brand-red);
            color: #fff;
            padding: 10px 14px;
            box-shadow: 0 3px 16px rgba(194, 22, 50, 0.35);
            border-bottom: 2px solid rgba(255, 255, 255, 0.4);
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }""",
        """        /* =======================================================
           ■ トップ固定バナー（黒帯・赤数字）
           ======================================================= */
        .gold-metallic-banner {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            background: #111111;
            color: #fff;
            padding: 10px 14px;
            box-shadow: none;
            border-bottom: none;
            transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }""",
    ),
    (
        """        .banner-capacity-pill .banner-capacity-num {
            display: inline-block;
            margin: 0 0.12em;
            font-size: 1.05em;
            font-weight: 900;
            color: #F8E71C;
        }""",
        """        .banner-capacity-pill .banner-capacity-num {
            display: inline-block;
            margin: 0 0.12em;
            font-size: 1.05em;
            font-weight: 900;
            color: #C21632;
        }""",
    ),
    (
        """        .banner-capacity-pill {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(0, 0, 0, 0.18);
            border: 1px solid rgba(255, 255, 255, 0.28);
            white-space: nowrap;
        }""",
        """        .banner-capacity-pill {
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.06em;
            padding: 5px 10px;
            border-radius: 0;
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.35);
            white-space: nowrap;
        }""",
    ),
    (
        """        .banner-remaining-block {
            display: flex;
            align-items: center;
            gap: 6px;
            background: #fff;
            color: var(--color-text);
            padding: 5px 12px 5px 10px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
            min-width: 88px;
        }""",
        """        .banner-remaining-block {
            display: flex;
            align-items: center;
            gap: 6px;
            background: #ffffff;
            color: #111111;
            padding: 5px 12px 5px 10px;
            border-radius: 0;
            box-shadow: none;
            border: none;
            min-width: 88px;
        }""",
    ),
    # Dividers #eee → thin black / white context
    ("border: 1px solid #eee;", "border: 1px solid #111111;"),
    ("border-top: 1px solid #eee;", "border-top: 1px solid #111111;"),
    ("border-bottom: 1px solid #eee;", "border-bottom: 1px solid #111111;"),
    ("border-top: 1px solid #eee; border-bottom: 1px solid #eee;", "border-top: 1px solid #111111; border-bottom: 1px solid #111111;"),
    # pink chip
    ("background: #fff0f0;", "background: #ffffff;"),
    # step buttons / badges flatten
    (
        """        .step-action-btn { display: inline-flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 900; padding: 10px 15px; border-radius: 8px; text-decoration: none; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        .btn-gold-flat { background: var(--gold-gradient); color: #3e2723; border: 1px solid #d4af37; }""",
        """        .step-action-btn { display: inline-flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 900; padding: 12px 18px; border-radius: 0; text-decoration: none; box-shadow: none; }
        .btn-gold-flat { background: #111111; color: #ffffff; border: 1px solid #111111; }""",
    ),
    (
        """        .notice-warning-v22 { display: block; font-size: 0.8rem; font-weight: 900; color: #fff; background: var(--brand-red); padding: 15px; border-radius: 8px; margin-top: 20px; }""",
        """        .notice-warning-v22 { display: block; font-size: 0.85rem; font-weight: 900; color: #fff; background: var(--brand-red); padding: 15px; border-radius: 0; margin-top: 20px; }""",
    ),
    (
        """            border-radius: 999px;
            background: rgba(255, 255, 255, 0.12);
            color: #fff;
            font-size: 0.82rem;""",
        """            border-radius: 0;
            background: rgba(255, 255, 255, 0.12);
            color: #fff;
            font-size: 0.82rem;""",
    ),
    (
        """        .lp-frame-badge,
        .step-badge {
            position: absolute;
            top: -14px;
            left: 50%;
            transform: translateX(-50%);
            display: inline-block;
            font-size: 0.72rem;
            font-weight: 900;
            letter-spacing: 0.1em;
            padding: 7px 18px;
            border-radius: 999px;
            border: 2px solid var(--lp-frame);
            margin: 0;
            white-space: nowrap;
            box-shadow: 0 3px 0 rgba(0, 0, 0, 0.12);
            z-index: 2;
        }""",
        """        .lp-frame-badge,
        .step-badge {
            position: absolute;
            top: -14px;
            left: 50%;
            transform: translateX(-50%);
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 900;
            letter-spacing: 0.1em;
            padding: 7px 18px;
            border-radius: 0;
            border: none;
            margin: 0;
            white-space: nowrap;
            box-shadow: none;
            z-index: 2;
        }""",
    ),
    (
        """        .options-unified-inner {
            border-radius: 16px;
            overflow: hidden;
        }""",
        """        .options-unified-inner {
            border-radius: 0;
            overflow: hidden;
        }""",
    ),
    (
        """        .access-section {
            background: #fff;
            border-radius: 16px;
            overflow: hidden;
        }""",
        """        .access-section {
            background: #fff;
            border-radius: 0;
            overflow: hidden;
        }""",
    ),
    (
        """        .card-badge { position: absolute; top: 1rem; left: 1rem; padding: 0.4rem 0.8rem; font-weight: 900; font-size: 0.75rem; border-radius: 6px; }""",
        """        .card-badge { position: absolute; top: 1rem; left: 1rem; padding: 0.4rem 0.8rem; font-weight: 900; font-size: 0.75rem; border-radius: 0; }""",
    ),
    (
        """        .facilities-grid img {
            width: 45px;
            margin: 0 auto 10px;
            border-radius: 6px;
            object-fit: cover;
            filter: saturate(0.94) contrast(1.04) brightness(1.02);
        }""",
        """        .facilities-grid img {
            width: 45px;
            margin: 0 auto 10px;
            border-radius: 0;
            object-fit: cover;
            filter: none;
        }""",
    ),
    (
        'style="width: 100%; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);"',
        'style="width: 100%; border-radius: 0; box-shadow: none;"',
    ),
    (
        'style="padding: 25px; background: #fff; border-top: 1px solid #eee; border-bottom: 1px solid #eee;"',
        'style="padding: 25px; background: #fff; border-top: 1px solid #111111; border-bottom: 1px solid #111111;"',
    ),
    # campaign-price-chip
    (
        """.campaign-price-chip { display: inline-block; margin-top: 8px; background: #fff; color: var(--brand); border: 2px solid var(--brand); border-radius: 999px; padding: 3px 12px; font-size: 0.78rem; font-weight: 900; letter-spacing: 0.01em; }""",
        """.campaign-price-chip { display: inline-block; margin-top: 8px; background: #fff; color: var(--brand); border: 2px solid var(--brand); border-radius: 0; padding: 3px 12px; font-size: 0.78rem; font-weight: 900; letter-spacing: 0.01em; }""",
    ),
    (
        """        .price-item .perk-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 0;
            height: 1.7rem;
            padding: 0 0.55rem;
            border-radius: 6px;""",
        """        .price-item .perk-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-width: 0;
            height: 1.7rem;
            padding: 0 0.55rem;
            border-radius: 0;""",
    ),
    # plan container radius
    (
        """            border-radius: 0 0 var(--radius-lg) var(--radius-lg);""",
        """            border-radius: 0;""",
    ),
]

for a, b in replacements:
    if a not in html:
        print("MISSING:", a[:80].replace("\n", " "))
    else:
        html = html.replace(a, b)
        print("ok:", a[:50].replace("\n", " "))

# Strengthen / refresh simple theme overrides for banners
old_override_tail = """        .fixed-banner .banner-btn.trial {
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


    </style>"""

new_override_tail = """        .fixed-banner .banner-btn.trial {
            background: #111111 !important;
            color: #ffffff !important;
        }
        .fixed-banner .banner-btn.app {
            background: #C21632 !important;
            color: #ffffff !important;
        }

        .gold-metallic-banner {
            background: #111111 !important;
            box-shadow: none !important;
            border-bottom: none !important;
        }
        .banner-capacity-pill .banner-capacity-num {
            color: #C21632 !important;
        }
        .cta-button-video {
            background: #111111 !important;
            color: #ffffff !important;
            border-radius: 0 !important;
        }
        .step-action-btn,
        .btn-gold-flat,
        .btn-red-flat,
        .access-map-btn,
        .notice-warning-v22,
        .banner-capacity-pill,
        .banner-remaining-block,
        .campaign-app-badge,
        .perk-badge,
        .card-badge {
            border-radius: 0 !important;
        }

        .lp-opening {
            background: #C21632 !important;
        }
        .lp-opening::before {
            display: none !important;
        }
        .lp-o-intro-box,
        .lp-opening-badge { color: #ffffff !important; }


    </style>"""

if old_override_tail not in html:
    raise SystemExit("override tail not found")
html = html.replace(old_override_tail, new_override_tail)

PROD.write_text(html, encoding="utf-8")
print("wrote prod")

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
print("synced aug")
