# A4 オプション一覧（印刷用）

サンプル（Canva 27ページ）と同型の、JOYFIT24経堂オプション訴求チラシです。

## ファイル

| ファイル | 用途 |
|---------|------|
| [`index.html`](./index.html) | 表面プレビュー・再編集用 |
| [`back.html`](./back.html) | 裏面（JOYFITアプリ Q&A）プレビュー |
| [`joyfit-options-a4-300dpi.png`](./joyfit-options-a4-300dpi.png) | 表面・印刷用PNG |
| [`joyfit-app-qa-a4-300dpi.png`](./joyfit-app-qa-a4-300dpi.png) | 裏面・印刷用PNG |
| [`joyfit-options-a4.pdf`](./joyfit-options-a4.pdf) | 表面・印刷用PDF |
| [`joyfit-app-qa-a4.pdf`](./joyfit-app-qa-a4.pdf) | 裏面・印刷用PDF |
| [`export.py`](./export.py) | PNG/PDF再書き出し |

## 内容

- **01〜09**：自動契約オプション（キャンペーン中・8月分0円）
- **10〜12**：キャンペーン外オプション（任意契約）
- 画像はLPと同じ `36.png`〜`47.png` を使用

## 再書き出し

```bash
cd print/a4-options
python export.py
```
