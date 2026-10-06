# -*- coding: utf-8 -*-
import random
from PIL import Image

SRC = "A_hand_drawn_watercolor_illust_2026-10-06T06-32-22.png"
im = Image.open(SRC).convert("RGB").resize((1536, 1024), Image.LANCZOS)
arr = im.load()
rng = random.Random(7)

def fill_mirror_h(x0, y0, x1, y1, sx0, sx1):
    """Fill rect by horizontally mirror-tiling the clean strip sx0..sx1 (same rows)."""
    SW = sx1 - sx0
    for y in range(y0, y1):
        for x in range(x0, x1):
            m = (x - x0) % (2 * SW)
            sx = sx0 + (m if m < SW else 2 * SW - m - 1)
            c = arr[sx, y]
            n = rng.randint(-3, 3)
            arr[x, y] = tuple(max(0, min(255, c[i] + n)) for i in range(3))

# watermark (bottom-right, ~1396-1529 x 960-1017): mirror clean paper from its left.
# Strip y starts 955 to stay below the Houhai label (ends ~950).
fill_mirror_h(1370, 955, 1532, 1024, 1220, 1370)

im.save("cover_no_wm.png")
im.save("map_web.jpg", "JPEG", quality=88, optimize=True, progressive=True)
im.resize((1080, 720)).save("_prev_v7.png")
print("saved")
