/**
 * サイネージ撮影用 — 本番 LP (index.html) 上で実行
 */
(function () {
  const SCENES = [
    { start: 0, end: 2.5, selector: ".campaign-header-enhanced" },
    { start: 2.5, end: 6, selector: ".half-year-block" },
    { start: 6, end: 7.5, selector: "#signage-scene-option" },
    { start: 7.5, end: 9.5, selector: "#signage-scene-initial" },
    { start: 9.5, end: 11.5, selector: ".mid-list-total-block" },
    { start: 11.5, end: 15, selector: "#signage-scene-app" },
  ];

  const HIDE_SELECTORS = [
    "#lp-opening-scroll",
    ".gold-metallic-banner",
    ".hero-first-view",
    ".options-unified-section",
    ".access-section",
    ".condition-card",
    ".monthly-fee",
    ".fixed-banner",
    "#banner-toggle-container",
  ];

  function easeInOutCubic(t) {
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  }

  function clamp01(v) {
    return Math.max(0, Math.min(1, v));
  }

  function injectStyles() {
    const style = document.createElement("style");
    style.textContent = `
      html.signage-capture, html.signage-capture body {
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: #fffdf0 !important;
        width: 1080px !important;
        min-height: 1920px !important;
      }
      html.signage-capture .lp-wrapper {
        max-width: 1000px !important;
        padding-top: 88px !important;
      }
      html.signage-capture .reveal-up {
        opacity: 1 !important;
        transform: none !important;
      }
      #signage-top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 99999;
        background: #1a1a1a;
        color: #fff;
        text-align: center;
        font-family: 'Noto Sans JP', sans-serif;
        font-weight: 900;
        font-size: 1.05rem;
        letter-spacing: 0.06em;
        padding: 14px 16px;
        border-bottom: 3px solid #C21632;
      }
      #signage-top-bar span {
        color: #F8E71C;
      }
      .signage-focus-target {
        position: relative;
        z-index: 2;
      }
      .signage-focus-target::after {
        content: '';
        position: absolute;
        inset: -6px;
        border: 3px solid rgba(194, 22, 50, 0.55);
        border-radius: 16px;
        pointer-events: none;
        box-shadow: 0 0 0 4px rgba(255,255,255,0.85);
      }
      html.signage-capture .how-to-join-container .digital-step-card:first-child {
        display: none !important;
      }
    `;
    document.head.appendChild(style);
  }

  function finishOpening() {
    document.getElementById("lp-opening-scroll")?.remove();
    document.documentElement.classList.remove("lp-opening-lock");
    document.body.classList.remove("lp-opening-active", "lp-opening-reveal");
    document.body.classList.add("banner-hidden", "top-banner-hidden");
  }

  function hideNoise() {
    HIDE_SELECTORS.forEach((sel) => {
      document.querySelectorAll(sel).forEach((el) => {
        el.style.setProperty("display", "none", "important");
      });
    });
  }

  function tagScenes() {
    const optionRow = document.querySelector(".price-list > .price-item:not(.price-item--half-year):not(.price-item--initial)");
    if (optionRow) optionRow.id = "signage-scene-option";
    const initial = document.querySelector(".price-item--initial");
    if (initial) initial.id = "signage-scene-initial";
    const appStep = document.querySelector(".how-to-join-container .digital-step-card:last-child");
    if (appStep) appStep.id = "signage-scene-app";
  }

  function addTopBar() {
    if (document.getElementById("signage-top-bar")) return;
    const bar = document.createElement("div");
    bar.id = "signage-top-bar";
    bar.innerHTML = 'JOYFIT24 経堂　<span>7/24(金)まで</span>　先着15名';
    document.body.prepend(bar);
  }

  function scrollOffsetFor(selector) {
    const el = document.querySelector(selector);
    if (!el) return 0;
    const top = el.getBoundingClientRect().top + window.scrollY;
    return Math.max(0, top - 96);
  }

  function computeOffsets() {
    return SCENES.map((s) => scrollOffsetFor(s.selector));
  }

  function clearFocus() {
    document.querySelectorAll(".signage-focus-target").forEach((el) => {
      el.classList.remove("signage-focus-target");
    });
  }

  function focusScene(index) {
    clearFocus();
    const sel = SCENES[index]?.selector;
    const el = sel && document.querySelector(sel);
    if (el) el.classList.add("signage-focus-target");
  }

  function scrollAtTime(t) {
    const offsets = window.__signageOffsets;
    if (!offsets) return;

    let i = SCENES.length - 1;
    for (let j = 0; j < SCENES.length; j++) {
      if (t < SCENES[j].end) {
        i = j;
        break;
      }
    }

    const scene = SCENES[i];
    const y0 = offsets[Math.max(0, i - 1)] ?? offsets[0];
    const y1 = offsets[i];
    const local = t - scene.start;
    const dur = scene.end - scene.start;
    const p = dur > 0 ? easeInOutCubic(clamp01(local / Math.min(0.55, dur * 0.35))) : 1;
    const y = i === 0 ? y1 : lerp(y0, y1, p);

    window.scrollTo(0, y);
    focusScene(i);
  }

  function lerp(a, b, t) {
    return a + (b - a) * t;
  }

  function init() {
    document.documentElement.classList.add("signage-capture");
    injectStyles();
    finishOpening();
    hideNoise();
    tagScenes();
    addTopBar();
    document.querySelectorAll(".reveal-up").forEach((el) => el.classList.add("is-visible"));

    if (typeof updateProratedFee === "function") {
      updateProratedFee();
    } else {
      const total = document.getElementById("dynamic-total-price");
      const label = document.getElementById("dynamic-date-label");
      if (total) total.textContent = "8,913";
      if (label) label.innerHTML = '(<span class="join-date">7/15</span>)ご入会時金額';
    }

    window.__signageOffsets = computeOffsets();
    window.__signageReady = true;
    window.setSignageTime(0);
  }

  window.setSignageTime = function (t) {
    scrollAtTime(Math.max(0, Math.min(15, t)));
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
