# FV GIF 作業メモ（別PC引き継ぎ用）

最終更新: 2026-09-13

## いまの状態

ホームページFV用の訴求GIFを作成中。WordPressに載せる想定。

### 使うファイル（本番候補）

- `kyodo-fv-3300-web.gif` … **WordPress用（軽量）** ← これをアップ
- `kyodo-fv-3300.gif` … 高画質マスター
- `1.png` / `2.png` / `3.png` … 素材
  - `3.png` 土台（バッジ・CTA・女の子）
  - `2.png` ＋「6ヶ月間ずっーと」
  - `1.png` ＋「3,300円」完成形
- `make_gif.py` … 再生成スクリプト

### ダウンロード場所（作業PC）

`C:\Users\ryuta-kusaka\Downloads\kyodo-fv-3300-web.gif`

## いま入っている演出

1. 最初のコマは完成形（空コマなし／WPプレビュー対策）
2. 「6ヶ月間ずっーと」→「3,300円」登場
3. **金ピカ**の光スイープ＋キラキラ（赤光・ピンクはなし）
4. 「詳細はこちらをタップ」全体のドクンドクン（右端まで）
5. カンマは描き足し補強済み（要・目視確認）

## 再生成

```bash
cd assets/fv-gif
python make_gif.py
ffmpeg -y -i kyodo-fv-3300.gif -vf "fps=20,scale=720:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=192:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=2" kyodo-fv-3300-web.gif
```

必要: Python + Pillow + numpy + ffmpeg

## WordPress手順

1. `kyodo-fv-3300-web.gif` をメディアにアップロード
2. 画像枠にセット
3. リンク先例: `https://lp-24kyodo.vercel.app/`
4. 管理画面プレビューはGIFの1コマ目だけ見えることがある → 公開ページ／スマホで確認

## 途中・未確定／次に触りそうな点

- カンマ下端の見え方（まだ気になるなら `reinforce_comma()` を調整）
- 金ピカの強さ（`apply_shimmer_rgb` / `add_price_glow`）
- CTA拡大範囲（`CTA_BOX`）
- 女の子を含めたドクンドクンが広すぎる場合の調整
- LP本体（`index.html`）への埋め込みは未実施（現状はWP用書き出し）

## デバッグ用（コミットしない）

`_debug-*.png` / `_comma-raw.png` / `__pycache__/`
