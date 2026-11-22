#!/usr/bin/env python3
"""Synth loop for the v2 ad (fresh authoring): 26 s, 44100 Hz stereo WAV.

Pad chords (even frequencies, integer cycles over each 6.5 s chord so the
loop is seamless), a soft kick every 0.5 s, and a plucked arpeggio every
0.25 s. No copyrighted audio, no samples.
"""
import math
import struct
import wave

SR = 44100
DUR = 26
N = SR * DUR

# 4 chords x 6.5 s; all tones even Hz -> integer cycles per chord and per clip
CHORDS = [
    [130, 164, 196],   # C major
    [174, 220, 262],   # F major
    [146, 220, 294],   # G-ish (D/G)
    [130, 164, 196],   # C major
]
CHORD_LEN = 6.5

samples = [0.0] * N


def add(t0, t1, fn):
    i0, i1 = int(t0 * SR), min(N, int(t1 * SR))
    for i in range(i0, i1):
        samples[i] += fn((i - i0) / SR, i / SR)


# pad: soft sines with a slow tremolo (period divides 26 s) + crossfades
for ci, chord in enumerate(CHORDS):
    c0, c1 = ci * CHORD_LEN, (ci + 1) * CHORD_LEN
    for f in chord:
        def pad(dt, tabs, f=f, c0=c0, c1=c1):
            env = min(1.0, dt / 0.4, (c1 - tabs) / 0.4 + 0.0)
            env = max(0.0, env)
            trem = 0.85 + 0.15 * math.sin(2 * math.pi * tabs / 6.5)
            return 0.055 * env * trem * math.sin(2 * math.pi * f * tabs)
        add(c0, c1, pad)

# kick every 0.5 s: sine 120 -> 50 Hz, exp decay 0.18 s
for k in range(52):
    t0 = k * 0.5

    def kick(dt, tabs, t0=t0):
        if dt > 0.22:
            return 0.0
        f = 120 - 70 * (dt / 0.22)
        return 0.5 * math.exp(-dt / 0.06) * math.sin(2 * math.pi * f * dt)
    add(t0, t0 + 0.22, kick)

# arpeggio pluck every 0.25 s cycling the chord tones x2
notes = []
for ci, chord in enumerate(CHORDS):
    for j in range(26):
        notes.append((ci * CHORD_LEN + j * 0.25, chord[j % 3] * 2))
for (t0, f) in notes:
    def pluck(dt, tabs, f=f):
        if dt > 0.3:
            return 0.0
        return 0.09 * math.exp(-dt / 0.09) * math.sin(2 * math.pi * f * dt)
    add(t0, t0 + 0.3, pluck)

peak = max(abs(s) for s in samples) or 1.0
gain = 0.85 / peak
frames = b"".join(
    struct.pack("<hh", int(max(-1.0, min(1.0, s * gain)) * 32767),
                int(max(-1.0, min(1.0, s * gain)) * 32767))
    for s in samples)

with wave.open("audio.wav", "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(frames)

print("wrote audio.wav", N, "samples, peak", round(peak, 3))
