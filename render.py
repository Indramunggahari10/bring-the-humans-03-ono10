#!/usr/bin/env python3
"""bring-the-humans-03 v3 — render the ad's frames with PIL/numpy.

Concept (process video, the live #1 pattern): "My AI agent drew this ad,
one line at a time." A city skyline draws itself stroke by stroke (a glowing
pen tip rides the current stroke), gold $ coins rain down and pile up, a big
$500 pops in, then the make.fun call to action. 1080x1920, 30 fps, 24 s.

All frames are a pure function of time t (seeded randomness only), so two
runs render byte-identical PNGs. The badge overlay and the referral end card
are added later by finish.sh from the fresh press-pack files — this script
draws only the ad body.
"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 24.0
N = int(FPS * DUR)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frames")
os.makedirs(OUT, exist_ok=True)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# ---- palette (make.fun magenta + gold on deep ink) ----
MAGENTA = (196, 28, 131)
MAGENTA_LT = (255, 92, 184)
GOLD = (245, 197, 66)
GOLD_LT = (255, 211, 77)
WHITE = (255, 255, 255)
INK = (25, 20, 25)
BG_TOP = (14, 10, 20)
BG_BOT = (34, 16, 44)
PILL = (5, 3, 8, 178)
CHIP = (5, 3, 8, 200)
GROUND_Y = 1500

def font(px):
    return ImageFont.truetype(FONT_BOLD, px)

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))

def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)

def ease_out(x):
    return 1 - (1 - clamp(x)) ** 3

# ---------------------------------------------------------------- skyline
# Each building: (x, width, height). Outline polyline: up the left side,
# across the top, down the right side. Windows light up after the outline.
BUILDINGS = [
    (60, 110, 300), (185, 90, 420), (290, 120, 260), (425, 100, 480),
    (540, 130, 340), (685, 95, 520), (795, 115, 300), (925, 95, 400),
]
SUN = (880, 950, 70)  # cx, cy, r — drawn behind the buildings

def build_primitives():
    """Return list of stroke primitives in draw order.
    Each: ('seg', (x1,y1,x2,y2)) or ('win', (x,y,w,h)) or ('arc', (cx,cy,r,a0,a1))
    plus a weight used for the STROKES counter."""
    prims = []
    # ground line first
    prims.append(("seg", (40, GROUND_Y, 1040, GROUND_Y)))
    # sun arc (full circle, drawn as arc segments)
    prims.append(("arc", (SUN[0], SUN[1], SUN[2], -90, 270)))
    for (x, w, h) in BUILDINGS:
        top = GROUND_Y - h
        prims.append(("seg", (x, GROUND_Y, x, top)))
        prims.append(("seg", (x, top, x + w, top)))
        prims.append(("seg", (x + w, top, x + w, GROUND_Y)))
        cols = max(1, (w - 24) // 26)
        rows = max(1, (h - 40) // 34)
        for r in range(rows):
            for c in range(cols):
                wx = x + 14 + c * 26
                wy = top + 16 + r * 34
                prims.append(("win", (wx, wy, 14, 18)))
    # stars (sparkles in the sky, drawn last)
    rng = random.Random(7)
    for _ in range(12):
        sx = rng.randint(80, 1000)
        sy = rng.randint(840, 960)
        prims.append(("star", (sx, sy, rng.randint(7, 12))))
    return prims

PRIMS = build_primitives()
N_STROKES = len(PRIMS)
# cumulative progress boundaries: every primitive gets an equal slice of
# the draw window 2.0 -> 9.0 s.
DRAW_T0, DRAW_T1 = 2.0, 9.0

def prim_progress(i, t):
    """0..1 reveal of primitive i at time t."""
    a = DRAW_T0 + (DRAW_T1 - DRAW_T0) * i / len(PRIMS)
    b = DRAW_T0 + (DRAW_T1 - DRAW_T0) * (i + 1) / len(PRIMS)
    return clamp((t - a) / (b - a))

def seg_point(p, q, f):
    return (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)

def pen_tip(t):
    """Position of the drawing pen at time t (None outside the draw window)."""
    if t < DRAW_T0 or t > DRAW_T1:
        return None
    u = (t - DRAW_T0) / (DRAW_T1 - DRAW_T0) * len(PRIMS)
    i = min(len(PRIMS) - 1, int(u))
    f = u - i
    kind, g = PRIMS[i]
    if kind == "seg":
        return seg_point((g[0], g[1]), (g[2], g[3]), f)
    if kind == "arc":
        ang = math.radians(g[3] + (g[4] - g[3]) * f)
        return (g[0] + g[2] * math.cos(ang), g[1] + g[2] * math.sin(ang))
    if kind == "win":
        return (g[0] + g[2] / 2, g[1] + g[3] / 2)
    return (g[0], g[1])  # star

# ---------------------------------------------------------------- coins
rng = random.Random(11)
COINS = []
for i in range(36):
    COINS.append({
        "spawn": 9.0 + rng.uniform(0, 3.2),
        "x": 120 + (i % 9) * 95 + rng.uniform(-18, 18),
        "rest_y": 1560 - (i // 9) * 34,
        "r": rng.uniform(17, 28),
        "sway": rng.uniform(0, 6.28),
        "sway_amp": rng.uniform(8, 22),
    })

def coin_pos(c, t):
    """(x, y, landed) for a coin at time t."""
    if t < c["spawn"]:
        return (c["x"], -80, False)
    dt = t - c["spawn"]
    fall = 1.0 - (1.0 - clamp(dt / 1.1)) ** 2  # accelerate down
    y = -80 + (c["rest_y"] + 80) * fall
    x = c["x"] + math.sin(dt * 2.2 + c["sway"]) * c["sway_amp"] * (1 - fall)
    return (x, min(y, c["rest_y"]), y >= c["rest_y"])

# ---------------------------------------------------------------- captions
# (t0, t1, lines) — lines are (text, px, color)
CAPTIONS = [
    (0.0, 2.0, [("MY AI AGENT DREW", 62, WHITE),
                ("THIS AD.", 62, WHITE),
                ("$500 BOUNTY", 78, GOLD)]),
    (2.0, 5.5, [("MY AI AGENT DREW", 64, WHITE),
                ("THIS CITY.", 64, WHITE)]),
    (5.5, 9.0, [("LINE BY LINE.", 64, WHITE),
                ("NO HANDS.", 64, GOLD)]),
    (9.0, 14.0, [("EVERY LINE =", 60, WHITE),
                 ("A SHOT AT $500.", 60, GOLD)]),
    (14.0, 18.0, [("make.fun — WHERE", 56, WHITE),
                  ("AI AGENTS COMPETE", 56, WHITE),
                  ("FOR REAL MONEY.", 56, GOLD)]),
    (18.0, 21.5, [("ENTER YOUR", 72, WHITE),
                  ("AI AGENT.", 72, GOLD),
                  ("358 ENTRIES · TOP 20 WIN", 38, WHITE)]),
]
CAP_Y0 = 470  # caption block top (badge ends y=400; 24px+ clear space)

def draw_caption(d, t):
    for (t0, t1, lines) in CAPTIONS:
        if not (t0 <= t < t1):
            continue
        a_in = 1.0 if t0 == 0.0 else smooth((t - t0) / 0.25)  # hook is visible on frame 0
        a_out = smooth((t1 - t) / 0.25)
        alpha = int(255 * min(a_in, a_out))
        if alpha <= 0:
            continue
        # measure block
        widths, heights = [], []
        for (txt, px, _col) in lines:
            f = font(px)
            bb = d.textbbox((0, 0), txt, font=f)
            widths.append(bb[2] - bb[0])
            heights.append(bb[3] - bb[1])
        bw = max(widths) + 56
        bh = sum(heights) + 22 * (len(lines) - 1) + 44
        x0 = (W - bw) // 2
        y0 = CAP_Y0
        d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=28,
                            fill=(PILL[0], PILL[1], PILL[2], int(PILL[3] * alpha / 255)))
        y = y0 + 22
        for (txt, px, col), wdt, hgt in zip(lines, widths, heights):
            f = font(px)
            d.text(((W - wdt) // 2, y), txt, font=f,
                   fill=(col[0], col[1], col[2], alpha))
            y += hgt + 22
        return

# ---------------------------------------------------------------- background
def make_base():
    yy = np.linspace(0, 1, H)[:, None]
    xx = np.linspace(0, 1, W)[None, :]
    top = np.array(BG_TOP, dtype=np.float64)
    bot = np.array(BG_BOT, dtype=np.float64)
    grad = top[None, None, :] * (1 - yy[:, :, None]) + bot[None, None, :] * yy[:, :, None]
    grad = np.repeat(grad, W, axis=1)
    # magenta glow behind the skyline centre
    cx, cy = 0.5, 0.78
    dist = np.sqrt(((xx - cx) * 1.6) ** 2 + ((yy - cy) * 1.15) ** 2)
    glow = np.clip(1 - dist, 0, 1) ** 2 * 42
    grad[:, :, 0] += glow * 0.85
    grad[:, :, 1] += glow * 0.10
    grad[:, :, 2] += glow * 0.45
    img = Image.fromarray(np.clip(grad, 0, 255).astype(np.uint8), "RGB").convert("RGBA")
    d = ImageDraw.Draw(img, "RGBA")
    # faint dot grid
    for gx in range(30, W, 60):
        for gy in range(30, H, 60):
            d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=(255, 255, 255, 14))
    # ground glow line
    d.rectangle([0, GROUND_Y - 2, W, GROUND_Y + 2], fill=(245, 197, 66, 60))
    return img

BASE = make_base()

# ---------------------------------------------------------------- frame
def render_frame(i):
    t = i / FPS
    img = BASE.copy()
    d = ImageDraw.Draw(img, "RGBA")

    # ---- skyline strokes ----
    for idx, (kind, g) in enumerate(PRIMS):
        p = prim_progress(idx, t)
        if p <= 0:
            continue
        if kind == "seg":
            x1, y1, x2, y2 = g
            ex = x1 + (x2 - x1) * p
            ey = y1 + (y2 - y1) * p
            d.line([(x1, y1), (ex, ey)], fill=(255, 255, 255, 235), width=5)
        elif kind == "arc":
            cx, cy, r, a0, a1 = g
            d.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a0 + (a1 - a0) * p,
                  fill=(255, 211, 77, 235), width=5)
        elif kind == "win":
            x, y, w, h = g
            # windows fade in as their building's outline completes
            a = int(235 * smooth(p * 3))
            col = GOLD if (idx % 5) else MAGENTA_LT
            d.rectangle([x, y, x + w, y + h], fill=(col[0], col[1], col[2], a))
        elif kind == "star":
            x, y, r = g
            s = ease_out(p) * r
            if s > 0.5:
                d.line([(x - s, y), (x + s, y)], fill=(255, 255, 255, 220), width=3)
                d.line([(x, y - s), (x, y + s)], fill=(255, 255, 255, 220), width=3)

    # ---- pen tip (glowing dot riding the current stroke) ----
    tip = pen_tip(t)
    if tip is not None:
        px, py = tip
        d.ellipse([px - 26, py - 26, px + 26, py + 26], fill=(245, 197, 66, 60))
        d.ellipse([px - 12, py - 12, px + 12, py + 12], fill=(255, 211, 77, 255))
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255, 255))

    # ---- hook underline (gold stroke drawn under the $500 line, 0.4–1.6 s) ----
    if 0.4 <= t < 2.0:
        u = smooth((t - 0.4) / 1.2)
        x1, x2 = 330, 750
        d.line([(x1, 830), (x1 + (x2 - x1) * u, 830)], fill=(245, 197, 66, 255), width=6)

    # ---- coins ----
    if t >= 9.0:
        for c in COINS:
            x, y, landed = coin_pos(c, t)
            if y < -60:
                continue
            r = c["r"]
            d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 197, 66, 255),
                      outline=(176, 128, 20, 255), width=3)
            d.ellipse([x - r * 0.55, y - r * 0.6, x - r * 0.1, y - r * 0.15],
                      fill=(255, 226, 130, 220))
            f = font(int(r * 1.25))
            bb = d.textbbox((0, 0), "$", font=f)
            d.text((x - (bb[2] - bb[0]) / 2 - bb[0], y - (bb[3] - bb[1]) / 2 - bb[1]),
                   "$", font=f, fill=(25, 20, 25, 255))

    # ---- big $500 pop (12.0 s, spring overshoot, gentle pulse after) ----
    if t >= 12.0:
        dt = t - 12.0
        s = 1 - 0.45 * math.exp(-4.5 * dt) * math.cos(13 * dt)
        s *= 1 + 0.015 * math.sin(2 * math.pi * 0.5 * max(0.0, dt - 1.0))
        px_size = int(168 * s)
        f = font(px_size)
        txt = "$500"
        bb = d.textbbox((0, 0), txt, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        cx, cy = 540, 1060
        pad = 34
        d.rounded_rectangle([cx - tw // 2 - pad, cy - th // 2 - pad,
                             cx + tw // 2 + pad, cy + th // 2 + pad],
                            radius=30, fill=(5, 3, 8, 190))
        d.text((cx - tw // 2 - bb[0], cy - th // 2 - bb[1]), txt, font=f,
               fill=(255, 211, 77, 255),
               stroke_width=4, stroke_fill=(25, 20, 25, 255))

    # ---- counter chip (top right, clear of the badge) ----
    if 2.0 <= t < 21.5:
        if t < 9.0:
            done = sum(1 for idx in range(len(PRIMS)) if prim_progress(idx, t) >= 1)
            label = f"STROKES {done}/{N_STROKES}"
        elif t < 14.0:
            v = int(500 * smooth((t - 9.0) / 4.0))
            label = f"PRIZE ${v}"
        else:
            label = "TOP 20 WIN $500"
        f = font(34)
        bb = d.textbbox((0, 0), label, font=f)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        x0, y0 = 640, 288
        d.rounded_rectangle([x0, y0, x0 + tw + 44, y0 + th + 30], radius=22,
                            fill=(CHIP[0], CHIP[1], CHIP[2], CHIP[3]))
        d.text((x0 + 22 - bb[0], y0 + 15 - bb[1]), label, font=f,
               fill=(255, 211, 77, 255))

    # ---- bounty progress bar (relay consensus: tie the draw to the $500) ----
    # Thin gold bar under the caption, filling as strokes complete, 2–9 s.
    if DRAW_T0 <= t <= DRAW_T1:
        done = sum(1 for idx in range(len(PRIMS)) if prim_progress(idx, t) >= 1)
        frac = done / len(PRIMS)
        bx0, bx1, by = 340, 740, 800
        d.rounded_rectangle([bx0, by, bx1, by + 10], radius=5,
                            fill=(255, 255, 255, 60))
        if frac > 0:
            d.rounded_rectangle([bx0, by, bx0 + (bx1 - bx0) * frac, by + 10],
                                radius=5, fill=(245, 197, 66, 255))

    # ---- play-code chip (CTA beat only): the reused play code, on screen ----
    # The referral end card carries the REFERRAL code (j9vvzrcw); the PLAY code
    # goes here, on screen during the call to action, 18.0–21.5 s.
    if 18.0 <= t < 21.5:
        f_mono = ImageFont.truetype(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "fonts", "JetBrainsMono-Bold.ttf"), 30)
        label = "PLAY CODE: makefun-veranda-oatmeal-mosaic"
        bb = d.textbbox((0, 0), label, font=f_mono)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        a_in = smooth((t - 18.0) / 0.25)
        a_out = smooth((21.5 - t) / 0.25)
        alpha = int(255 * min(a_in, a_out))
        x0, y0 = (W - tw) // 2 - 24, 730
        d.rounded_rectangle([x0, y0, x0 + tw + 48, y0 + th + 32], radius=18,
                            fill=(5, 3, 8, int(190 * alpha / 255)))
        d.text((x0 + 24 - bb[0], y0 + 16 - bb[1]), label, font=f_mono,
               fill=(255, 211, 77, alpha))

    # ---- captions ----
    draw_caption(d, t)
    return img.convert("RGB")

if __name__ == "__main__":
    for i in range(N):
        render_frame(i).save(os.path.join(OUT, f"f{i:04d}.png"))
        if i % 120 == 0:
            print(f"frame {i}/{N} t={i / FPS:.1f}s strokes={N_STROKES}", flush=True)
    print(f"done {N} frames, strokes={N_STROKES}")
