"""Dark atmospheric roller (~3 min, 128 bars @174) - mid-90s Metalheadz mood:
formant choir, ensemble strings, orchestra hits, laser zaps, reese/wobble bass,
an acid 303 interlude, tight amen edits.

  b0-15    intro: choir + strings swell out of the dark, zap echoes, hats
  b16-23   build: break rides in filtered, reese warms up underneath
  b24-55   drop 1: rolling reese groove, orch hits mark the changes, zap fills
  b56-71   interlude: halftime + acid 303 squelch over wobble
  b72-103  drop 2: wobble bass, dirtier break, double-snare edits, choir wide
  b104-127 outro: bass gone, choir and strings sink back into the dark
"""
import numpy as np
from amenlib import *

np.random.seed(5)
s = Session(128, tail=2.5)

# E aeolian roller loop: Em - G - A - C, two bars each
PROG  = [('Em', 40, [52, 55, 59, 64]), ('G', 43, [55, 59, 62, 67]),
         ('A', 45, [57, 60, 64, 69]), ('C', 48, [55, 60, 64, 71])]

def chord_at(b):
    return PROG[(b // 2) % 4]

def atmos(b, wide=False):
    _, root, tones = chord_at(b)
    s.place(s.pos(b), vox([midi(n) for n in tones], 32, vowel='oh' if b % 8 < 4 else 'ah'), 0.16)
    if wide:
        s.place(s.pos(b), strings([midi(n + 12) for n in tones[:3]], 32), 0.10)

def bass_reese(b):
    _, root, _ = chord_at(b)
    r = midi(root - 12)
    s.place(s.pos(b, 0), reese(r, 6), 0.38)
    s.place(s.pos(b, 8), reese(r, 4, 500), 0.33)
    s.place(s.pos(b, 12), reese(r * (2 ** (3 / 12)) if b % 4 == 3 else r, 4, 300), 0.36)

def bass_wobble(b):
    _, root, _ = chord_at(b)
    s.place(s.pos(b, 0), wobble(midi(root - 24), 14, 2.2 if b % 2 == 0 else 3.5), 0.36)

def drums(b, kind='roll'):
    if kind == 'roll':
        s.place(s.pos(b), bar_of([0, 1, 2, 1][b % 4]), 0.92)
    elif kind == 'dirty':
        s.place(s.pos(b), dirty(bar_of([0, 1, 2, 3][b % 4]), 1.6), 0.9)
        s.pat(b, [(6.5, G, 0.4), (10.5, SN1, 0.45)])
    elif kind == 'edit':
        s.pat(b, [(0, K), (2, K2), (4, SN), (6, G, 0.7), (8, K), (10, SN1, 0.85),
                  (11, K2, 0.75), (12, S2), (14, rev(SN1), 0.8)])
    elif kind == 'half':
        s.pat(b, [(0, K, 0.9), (3, G, 0.5), (8, SN, 0.9), (11, G, 0.5), (14, K2, 0.7)])

def snare_roll(b, start=8):
    steps = np.arange(start, 16, 1.0 if start >= 12 else 2.0)
    for i, st in enumerate(steps):
        s.place(s.pos(b, st), SN1, 0.5 + 0.5 * i / max(len(steps) - 1, 1))

# ================= intro (b0-15) =================
for b in range(0, 16, 2):
    atmos(b, wide=b >= 8)
s.place_echo(s.pos(2, 8), zap(2), 0.2, times=3, delay_steps=3, fb=0.5)
s.place_echo(s.pos(6, 12), zap(2, 1800, 60), 0.18, times=3, delay_steps=3, fb=0.5)
for b in range(8, 16):
    for st in (2, 6, 10, 14):
        s.place(s.pos(b, st), hat(), 0.26)
    s.place(s.pos(b, 0), sub(midi(chord_at(b)[1] - 24), 6), 0.2)
s.place(s.pos(12), lp(bar_of(0), 900), 0.55)
s.place(s.pos(13), lp(bar_of(1), 900), 0.55)
s.place(s.pos(14), riser(32), 0.6)
s.place(s.pos(14), lp(bar_of(0), 2000), 0.7)
snare_roll(15, 8)
s.place(s.pos(16) - len(CR), rev(CR), 0.9)

# ================= build (b16-23) =================
for b in range(16, 24):
    drums(b, 'edit' if b == 23 else 'roll')
    atmos(b) if b % 2 == 0 else None
    s.place(s.pos(b, 0), sub(midi(chord_at(b)[1] - 24), 6), 0.24)
s.place(s.pos(16), CR, 0.7)
s.place(s.pos(22), riser(32), 0.7)
snare_roll(22, 8); snare_roll(23, 4)
s.place(s.pos(24) - len(CR), rev(CR), 0.95)

# ================= drop 1 (b24-55) =================
s.place(s.pos(24), subdrop(10), 0.5)
s.place(s.pos(24), CR, 0.9)
for b in range(24, 56):
    drums(b, 'edit' if b % 8 == 7 else 'roll')
    bass_reese(b)
    if b % 2 == 0:
        atmos(b, wide=b >= 40)
        s.place(s.pos(b), orchhit(chord_at(b)[1] + 12), 0.30)   # hit marks the change
    if b % 8 == 6:
        s.place_echo(s.pos(b, 14), zap(2), 0.16, times=2, delay_steps=2, fb=0.45)
s.place(s.pos(40), CR, 0.6)
s.place(s.pos(40), subdrop(8, 65, 30), 0.35)
snare_roll(55, 8)
s.place(s.pos(54), riser(32), 0.5)

# ================= acid interlude (b56-71) =================
ACID = [40, 40, 52, 40, 43, 40, 55, 43]                    # E pentatonic squelch line
for b in range(56, 72):
    drums(b, 'half')
    bass_wobble(b)
    if b % 2 == 0:
        atmos(b)
    for i, st in enumerate((0, 2, 4, 6, 8, 10, 12, 14)):
        note = ACID[i] + (12 if (b + i) % 5 == 0 else 0)
        s.place(s.pos(b, st), acid(midi(note), 1.5, cutoff=600 + 90 * ((b - 56) % 8),
                                   accent=i % 4 == 2), 0.20)
s.place_echo(s.pos(63, 12), zap(2, 3000, 50), 0.18, times=3, delay_steps=3, fb=0.5)
for b in range(68, 72):
    s.place(s.pos(b, 4), hat(), 0.25); s.place(s.pos(b, 12), hat(), 0.25)
s.place(s.pos(68), riser(64), 0.75)
snare_roll(70, 8); snare_roll(71, 4)
s.place(s.pos(72) - len(CR), rev(CR), 0.95)

# ================= drop 2 (b72-103) =================
s.place(s.pos(72), subdrop(10, 80, 27), 0.55)
s.place(s.pos(72), CR, 0.9)
for b in range(72, 104):
    if b % 8 == 7:
        drums(b, 'edit')
    else:
        drums(b, 'dirty')
    bass_wobble(b)
    if b % 2 == 0:
        atmos(b, wide=True)
        s.place(s.pos(b), orchhit(chord_at(b)[1] + 12), 0.32)
    if b % 4 == 1:
        s.place(s.pos(b, 10), orchhit(chord_at(b)[1] + 24, 2), 0.2)  # answer hit up top
s.place(s.pos(88), CR, 0.6)
s.place(s.pos(88), subdrop(8, 65, 30), 0.35)
snare_roll(103, 8)

# ================= outro (b104-127) =================
for b in range(104, 112):
    drums(b, 'roll' if b < 108 else 'half')
    s.place(s.pos(b, 0), sub(midi(chord_at(b)[1] - 24), 6), 0.22)
    if b % 2 == 0:
        atmos(b, wide=True)
for b in range(112, 124, 2):
    atmos(b)
    if b < 118:
        for st in (2, 10):
            s.place(s.pos(b, st), hat(), 0.18)
s.place_echo(s.pos(114, 8), zap(2), 0.14, times=4, delay_steps=3, fb=0.55)
s.place_echo(s.pos(120, 0), orchhit(52, 3), 0.18, times=3, delay_steps=4, fb=0.5)
s.place(s.pos(124), vox([midi(n) for n in (52, 55, 59, 64)], 56, vowel='oo'), 0.18)
s.place(s.pos(124, 0), sub(midi(16), 32), 0.2)             # low E rumble to the end

s.render('amen_roller_174.wav', drive=1.2)
