"""
入口サイネージ 30秒動画（グラフィック版）

・縦 1080x1920 → 90°回転で 1920x1080（左傾け設置用）
・最終画面（15.5〜30秒）: QRコード + 詳細はこちらをチェック
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PW, PH = 1080, 1920
CX = PW // 2

FPS = 30
DURATION = 30
FRAMES = FPS * DURATION
OUT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = OUT_DIR / "_frames"
OUTPUT = OUT_DIR / "joyfit-signage-30s.mp4"
QR_PATH = OUT_DIR / "qr.png"

BRAND = (194, 22, 50)
BRAND_DARK = (100, 12, 28)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY_LIGHT = (220, 220, 220)

_QR_IMAGE: Image.Image | None = None


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    size = max(12, int(size))
    candidates = (
        [r"C:\Windows\Fonts\meiryob.ttc", r"C:\Windows\Fonts\YuGothB.ttc"]
        if bold
        else [r"C:\Windows\Fonts\meiryo.ttc", r"C:\Windows\Fonts\YuGothM.ttc"]
    )
    for path in candidates:
        if os.path.isfile(path):
            try:
                return ImageFont.truetype(path, size, index=0)
            except OSError:
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    continue
    return ImageFont.load_default()


def ease_out_cubic(t: float) -> float:
    return 1 - pow(1 - t, 3)


def clamp01(v: float) -> float:
    return max(0.0, min(1.0, v))


def scene_alpha(t: float, start: float, end: float, fade: float = 0.28) -> float:
    if t < start or t > end:
        return 0.0
    if t < start + fade:
        return ease_out_cubic((t - start) / fade)
    if t > end - fade:
        return ease_out_cubic((end - t) / fade)
    return 1.0


def slide_y(t: float, at: float, dur: float, dist: int) -> int:
    if t < at:
        return dist
    return int(dist * (1 - ease_out_cubic(clamp01((t - at) / dur))))


def draw_bg(img: Image.Image, t: float) -> None:
    draw = ImageDraw.Draw(img)
    for y in range(PH):
        ratio = y / PH
        r = int(BRAND[0] + (BRAND_DARK[0] - BRAND[0]) * ratio * 0.5)
        g = int(BRAND[1] + (BRAND_DARK[1] - BRAND[1]) * ratio * 0.5)
        b = int(BRAND[2] + (BRAND_DARK[2] - BRAND[2]) * ratio * 0.5)
        draw.line([(0, y), (PW, y)], fill=(r, g, b))

    overlay = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    sx, sy = int(PW * 0.8), int(PH * 0.12)
    for i in range(5):
        ang = i * math.pi / 2.5 + t * 0.25
        od.line(
            [(sx, sy), (sx + int(math.cos(ang) * 80), sy + int(math.sin(ang) * 80))],
            fill=(255, 255, 255, 18),
            width=2,
        )
    shift = int((t * 60) % 320)
    for i in range(-1, 4):
        x0 = i * 320 + shift
        od.polygon([(x0, 0), (x0 + 40, 0), (x0 - 60, PH), (x0 - 100, PH)], fill=(0, 0, 0, 16))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    ImageDraw.Draw(img).rectangle([20, 20, PW - 20, PH - 20], outline=WHITE, width=2)


def draw_micro(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    a: float,
    sy: int = 0,
    size: int = 52,
    stroke: int = 3,
) -> None:
    if a <= 0:
        return
    alpha = int(255 * a)
    draw.text(
        (CX, y + sy), text, font=find_font(size, True),
        fill=(*WHITE, alpha), anchor="mm",
        stroke_width=stroke, stroke_fill=(*BLACK, alpha),
    )


def draw_head(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, a: float, sy: int = 0, stroke: int = 6) -> None:
    if a <= 0 or not text:
        return
    alpha = int(255 * a)
    draw.text(
        (CX, y + sy), text, font=find_font(size, True),
        fill=(*WHITE, alpha), anchor="mm",
        stroke_width=stroke, stroke_fill=(*BLACK, alpha),
    )


def draw_band(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, a: float, sy: int = 0) -> None:
    if a <= 0:
        return
    font = find_font(size, True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw = bbox[2] - bbox[0]
    py = max(30, size // 2 + 10)
    alpha = int(255 * a)
    draw.rectangle([CX - tw // 2 - 24, y - py + sy, CX + tw // 2 + 24, y + py + sy], fill=(*BLACK, int(220 * a)))
    draw.text((CX, y + sy), text, font=font, fill=(*WHITE, alpha), anchor="mm")


def draw_store_badge(draw: ImageDraw.ImageDraw, y: int, a: float, sy: int = 0) -> None:
    if a <= 0:
        return
    text, font = "JOYFIT24 経堂", find_font(56, True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    alpha = int(255 * a)
    rx = CX - tw // 2 - 30
    ry = y - th // 2 - 14 + sy
    draw.rounded_rectangle([rx, ry, rx + tw + 60, ry + th + 28], radius=10, fill=(*BLACK, alpha))
    draw.text((CX, y + sy), text, font=font, fill=(*WHITE, alpha), anchor="mm")


def load_qr() -> Image.Image:
    global _QR_IMAGE
    if _QR_IMAGE is not None:
        return _QR_IMAGE
    if not QR_PATH.is_file():
        raise FileNotFoundError(f"QRコード画像がありません: {QR_PATH}")
    _QR_IMAGE = Image.open(QR_PATH).convert("RGBA")
    return _QR_IMAGE


def draw_qr_panel(
    overlay: Image.Image,
    draw: ImageDraw.ImageDraw,
    a: float,
    sy: int,
    t: float,
    center_y: int = 960,
) -> None:
    if a <= 0:
        return
    pulse = 1.0 + 0.008 * math.sin((t - 15.5) * 3) if t > 15.5 else 1.0
    qr_size = int(480 * pulse)
    pad = 32
    frame_w = qr_size + pad * 2
    frame_h = qr_size + pad * 2
    fx = CX - frame_w // 2
    fy = center_y - frame_h // 2 + sy
    alpha = int(255 * a)

    draw_band(draw, fy - 56, "ここのQRを読み取ってね", 48, a, sy)

    frame_layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame_layer)
    fd.rounded_rectangle([fx, fy, fx + frame_w, fy + frame_h], radius=24, fill=(255, 255, 255, alpha))
    fd.rounded_rectangle([fx + 6, fy + 6, fx + frame_w - 6, fy + frame_h - 6], radius=20, outline=(26, 26, 26, alpha), width=4)
    fd.rounded_rectangle([fx + 14, fy + 14, fx + frame_w - 14, fy + frame_h - 14], radius=16, outline=(*BRAND, alpha), width=5)

    for corner in ((fx + 18, fy + 18), (fx + frame_w - 58, fy + 18), (fx + 18, fy + frame_h - 58), (fx + frame_w - 58, fy + frame_h - 58)):
        fd.rectangle([corner[0], corner[1], corner[0] + 40, corner[1] + 8], fill=(*BRAND, alpha))
        fd.rectangle([corner[0], corner[1], corner[0] + 8, corner[1] + 40], fill=(*BRAND, alpha))

    qr = load_qr().resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qx = CX - qr_size // 2
    qy = fy + pad
    frame_layer.paste(qr, (qx, qy), qr)
    overlay.alpha_composite(frame_layer)


# ── シーン（複数要素を同時表示）────────────────────────

def scene_open(draw, t, a, sy):
    draw_store_badge(draw, 420, a, sy)
    draw_head(draw, 820, "夏得", 190, a, sy)
    draw_head(draw, 1040, "キャンペーン", 105, a, sy, stroke=5)
    draw_band(draw, 1280, "7/12(日)まで · 先着20名", 54, a, sy)


def scene_price(draw, t, a, sy):
    local = t - 3.0
    pulse = 1.0 + 0.012 * math.sin(local * 4) if local > 0 else 1.0
    draw_micro(draw, 520, "7〜12月 · 半年間ずーっとお得", a, sy, size=52)
    draw_micro(draw, 700, "通常 9,350円 →", a, sy, size=52)
    draw_head(draw, 920, "3,630", int(270 * pulse), a, sy, stroke=10)
    draw_head(draw, 1160, "円(税込) / 月", 74, a, sy, stroke=4)


def scene_facility(draw, t, a, sy):
    draw_head(draw, 880, "24時間営業", 115, a, sy, stroke=5)
    draw_band(draw, 1100, "充実した設備", 60, a, sy)
    draw_micro(draw, 1300, "入会当日から利用OK", a, sy, size=52)


def scene_combo(draw, t, a, sy):
    """7月オプション0円 ＋ 入会受付中 を1画面に集約"""
    draw_band(draw, 780, "7月オプション 0円", 66, a, sy)
    draw_micro(draw, 960, "無料オプション8つ", a, sy, size=52)
    draw_head(draw, 1160, "入会受付中", 100, a, sy, stroke=6)
    draw_band(draw, 1380, "7/12(日)まで · 先着20名", 54, a, sy)


def scene_qr(overlay: Image.Image, draw, t, a, sy):
    draw_store_badge(draw, 480, a, sy)
    draw_head(draw, 620, "詳細はこちらをチェック", 70, a, sy, stroke=5)
    draw_micro(draw, 720, "キャンペーン内容・入会方法", a, sy, size=50)
    draw_qr_panel(overlay, draw, a, sy, t, center_y=1100)
    draw_micro(draw, 1480, "7/12(日)まで · 先着20名", a, sy, size=52)


TIMELINE = [
    (0.0, 3.0, scene_open, False),
    (3.0, 8.5, scene_price, False),
    (8.5, 11.5, scene_facility, False),
    (11.5, 15.5, scene_combo, False),
    (15.5, 30.0, scene_qr, True),
]


def render_portrait_frame(t: float) -> Image.Image:
    img = Image.new("RGB", (PW, PH), BRAND)
    draw_bg(img, t)
    overlay = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for start, end, fn, use_overlay in TIMELINE:
        if end >= DURATION:
            if t < start:
                alpha = 0.0
            elif t < start + 0.35:
                alpha = ease_out_cubic((t - start) / 0.35)
            else:
                alpha = 1.0
        else:
            alpha = scene_alpha(t, start, end, fade=0.3)
        if alpha > 0:
            sy = slide_y(t, start + 0.04, 0.35, 100) if t < start + 0.4 else 0
            if use_overlay:
                fn(overlay, draw, t, alpha, sy)
            else:
                fn(draw, t, alpha, sy)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def to_signage_frame(portrait: Image.Image) -> Image.Image:
    return portrait.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)


def render_frame(frame_idx: int) -> Image.Image:
    return to_signage_frame(render_portrait_frame(frame_idx / FPS))


def main() -> int:
    load_qr()
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True)

    print(f"フレーム生成中… {DURATION}秒 / {FRAMES}枚")
    for i in range(FRAMES):
        render_frame(i).save(FRAMES_DIR / f"frame_{i:04d}.png", optimize=True)
        if i % 30 == 0:
            print(f"  {i}/{FRAMES}")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg が見つかりません。", file=sys.stderr)
        return 1

    subprocess.run([
        ffmpeg, "-y", "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart", "-t", str(DURATION), str(OUTPUT),
    ], check=True)
    shutil.rmtree(FRAMES_DIR)
    print(f"完成: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
