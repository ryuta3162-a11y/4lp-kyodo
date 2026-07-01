"""
Instagramストーリー用 10秒動画（1080x1920）
実行: python generate.py → joyfit-story-10s.mp4
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

BRAND = (194, 22, 50)
BRAND_DEEP = (154, 16, 40)
GOLD = (248, 231, 28)
WHITE = (255, 255, 255)


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    size = max(12, int(size))
    if bold:
        candidates = [
            r"C:\Windows\Fonts\meiryob.ttc",
            r"C:\Windows\Fonts\YuGothB.ttc",
            r"C:\Windows\Fonts\msgothic.ttc",
            r"C:\Windows\Fonts\meiryo.ttc",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\meiryo.ttc",
            r"C:\Windows\Fonts\YuGothM.ttc",
            r"C:\Windows\Fonts\msgothic.ttc",
        ]
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


def ease_in_out(t: float) -> float:
    return 3 * t * t - 2 * t * t * t if t < 1 else 1.0


def scene_window(t: float, start: float, end: float, fade: float = 0.28) -> float:
    if t < start or t > end:
        return 0.0
    if t < start + fade:
        return ease_out_cubic((t - start) / fade)
    if t > end - fade:
        return ease_out_cubic((end - t) / fade)
    return 1.0


def line_enter(t: float, at: float, dur: float = 0.32) -> tuple[float, float, int]:
    """alpha, scale, slide_y"""
    if t < at:
        return 0.0, 0.75, 48
    p = min(1.0, (t - at) / dur)
    e = ease_out_back(p)
    return e, 0.75 + 0.25 * e, int(48 * (1 - e))


def draw_bg(img: Image.Image, t: float) -> None:
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(BRAND[0] + (BRAND_DEEP[0] - BRAND[0]) * ratio)
        g = int(BRAND[1] + (BRAND_DEEP[1] - BRAND[1]) * ratio)
        b = int(BRAND[2] + (BRAND_DEEP[2] - BRAND[2]) * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    pulse = 0.5 + 0.5 * math.sin(t * 2.2)
    orbs = [
        (200 + 40 * math.sin(t * 1.1), 320 + 30 * math.cos(t * 0.9), 280, int(38 * pulse)),
        (W - 180 + 35 * math.cos(t * 1.3), 520 + 25 * math.sin(t * 1.0), 240, int(32 * pulse)),
        (CX + 50 * math.sin(t * 0.7), H - 400 + 40 * math.cos(t * 0.8), 320, int(28 * pulse)),
    ]
    for ox, oy, radius, alpha in orbs:
        od.ellipse([ox - radius, oy - radius, ox + radius, oy + radius], fill=(248, 231, 28, alpha))

    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))

    draw = ImageDraw.Draw(img)
    margin = 40
    draw.rectangle([margin, margin, W - margin, H - margin], outline=(255, 255, 255, 90), width=3)
    draw.rectangle([margin + 10, margin + 10, W - margin - 10, H - margin - 10], outline=(212, 175, 55, 140), width=2)

    sweep_x = int((t / DURATION) * (W + 400)) - 200
    shine = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shine)
    sd.polygon([(sweep_x - 80, 0), (sweep_x + 40, 0), (sweep_x - 200, H), (sweep_x - 320, H)], fill=(255, 255, 255, 18))
    img.paste(Image.alpha_composite(img.convert("RGBA"), shine).convert("RGB"))


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
    stroke: int = 6,
) -> None:
    if alpha <= 0 or not text:
        return
    font = find_font(int(base_size * scale), bold=bold)
    a = int(255 * alpha)
    draw.text(
        (CX, y + slide),
        text,
        font=font,
        fill=(*color, a),
        anchor="mm",
        stroke_width=stroke,
        stroke_fill=(0, 0, 0, int(170 * alpha)),
    )


def draw_store_badge(draw: ImageDraw.ImageDraw, y: int, alpha: float, scale: float, slide: int) -> None:
    if alpha <= 0:
        return
    text = "JOYFIT24 経堂"
    font = find_font(int(64 * scale), bold=True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pad_x, pad_y = 48, 22
    rx = CX - tw // 2 - pad_x
    ry = y + slide - th // 2 - pad_y
    rw = tw + pad_x * 2
    rh = th + pad_y * 2
    a = int(255 * alpha)
    draw.rounded_rectangle([rx, ry, rx + rw, ry + rh], radius=20, fill=(255, 255, 255, a))
    draw.text(
        (CX, y + slide),
        text,
        font=font,
        fill=(*BRAND, a),
        anchor="mm",
    )


def render_frame(frame_idx: int) -> Image.Image:
    t = frame_idx / FPS
    img = Image.new("RGB", (W, H), BRAND)
    draw_bg(img, t)
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # --- Scene 1: タイトル (0〜2.2s) ---
    s1 = scene_window(t, 0.0, 2.2)
    if s1 > 0:
        a1, sc1, sl1 = line_enter(t, 0.05)
        a2, sc2, sl2 = line_enter(t, 0.35)
        draw_text(draw, CY - 100, "まだ間に合う！", 110, WHITE, s1 * a1, sc1, sl1)
        draw_text(draw, CY + 50, "夏得キャンペーン！", 120, GOLD, s1 * a2, sc2, sl2)

    # --- Scene 2: 価格 (2.0〜4.8s) ---
    s2 = scene_window(t, 2.0, 4.8)
    if s2 > 0:
        a_c, sc_c, sl_c = line_enter(t, 2.05)
        a_p, sc_p, sl_p = line_enter(t, 2.35)
        a_u1, sc_u1, sl_u1 = line_enter(t, 2.65)
        a_u2, sc_u2, sl_u2 = line_enter(t, 2.85)
        zoom = 1.0 + 0.04 * math.sin((t - 2.35) * 8) if t > 2.35 else 1.0
        draw_text(draw, CY - 220, "半年間ずーっとお得", 84, GOLD, s2 * a_c, sc_c, sl_c)
        draw_text(draw, CY + 10, "3,630", 300, WHITE, s2 * a_p, sc_p * zoom, sl_p, stroke=10)
        draw_text(draw, CY + 210, "円(税込)/月", 70, WHITE, s2 * a_u1, sc_u1, sl_u1, stroke=4)
        draw_text(draw, CY + 300, "7〜12月", 70, WHITE, s2 * a_u2, sc_u2, sl_u2, stroke=4)

    # --- Scene 3: オプション (4.6〜6.8s) ---
    s3 = scene_window(t, 4.6, 6.8)
    if s3 > 0:
        a1, sc1, sl1 = line_enter(t, 4.65)
        a2, sc2, sl2 = line_enter(t, 4.95)
        a3, sc3, sl3 = line_enter(t, 5.25)
        pulse = 1.0 + 0.03 * math.sin((t - 4.95) * 10) if t > 4.95 else 1.0
        draw_text(draw, CY - 170, "7月オプション", 102, WHITE, s3 * a1, sc1, sl1)
        draw_text(draw, CY + 50, "0円", 280, GOLD, s3 * a2, sc2 * pulse, sl2, stroke=10)
        draw_text(draw, CY + 250, "無料オプション8つ", 58, WHITE, s3 * a3, sc3, sl3, stroke=4)
        draw_text(draw, CY + 330, "自動契約", 58, WHITE, s3 * a3, sc3, sl3 + 8, stroke=4)

    # --- Scene 4: 締切 (6.6〜8.5s) ---
    s4 = scene_window(t, 6.6, 8.5)
    if s4 > 0:
        a1, sc1, sl1 = line_enter(t, 6.65)
        a2, sc2, sl2 = line_enter(t, 7.0)
        draw_text(draw, CY - 70, "7/12(日)まで限定", 100, WHITE, s4 * a1, sc1, sl1)
        draw_text(draw, CY + 110, "先着20名様", 88, GOLD, s4 * a2, sc2, sl2)

    # --- Scene 5: CTA (8.4〜10s) ---
    s5 = scene_window(t, 8.4, 10.0, fade=0.22)
    if s5 > 0:
        a1, sc1, sl1 = line_enter(t, 8.45)
        a2, sc2, sl2 = line_enter(t, 8.75)
        a3, sc3, sl3 = line_enter(t, 9.05)
        draw_text(draw, CY - 120, "詳細はインスタ", 82, WHITE, s5 * a1, sc1, sl1)
        draw_text(draw, CY - 10, "プロフィールリンクから", 72, GOLD, s5 * a2, sc2, sl2)
        draw_store_badge(draw, CY + 150, s5 * a3, sc3, sl3)

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

    subprocess.run([
        ffmpeg, "-y",
        "-framerate", str(FPS),
        "-i", str(FRAMES_DIR / "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-t", str(DURATION),
        str(OUTPUT),
    ], check=True)
    shutil.rmtree(FRAMES_DIR)
    print(f"完成: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
