# 9/25(金) 本番切替手順

**9/24まで**: ルート `index.html`（9月キャンペーン・先着10名・3,300円）のまま公開  
**9/25 0:00〜**: 下記を実行して 10月版へ切替

## 手順

1. ルート `index.html` ← `10月/index.html` を上書きコピー
2. `locales/campaign/*.json` ← `10月/locales-for-switch/*.json` を上書きコピー
3. `campaign-i18n.js` ← `10月/campaign-i18n.js` を上書きコピー
4. `python build_locales.py` でルート `locales.bundle.js` 再生成
5. ルート `index.html` の `../i18n.css` / `../i18n.js` を `i18n.css` / `i18n.js` に戻す（`locales.bundle.js`・`campaign-i18n.js` は同階層）
6. `git commit` → `git push`（Vercel 自動反映）

切替後も 9月証跡は [`../9月/archive/2026-09-24まで-先着10名・3300円版/`](../9月/archive/2026-09-24まで-先着10名・3300円版/) に残す。
