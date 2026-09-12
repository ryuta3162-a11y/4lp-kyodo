"""A4印刷用HTMLを高解像度PNG/PDFに書き出す。"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent

# A4 @ 300dpi ≈ 2480 × 3508
TARGET_W = 2480

JOBS = [
    ("index.html", "joyfit-options-a4-300dpi.png", "joyfit-options-a4.pdf"),
    ("back.html", "joyfit-app-qa-a4-300dpi.png", "joyfit-app-qa-a4.pdf"),
]


def export_one(browser, html_name: str, out_png: Path, out_pdf: Path) -> None:
    html = ROOT / html_name
    url = html.as_uri()

    probe = browser.new_page(viewport={"width": 1200, "height": 1700}, device_scale_factor=1)
    probe.goto(url, wait_until="networkidle")
    probe.evaluate(
        """() => {
          document.body.style.background = '#fff';
          document.body.style.margin = '0';
          const s = document.getElementById('sheet');
          s.style.margin = '0';
          s.style.boxShadow = 'none';
        }"""
    )
    box = probe.locator("#sheet").bounding_box()
    probe.close()
    if not box:
        raise RuntimeError(f"sheet not found in {html_name}")

    scale = TARGET_W / box["width"]
    context = browser.new_context(
        viewport={"width": int(box["width"]) + 2, "height": int(box["height"]) + 2},
        device_scale_factor=scale,
    )
    page = context.new_page()
    page.goto(url, wait_until="networkidle")
    page.evaluate(
        """() => {
          document.body.style.background = '#fff';
          document.body.style.margin = '0';
          const s = document.getElementById('sheet');
          s.style.margin = '0';
          s.style.boxShadow = 'none';
        }"""
    )
    page.wait_for_timeout(1000)
    page.locator("#sheet").screenshot(path=str(out_png), type="png")
    page.pdf(
        path=str(out_pdf),
        width="210mm",
        height="297mm",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
    )
    context.close()


def main() -> None:
    from PIL import Image

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html_name, png_name, pdf_name in JOBS:
            out_png = ROOT / png_name
            out_pdf = ROOT / pdf_name
            export_one(browser, html_name, out_png, out_pdf)
            img = Image.open(out_png)
            print(
                f"Wrote {png_name}  {img.size[0]}x{img.size[1]}  "
                f"{out_png.stat().st_size // 1024} KB"
            )
            print(f"Wrote {pdf_name}  {out_pdf.stat().st_size // 1024} KB")
        browser.close()


if __name__ == "__main__":
    main()
