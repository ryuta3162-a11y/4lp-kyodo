# 9/1(火) 本番切替手順

**8/31まで**: ルート `index.html`（8月会費0円版）のまま公開  
**9/1 0:00〜**: 下記を実行して 9月VERへ切替

## 手順

1. ルート `index.html` ← `9月/index.html` を上書きコピー
2. `locales/campaign/*.json` ← `9月/locales-for-switch/*.json` を上書きコピー
3. `campaign-i18n.js` ← `9月/campaign-i18n.js` を上書きコピー
4. `python build_locales.py` で `locales.bundle.js` 再生成
5. `git commit` → `git push`（Vercel 自動反映）

## 9月VERで変わる点（大枠は同じ）

- 8月会費0円の表示を削除
- オプション表記: 8・9月 → **9月**
- 入会時金額: 9月日割のみ（8月無料ロジック削除）
- 多言語（en/ko/zh）も 8月表記を削除

## 参照

- 8月会費0円版の保存: [`archive/2026-08-31まで-8月会費0円版/`](./archive/2026-08-31まで-8月会費0円版/)
- 8月キャンペーン（夏得）: [`../8月/`](../8月/)
