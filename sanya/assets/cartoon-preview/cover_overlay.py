# -*- coding: utf-8 -*-
import random
from PIL import Image

SRC = "A_hand_drawn_watercolor_illust_2026-10-06T05-20-31.png"
im = Image.open(SRC).convert("RGB").resize((1536, 1024), Image.LANCZOS)
arr = im.load()
W, H = 1536, 1024
rng = random.Random(7)

# Remove AI watermark (bottom-right): mirror the clean paper strip to its left.
# No blur, no distant clone - local mirrored grain keeps the paper texture identical.
X0, Y0, X1, Y1 = 1370, 938, 1532, 1024
SW = 150  # clean paper strip to the left: x 1228-1380
for y in range(Y0, Y1):
    for x in range(X0, X1):
        m = (x - X0) % (2 * SW)
        sx = (X0 - SW) + (m if m < SW else 2 * SW - m - 1)
        c = arr[sx, y]
        n = rng.randint(-3, 3)
        arr[x, y] = tuple(max(0, min(255, c[i] + n)) for i in range(3))

im.save("cover_no_wm.png")
im.save("map_web.jpg", "JPEG", quality=88, optimize=True, progressive=True)
im.resize((1080, 720)).save("_prev_v5.png")
print("saved")
