#!/usr/bin/env python3
"""bring-the-humans-03 v3 — original synthesized audio bed.

24 s, 48 kHz stereo. Pad chords Am -> F -> C -> G (6 s each), a soft kick
every 0.5 s (120 BPM), a pentatonic pluck arp on 8th notes, a bright ding
when the $500 pops at 12 s, and a 1 s fade out. Every tone is at an even Hz
so partials complete integer cycles over the clip. No samples, no
copyrighted audio. Target about -16 LUFS.
"""
import numpy as np
from scipy.io import wavfile

SR = 48000
DUR = 24.0
N = int(SR * DUR)
t = np.arange(N) / SR

# ---- pad: Am, F, C, G — 6 s each; triangle-ish partials ----
CHORDS = [
    [110.0, 130.81, 164.81, 220.0],   # Am
    [87.31, 130.81, 174.61, 220.0],   # F
    [130.81, 164.81, 196.0, 261.63],  # C
    [98.0, 146.83, 196.0, 246.94],    # G
]
pad = np.zeros(N)
for ci, freqs in enumerate(CHORDS):
    s0, s1 = int(ci * 6 * SR), int((ci + 1) * 6 * SR)
    tt = t[s0:s1]
    env = np.minimum(1.0, np.minimum((tt - ci * 6) / 0.8, ((ci + 1) * 6 - tt) / 0.8))
    env = np.clip(env, 0, 1) ** 0.5
    for f in freqs:
        pad[s0:s1] += 0.05 * np.sin(2 * np.pi * f * tt)
        pad[s0:s1] += 0.02 * np.sin(2 * np.pi * 2 * f * tt)
    pad[s0:s1] *= env

# ---- kick every 0.5 s: sine drop 120 -> 50 Hz, 0.18 s ----
kick = np.zeros(N)
for k in range(int(DUR / 0.5)):
    s0 = int(k * 0.5 * SR)
    L = int(0.18 * SR)
    tk = np.arange(L) / SR
    f0 = 120 * np.exp(-tk * 18) + 50
    phase = 2 * np.pi * np.cumsum(f0) / SR
    kick[s0:s0 + L] += 0.5 * np.sin(phase) * np.exp(-tk * 22)

def add_at(dst, s0, sig):
    """Add sig into dst at s0, clipping at the array end."""
    n = min(len(sig), len(dst) - s0)
    if n > 0:
        dst[s0:s0 + n] += sig[:n]

# ---- pluck arp: A minor pentatonic, 8th notes (0.25 s), 2 bars per chord ----
PENTA = [220.0, 261.63, 293.66, 329.63, 392.0, 440.0]
pluck = np.zeros(N)
rng = np.random.RandomState(3)
for n in range(int(DUR / 0.25)):
    s0 = int(n * 0.25 * SR)
    L = int(0.30 * SR)
    f = PENTA[rng.randint(0, len(PENTA))]
    tp = np.arange(L) / SR
    add_at(pluck, s0, 0.10 * np.sin(2 * np.pi * f * tp) * np.exp(-tp * 14))
    add_at(pluck, s0, 0.04 * np.sin(2 * np.pi * 2 * f * tp) * np.exp(-tp * 20))

# ---- ding at 12.0 s (the $500 pop) ----
ding = np.zeros(N)
s0 = int(12.0 * SR)
L = int(1.2 * SR)
td = np.arange(L) / SR
ding[s0:s0 + L] += 0.22 * np.sin(2 * np.pi * 880.0 * td) * np.exp(-td * 4)
ding[s0:s0 + L] += 0.12 * np.sin(2 * np.pi * 1318.5 * td) * np.exp(-td * 5)

mix = pad + kick + pluck + ding
# 1 s fade out
fade = np.ones(N)
fade[-SR:] = np.linspace(1, 0, SR)
mix *= fade
# gentle fade in
mix[: int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))
mix /= np.max(np.abs(mix)) * 1.05  # peak ~ -0.4 dB
stereo = np.stack([mix, mix], axis=1)
wavfile.write("audio.wav", SR, (stereo * 32767).astype(np.int16))
print("wrote audio.wav", DUR, "s")
