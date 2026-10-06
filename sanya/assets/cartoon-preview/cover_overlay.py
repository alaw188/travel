# -*- coding: utf-8 -*-
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = "A_hand_drawn_watercolor_illust_2026-10-06T02-33-54.png"
im = Image.open(SRC).convert("RGB").resize((1536, 1024), Image.LANCZOS)
arr = im.load()
W, H = 1536, 1024

EXCLUDE = [(890, 620, 1210, 870), (730, 595, 1150, 885), (1240, 900, W, H)]

def find_clean_block(bw, bh):
    """Scan for the smoothest, lightest paper window of size bw x bh."""
    g = im.convert('L')
    gp = g.load()
    best, best_score = None, 1e9
    for y0 in range(2, H - bh - 2, 12):
        for x0 in range(2, W - bw - 2, 16):
            if any(x0 < ex1 and x0 + bw > ex0 and y0 < ey1 and y0 + bh > ey0
                   for ex0, ey0, ex1, ey1 in EXCLUDE):
                continue
            mn, mx, s, s2 = 255, 0, 0.0, 0.0
            n = 0
            for y in range(y0, y0 + bh, 4):
                for x in range(x0, x0 + bw, 6):
                    v = gp[x, y]
                    if v < mn: mn = v
                    if v > mx: mx = v
                    s += v; s2 += v * v; n += 1
            mean = s / n
            var = s2 / n - mean * mean
            score = var ** 0.5 + max(0, 170 - mn) * 2 + max(0, mean - 225) * 2
            if score < best_score:
                best_score, best = score, (x0, y0)
    return best[0], best[1], best[0] + bw, best[1] + bh

CLEAN = find_clean_block(285, 72)

def paper_fill(x0, y0, x1, y1, seed=3, noise=4):
    """Clone-stamp the cleanest paper block found."""
    rng = random.Random(seed)
    sx0, sy0, sx1, sy1 = CLEAN
    bw, bh = sx1 - sx0, sy1 - sy0
    for y in range(y0, y1):
        iy = (y - y0) % (2 * bh)
        src_y = sy0 + (iy if iy < bh else 2 * bh - iy - 1)
        for x in range(x0, x1):
            ix = (x - x0) % (2 * bw)
            src_x = sx0 + (ix if ix < bw else 2 * bw - ix - 1)
            c = arr[src_x, src_y]
            n = rng.randint(-noise, noise)
            arr[x, y] = tuple(max(0, min(255, c[i]+n)) for i in range(3))

paper_fill(700, 605, 1140, 755, 3)
paper_fill(740, 605, 1140, 875, 3)
paper_fill(1330, 960, W-4, H-4, 9, 5)
dr = ImageDraw.Draw(im)

SC = {
    "airport":  ((213, 128), (170, 85)),
    "cdf":      ((1329, 156), (150, 72)),
    "hotel":    ((774, 362), (306, 192)),
    "mayan":    ((1329, 402), (163, 68)),
    "aquarium": ((1294, 637), (128, 75)),
    "diadia":   ((1304, 796), (146, 71)),
    "houhai":   ((480, 630), (117, 82)),
    "yalong":   ((242, 490), (156, 100)),
    "tianya":   ((256, 819), (199, 103)),
    "town":     ((619, 846), (114, 92)),
}
GAP = 10

def edge(p_from, p_to, r):
    dx, dy = p_to[0]-p_from[0], p_to[1]-p_from[1]
    L = math.hypot(dx, dy) or 1.0
    ux, uy = dx/L, dy/L
    ray = 1.0/math.sqrt((ux/r[0])**2 + (uy/r[1])**2)
    k = min(ray + GAP, L)
    return (p_from[0] + ux*k, p_from[1] + uy*k)

def qbez(p0, pc, p2, t):
    mt = 1 - t
    return (mt*mt*p0[0] + 2*mt*t*pc[0] + t*t*p2[0],
            mt*mt*p0[1] + 2*mt*t*pc[1] + t*t*p2[1])

def dashed(dr, pts, color, dash=15, gap=11, width=6):
    cur = pts[0]
    on, remain = True, float(dash)
    for nxt in pts[1:]:
        seg = math.hypot(nxt[0]-cur[0], nxt[1]-cur[1])
        t = 0.0
        while t < seg:
            step = min(remain, seg - t)
            a = (cur[0] + (nxt[0]-cur[0])*t/seg, cur[1] + (nxt[1]-cur[1])*t/seg)
            if on:
                b = (cur[0] + (nxt[0]-cur[0])*min(t+step, seg)/seg,
                     cur[1] + (nxt[1]-cur[1])*min(t+step, seg)/seg)
                dr.line([a, b], fill=color, width=width)
                r = width/2
                dr.ellipse([a[0]-r, a[1]-r, a[0]+r, a[1]+r], fill=color)
                dr.ellipse([b[0]-r, b[1]-r, b[0]+r, b[1]+r], fill=color)
            t += step
            remain -= step
            if remain <= 0.001:
                on, remain = (False, gap) if on else (True, dash)
        cur = nxt

def leg(a, b, color, ctrl=None):
    p1, r1 = SC[a]; p2, r2 = SC[b]
    A = edge(p1, p2, r1); B = edge(p2, p1, r2)
    pts = [A, B] if ctrl is None else [qbez(A, ctrl, B, i/90.0) for i in range(91)]
    dashed(dr, pts, color)

# 2026-10-06 per user: no route lines, no day badges — key locations only

def soften(x0, y0, x1, y1, rad=9, feather=20):
    """Blur the filled area to hide tile seams, feathered at borders."""
    box = (max(0, x0 - feather), max(0, y0 - feather),
           min(W, x1 + feather), min(H, y1 + feather))
    region = im.crop(box).filter(ImageFilter.GaussianBlur(rad))
    mask = Image.new('L', (box[2] - box[0], box[3] - box[1]), 0)
    md = mask.load()
    for yy in range(mask.height):
        for xx in range(mask.width):
            dx = min(xx, mask.width - 1 - xx)
            dy = min(yy, mask.height - 1 - yy)
            md[xx, yy] = int(255 * min(1.0, min(dx, dy) / feather))
    im.paste(region, box, mask)

soften(740, 605, 1140, 875)
soften(1330, 960, W - 4, H - 4)

im.save("cover_no_wm.png")
im.resize((1080, 720)).save("_cover_prev.png")
print("saved")
