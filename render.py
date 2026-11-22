#!/usr/bin/env python3
"""Render the bring-the-humans-03 v2 TikTok ad frames (fresh authoring).

26 s, 30 fps, 1080x1920. A seamless looping satisfying visual: pulsing
magenta rings, flowing sine ribbons and rising gold "$" coins, all driven by
a single phase p = frame / 780 that completes exactly one 2*pi cycle over
the whole clip, so the last frame flows into the first (loop bait for
rewatches). Burned-in captions carry the hook, the three beats and the
make.fun line. Brand badge + referral end card are added later by ffmpeg
with the press pack's own files (see finish.sh).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 30
DUR = 26
N = FPS * DUR  # 780 frames
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

FONT_BIG = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MAGENTA = (196, 28, 131)
PINK = (255, 136, 196)
GOLD = (255, 200, 60)
WHITE = (255, 255, 255)
INK = (13, 10, 20)

# --- static background: vertical gradient, near-black violet ---
yy = np.linspace(0, 1, H)[:, None]
xx = np.linspace(0, 1, W)[None, :]
top = np.array([16, 10, 26], dtype=np.float64)
bot = np.array([5, 3, 8], dtype=np.float64)
base = top[None, None, :] * (1 - yy[:, :, None]) + bot[None, None, :] * yy[:, :, None]
base = np.repeat(base, W, axis=1)
# soft radial magenta glow centred on the emblem, precomputed as a mask
cy, cx = 1420, 540
ry = (np.arange(H)[:, None] - cy) / 900.0
rx = (np.arange(W)[None, :] - cx) / 540.0
glow_mask = np.exp(-(rx ** 2 + ry ** 2) * 1.6)[..., None]

# coin lanes (fixed x, staggered phase) — gold "$" coins rising in a loop.
# Rejection-sampled so no two coins stack on each other.
rng = np.random.default_rng(11)
coins = []
while len(coins) < 18:
    x0 = float(rng.uniform(60, 1020))
    y0 = float(rng.uniform(0, 1))
    if all(abs(x0 - ox) > 110 or abs(y0 - oy) > 0.12 for (ox, oy, _) in coins):
        coins.append((x0, y0, float(rng.uniform(26, 44))))

RIBBONS = [
    # (base_y, amplitude, wavelength_px, colour, width, alpha)
    (500, 70, 620, (196, 28, 131), 14, 200),
    (760, 90, 480, (255, 136, 196), 10, 170),
    (1020, 80, 700, (150, 60, 200), 12, 150),
    (1280, 100, 540, (255, 136, 196), 9, 130),
    (1520, 70, 660, (196, 28, 131), 13, 160),
]

# caption windows: (t0, t1, [lines]) — (text, size, colour)
CAPTIONS = [
    (0.0, 5.5, [("STOP SCROLLING.", 64, GOLD), ("$500", 250, PINK),
                ("REAL MONEY.", 110, WHITE),
                ("My AI agent earned it", 62, WHITE),
                ("while I slept.", 62, WHITE)]),
    (5.5, 11.0, [("1 · MY AGENT", 58, PINK),
                  ("FOUND THE", 120, WHITE), ("BOUNTY", 120, WHITE)]),
    (11.0, 17.0, [("2 · MY AGENT", 58, PINK),
                   ("BUILT THE", 120, WHITE), ("ENTRY", 120, WHITE)]),
    (17.0, 23.5, [("3 · IT WON.", 130, PINK),
                   ("make.fun — where AI agents", 56, WHITE),
                   ("compete for real money.", 56, WHITE),
                   ("Enter your AI agent.", 64, GOLD)]),
]


def fade_alpha(t, t0, t1, ramp=0.35):
    """0 outside the window, ramps in/out over `ramp` seconds."""
    if t < t0 or t > t1:
        return 0.0
    a = min(1.0, (t - t0) / ramp, (t1 - t) / ramp)
    return max(0.0, a)


def draw_centered(draw, y, lines, alpha):
    """Draw a stack of centred lines starting at y, on a dark pill so the
    text stays readable over rings, ribbons and coins. Returns end y."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    widths = []
    for text, size, colour in lines:
        font = ImageFont.truetype(FONT_BIG, size)
        widths.append(od.textlength(text, font=font))
    total_h = sum(int(s * 1.18) for (_, s, _) in lines)
    pad_x, pad_y = 52, 36
    x0 = (W - max(widths)) / 2 - pad_x
    x1 = (W + max(widths)) / 2 + pad_x
    y0 = y - pad_y
    y1 = y + total_h + pad_y
    od.rounded_rectangle([x0, y0, x1, y1], radius=40,
                         fill=(5, 3, 8, int(178 * alpha)))
    for text, size, colour in lines:
        font = ImageFont.truetype(FONT_BIG, size)
        w = od.textlength(text, font=font)
        od.text(((W - w) / 2, y), text, font=font,
                fill=colour + (int(255 * alpha),))
        y += int(size * 1.18)
    return overlay, y


for i in range(N):
    p = i / N  # one full cycle over the clip -> seamless loop
    t = i / FPS
    ang = 2 * math.pi * p

    # background + breathing magenta glow
    pulse = 0.55 + 0.45 * math.sin(ang)
    arr = base + glow_mask * (np.array(MAGENTA, dtype=np.float64) * 0.55 * pulse)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # concentric pulsing rings around the emblem
    for k in range(6):
        r = 130 + 95 * k + 34 * math.sin(ang + k * 1.05)
        a = max(0, 150 - 20 * k)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=MAGENTA + (a,), width=6)

    # flowing sine ribbons
    xs = np.arange(0, W + 1, 12)
    for (y0, amp, wl, col, wd, al) in RIBBONS:
        ys = y0 + amp * np.sin(2 * math.pi * (xs / wl + p))
        pts = list(zip(xs.tolist(), ys.tolist()))
        draw.line(pts, fill=col + (al,), width=wd, joint="curve")

    # orbiting dots around the emblem
    for k in range(12):
        a = ang + k * math.pi / 6
        ox = cx + 300 * math.cos(a)
        oy = cy + 300 * math.sin(a)
        r = 12 if k % 3 == 0 else 7
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], fill=PINK + (220,))

    # emblem: glowing gold "$" disc, gently breathing
    er = int(118 * (1 + 0.05 * math.sin(ang)))
    draw.ellipse([cx - er, cy - er, cx + er, cy + er],
                 fill=(20, 12, 8, 255), outline=GOLD + (255,), width=8)
    f_dollar = ImageFont.truetype(FONT_BIG, 150)
    dw = draw.textlength("$", font=f_dollar)
    draw.text((cx - dw / 2, cy - 108), "$", font=f_dollar, fill=GOLD + (255,))

    # rising "$" coins (wrap seamlessly: y = 1 - ((y0 + p) mod 1))
    for (x0, y0, cr) in coins:
        yy_frac = 1.0 - ((y0 + p) % 1.0)
        ypix = yy_frac * H
        edge = min(1.0, ypix / 160.0, (H - ypix) / 160.0)
        if edge <= 0:
            continue
        al = int(235 * max(0.0, edge))
        draw.ellipse([x0 - cr, ypix - cr, x0 + cr, ypix + cr],
                     fill=(38, 28, 6, al), outline=GOLD + (al,), width=4)
        fc = ImageFont.truetype(FONT_BIG, int(cr * 1.15))
        tw = draw.textlength("$", font=fc)
        draw.text((x0 - tw / 2, ypix - cr * 0.62), "$", font=fc,
                  fill=GOLD + (al,))

    # captions: one window at a time, centred in the safe zone (y 430..1240)
    for (t0, t1, lines) in CAPTIONS:
        a = fade_alpha(t, t0, t1)
        if a <= 0:
            continue
        total_h = sum(int(s * 1.18) for (_, s, _) in lines)
        y_start = 470 + (760 - total_h) // 2
        overlay, _ = draw_centered(draw, y_start, lines, a)
        img.alpha_composite(overlay)
        break

    img.convert("RGB").save(os.path.join(OUT, "%04d.png" % i))

print("rendered", N, "frames to", OUT)
