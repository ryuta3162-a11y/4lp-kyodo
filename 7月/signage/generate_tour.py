"""
入口サイネージ：見学・体験無料（15秒）

30秒キャンペーンと同じデザイン。
文言はフリートライアルLP（24-kyodo-freetrial）＋スタッフ時間は看板用指定値。
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import generate as g

FPS = 30
DURATION = 15
FRAMES = FPS * DURATION
OUT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = OUT_DIR / "_frames_tour"
OUTPUT = OUT_DIR / "joyfit-signage-tour.mp4"


def draw_square_panel(
    overlay: Image.Image,
    center_y: int,
    height: int,
    a: float,
    sy: int,
) -> tuple[int, int, int, int]:
    """四角パネルを描き、(x0, y0, x1, y1) を返す。"""
    card_w = g.PW - 80
    x0 = (g.PW - card_w) // 2
    y0 = center_y - height // 2 + sy
    y1 = y0 + height
    if a <= 0:
        return x0, y0, x0 + card_w, y1
    alpha = int(255 * a)
    layer = Image.new("RGBA", (g.PW, g.PH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x0 + 8, y0 + 8, x0 + card_w + 8, y1 + 8], fill=(255, 255, 255, int(80 * a)))
    ld.rectangle(
        [x0, y0, x0 + card_w, y1],
        fill=(0, 0, 0, alpha),
        outline=(255, 255, 255, alpha),
        width=3,
    )
    overlay.alpha_composite(layer)
    return x0, y0, x0 + card_w, y1


def scene_value(overlay: Image.Image, draw, t, a, sy):
    """見学・体験（利用ルールをシンプルに大きく）。"""
    if a <= 0:
        return
    local = max(0.0, t - 0.0)
    # バッジ / 見出し / サブ / すぐ使える / ルールパネル
    y0, y1, y2, y3, y4 = g.stack_ys([84, 100, 56, 100, 700])

    a0 = g.stagger_a(a, local, 0.00)
    a1 = g.stagger_a(a, local, 0.06)
    a2 = g.stagger_a(a, local, 0.12)
    a3 = g.stagger_a(a, local, 0.18)
    a4 = g.stagger_a(a, local, 0.24)

    g.draw_store_badge(draw, y0, a0, sy)
    g.draw_head(draw, y1, "ジム無料見学・体験", 74, a1, sy, stroke=7)
    g.draw_micro(draw, y2, "24時間ジムを無料で見学・体験できます", a2, sy, size=38)
    g.draw_band(draw, y3, "すぐ使える!!", 56, a3, sy)

    # ルールは中央揃え＋区切り線（ラベル列をやめてすっきり）
    rules = [
        "ご利用は運動に適していればOK！",
        "土足利用OK　サンダルNG",
        "2階ジムエリアのみ",
        "3階ホットスタジオの体験は出来ません",
    ]
    x0, top, x1, bot = draw_square_panel(overlay, y4, 700, a4, sy)
    if a4 > 0:
        alpha = int(255 * a4)
        pad_top, pad_bot = 28, 28
        area_top = top + pad_top
        area_bot = bot - pad_bot
        step = (area_bot - area_top) / len(rules)
        for i, text in enumerate(rules):
            cy = int(area_top + step * (i + 0.5))
            # 行間の細い区切り
            if i > 0:
                ly = int(area_top + step * i)
                draw.line(
                    [(x0 + 48, ly), (x1 - 48, ly)],
                    fill=(*g.WHITE, int(55 * a4)),
                    width=2,
                )
            size = 40 if len(text) > 16 else 44
            draw.text(
                (g.CX, cy), text, font=g.find_font(size, True),
                fill=(*g.WHITE, alpha), anchor="mm",
                stroke_width=5, stroke_fill=(*g.BLACK, alpha),
            )


def scene_visit(overlay: Image.Image, draw, t, a, sy):
    """来店方法＋スタッフ時間。"""
    if a <= 0:
        return
    local = max(0.0, t - 7.5)
    y0, y1, y2, y3, y4 = g.stack_ys([84, 80, 96, 560, 80])

    a0 = g.stagger_a(a, local, 0.00)
    a1 = g.stagger_a(a, local, 0.06)
    a2 = g.stagger_a(a, local, 0.12)
    a3 = g.stagger_a(a, local, 0.18)
    a4 = g.stagger_a(a, local, 0.24)

    g.draw_store_badge(draw, y0, a0, sy)
    g.draw_micro(draw, y1, "ご来店の際は", a1, sy, size=48)
    g.draw_band(draw, y2, "入口インターホンを押してください", 42, a2, sy)

    x0, top, x1, bot = draw_square_panel(overlay, y3, 560, a3, sy)
    if a3 > 0:
        alpha = int(255 * a3)
        # タイトル
        title = "スタッフ常駐時間"
        tfont = g.find_font(42, True)
        tbb = draw.textbbox((0, 0), title, font=tfont, anchor="mm")
        tw = tbb[2] - tbb[0]
        ty = top + 56
        draw.rectangle(
            [g.CX - tw // 2 - 28, ty - 30, g.CX + tw // 2 + 28, ty + 30],
            fill=(*g.WHITE, alpha),
        )
        draw.text((g.CX, ty), title, font=tfont, fill=(*g.BLACK, alpha), anchor="mm")

        hours = [
            ("平日", "10:00 〜 21:00"),
            ("土日祝", "12:00 〜 20:00"),
        ]
        hy0 = ty + 70
        hy1 = bot - 120
        step = (hy1 - hy0) / len(hours)
        for i, (label, time) in enumerate(hours):
            cy = int(hy0 + step * (i + 0.5))
            draw.text(
                (g.CX - 200, cy), label, font=g.find_font(40, True),
                fill=(*g.WHITE, alpha), anchor="mm",
                stroke_width=4, stroke_fill=(*g.BLACK, alpha),
            )
            draw.text(
                (g.CX + 80, cy), time, font=g.find_font(46, True),
                fill=(*g.WHITE, alpha), anchor="mm",
                stroke_width=5, stroke_fill=(*g.BLACK, alpha),
            )

        note_y = bot - 56
        draw.line([(x0 + 48, note_y - 36), (x1 - 48, note_y - 36)], fill=(*g.WHITE, int(55 * a3)), width=2)
        draw.text(
            (g.CX, note_y), "※毎週 月・木は終日スタッフ不在",
            font=g.find_font(36, True),
            fill=(*g.WHITE, alpha), anchor="mm",
            stroke_width=4, stroke_fill=(*g.BLACK, alpha),
        )

    g.draw_micro(draw, y4, "まずは気軽にチェック！", a4, sy, size=46)


TIMELINE = [
    (0.0, 7.5, scene_value, True),
    (7.5, 15.0, scene_visit, True),
]


def render_portrait_frame(t: float) -> Image.Image:
    img = Image.new("RGB", (g.PW, g.PH), g.BRAND)
    g.draw_bg(img, t)
    overlay = Image.new("RGBA", (g.PW, g.PH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for start, end, fn, use_overlay in TIMELINE:
        if end >= DURATION:
            if t < start:
                alpha = 0.0
            elif t < start + g.TRANS_FADE:
                alpha = g.ease_in_out_cubic((t - start) / g.TRANS_FADE)
            else:
                alpha = 1.0
        else:
            alpha = g.scene_alpha(t, start, end, fade=g.TRANS_FADE)
        if alpha > 0:
            sy = g.slide_y(t, start, g.TRANS_SLIDE_DUR, g.TRANS_SLIDE) if t < start + g.TRANS_SLIDE_DUR else 0
            if use_overlay:
                fn(overlay, draw, t, alpha, sy)
            else:
                fn(draw, t, alpha, sy)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")


def render_frame(frame_idx: int) -> Image.Image:
    return render_portrait_frame(frame_idx / FPS).rotate(90, expand=True, resample=Image.Resampling.BICUBIC)


def main() -> int:
    if FRAMES_DIR.exists():
        shutil.rmtree(FRAMES_DIR)
    FRAMES_DIR.mkdir(parents=True)

    print(f"見学・体験動画を生成中… {DURATION}秒 / {FRAMES}枚")
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
