#!/usr/bin/env python3
"""
render_design.py — turn any t-shirt design SVG into a print-ready PNG + preview.

Usage:
  python3 render_design.py path/to/design.svg [output_dir]

Produces:
  <output_dir>/<name>.png          4500x5400, transparent — Printify/Etsy upload spec
  <output_dir>/preview_<name>.jpg  small dark-shirt preview for visual verification

Why the preview matters: text-path designs overflow silently. ALWAYS open the
preview image and look at it before publishing — check that no text is cut off
at the canvas edges and nothing overlaps. Fix the SVG and re-render if so.
"""
import os, sys, subprocess, shutil

W, H = 4500, 5400

def find_chromium():
    for c in ("/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"):
        p = shutil.which(c) or (c if os.path.exists(c) else None)
        if p:
            return p
    # playwright-managed browser
    for root in ("/ms-playwright", os.path.expanduser("~/.cache/ms-playwright")):
        if os.path.isdir(root):
            for d in sorted(os.listdir(root)):
                cand = os.path.join(root, d, "chrome-linux", "chrome")
                if os.path.exists(cand):
                    return cand
    raise SystemExit("chromium not found — install a headless chromium first")

def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    svg = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.dirname(svg)
    os.makedirs(out_dir, exist_ok=True)
    name = os.path.splitext(os.path.basename(svg))[0]
    png = os.path.join(out_dir, name + ".png")

    subprocess.run([find_chromium(), "--headless", "--no-sandbox", "--disable-gpu",
                    "--default-background-color=00000000", f"--window-size={W},{H}",
                    f"--screenshot={png}", f"file://{svg}"], check=True, capture_output=True)

    from PIL import Image
    im = Image.open(png)
    assert im.size == (W, H), f"unexpected size {im.size}"
    prev = im.copy(); prev.thumbnail((700, 840))
    bg = Image.new("RGB", prev.size, (40, 42, 54))
    bg.paste(prev, mask=prev.split()[3])
    prev_path = os.path.join(out_dir, f"preview_{name}.jpg")
    bg.save(prev_path, quality=88)
    print(png)
    print(prev_path)

if __name__ == "__main__":
    main()
