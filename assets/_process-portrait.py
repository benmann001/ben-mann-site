"""
Re-grade Ben's portrait for the dark/chartreuse theme.

1. Remove the dark studio background via rembg
2. Cool / desaturate the subject (mute the red rim, deepen contrast)
3. Composite onto a dark midnight background with a soft chartreuse halo
   placed behind the head
4. Save back to ben-portrait.png (original is preserved as a backup)
"""

import os
from rembg import remove
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

ASSETS = "/Users/Ben/Desktop/ben-mann-site-v2/assets"
INPUT  = f"{ASSETS}/ben-mann-portrait.png"
OUTPUT = f"{ASSETS}/ben-mann-portrait.png"
BACKUP = f"{ASSETS}/ben-mann-portrait-original.png"

# Brand palette
PAGE_BG  = (10, 14, 23, 255)      # #0A0E17 midnight
ACCENT   = (205, 244, 74)         # #CDF44A chartreuse


def main():
    # Always work from the original (idempotent re-runs)
    if os.path.exists(BACKUP):
        print(f"• Using backed-up original ({BACKUP})")
        src = Image.open(BACKUP).convert("RGBA")
    else:
        print(f"• First run — backing up {INPUT} → {BACKUP}")
        src = Image.open(INPUT).convert("RGBA")
        src.save(BACKUP, "PNG")

    W, H = src.size
    print(f"• Source size: {W}×{H}")

    # 1. Remove background (downloads u2net model on first run, ~170MB)
    print("• Removing background...")
    cutout = remove(src)
    print("  ✓ background removed")

    # 2. Cool colour grade on the subject
    r, g, b, a = cutout.split()
    r = r.point(lambda v: int(v * 0.82))             # mute the warm rim
    g = g.point(lambda v: int(v * 0.97))             # very slight green pull
    b = b.point(lambda v: min(255, int(v * 1.06)))   # lift the cool side
    graded = Image.merge("RGBA", (r, g, b, a))

    rgb = graded.convert("RGB")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.10)   # crisper
    rgb = ImageEnhance.Color(rgb).enhance(0.80)      # desaturate (modern tone)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.96) # ease the highlights
    graded = Image.merge("RGBA", (*rgb.split(), a))
    print("  ✓ cool grade applied")

    # 3. New background: midnight + soft chartreuse halo behind the head
    bg = Image.new("RGBA", (W, H), PAGE_BG)

    bbox = graded.getbbox()
    if bbox:
        cx = (bbox[0] + bbox[2]) // 2
        cy = bbox[1] + (bbox[3] - bbox[1]) // 6   # halo over the upper area
    else:
        cx, cy = W // 2, H // 4

    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    max_r = int(min(W, H) * 0.55)
    for ring_r in range(max_r, 0, -6):
        fade = ring_r / max_r
        alpha_val = max(0, int(75 * (1 - fade)))
        draw.ellipse(
            [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
            fill=(*ACCENT, alpha_val),
        )
    glow = glow.filter(ImageFilter.GaussianBlur(radius=85))
    bg = Image.alpha_composite(bg, glow)
    print("  ✓ chartreuse halo composited")

    # 4. Composite subject onto new background
    result = Image.alpha_composite(bg, graded)

    # 5. Save (RGB, optimized)
    result.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(f"✓ Saved → {OUTPUT} ({os.path.getsize(OUTPUT) // 1024} KB)")


if __name__ == "__main__":
    main()
