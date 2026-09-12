"""
Instagramストーリー用 10秒動画（1080x1920）
実行: python generate.py → joyfit-story-10s.mp4

①金額  ②詳細はインスタ
"""
from __future__ import annotations

import math
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
CX, CY = W // 2, H // 2
FPS = 30
DURATION = 10
FRAMES = FPS * DURATION
OUT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = OUT_DIR / "_frames"
OUTPUT = OUT_DIR / "joyfit-story-10s.mp4"

# --- 金額だけここを変えればOK ---
TOP_BADGE = "JOYFIT24経堂限定"
CATCH = "6カ月ずっと"
PRICE_MAIN = "3,300"
PRICE_TAX = "3,630"
# --------------------------------

WHITE = (255, 255, 255)
INK = (17, 17, 17)
MUTED = (102, 102, 102)
BRAND = (194, 22, 50)


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    size = max(12, int(size))
    candidates = (
        [
            r"C:\Windows\Fonts\meiryob.ttc",
            r"C:\Windows\Fonts\YuGothB.ttc",
            r"C:\Windows\Fonts\msgothic.ttc",
        ]
        if bold
        else [
            r"C:\Windows\Fonts\meiryo.ttc",
            r"C:\Windows\Fonts\YuGothM.ttc",
            r"C:\Windows\Fonts\msgothic.ttc",
        ]
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


def ease_out_back(t: float) -> float:
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)


def scene_window(t: float, start: float, end: float, fade: float = 0.22) -> float:
    if t < start or t > end:
        return 0.0
    if t < start + fade:
        return ease_out_cubic((t - start) / fade)
    if t > end - fade:
        return ease_out_cubic((end - t) / fade)
    return 1.0


def line_enter(t: float, at: float, dur: float = 0.32) -> tuple[float, float, int]:
    if t < at:
        return 0.0, 0.9, 28
    p = min(1.0, (t - at) / dur)
    e = ease_out_back(p)
    return e, 0.9 + 0.1 * e, int(28 * (1 - e))


def draw_bg(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, H], fill=WHITE)
    draw.rectangle([0, 0, W, 8], fill=BRAND)
    draw.rectangle([0, H - 8, W, H], fill=BRAND)
    margin = 40
    draw.rectangle([margin, margin, W - margin, H - margin], outline=INK, width=3)


def draw_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    base_size: int,
    color: tuple[int, int, int],
    alpha: float,
    scale: float = 1.0,
    slide: int = 0,
    bold: bool = True,
) -> None:
    if alpha <= 0 or not text:
        return
    font = find_font(int(base_size * scale), bold=bold)
    a = int(255 * alpha)
    draw.text((CX, y + slide), text, font=font, fill=(*color, a), anchor="mm")


def draw_badge(draw: ImageDraw.ImageDraw, y: int, text: str, alpha: float, scale: float, slide: int) -> None:
    if alpha <= 0:
        return
    font = find_font(int(48 * scale), bold=True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 36, 16
    rx = CX - tw // 2 - pad_x
    ry = y + slide - th // 2 - pad_y
    a = int(255 * alpha)
    draw.rectangle([rx, ry, rx + tw + pad_x * 2, ry + th + pad_y * 2], fill=(*BRAND, a))
    draw.text((CX, y + slide), text, font=font, fill=(*WHITE, a), anchor="mm")


def render_frame(frame_idx: int) -> Image.Image:
    t = frame_idx / FPS
    img = Image.new("RGB", (W, H), WHITE)
    draw_bg(img)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # ① 金額 (0〜6.5s)
    s1 = scene_window(t, 0.0, 6.5, fade=0.22)
    if s1 > 0:
        ba, bsc, bsl = line_enter(t, 0.08)
        ca, csc, csl = line_enter(t, 0.28)
        pa, psc, psl = line_enter(t, 0.55, 0.4)
        ya, ysc, ysl = line_enter(t, 0.85)
        ta, tsc, tsl = line_enter(t, 1.15)
        pulse = 1.0 + 0.015 * math.sin((t - 1.2) * 6) if t > 1.2 else 1.0
        draw_badge(draw, CY - 380, TOP_BADGE, s1 * ba, bsc, bsl)
        draw_text(draw, CY - 220, CATCH, 92, INK, s1 * ca, csc, csl)
        draw_text(draw, CY + 20, PRICE_MAIN, 280, BRAND, s1 * pa, psc * pulse, psl)
        draw_text(draw, CY + 240, "円", 96, BRAND, s1 * ya, ysc, ysl)
        draw_text(draw, CY + 380, f"{PRICE_TAX}円(税込)/月", 52, MUTED, s1 * ta, tsc, tsl, bold=False)

    # ② 詳細はインスタ (6.3〜10s)
    s2 = scene_window(t, 6.3, 10.0, fade=0.18)
    if s2 > 0:
        a1, sc1, sl1 = line_enter(t, 6.4)
        a2, sc2, sl2 = line_enter(t, 6.75)
        draw_text(draw, CY - 60, "詳細はインスタ", 80, INK, s2 * a1, sc1, sl1)
        draw_text(draw, CY + 80, "プロフィールリンクから", 52, MUTED, s2 * a2, sc2, sl2, bold=False)

    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def main() -> int:
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True)

    print(f"フレーム生成中… ({FRAMES}枚)")
    for i in range(FRAMES):
        frame = render_frame(i)
        frame.save(FRAMES_DIR / f"frame_{i:04d}.png", optimize=True)
        if i % 30 == 0:
            print(f"  {i}/{FRAMES}")

    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        print("ffmpeg が見つかりません。", file=sys.stderr)
        return 1

    subprocess.run(
        [
            ffmpeg,
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(FRAMES_DIR / "frame_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-t",
            str(DURATION),
            str(OUTPUT),
        ],
        check=True,
    )
    shutil.rmtree(FRAMES_DIR)
    print(f"完成: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
