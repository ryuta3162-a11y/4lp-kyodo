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

# 上下余白を揃え、要素間ギャップを一定にする安全領域
SAFE_TOP = 160
SAFE_BOTTOM = 1760

FPS = 30
DURATION = 30
FRAMES = FPS * DURATION
OUT_DIR = Path(__file__).resolve().parent
FRAMES_DIR = OUT_DIR / "_frames"
OUTPUT = OUT_DIR / "joyfit-signage-30s.mp4"
QR_PATH = OUT_DIR / "qr.png"

# 背景の鮮やかな赤（#C12632）
BRAND = (0xC1, 0x26, 0x32)
BRAND_DARK = (0xC1, 0x26, 0x32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY_LIGHT = (220, 220, 220)


def stack_ys(heights: list[int]) -> list[int]:
    """要素の高さを渡し、上下・要素間のギャップが等しい中心Y座標を返す。"""
    if not heights:
        return []
    total_h = sum(heights)
    free = max(0, (SAFE_BOTTOM - SAFE_TOP) - total_h)
    gap = free / (len(heights) + 1)
    ys: list[int] = []
    y = SAFE_TOP + gap
    for h in heights:
        ys.append(int(y + h / 2))
        y += h + gap
    return ys

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


def ease_in_out_cubic(t: float) -> float:
    t = clamp01(t)
    if t < 0.5:
        return 4 * t * t * t
    return 1 - pow(-2 * t + 2, 3) / 2


def clamp01(v: float) -> float:
    return max(0.0, min(1.0, v))


# 全シーン共通トランジション
TRANS_FADE = 0.42
TRANS_SLIDE = 56
TRANS_SLIDE_DUR = 0.42


def scene_alpha(t: float, start: float, end: float, fade: float = TRANS_FADE) -> float:
    if t < start or t > end:
        return 0.0
    if t < start + fade:
        return ease_in_out_cubic((t - start) / fade)
    if t > end - fade:
        return ease_in_out_cubic((end - t) / fade)
    return 1.0


def slide_y(t: float, at: float, dur: float = TRANS_SLIDE_DUR, dist: int = TRANS_SLIDE) -> int:
    if t < at:
        return dist
    return int(dist * (1 - ease_in_out_cubic(clamp01((t - at) / dur))))


def stagger_a(base_a: float, local: float, delay: float, dur: float = 0.3) -> float:
    """要素ごとの順次フェードイン（統一感のある登場）。"""
    if base_a <= 0:
        return 0.0
    return base_a * ease_out_cubic(clamp01((local - delay) / dur))


def draw_bg(img: Image.Image, t: float) -> None:
    """単色の鮮やかな赤（#C12632）＋白枠。"""
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, PW, PH], fill=BRAND)
    draw.rectangle([20, 20, PW - 20, PH - 20], outline=WHITE, width=3)


def draw_micro(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    a: float,
    sy: int = 0,
    size: int = 52,
    stroke: int = 5,
) -> None:
    """白文字＋黒縁（立体感）。"""
    if a <= 0:
        return
    alpha = int(255 * a)
    draw.text(
        (CX, y + sy), text, font=find_font(size, True),
        fill=(*WHITE, alpha), anchor="mm",
        stroke_width=stroke, stroke_fill=(*BLACK, alpha),
    )


def draw_head(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, a: float, sy: int = 0, stroke: int = 7) -> None:
    """白文字＋黒縁（立体感）。"""
    if a <= 0 or not text:
        return
    alpha = int(255 * a)
    draw.text(
        (CX, y + sy), text, font=find_font(size, True),
        fill=(*WHITE, alpha), anchor="mm",
        stroke_width=stroke, stroke_fill=(*BLACK, alpha),
    )


def draw_band(draw: ImageDraw.ImageDraw, y: int, text: str, size: int, a: float, sy: int = 0) -> None:
    """白枠の四角バナー（黒地に白文字）。"""
    if a <= 0:
        return
    font = find_font(size, True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw = bbox[2] - bbox[0]
    py = max(30, size // 2 + 12)
    alpha = int(255 * a)
    x0, y0 = CX - tw // 2 - 28, y - py + sy
    x1, y1 = CX + tw // 2 + 28, y + py + sy
    # 立体影
    draw.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(*WHITE, int(80 * a)))
    draw.rectangle([x0, y0, x1, y1], fill=(*BLACK, alpha), outline=(*WHITE, alpha), width=3)
    draw.text(
        (CX, y + sy), text, font=font, fill=(*WHITE, alpha), anchor="mm",
        stroke_width=3, stroke_fill=(*BLACK, alpha),
    )


def draw_store_badge(draw: ImageDraw.ImageDraw, y: int, a: float, sy: int = 0) -> None:
    if a <= 0:
        return
    text, font = "JOYFIT24 経堂", find_font(56, True)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="mm")
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    alpha = int(255 * a)
    x0 = CX - tw // 2 - 30
    y0 = y - th // 2 - 16 + sy
    x1 = x0 + tw + 60
    y1 = y0 + th + 32
    draw.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(*WHITE, int(90 * a)))
    draw.rectangle([x0, y0, x1, y1], fill=(*BLACK, alpha), outline=(*WHITE, alpha), width=3)
    draw.text(
        (CX, y + sy), text, font=font, fill=(*WHITE, alpha), anchor="mm",
        stroke_width=3, stroke_fill=(*BLACK, alpha),
    )


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
    band_y: int,
    center_y: int,
    qr_size: int = 460,
) -> None:
    if a <= 0:
        return
    pulse = 1.0 + 0.008 * math.sin((t - 18.5) * 3) if t > 18.5 else 1.0
    qr_size = int(qr_size * pulse)
    pad = 32
    frame_w = qr_size + pad * 2
    frame_h = qr_size + pad * 2
    fx = CX - frame_w // 2
    fy = center_y - frame_h // 2 + sy
    alpha = int(255 * a)

    draw_band(draw, band_y, "ここのQRを読み取ってね", 48, a, sy)

    frame_layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    fd = ImageDraw.Draw(frame_layer)
    # 四角・立体（白影＋白枠）
    fd.rectangle([fx + 8, fy + 8, fx + frame_w + 8, fy + frame_h + 8], fill=(255, 255, 255, int(90 * a)))
    fd.rectangle([fx, fy, fx + frame_w, fy + frame_h], fill=(255, 255, 255, alpha))
    fd.rectangle([fx + 6, fy + 6, fx + frame_w - 6, fy + frame_h - 6], outline=(0, 0, 0, alpha), width=4)
    fd.rectangle([fx + 14, fy + 14, fx + frame_w - 14, fy + frame_h - 14], outline=(0, 0, 0, int(120 * a)), width=2)

    qr = load_qr().resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qx = CX - qr_size // 2
    qy = fy + pad
    frame_layer.paste(qr, (qx, qy), qr)
    overlay.alpha_composite(frame_layer)


# ── シーン（複数要素を同時表示・均等ギャップ）────────────

def scene_open(draw, t, a, sy):
    y0, y1, y2, y3 = stack_ys([90, 220, 130, 90])
    draw_store_badge(draw, y0, a, sy)
    draw_head(draw, y1, "夏得", 190, a, sy)
    draw_head(draw, y2, "キャンペーン", 105, a, sy, stroke=5)
    draw_band(draw, y3, "7/24(金)まで · 先着15名", 54, a, sy)


def draw_strike_price(draw: ImageDraw.ImageDraw, y: int, text: str, a: float, sy: int = 0, size: int = 52) -> None:
    """通常価格（白文字＋黒縁＋取り消し線）。"""
    if a <= 0:
        return
    alpha = int(255 * a)
    font = find_font(size, True)
    draw.text(
        (CX, y + sy), text, font=font,
        fill=(*WHITE, alpha), anchor="mm",
        stroke_width=5, stroke_fill=(*BLACK, alpha),
    )
    bbox = draw.textbbox((CX, y + sy), text, font=font, anchor="mm")
    mid_y = (bbox[1] + bbox[3]) // 2
    draw.line([(bbox[0] - 10, mid_y), (bbox[2] + 10, mid_y)], fill=(*WHITE, alpha), width=5)


def draw_month_chips(overlay: Image.Image, draw: ImageDraw.ImageDraw, y: int, a: float, sy: int) -> None:
    """7〜12月を大きな四角チップで一列表示。"""
    if a <= 0:
        return
    months = ["7月", "8月", "9月", "10月", "11月", "12月"]
    margin = 48
    gap = 8
    avail = PW - margin * 2
    cell_w = (avail - gap * (len(months) - 1)) // len(months)
    chip_h = 92
    font = find_font(42, True)
    alpha = int(255 * a)
    x = margin
    layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for m in months:
        x0 = x
        y0 = y - chip_h // 2 + sy
        x1 = x0 + cell_w
        y1 = y0 + chip_h
        # 立体影（白）
        ld.rectangle([x0 + 5, y0 + 5, x1 + 5, y1 + 5], fill=(255, 255, 255, int(70 * a)))
        ld.rectangle([x0, y0, x1, y1], fill=(0, 0, 0, alpha), outline=(255, 255, 255, alpha), width=3)
        ld.text(
            (x0 + cell_w // 2, y + sy), m, font=font,
            fill=(*WHITE, alpha), anchor="mm",
            stroke_width=4, stroke_fill=(*BLACK, alpha),
        )
        x += cell_w + gap
    overlay.alpha_composite(layer)


def scene_offer(overlay: Image.Image, draw, t, a, sy):
    """夏得キャンペーン価格画面（白黒・大きめ文字・四角立体）。"""
    if a <= 0:
        return
    local = max(0.0, t - 4.0)
    pulse = 1.0 + 0.006 * math.sin(local * 3.0)

    # まだ間に合う / 夏得 / APP / 半年間 / 月 / 通常価格 / 特価
    y0, y1, y2, y3, y4, y5, y6 = stack_ys([88, 130, 72, 72, 100, 72, 360])

    a0 = stagger_a(a, local, 0.00)
    a1 = stagger_a(a, local, 0.08)
    a2 = stagger_a(a, local, 0.16)
    a3 = stagger_a(a, local, 0.24)
    a4 = stagger_a(a, local, 0.32)
    a5 = stagger_a(a, local, 0.40)
    a6 = stagger_a(a, local, 0.48)

    draw_band(draw, y0, "まだ間に合う！", 50, a0, sy)
    draw_head(draw, y1, "夏得キャンペーン！", 96, a1, sy, stroke=8)
    draw_micro(draw, y2, "APP入会最短5分　当日すぐ使える!", a2, sy, size=44, stroke=5)
    draw_micro(draw, y3, "半年間ずーっとお得", a3, sy, size=54, stroke=5)
    draw_month_chips(overlay, draw, y4, a4, sy)
    draw_strike_price(draw, y5, "通常月額9,350円(税込)", a5, sy, size=50)

    # 価格パネル（四角・立体）
    price_h = 360
    panel_w = PW - 96
    px0 = (PW - panel_w) // 2
    py0 = y6 - price_h // 2 + sy
    layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    # 白の影で立体感
    ld.rectangle(
        [px0 + 10, py0 + 10, px0 + panel_w + 10, py0 + price_h + 10],
        fill=(255, 255, 255, int(90 * a6)),
    )
    ld.rectangle(
        [px0, py0, px0 + panel_w, py0 + price_h],
        fill=(0, 0, 0, int(255 * a6)),
        outline=(255, 255, 255, int(255 * a6)),
        width=4,
    )
    # 内側の二重枠
    ld.rectangle(
        [px0 + 10, py0 + 10, px0 + panel_w - 10, py0 + price_h - 10],
        outline=(255, 255, 255, int(180 * a6)),
        width=2,
    )
    overlay.alpha_composite(layer)

    draw_head(draw, y6 - 42, "3,630", int(210 * pulse), a6, sy, stroke=10)
    draw_head(draw, y6 + 100, "円(税込)/月", 60, a6, sy, stroke=6)


def draw_area_card(
    overlay: Image.Image,
    draw: ImageDraw.ImageDraw,
    center_y: int,
    height: int,
    floor: str,
    title: str,
    lines: list[str],
    a: float,
    sy: int,
) -> None:
    """フロア紹介カード（四角・白黒・左Fボタン）。"""
    if a <= 0:
        return
    alpha = int(255 * a)
    card_w = PW - 80
    x0 = (PW - card_w) // 2
    y0 = center_y - height // 2 + sy
    y1 = y0 + height
    pad = 28

    layer = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rectangle([x0 + 6, y0 + 6, x0 + card_w + 6, y1 + 6], fill=(255, 255, 255, int(70 * a)))
    ld.rectangle([x0, y0, x0 + card_w, y1], fill=(0, 0, 0, alpha), outline=(255, 255, 255, alpha), width=3)

    # ヘッダー左：四角フロアボタン（2F / 3F）
    btn = 68
    bx0 = x0 + pad
    by0 = y0 + pad
    ld.rectangle([bx0 + 4, by0 + 4, bx0 + btn + 4, by0 + btn + 4], fill=(255, 255, 255, int(60 * a)))
    ld.rectangle([bx0, by0, bx0 + btn, by0 + btn], fill=(255, 255, 255, alpha))
    overlay.alpha_composite(layer)

    draw.text(
        (bx0 + btn // 2, by0 + btn // 2), floor, font=find_font(32, True),
        fill=(*BLACK, alpha), anchor="mm",
    )

    title_font = find_font(46 if len(title) <= 8 else 40, True)
    title_x = bx0 + btn + 20
    draw.text(
        (title_x, by0 + btn // 2), title, font=title_font,
        fill=(*WHITE, alpha), anchor="lm",
        stroke_width=4, stroke_fill=(*BLACK, alpha),
    )

    line_y = by0 + btn + 16
    draw.line(
        [(x0 + pad, line_y), (x0 + card_w - pad, line_y)],
        fill=(*WHITE, int(120 * a)),
        width=2,
    )

    body_top = line_y + 16
    body_bottom = y1 - 24
    if lines:
        step = (body_bottom - body_top) / max(1, len(lines))
        body_size = 36 if max(len(s) for s in lines) > 18 else 40
        for i, line in enumerate(lines):
            ly = int(body_top + step * (i + 0.5))
            draw.text(
                (CX, ly), line, font=find_font(body_size, True),
                fill=(*WHITE, alpha), anchor="mm",
                stroke_width=4, stroke_fill=(*BLACK, alpha),
            )


def scene_facility(overlay: Image.Image, draw, t, a, sy):
    """ジム以外のサービス紹介（見出し＋3カード）"""
    if a <= 0:
        return
    cards = [
        (
            "2F",
            "ジムエリア",
            [
                "50台以上の本格的なマシンが充実",
                "店舗スタッフが手厚くサポート",
                "サウナも無料！トレーニング後のリカバリーに是非！",
            ],
            420,
        ),
        (
            "2F",
            "ピラティスリフォーマー",
            [
                "月額3,300円(税込)",
                "4名体制。セミパーソナル型で",
                "初心者でも安心してピラティスを体験！！",
            ],
            420,
        ),
        (
            "3F",
            "ホットスタジオ",
            [
                "月額1,100円(税込)",
                "ヨガレッスンが受け放題！！",
            ],
            380,
        ),
    ]
    header_h = 100
    ys = stack_ys([header_h] + [h for *_, h in cards])
    hy = ys[0]

    draw_band(draw, hy, "JOYFIT24経堂はジム以外のサービスも充実！", 34, a, sy)

    for (floor, title, lines, height), cy in zip(cards, ys[1:]):
        draw_area_card(overlay, draw, cy, height, floor, title, lines, a, sy)


def scene_qr(overlay: Image.Image, draw, t, a, sy):
    qr_size, pad, band_h = 460, 32, 90
    frame_h = qr_size + pad * 2
    y0, y1, y2, y3, y4, y5 = stack_ys([90, 90, 70, band_h, frame_h, 70])
    draw_store_badge(draw, y0, a, sy)
    draw_head(draw, y1, "詳細はこちらをチェック", 70, a, sy, stroke=5)
    draw_micro(draw, y2, "キャンペーン内容・入会方法", a, sy, size=50)
    draw_qr_panel(overlay, draw, a, sy, t, band_y=y3, center_y=y4, qr_size=qr_size)
    draw_micro(draw, y5, "7/24(金)まで · 先着15名", a, sy, size=52)


# 尺配分（おすすめ）:
# オープニング 4秒 / 特典まとめ 7.5秒 / フロア紹介 7秒 / QR 11.5秒
TIMELINE = [
    (0.0, 4.0, scene_open, False),
    (4.0, 11.5, scene_offer, True),
    (11.5, 18.5, scene_facility, True),
    (18.5, 30.0, scene_qr, True),
]


def render_portrait_frame(t: float) -> Image.Image:
    img = Image.new("RGB", (PW, PH), BRAND)
    draw_bg(img, t)
    overlay = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for start, end, fn, use_overlay in TIMELINE:
        # 最終シーンはフェードアウトせず、他は同一のクロスフェード
        if end >= DURATION:
            if t < start:
                alpha = 0.0
            elif t < start + TRANS_FADE:
                alpha = ease_in_out_cubic((t - start) / TRANS_FADE)
            else:
                alpha = 1.0
        else:
            alpha = scene_alpha(t, start, end, fade=TRANS_FADE)
        if alpha > 0:
            # 全シーン共通: 下からすっと上がるスライド＋フェード
            sy = slide_y(t, start, TRANS_SLIDE_DUR, TRANS_SLIDE) if t < start + TRANS_SLIDE_DUR else 0
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
