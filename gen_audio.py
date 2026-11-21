#!/usr/bin/env python3
"""Synthesize a punchy 26-second backing track for the make.fun TikTok ad.

120 BPM, 4-on-the-floor kick, offbeat hats, a driving bassline and a
bright pluck arp. Written from scratch with numpy; no samples, no
copyrighted material. Deterministic output: same bytes every run.
"""
import numpy as np

SR = 48000
DUR = 26.0
N = int(SR * DUR)
t = np.arange(N, dtype=np.float64) / SR
mix = np.zeros(N, dtype=np.float64)

# --- kick: every 0.5 s, sine dropping 130 -> 45 Hz, fast decay ---
for start in np.arange(0, DUR, 0.5):
    i0 = int(start * SR)
    ln = int(0.28 * SR)
    i1 = min(N, i0 + ln)
    tt = np.arange(i1 - i0, dtype=np.float64) / SR
    freq = 130.0 * np.exp(-tt * 22.0) + 45.0
    phase = 2 * np.pi * np.cumsum(freq) / SR
    env = np.exp(-tt * 26.0)
    mix[i0:i1] += 0.9 * np.sin(phase) * env

# --- hats: offbeats, short noise bursts ---
rng = np.random.default_rng(7)
for start in np.arange(0.25, DUR, 0.5):
    i0 = int(start * SR)
    ln = int(0.05 * SR)
    i1 = min(N, i0 + ln)
    noise = rng.standard_normal(i1 - i0)
    # crude high-pass: first difference
    noise = np.diff(noise, prepend=noise[0])
    tt = np.arange(i1 - i0, dtype=np.float64) / SR
    mix[i0:i1] += 0.16 * noise * np.exp(-tt * 160.0)

# --- bassline: one note per beat, A1 A1 C2 G1 cycling, soft square ---
notes = [55.0, 55.0, 65.41, 49.0]
for b, start in enumerate(np.arange(0, DUR, 0.5)):
    f = notes[b % 4]
    i0 = int(start * SR)
    ln = int(0.44 * SR)
    i1 = min(N, i0 + ln)
    tt = np.arange(i1 - i0, dtype=np.float64) / SR
    wave = np.tanh(2.2 * np.sin(2 * np.pi * f * tt))
    mix[i0:i1] += 0.34 * wave * np.exp(-tt * 5.0)

# --- pluck arp: bright sine plucks on the "and" of beats 2 and 4 ---
arp = [659.25, 783.99, 880.0, 1046.5]
for bar in range(int(DUR // 2)):
    for k, off in enumerate((1.0, 1.5)):
        start = bar * 2.0 + off
        if start >= DUR - 0.4:
            continue
        f = arp[(bar + k) % 4]
        i0 = int(start * SR)
        ln = int(0.32 * SR)
        i1 = min(N, i0 + ln)
        tt = np.arange(i1 - i0, dtype=np.float64) / SR
        mix[i0:i1] += 0.13 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14.0)

# --- master: fade out last 0.6 s, normalize to -3 dBFS ---
fade = np.ones(N)
fl = int(0.6 * SR)
fade[-fl:] = np.linspace(1.0, 0.0, fl)
mix *= fade
peak = np.max(np.abs(mix))
mix *= 0.7079 / peak
stereo = np.stack([mix, mix], axis=1)
pcm = np.clip(stereo * 32767, -32768, 32767).astype('<i2')
with open('audio.wav', 'wb') as fh:
    fh.write(b'RIFF')
    fh.write((36 + pcm.nbytes).to_bytes(4, 'little'))
    fh.write(b'WAVEfmt ')
    fh.write((16).to_bytes(4, 'little'))
    fh.write((1).to_bytes(2, 'little'))          # PCM
    fh.write((2).to_bytes(2, 'little'))          # stereo
    fh.write((SR).to_bytes(4, 'little'))
    fh.write((SR * 4).to_bytes(4, 'little'))     # byte rate
    fh.write((4).to_bytes(2, 'little'))          # block align
    fh.write((16).to_bytes(2, 'little'))         # bits
    fh.write(b'data')
    fh.write(pcm.nbytes.to_bytes(4, 'little'))
    fh.write(pcm.tobytes())
print('wrote audio.wav', pcm.nbytes, 'bytes, peak-normalized')
