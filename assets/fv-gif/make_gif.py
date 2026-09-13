"""Premium FV GIF: gold shimmer, full CTA pulse, reinforced comma."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parent
FRAME_MS = 40
PRICE_BOX = (90, 540, 995, 830)
CTA_BOX = (200, 915, 1020, 1125)


def load_rgb(name: str) -> Image.Image:
    return Image.open(ROOT / name).convert("RGB")


def extract_layer(full: Image.Image, base: Image.Image, y_min: int, y_max: int, pad: int = 24, thresh: int = 12):
    a = np.array(full.convert("RGB"))
    b = np.array(base.convert("RGB"))
    diff = np.abs(a.astype(np.int16) - b.astype(np.int16)).sum(axis=2)
    mask = diff > thresh
    mask[:y_min, :] = False
    mask[y_max:, :] = False
    alpha = np.clip((diff - (thresh - 4)) * 18, 0, 255).astype(np.uint8)
    alpha[~mask] = 0
    alpha = np.array(Image.fromarray(alpha, "L").filter(ImageFilter.MaxFilter(5)))
    alpha[diff <= 3] = 0
    layer = Image.fromarray(np.dstack([a, alpha]), "RGBA")
    ys, xs = np.where(alpha > 0)
    bbox = (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(a.shape[1], int(xs.max()) + 1 + pad),
        min(a.shape[0], int(ys.max()) + 1 + pad),
    )
    return layer.crop(bbox), bbox


def reinforce_comma(plate: Image.Image, box) -> Image.Image:
    """Draw a clear comma tail so the bottom is always visible."""
    arr = np.array(plate)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    red = (r > 140) & (r > g + 35) & (r > b + 35) & (g < 140)
    x0, y0 = box[0], box[1]
    zx0, zx1 = max(0, 330 - x0), min(arr.shape[1], 420 - x0)
    zy0, zy1 = max(0, 720 - y0), min(arr.shape[0], 820 - y0)
    zone = red[zy0:zy1, zx0:zx1]
    ys, xs = np.where(zone)
    if len(xs) == 0:
        return plate
    cx = int(xs.mean()) + zx0
    cy = int(np.percentile(ys, 30)) + zy0
    color = tuple(int(v) for v in arr[cy, cx])
    out = plate.copy()
    draw = ImageDraw.Draw(out)
    # cover old short comma then redraw fuller one
    draw.ellipse((cx - 11, cy - 7, cx + 13, cy + 14), fill=color)
    draw.polygon(
        [
            (cx + 2, cy + 8),
            (cx + 10, cy + 6),
            (cx + 1, cy + 26),
            (cx - 10, cy + 44),
            (cx - 16, cy + 46),
            (cx - 14, cy + 40),
            (cx - 4, cy + 22),
        ],
        fill=color,
    )
    return out


def price_rgb_plate(full: Image.Image, box=PRICE_BOX):
    plate = full.crop(box).convert("RGB")
    plate = reinforce_comma(plate, box)
    return plate, box


def ease_out_quart(t: float) -> float:
    return 1 - (1 - t) ** 4


def ease_in_out_cubic(t: float) -> float:
    if t < 0.5:
        return 4 * t * t * t
    return 1 - (-2 * t + 2) ** 3 / 2


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def paste_rgb(canvas: Image.Image, plate: Image.Image, xy, opacity: float = 1.0) -> Image.Image:
    out = canvas.copy()
    x, y = int(round(xy[0])), int(round(xy[1]))
    if opacity >= 0.999:
        out.paste(plate, (x, y))
        return out
    base = out.crop((x, y, x + plate.size[0], y + plate.size[1])).convert("RGB")
    blended = Image.blend(base, plate, max(0.0, min(1.0, opacity)))
    out.paste(blended, (x, y))
    return out


def paste_layer(canvas_rgb: Image.Image, layer: Image.Image, xy, opacity: float = 1.0) -> Image.Image:
    out = canvas_rgb.convert("RGBA")
    if opacity <= 0.001:
        return out.convert("RGB")
    overlay = layer
    if opacity < 0.999:
        arr = np.array(overlay).astype(np.float32)
        arr[..., 3] *= max(0.0, min(1.0, opacity))
        overlay = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGBA")
    out.paste(overlay, (int(round(xy[0])), int(round(xy[1]))), overlay)
    return out.convert("RGB")


def add_price_glow(frame: Image.Image, box, strength: float) -> Image.Image:
    """Gold glow only (no red / pink)."""
    if strength <= 0.01:
        return frame
    out = frame.convert("RGBA")
    x0, y0, x1, y1 = box
    glow = Image.new("RGBA", out.size, (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    pad = int(36 + 26 * strength)
    g.ellipse((x0 - pad, y0 - pad // 2, x1 + pad, y1 + pad // 2), fill=(255, 205, 70, int(52 * strength)))
    glow = glow.filter(ImageFilter.GaussianBlur(32))
    return Image.alpha_composite(out, glow).convert("RGB")


def apply_shimmer_rgb(plate: Image.Image, progress: float, intensity: float = 1.0) -> Image.Image:
    """Gold kiraaan sweep."""
    arr = np.array(plate).astype(np.float32)
    h, w = arr.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    cx = lerp(-0.35 * w, 1.35 * w, progress)
    dist = ((xx - cx) + (yy - h * 0.4) * 0.45) / max(w * 0.08, 1)
    band = np.exp(-(dist ** 2))
    cx2 = lerp(-0.2 * w, 1.2 * w, (progress + 0.2) % 1.0)
    dist2 = ((xx - cx2) + (yy - h * 0.55) * 0.35) / max(w * 0.14, 1)
    band2 = np.exp(-(dist2 ** 2)) * 0.65
    boost = (band + band2) * (120 * intensity)
    arr[..., 0] = np.clip(arr[..., 0] + boost * 1.2, 0, 255)
    arr[..., 1] = np.clip(arr[..., 1] + boost * 0.95, 0, 255)
    arr[..., 2] = np.clip(arr[..., 2] + boost * 0.22, 0, 255)
    arr = np.clip(arr + band[..., None] * 8 * intensity, 0, 255)
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def draw_sparkles(frame: Image.Image, progress: float, box) -> Image.Image:
    out = frame.convert("RGBA")
    draw = ImageDraw.Draw(out)
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(7)
    pts = [(int(rng.integers(x0 + 20, x1 - 20)), int(rng.integers(y0 + 10, y1 - 10))) for _ in range(36)]
    pts += [
        (x0 + 30, y0 + 25), (x1 - 40, y0 + 30), (x0 + 80, y1 - 25), (x1 - 70, y1 - 30),
        ((x0 + x1) // 2, y0 + 8), ((x0 + x1) // 2, y1 - 12),
    ]
    for i, (x, y) in enumerate(pts):
        phase = (progress * 1.4 + i * 0.11) % 1.0
        bright = abs(np.sin(phase * np.pi)) ** 0.7
        if bright < 0.2:
            continue
        s = 2 + int(5 * bright)
        c = (255, 230, 120, int(240 * bright)) if i % 2 else (255, 245, 190, int(210 * bright))
        draw.line((x - s, y, x + s, y), fill=c, width=2)
        draw.line((x, y - s, x, y + s), fill=c, width=2)
        if bright > 0.6:
            draw.line((x - s // 2, y - s // 2, x + s // 2, y + s // 2), fill=c, width=1)
            draw.line((x - s // 2, y + s // 2, x + s // 2, y - s // 2), fill=c, width=1)
    return out.convert("RGB")


def grow_cta(full: Image.Image, amount: float) -> Image.Image:
    """Pulse entire CTA including right side of プ. Clear ghosts first."""
    x0, y0, x1, y1 = CTA_BOX
    region = full.crop((x0, y0, x1, y1))
    scale = lerp(1.0, 1.11, amount)
    w, h = region.size
    grown = region.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    grown = ImageEnhance.Brightness(grown).enhance(1.0 + 0.06 * amount)

    out = full.copy()
    red = tuple(int(v) for v in np.array(full)[1100, 540])
    draw = ImageDraw.Draw(out)
    # wipe old button completely (prevents right-edge remnant)
    draw.rectangle((x0 - 8, y0 - 4, x1 + 8, 970), fill=(255, 255, 255))
    draw.rectangle((x0 - 8, 971, x1 + 8, y1 + 4), fill=red)

    gx = x0 - (grown.size[0] - w) // 2
    gy = y0 - (grown.size[1] - h) // 2
    out.paste(grown, (gx, gy))
    return out


def push(seq: list, durations: list, im: Image.Image, ms: int):
    n = max(1, int(round(ms / FRAME_MS)))
    for _ in range(n):
        seq.append(im.copy())
        durations.append(FRAME_MS)


def compose_price(base, plate, box, opacity, shimmer_t, sparkle_t, glow):
    px0, py0, _, _ = box
    plate_use = apply_shimmer_rgb(plate, shimmer_t, 1.35) if shimmer_t is not None else plate
    frame = paste_rgb(base, plate_use, (px0, py0), opacity)
    frame = add_price_glow(frame, box, glow * opacity)
    if sparkle_t is not None and opacity > 0.5:
        frame = draw_sparkles(frame, sparkle_t, box)
    return frame


def main():
    stage = load_rgb("3.png")
    with_text = load_rgb("2.png")
    full = load_rgb("1.png")

    text_layer, text_bbox = extract_layer(with_text, stage, 300, 510, pad=20)
    price_plate, price_box = price_rgb_plate(full)
    tx0, ty0, _, _ = text_bbox

    frames: list[Image.Image] = []
    durations: list[int] = []

    push(frames, durations, full, 600)

    for i in range(6):
        t = ease_in_out_cubic((i + 1) / 6)
        empty = with_text.crop(price_box)
        blended = Image.blend(price_plate, empty, t)
        frame = paste_layer(stage, text_layer, (tx0, ty0), 1.0 - t)
        frame.paste(blended, (price_box[0], price_box[1]))
        push(frames, durations, frame, FRAME_MS)

    push(frames, durations, stage, 100)

    for i in range(11):
        t = ease_out_quart((i + 1) / 11)
        y = lerp(ty0 + 12, ty0, t)
        push(frames, durations, paste_layer(stage, text_layer, (tx0, y), t), FRAME_MS)

    push(frames, durations, with_text, 150)

    for i in range(14):
        t = ease_out_quart((i + 1) / 14)
        shimmer = t * 0.9 if t > 0.25 else None
        sparkle = t if t > 0.4 else None
        frame = compose_price(with_text, price_plate, price_box, t, shimmer, sparkle, 0.4 + 0.85 * t)
        push(frames, durations, frame, FRAME_MS)

    for pass_i in range(2):
        for i in range(12):
            t = i / 11
            glow = 0.75 + 0.45 * abs(np.sin(t * np.pi))
            frame = compose_price(with_text, price_plate, price_box, 1.0, t, t + pass_i * 0.2, glow)
            if 0.4 < t < 0.7:
                frame = ImageEnhance.Brightness(frame).enhance(1.03)
            push(frames, durations, frame, FRAME_MS)

    push(frames, durations, full, 300)

    for _ in range(2):
        for i in range(9):
            t = ease_in_out_cubic(i / 8)
            push(frames, durations, grow_cta(full, float(np.sin(t * np.pi))), FRAME_MS)
        push(frames, durations, full, 160)

    for i in range(10):
        t = i / 9
        frame = compose_price(with_text, price_plate, price_box, 1.0, t, t, 0.65)
        frame.paste(full.crop((0, 850, 1080, 1180)), (0, 850))
        frame.paste(full.crop((0, 0, 1080, 200)), (0, 0))
        push(frames, durations, frame, FRAME_MS)

    push(frames, durations, full, 900)

    out = ROOT / "kyodo-fv-3300.gif"
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
        disposal=2,
    )
    price_plate.save(ROOT / "_debug-price-layer.png")
    print(f"wrote {out} ({out.stat().st_size:,} bytes, {len(frames)} frames)")


if __name__ == "__main__":
    main()
