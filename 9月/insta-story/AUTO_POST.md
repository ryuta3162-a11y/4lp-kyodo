# Instagramストーリー 毎日自動投稿

毎日 **10:00（日本時間）** に `joyfit-story-10s.mp4` をストーリー投稿します。  
文字・キャプションなし。公式 Instagram Graph API のみ使用。

## 流れ（初回のみ人手）

1. Metaでアプリ作成・権限取得
2. GitHub Secrets にトークン等を入れる
3. このリポジトリの GitHub Actions が毎日自動実行

以降は手作業なし。動画を変えるときは `joyfit-story-10s.mp4` を差し替えて push。

## Meta セットアップ

1. [Meta for Developers](https://developers.facebook.com/) でアプリ作成  
2. **Instagram** 製品を追加（Facebook Login for Business が必要な場合あり）  
3. 経堂ビジネスアカウントを連携  
4. 権限（例）:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
5. 本番利用前に **App Review**（投稿権限）が必要なことがあります  
6. **長期アクセストークン** を発行  
7. **Instagram ビジネスアカウント ID**（数字の IG User ID）を控える

IDの確認例（ブラウザや Graph API Explorer）:

```text
GET /me/accounts
→ ページ → linked Instagram business account id
```

## GitHub Secrets（必須）

リポジトリ → Settings → Secrets and variables → Actions

| Name | 内容 |
|------|------|
| `INSTAGRAM_ACCESS_TOKEN` | 長期アクセストークン |
| `INSTAGRAM_IG_USER_ID` | InstagramビジネスアカウントID |

任意:

| Name | 内容 |
|------|------|
| `INSTAGRAM_STORY_VIDEO_URL` | 公開HTTPSの動画URL（指定時はローカルupload不要） |

## 動作確認

Actions → **Instagram Story Daily** → **Run workflow** で手動実行できます。

ローカルテスト:

```powershell
$env:INSTAGRAM_ACCESS_TOKEN="..."
$env:INSTAGRAM_IG_USER_ID="..."
python publish_story.py
```

## スケジュール

- cron: `0 1 * * *`（UTC）＝ **毎日 10:00 JST**
- ワークフロー: `.github/workflows/instagram-story-daily.yml`

## セキュリティ

- トークンは Secrets のみ（リポジトリ本文に書かない）
- 権限は投稿に必要なものだけ
- 漏れたら Meta でトークン無効化

## 注意

- 同じ動画の毎日投稿はAPI上可能ですが、Instagram側のスパム判定で表示が弱くなる可能性はゼロではありません
- トークン期限切れ時は Secrets を更新
- Meta審査が通るまで本番投稿は失敗します
