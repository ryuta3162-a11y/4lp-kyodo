"""
Instagramストーリー自動投稿（公式 Graph API）

使い方:
  set INSTAGRAM_ACCESS_TOKEN=...
  set INSTAGRAM_IG_USER_ID=...
  python publish_story.py

動画はデフォルトで同フォルダの joyfit-story-10s.mp4 をアップロード。
公開URLがある場合は INSTAGRAM_STORY_VIDEO_URL を指定（その場合ローカルファイル不要）。
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API_VERSION = os.environ.get("INSTAGRAM_GRAPH_API_VERSION", "v22.0")
GRAPH = f"https://graph.facebook.com/{API_VERSION}"
DEFAULT_VIDEO = Path(__file__).resolve().parent / "joyfit-story-10s.mp4"
POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 300


def env_required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"環境変数 {name} が未設定です。", file=sys.stderr)
        sys.exit(1)
    return value


def http_json(method: str, url: str, data: dict | None = None, headers: dict | None = None) -> dict:
    body = None
    req_headers = {"Accept": "application/json"}
    if headers:
        req_headers.update(headers)
    if data is not None:
        body = urllib.parse.urlencode(data).encode("utf-8")
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    req = urllib.request.Request(url, data=body, headers=req_headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            raw = res.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {url}\n{err}") from e


def create_container_from_url(ig_user_id: str, token: str, video_url: str) -> str:
    print(f"コンテナ作成（video_url）…")
    result = http_json(
        "POST",
        f"{GRAPH}/{ig_user_id}/media",
        data={
            "media_type": "STORIES",
            "video_url": video_url,
            "access_token": token,
        },
    )
    container_id = result.get("id")
    if not container_id:
        raise RuntimeError(f"コンテナIDが返りませんでした: {result}")
    print(f"  container_id={container_id}")
    return container_id


def create_container_resumable(ig_user_id: str, token: str) -> tuple[str, str]:
    print("コンテナ作成（resumable）…")
    result = http_json(
        "POST",
        f"{GRAPH}/{ig_user_id}/media",
        data={
            "media_type": "STORIES",
            "upload_type": "resumable",
            "access_token": token,
        },
    )
    container_id = result.get("id")
    upload_uri = result.get("uri")
    if not container_id:
        raise RuntimeError(f"コンテナIDが返りませんでした: {result}")
    if not upload_uri:
        upload_uri = f"https://rupload.facebook.com/ig-api-upload/{API_VERSION}/{container_id}"
    print(f"  container_id={container_id}")
    return container_id, upload_uri


def upload_video_bytes(upload_uri: str, token: str, video_path: Path) -> None:
    size = video_path.stat().st_size
    print(f"動画アップロード中… ({size} bytes) {video_path.name}")
    data = video_path.read_bytes()
    req = urllib.request.Request(
        upload_uri,
        data=data,
        method="POST",
        headers={
            "Authorization": f"OAuth {token}",
            "offset": "0",
            "file_size": str(size),
            "Content-Type": "application/octet-stream",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as res:
            raw = res.read().decode("utf-8")
            print(f"  upload response: {raw or '(empty)'}")
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"アップロード失敗 HTTP {e.code}\n{err}") from e


def wait_until_finished(container_id: str, token: str) -> None:
    print("処理待ち…")
    deadline = time.time() + POLL_TIMEOUT_SEC
    while time.time() < deadline:
        result = http_json(
            "GET",
            f"{GRAPH}/{container_id}?fields=status_code&access_token={urllib.parse.quote(token)}",
        )
        status = result.get("status_code")
        print(f"  status={status}")
        if status == "FINISHED":
            return
        if status in {"ERROR", "EXPIRED"}:
            raise RuntimeError(f"コンテナ処理失敗: {result}")
        time.sleep(POLL_INTERVAL_SEC)
    raise RuntimeError("コンテナ処理がタイムアウトしました")


def publish(ig_user_id: str, token: str, container_id: str) -> dict:
    print("公開中…")
    result = http_json(
        "POST",
        f"{GRAPH}/{ig_user_id}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": token,
        },
    )
    print(f"  publish result: {result}")
    return result


def main() -> int:
    token = env_required("INSTAGRAM_ACCESS_TOKEN")
    ig_user_id = env_required("INSTAGRAM_IG_USER_ID")
    video_url = os.environ.get("INSTAGRAM_STORY_VIDEO_URL", "").strip()
    video_path = Path(os.environ.get("INSTAGRAM_STORY_VIDEO_PATH", str(DEFAULT_VIDEO)))

    if video_url:
        container_id = create_container_from_url(ig_user_id, token, video_url)
    else:
        if not video_path.is_file():
            print(f"動画が見つかりません: {video_path}", file=sys.stderr)
            print("INSTAGRAM_STORY_VIDEO_URL か、ローカル動画パスを設定してください。", file=sys.stderr)
            return 1
        container_id, upload_uri = create_container_resumable(ig_user_id, token)
        upload_video_bytes(upload_uri, token, video_path)

    wait_until_finished(container_id, token)
    publish(ig_user_id, token, container_id)
    print("完了: ストーリーを投稿しました")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(f"エラー: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
