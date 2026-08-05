# -*- coding: utf-8 -*-
"""Typography system + gray cafe-menu polish."""
from pathlib import Path

ROOT = Path(r"C:\Users\ryuta-kusaka\Documents\GitHub\kyodo-lp-deta")
PROD = ROOT / "index.html"
html = PROD.read_text(encoding="utf-8")

# --- :root gray + type tokens ---
old_root = """        :root { 
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

new_root = """        :root { 
            --brand: #C21632;
            --brand-red: #C21632;
            --brand-dark: #C21632;
            --lp-frame: #111111;
            --lp-frame-shadow: none;
            /* 白 / 黒 / グレー / 濃い赤 */
            --gold-main: #111111; 
            --gold-light: #ffffff; 
            --gold-dark: #111111; 
            --gold-gradient: #111111;
            --summer-sun: transparent;
            --summer-sky: transparent;
            --gray-50: #f7f7f7;
            --gray-100: #efefef;
            --gray-200: #e4e4e4;
            --gray-500: #777777;
            --gray-700: #444444;
            
            --color-dark: #111111;
            --color-text: #111111;
            --bg-body: #ffffff;
            --radius-lg: 0;
            --radius-md: 0;
            --shadow-soft: none;

            /* 文字サイズ体系 */
            --text-body: 1rem;       /* 説明・ラベル共通 */
            --text-body-sm: 0.95rem;
            --text-note: 0.78rem;    /* ※・注意事項 */
            --num-hero: clamp(3.8rem, 18vw, 5.2rem); /* 3,740 */
            --num-sub: 2rem;         /* ご入会時金額 */
            --num-mini: 1.15rem;     /* 通常月額など */
            
            --container-max-width: 600px;
        }"""

if old_root not in html:
    raise SystemExit("root not found")
html = html.replace(old_root, new_root)

# --- Soft integrated header ---
old_header = """        /* 見出し（赤背景・タイポ中心） */
        .campaign-header-enhanced {
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

new_header = """        /* 見出し（控えめ・本文と一体化） */
        .campaign-header-enhanced {
            position: relative;
            margin-top: 0;
            padding: 1.35rem 1.25rem 1.1rem;
            border-radius: 0;
            text-align: center;
            overflow: hidden;
            background: #ffffff;
            border-bottom: 1px solid var(--gray-200);
            box-shadow: none;
        }"""

if old_header not in html:
    raise SystemExit("header not found")
html = html.replace(old_header, new_header)

html = html.replace(
    """        .campaign-header-enhanced h2 {
            margin: 0;
            font-size: clamp(1.7rem, 7vw, 2.15rem);
            font-weight: 900;
            color: #fff;
            letter-spacing: 0.14em;
            text-indent: 0.14em;
            line-height: 1.25;
        }""",
    """        .campaign-header-enhanced h2 {
            margin: 0;
            font-size: clamp(1.15rem, 4.5vw, 1.35rem);
            font-weight: 900;
            color: #111111;
            letter-spacing: 0.12em;
            text-indent: 0.12em;
            line-height: 1.3;
        }""",
)

html = html.replace(
    """        .campaign-title-summer {
            display: inline;
            padding: 0;
            background: none;
            color: #fff;
            -webkit-text-fill-color: #fff;
            border-radius: 0;
            box-shadow: none;
            filter: none;
            text-shadow: 0 2px 18px rgba(0, 0, 0, 0.18);
        }
        .campaign-app-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-top: 0;
            padding: 0.55rem 1.05rem;
            border-radius: 0;
            background: rgba(255, 255, 255, 0.12);
            color: #fff;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            border: 1px solid rgba(255, 255, 255, 0.38);
            box-shadow: none;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            max-width: calc(100% - 24px);
        }
        .campaign-app-badge span {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: #fff;
        }
        @media (min-width: 400px) {
            .campaign-header-enhanced h2 { font-size: 2rem; }
            .campaign-app-badge { font-size: 0.88rem; padding: 0.55rem 1.15rem; }
        }""",
    """        .campaign-title-summer {
            display: inline;
            padding: 0;
            background: none;
            color: #111111;
            -webkit-text-fill-color: #111111;
            border-radius: 0;
            box-shadow: none;
            filter: none;
            text-shadow: none;
        }
        .campaign-app-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            margin-top: 0;
            padding: 0.4rem 0.85rem;
            border-radius: 0;
            background: var(--gray-50);
            color: var(--gray-700);
            font-size: var(--text-note);
            font-weight: 700;
            letter-spacing: 0.04em;
            border: 1px solid var(--gray-200);
            box-shadow: none;
            backdrop-filter: none;
            -webkit-backdrop-filter: none;
            max-width: calc(100% - 24px);
        }
        .campaign-app-badge span {
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: var(--gray-700);
        }
        @media (min-width: 400px) {
            .campaign-header-enhanced h2 { font-size: 1.35rem; }
            .campaign-app-badge { font-size: 0.82rem; padding: 0.45rem 0.95rem; }
        }""",
)

# plan container: seamless with header
html = html.replace(
    """        .plan-container-wrapper {
            overflow: hidden;
            border-radius: 0;
            background-color: #fff;
            box-shadow: var(--shadow-soft);
            padding-top: 15px;
            padding-bottom: 30px;
            border: 2px solid var(--lp-frame);
            border-top: none;
            box-shadow: var(--lp-frame-shadow);
        }
        .price-showcase {
            border-radius: var(--radius-md);
            max-width: 100%;
            margin: 0 auto;
            text-align: left;
            border: 1px solid #111111;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        }""",
    """        .plan-container-wrapper {
            overflow: hidden;
            border-radius: 0;
            background-color: #fff;
            box-shadow: none;
            padding-top: 8px;
            padding-bottom: 24px;
            border: none;
        }
        .price-showcase {
            border-radius: 0;
            max-width: 100%;
            margin: 0 auto;
            text-align: left;
            border: none;
            box-shadow: none;
            background: #ffffff;
        }""",
)

# Typography for price blocks
old_type = """        .price-item--half-year .half-year-catch {
            margin: 0;
            order: 1;
            font-size: clamp(1.28rem, 5.2vw, 1.6rem);
            font-weight: 900;
            letter-spacing: 0.08em;
            color: #111111;
            line-height: 1.25;
            text-shadow: none;
        }
        .half-year-period {
            margin: 0 0 0.4rem;
            order: 2;
            font-size: clamp(1.1rem, 4.4vw, 1.35rem);
            font-weight: 800;
            letter-spacing: 0.12em;
            color: #111111;
            line-height: 1.3;
        }"""

new_type = """        .price-item--half-year .half-year-catch {
            margin: 0;
            order: 1;
            font-size: var(--text-body);
            font-weight: 800;
            letter-spacing: 0.06em;
            color: #111111;
            line-height: 1.4;
            text-shadow: none;
        }
        .half-year-period {
            margin: 0 0 0.55rem;
            order: 2;
            font-size: var(--text-body);
            font-weight: 700;
            letter-spacing: 0.1em;
            color: var(--gray-700);
            line-height: 1.4;
        }"""

if old_type not in html:
    raise SystemExit("half type not found")
html = html.replace(old_type, new_type)

html = html.replace(
    """        .price-item--half-year .half-year-price {
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
            margin: 0.2rem 0 0;
            font-size: clamp(1.05rem, 4vw, 1.28rem);
            font-weight: 800;
            color: #111111;
            letter-spacing: 0.04em;
            white-space: nowrap;
        }
        .price-item--option-simple {
            display: block;
            grid-template-columns: none;
            min-height: 0;
            padding: 0.95rem 0.5rem 1.1rem;
            border-bottom: none;
            text-align: center;
        }
        .option-simple-line {
            margin: 0;
            font-size: clamp(1.12rem, 4.4vw, 1.35rem);
            font-weight: 900;
            color: #111111;
            letter-spacing: 0.04em;
            line-height: 1.4;
        }""",
    """        .price-item--half-year .half-year-price {
            display: inline;
            font-size: var(--num-hero);
            font-weight: 900;
            letter-spacing: -0.04em;
            line-height: 0.95;
            color: #C21632;
            text-shadow: none;
            -webkit-text-stroke: 0;
        }
        .price-item--half-year .half-year-yen {
            display: inline;
            font-size: clamp(1.35rem, 5.5vw, 1.85rem);
            font-weight: 900;
            color: #C21632;
            letter-spacing: 0;
            line-height: 1;
            margin-left: 0.05em;
        }
        .price-item--half-year .half-year-unit {
            display: block;
            order: 4;
            margin: 0.25rem 0 0;
            font-size: var(--text-body);
            font-weight: 700;
            color: var(--gray-700);
            letter-spacing: 0.04em;
            white-space: nowrap;
        }
        .price-item--option-simple {
            display: block;
            grid-template-columns: none;
            min-height: 0;
            padding: 1rem 0.75rem;
            margin: 0 0.15rem 0.35rem;
            border-bottom: none;
            text-align: center;
            background: var(--gray-50);
        }
        .option-simple-line {
            margin: 0;
            font-size: var(--text-body);
            font-weight: 800;
            color: #111111;
            letter-spacing: 0.04em;
            line-height: 1.45;
        }""",
)

# mid-list + monthly + conditions type
html = html.replace(
    """        .mid-list-total-block {
            padding: 1.1rem 1rem;
            text-align: center;
            background: #ffffff;
            border: none;
            border-radius: 0;
            margin: 1.1rem 0;
            box-shadow: none;
        }
        .mid-list-total-block .label {
            font-size: 1.05rem;
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
            font-size: 1.05rem;
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
            font-size: 0.8rem;
            font-weight: 600;
            color: #111111;
            opacity: 0.8;
            letter-spacing: 0.02em;
            line-height: 1.45;
        }
        .monthly-fee {
            padding: 0.95rem 1rem 1.15rem;
            text-align: center;
            background: #ffffff;
            border-top: 1px solid #111111;
        }
        .monthly-fee-simple {
            margin: 0;
            font-size: 0.95rem;
            font-weight: 700;
            color: #111111;
            letter-spacing: 0.02em;
            line-height: 1.5;
        }
        .monthly-fee-amount {
            margin-left: 0.35em;
            font-size: 1.2rem;
            font-weight: 900;
            color: #C21632;
        }
        .monthly-fee-unit {
            font-size: 0.9rem;
            font-weight: 700;
            color: #111111;
        }
        
        .condition-list-content { padding: 8px 6px 4px; }
        .condition-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; text-align: left; font-size: 0.92rem; font-weight: 700; }""",
    """        .mid-list-total-block {
            padding: 1.25rem 1rem;
            text-align: center;
            background: var(--gray-50);
            border: none;
            border-radius: 0;
            margin: 0.75rem 0.15rem;
            box-shadow: none;
        }
        .mid-list-total-block .label {
            font-size: var(--text-body);
            font-weight: 800;
            margin-bottom: 0.35rem;
            color: #111111;
            letter-spacing: 0.02em;
            text-shadow: none;
        }
        .mid-list-total-block .label i {
            font-size: 1rem;
            vertical-align: -0.12em;
            margin-right: 2px;
            color: var(--gray-700);
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
            font-size: var(--num-sub) !important;
            font-weight: 900;
            color: #C21632 !important;
            line-height: 1;
            text-shadow: none;
        }
        .mid-list-total-block .unit-large {
            font-family: 'Noto Sans JP', sans-serif;
            font-size: var(--text-body);
            font-weight: 700;
            color: var(--gray-700);
            text-shadow: none;
        }
        .mid-list-total-block .join-date {
            color: #111111 !important;
            font-weight: 800;
        }
        .mid-list-total-block .total-prorate-note {
            margin: 0.5rem 0 0;
            font-size: var(--text-note);
            font-weight: 600;
            color: var(--gray-500);
            opacity: 1;
            letter-spacing: 0.02em;
            line-height: 1.5;
        }
        .monthly-fee {
            padding: 1rem 1rem 1.2rem;
            text-align: center;
            background: #ffffff;
            border-top: 1px solid var(--gray-200);
        }
        .monthly-fee-simple {
            margin: 0;
            font-size: var(--text-body);
            font-weight: 700;
            color: #111111;
            letter-spacing: 0.02em;
            line-height: 1.5;
        }
        .monthly-fee-amount {
            margin-left: 0.35em;
            font-size: var(--num-mini);
            font-weight: 900;
            color: #C21632;
        }
        .monthly-fee-unit {
            font-size: var(--text-body);
            font-weight: 700;
            color: var(--gray-700);
        }
        
        .condition-list-content { padding: 8px 6px 4px; }
        .condition-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; text-align: left; font-size: var(--text-note); font-weight: 700; color: var(--gray-700); line-height: 1.55; }""",
)

# STEP cards: restore clear boxes; condition softer
html = html.replace(
    """        /* 黒枠カード（STEP・注意事項・オプション・アクセスで共通） */
        .lp-framed {
            background: #fff;
            border: none;
            border-radius: 0;
            box-shadow: none;
            position: relative;
        }
        .lp-framed--hover {
            transition: transform 0.22s ease, box-shadow 0.22s ease;
        }
        .lp-framed--hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 7px 0 var(--lp-frame), 0 14px 28px rgba(0, 0, 0, 0.1);
        }""",
    """        /* 枠カード（STEPは区切る／全体はフラット） */
        .lp-framed {
            background: #fff;
            border: none;
            border-radius: 0;
            box-shadow: none;
            position: relative;
        }
        .how-to-join-container .lp-framed,
        .how-to-join-container .digital-step-card {
            background: #ffffff;
            border: 2px solid #111111;
            border-radius: 0;
            box-shadow: none;
        }
        .condition-card.lp-framed {
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
        }
        .lp-framed--hover {
            transition: none;
        }
        .lp-framed--hover:hover {
            transform: none;
            box-shadow: none;
        }""",
)

html = html.replace(
    """        .step-card-lead {
            display: block;
            font-size: 0.7rem;
            font-weight: 900;
            color: var(--brand);
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }
        .step-main-content { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .step-info { flex: 1; }
        .step-title { font-size: 0.95rem; font-weight: 900; margin-bottom: 4px; }""",
    """        .step-card-lead {
            display: block;
            font-size: var(--text-note);
            font-weight: 800;
            color: var(--gray-700);
            letter-spacing: 0.06em;
            margin-bottom: 6px;
        }
        .step-main-content { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .step-info { flex: 1; }
        .step-title { font-size: var(--text-body); font-weight: 900; margin-bottom: 4px; }""",
)

# Cafe menu carousel
html = html.replace(
    """        .options-unified-inner {
            border-radius: 0;
            overflow: hidden;
        }""",
    """        .options-unified-inner {
            border-radius: 0;
            overflow: hidden;
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
        }""",
)

html = html.replace(
    """        .options-carousel-section .text-box {
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
        }
        .options-notice-block {
            padding: 28px 20px 32px;
            border-top: none;
            background: #fff;
            text-align: center;
        }
        .options-notice-block .notice-title-v22 {
            margin-bottom: 20px;
        }
        .options-notice-block .notice-body {
            font-size: 0.85rem;
            line-height: 1.8;
            font-weight: 700;
            color: #333;
            margin-bottom: 20px;
        }

        .scene { width: 100%; height: 520px; display: flex; justify-content: center; align-items: center; position: relative; overflow: hidden; }
        .card-carousel { width: 320px; height: 400px; position: relative; cursor: grab; }
        .option-card-3d { position: absolute; width: 320px; height: 400px; border-radius: 0; background-color: #fff; border: 2px solid #111111; display: flex; flex-direction: column; padding: 1.35rem 1rem; left: 50%; top: 0; transform: translateX(-50%); transition: 0.5s; }
        .card-icon { max-width: 190px; max-height: 190px; margin: auto; width: 100%; object-fit: contain; }
        .card-title { font-size: 1.1rem; font-weight: 900; color: #333; }
        .card-price { font-size: 1.4rem; font-weight: 700; color: var(--brand); }""",
    """        .options-carousel-section .text-box {
            margin: 0 auto 1.2rem auto;
            max-width: 92%;
            text-align: center;
            background: #ffffff;
            border: 1px solid var(--gray-200);
            border-radius: 0;
            padding: 18px 14px;
            box-shadow: none;
            color: #111111;
        }
        .options-carousel-section .section-title {
            font-size: 1.2rem;
            font-weight: 900;
            margin-bottom: 0.65rem;
            position: relative;
            display: inline-block;
            padding-bottom: 0;
            color: #111111;
            letter-spacing: 0.06em;
        }
        .options-carousel-section .section-title::after {
            display: none !important;
        }
        .options-carousel-section .section-title .highlight {
            color: #C21632;
            font-size: 1.85rem;
            margin-right: 4px;
            text-shadow: none;
        }
        .options-carousel-section .text-box p {
            font-size: var(--text-body);
            line-height: 1.65;
            font-weight: 700;
            color: #111111;
            margin: 0;
        }
        .options-carousel-section .text-box .highlight-text {
            color: #C21632;
            font-size: var(--num-mini);
            font-weight: 900;
        }
        .options-carousel-section .text-box .text-box-note {
            font-size: var(--text-note);
            color: var(--gray-500);
            opacity: 1;
            display: inline-block;
            margin-top: 8px;
            font-weight: 600;
        }
        .options-notice-block {
            padding: 28px 20px 32px;
            border-top: 1px solid var(--gray-200);
            background: #ffffff;
            text-align: center;
        }
        .options-notice-block .notice-title-v22 {
            margin-bottom: 16px;
            font-size: var(--text-body);
        }
        .options-notice-block .notice-body {
            font-size: var(--text-note);
            line-height: 1.8;
            font-weight: 700;
            color: var(--gray-700);
            margin-bottom: 20px;
        }

        .scene {
            width: 100%;
            height: 520px;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
            background:
                linear-gradient(#ffffff, #ffffff) padding-box,
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 11px,
                    rgba(17, 17, 17, 0.04) 11px,
                    rgba(17, 17, 17, 0.04) 12px
                );
            margin: 0 12px;
            border: 1px solid var(--gray-200);
            background-color: #ffffff;
        }
        .card-carousel { width: 320px; height: 400px; position: relative; cursor: grab; }
        .option-card-3d {
            position: absolute;
            width: 320px;
            height: 400px;
            border-radius: 0;
            background-color: #fff;
            border: 1px solid #111111;
            outline: 1px solid transparent;
            box-shadow: inset 0 0 0 4px #ffffff, inset 0 0 0 5px var(--gray-200);
            display: flex;
            flex-direction: column;
            padding: 1.35rem 1rem;
            left: 50%;
            top: 0;
            transform: translateX(-50%);
            transition: 0.5s;
        }
        .card-icon { max-width: 190px; max-height: 190px; margin: auto; width: 100%; object-fit: contain; }
        .card-title { font-size: var(--text-body); font-weight: 900; color: #111111; }
        .card-price { font-size: var(--num-mini); font-weight: 900; color: var(--brand); }""",
)

# Fix media query that still shrinks hero price too much
html = html.replace(
    """            .price-item--half-year .half-year-price {
                font-size: clamp(3.8rem, 20vw, 5.2rem);
            }""",
    """            .price-item--half-year .half-year-price {
                font-size: var(--num-hero);
            }""",
)

# Update override block for header + framed steps
html = html.replace(
    """        .campaign-title-summer { text-shadow: none !important; }
        .campaign-app-badge {
            background: #ffffff !important;
            color: #C21632 !important;
            border: 2px solid #ffffff !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border-radius: 4px !important;
        }
        .campaign-app-badge span { color: #C21632 !important; }""",
    """        .campaign-header-enhanced {
            background: #ffffff !important;
        }
        .campaign-title-summer {
            text-shadow: none !important;
            color: #111111 !important;
            -webkit-text-fill-color: #111111 !important;
        }
        .campaign-app-badge {
            background: var(--gray-50) !important;
            color: var(--gray-700) !important;
            border: 1px solid var(--gray-200) !important;
            backdrop-filter: none !important;
            -webkit-backdrop-filter: none !important;
            border-radius: 0 !important;
        }
        .campaign-app-badge span { color: var(--gray-700) !important; }""",
)

html = html.replace(
    """        .lp-framed,
        .digital-step-card,
        .condition-card,
        .option-card-3d {
            border-radius: 0 !important;
            box-shadow: none !important;
        }
        .lp-framed { border: none !important; box-shadow: none !important; }
        .lp-frame-badge { border-radius: 0 !important; }""",
    """        .lp-framed,
        .digital-step-card,
        .condition-card,
        .option-card-3d {
            border-radius: 0 !important;
        }
        .how-to-join-container .lp-framed {
            border: 2px solid #111111 !important;
            box-shadow: none !important;
        }
        .condition-card.lp-framed {
            border: 1px solid var(--gray-200) !important;
            background: var(--gray-50) !important;
            box-shadow: none !important;
        }
        .lp-frame-badge { border-radius: 0 !important; }""",
)

# Inline step-desc sizes → use note size
html = html.replace(
    'style="font-size: 0.75rem; color: #666;"',
    'style="font-size: 0.78rem; color: #777;"',
)
html = html.replace(
    'style="font-size: 0.95rem;" data-i18n="steps.step1Title"',
    'style="font-size: 1rem;" data-i18n="steps.step1Title"',
)

PROD.write_text(html, encoding="utf-8")
print("updated prod")

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
