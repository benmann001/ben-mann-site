"""
Brand-edit ben-mann-photo.jpeg:

1. Strip the beach/driftwood background via rembg
2. Recolour the maroon Nixon hat to brand chartreuse, preserving fabric shading
   (HSV hue shift, not a flat fill — keeps highlights/shadows)
3. Detect the white Nixon triangle on the hat, paint it over with the new
   chartreuse hat colour
4. Composite the website's geometric 'b' monogram at that spot, in dark ink
   (mirrors the favicon / nav mark)
5. Place the result on the brand midnight background with a soft chartreuse
   halo behind the head

The original is preserved as ben-mann-photo-original.jpeg so the script is
idempotent — re-running always works from the untouched source.
"""

import os
import numpy as np
from rembg import remove
from PIL import Image, ImageDraw, ImageFilter

ASSETS = "/Users/Ben/Desktop/ben-mann-site-v2/assets"
INPUT  = f"{ASSETS}/ben-mann-photo.jpeg"
OUTPUT = f"{ASSETS}/ben-mann-photo.png"
BACKUP = f"{ASSETS}/ben-mann-photo-original.jpeg"

PAGE_BG = (10, 14, 23)     # #0A0E17
ACCENT  = (205, 244, 74)   # #CDF44A
INK     = (10, 14, 23)


# ─── Vectorised RGB↔HSV ──────────────────────────────────────────────────
def rgb_to_hsv_np(rgb):
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    cmax = np.max(rgb, axis=-1)
    cmin = np.min(rgb, axis=-1)
    delta = cmax - cmin

    h = np.zeros_like(cmax)
    safe = delta > 1e-8
    is_r = safe & (cmax == r)
    is_g = safe & (cmax == g) & ~is_r
    is_b = safe & (cmax == b) & ~is_r & ~is_g
    h[is_r] = ((g[is_r] - b[is_r]) / delta[is_r]) % 6
    h[is_g] = ((b[is_g] - r[is_g]) / delta[is_g]) + 2
    h[is_b] = ((r[is_b] - g[is_b]) / delta[is_b]) + 4
    h /= 6
    s = np.where(cmax > 1e-8, delta / np.maximum(cmax, 1e-8), 0)
    return np.stack([h, s, cmax], axis=-1)


def hsv_to_rgb_np(hsv):
    h6 = hsv[..., 0] * 6
    s, v = hsv[..., 1], hsv[..., 2]
    c = v * s
    x = c * (1 - np.abs((h6 % 2) - 1))
    m = v - c
    z = np.zeros_like(c)
    out = np.zeros_like(hsv)
    sectors = [
        ((h6 >= 0) & (h6 < 1), (c, x, z)),
        ((h6 >= 1) & (h6 < 2), (x, c, z)),
        ((h6 >= 2) & (h6 < 3), (z, c, x)),
        ((h6 >= 3) & (h6 < 4), (z, x, c)),
        ((h6 >= 4) & (h6 < 5), (x, z, c)),
        ((h6 >= 5) & (h6 <= 6), (c, z, x)),
    ]
    for mask, (rr, gg, bb) in sectors:
        out[..., 0] = np.where(mask, rr + m, out[..., 0])
        out[..., 1] = np.where(mask, gg + m, out[..., 1])
        out[..., 2] = np.where(mask, bb + m, out[..., 2])
    return np.clip(out, 0, 1)


# ─── Tiny morphological erosion (no scipy) ──────────────────────────────
def shrink_mask(mask, iterations=1):
    """Crude binary erosion: a pixel survives only if its 4 neighbours are also set."""
    m = mask.copy()
    for _ in range(iterations):
        up    = np.roll(m, -1, axis=0); up[-1, :] = False
        down  = np.roll(m,  1, axis=0); down[0, :] = False
        left  = np.roll(m, -1, axis=1); left[:, -1] = False
        right = np.roll(m,  1, axis=1); right[:, 0] = False
        m = m & up & down & left & right
    return m


def main():
    # Idempotent: always start from backup once it exists
    if os.path.exists(BACKUP):
        print(f"• Using backup ({os.path.basename(BACKUP)})")
        src = Image.open(BACKUP).convert("RGBA")
    else:
        src = Image.open(INPUT).convert("RGBA")
        Image.open(INPUT).save(BACKUP)
        print(f"• First run — backed up original")

    W, H = src.size
    print(f"• Source: {W}×{H}")

    # 1. Remove background
    print("• Removing background...")
    cutout = remove(src)
    arr = np.array(cutout)
    rgb = arr[..., :3].astype(float) / 255.0
    alpha = arr[..., 3]
    print("  ✓ done")

    Y, X = np.indices(rgb.shape[:2])
    visible = alpha > 200
    # Hat lives in the top ~40% of the figure; face/beard are below that
    in_upper = Y < (H * 0.40)

    # 2. Detect the maroon hat
    hsv = rgb_to_hsv_np(rgb)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    # Burgundy/maroon: reddish hue, moderate saturation, mid-low value range
    red_hue = (h > 0.88) | (h < 0.06)
    hat_mask = red_hue & (s > 0.20) & (v > 0.10) & (v < 0.85) & in_upper & visible
    if hat_mask.any():
        med_h = np.degrees(np.median(h[hat_mask]) * 2 * np.pi) / (2 * np.pi) * 360
        print(f"  • Hat pixels: {hat_mask.sum():,} | "
              f"median H={med_h:.0f}° S={np.median(s[hat_mask]):.2f} V={np.median(v[hat_mask]):.2f}")
    else:
        print(f"  • Hat pixels: 0")

    # 3. Recolour hat: shift hue to chartreuse, lift value
    new_hsv = hsv.copy()
    new_hsv[hat_mask, 0] = 70 / 360               # chartreuse hue
    new_hsv[hat_mask, 1] = np.clip(s[hat_mask] * 1.25, 0, 1)
    new_hsv[hat_mask, 2] = np.clip(v[hat_mask] * 1.55 + 0.18, 0, 1)
    new_rgb = hsv_to_rgb_np(new_hsv)
    print("  ✓ Hat hue-shifted")

    # 4. Detect the white Nixon logo within the hat region
    cx_logo = cy_logo = mark_size = None
    if hat_mask.any():
        ys, xs = np.where(hat_mask)
        y_min, y_max = int(ys.min()), int(ys.max())
        x_min, x_max = int(xs.min()), int(xs.max())

        # An interior region of the hat: erode the mask so we don't catch
        # eyes/teeth that might fall inside the hat bounding box.
        hat_interior = shrink_mask(hat_mask, iterations=8)

        # Generous white test (the Nixon logo is bright but slightly off-white
        # because of fabric texture)
        is_white = (rgb[..., 0] > 0.62) & (rgb[..., 1] > 0.62) & (rgb[..., 2] > 0.62) & visible

        # Logo = white pixels inside the hat bbox AND adjacent to interior hat
        in_bbox = (Y >= y_min) & (Y <= y_max) & (X >= x_min) & (X <= x_max)
        # Dilate hat_interior by reusing morphology in reverse: any pixel within
        # ~8 of an interior hat pixel
        near_interior = hat_interior.copy()
        for _ in range(10):
            up    = np.roll(near_interior, -1, axis=0); up[-1, :] = False
            down  = np.roll(near_interior,  1, axis=0); down[0, :] = False
            left  = np.roll(near_interior, -1, axis=1); left[:, -1] = False
            right = np.roll(near_interior,  1, axis=1); right[:, 0] = False
            near_interior = near_interior | up | down | left | right
        logo_mask = is_white & in_bbox & near_interior

        if logo_mask.any():
            print(f"  • Logo pixels: {logo_mask.sum():,}")
            non_logo_hat = hat_mask & ~logo_mask
            fill_rgb = (
                np.median(new_rgb[non_logo_hat], axis=0)
                if non_logo_hat.any()
                else np.array(ACCENT) / 255.0
            )
            new_rgb[logo_mask] = fill_rgb

            ly, lx = np.where(logo_mask)
            cx_logo = int(np.mean(lx))
            cy_logo = int(np.mean(ly))
            mark_size = int(max(lx.max() - lx.min(), ly.max() - ly.min()) * 1.55)
        else:
            print("  ! No logo detected")
    else:
        print("  ! No hat detected — skipping recolour")

    # Convert recoloured array back to image
    new_uint = (new_rgb * 255).clip(0, 255).astype(np.uint8)
    figure = Image.fromarray(np.dstack([new_uint, alpha]), "RGBA")

    # 5. Draw the website's geometric 'b' monogram in dark ink
    if cx_logo is not None and mark_size and mark_size > 12:
        mark = Image.new("RGBA", figure.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(mark)
        S = mark_size
        x0, y0 = cx_logo - S // 2, cy_logo - S // 2
        col = (*INK, 255)

        # Outer rounded square (the favicon frame)
        try:
            d.rounded_rectangle(
                [x0, y0, x0 + S, y0 + S],
                radius=int(S * 0.18),
                outline=col,
                width=max(2, int(S * 0.045)),
            )
        except AttributeError:
            d.rectangle([x0, y0, x0 + S, y0 + S], outline=col, width=max(2, int(S * 0.045)))

        # Stem (vertical bar — left side of the b)
        sx = x0 + int(S * 0.26)
        sy = y0 + int(S * 0.22)
        sw = max(2, int(S * 0.10))
        sh = int(S * 0.56)
        d.rectangle([sx, sy, sx + sw, sy + sh], fill=col)

        # Bowl (open circle)
        bcx = x0 + int(S * 0.55)
        bcy = y0 + int(S * 0.62)
        br  = int(S * 0.18)
        d.ellipse(
            [bcx - br, bcy - br, bcx + br, bcy + br],
            outline=col,
            width=max(2, int(S * 0.085)),
        )

        # Accent block (top-right corner)
        ax = x0 + int(S * 0.71)
        ay = y0 + int(S * 0.22)
        aw = int(S * 0.10)
        d.rectangle([ax, ay, ax + aw, ay + aw], fill=col)

        figure = Image.alpha_composite(figure, mark)
        print(f"  ✓ Mark drawn at ({cx_logo}, {cy_logo}) size {S}px")

    # 6. New background — midnight + chartreuse halo
    bg = Image.new("RGBA", figure.size, (*PAGE_BG, 255))
    glow = Image.new("RGBA", figure.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    bbox = figure.getbbox()
    gcx = (bbox[0] + bbox[2]) // 2 if bbox else W // 2
    gcy = bbox[1] + (bbox[3] - bbox[1]) // 6 if bbox else H // 4
    max_r = int(min(W, H) * 0.55)
    for r in range(max_r, 0, -6):
        a = max(0, int(75 * (1 - r / max_r)))
        gd.ellipse([gcx - r, gcy - r, gcx + r, gcy + r], fill=(*ACCENT, a))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=85))
    bg = Image.alpha_composite(bg, glow)

    # 7. Composite
    result = Image.alpha_composite(bg, figure)
    result.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(f"✓ Saved → {OUTPUT} ({os.path.getsize(OUTPUT) // 1024} KB)")


if __name__ == "__main__":
    main()
