"""Cosmos (~3:10, 136 bars @174) - drifting through space:
peace -> stardust -> the universe swallows us -> SUPERNOVA -> swallowed again -> peace.

  b0-23    void: deep A drone, stardust twinkles panned across the sky, faint choir
  b24-39   drifting: soft heartbeat, sub pulses, bells constellate
  b40-47   absorption: the drone rises, choir swells, long riser pulls us in
  b48-79   SUPERNOVA: impact boom, raging break + reese, choir wide open
  b80-87   collapse: everything darkens and sinks, swallowed again
  b88-111  after: drone returns, sparse twinkles, breath settles
  b112-135 peace: drone alone, last stardust, fade to void
"""
import numpy as np
from amenlib import *

rng = np.random.default_rng(42)
np.random.seed(42)
s = Session(136, tail=3.0)

A = 55.0                                                  # home: A
Am9  = [midi(45), midi(52), midi(60), midi(64), midi(71)]
Fx11 = [midi(41), midi(48), midi(57), midi(64), midi(71)] # Fmaj7#11 color
PENT = [81, 84, 88, 93, 96, 100]                          # high A-pentatonic stardust

def stardust(b0, nbars, density=1.5, gain=0.11):
    """random high bells scattered in time and stereo, ringing into deep space"""
    for _ in range(int(nbars * density)):
        t = s.pos(b0) + int(rng.uniform(0, nbars * BAR))
        note = int(rng.choice(PENT)) + int(rng.choice([0, 12]))
        seg = reverb(panned(bell(midi(note), 3), rng.uniform(-0.9, 0.9)),
                     decay=5.0, wet=0.85, tone=5500)
        s.place_echo(t, seg, gain * rng.uniform(0.5, 1.0), times=2,
                     delay_steps=4, fb=0.4)

def heartbeat(b, gain=0.3):
    s.place(s.pos(b, 0), subdrop(1.5, 65, 45), gain)
    s.place(s.pos(b, 2.5), subdrop(1.5, 60, 42), gain * 0.6)

# ================= void (b0-23) =================
s.place(s.pos(0), drone(A / 2, 200), 0.34)                # 12.5-bar deep breaths, overlapped
s.place(s.pos(10), drone(A / 2, 224), 0.30)
s.place(s.pos(2), wind(96), 0.35)
s.place(s.pos(12), wind(128), 0.3)
stardust(2, 20, density=1.2)
s.place(s.pos(8), vox(Am9[1:], 128, vowel='oo'), 0.10)
s.place(s.pos(16), vox(Fx11[1:], 96, vowel='oo'), 0.11)

# ================= drifting (b24-39) =================
s.place(s.pos(22), drone(A / 2, 224), 0.32)
stardust(24, 16, density=2.0)
for i, b in enumerate(range(24, 40, 4)):
    ch = [Am9, Fx11][i % 2]
    s.place(s.pos(b), pad(ch, 64, 1100), 0.10)
for b in range(28, 40):
    heartbeat(b, 0.26)
for b in range(32, 40):
    s.place(s.pos(b, 6), hat(0.8), 0.14)
    s.place(s.pos(b, 14), hat(0.8), 0.12)
s.place(s.pos(36, 0), sub(A / 2, 10), 0.18)

# ================= absorption (b40-47) =================
s.place(s.pos(38), drone(A, 160), 0.26)                   # octave up: pull begins
s.place(s.pos(40), vox(Am9, 128, vowel='oh'), 0.16)
stardust(40, 8, density=3.5, gain=0.13)
for b in range(40, 48):
    heartbeat(b, 0.3 + 0.02 * (b - 40))
    s.place(s.pos(b, 4), hat(0.8), 0.16); s.place(s.pos(b, 12), hat(0.8), 0.16)
s.place(s.pos(42), riser(96), 0.55)                       # 6-bar pull
s.place(s.pos(46), riser(32), 0.6)
for i, st in enumerate(np.arange(8, 16, 1.0)):
    s.place(s.pos(47, st), SN1, 0.4 + 0.07 * i)
s.place(s.pos(48) - len(CR), rev(CR), 0.95)

# ================= SUPERNOVA (b48-79) =================
s.place(s.pos(48), impact(32), 0.85)                      # the explosion
s.place(s.pos(48), CR, 0.9)
# strictly diatonic A minor triads for the choir - no lydian rub against the bass
CHAOS = [(33, [57, 64, 69, 72]),   # Am: A3 E4 A4 C5
         (29, [53, 60, 65, 69]),   # F:  F3 C4 F4 A4
         (31, [55, 62, 67, 71]),   # G:  G3 D4 G4 B4
         (28, [52, 59, 64, 67])]   # Em: E3 B3 E4 G4
for b in range(50, 80):
    root, ch = CHAOS[((b - 48) // 2) % 4]
    if b % 8 == 7:
        s.pat(b, [(0, K), (2, K2), (4, SN), (6, G, 0.7), (8, K), (10, SN1, 0.85),
                  (11, K2, 0.75), (12, S2), (14, rev(SN1), 0.8)])
    else:
        s.place(s.pos(b), dirty(bar_of([0, 1, 2, 1][b % 4]), 1.5), 0.92)
    s.place(s.pos(b, 0), reese(midi(root - 12), 6), 0.36)
    s.place(s.pos(b, 8), reese(midi(root - 12), 4, 450), 0.32)
    s.place(s.pos(b, 12), reese(midi(root - 12), 4, 280), 0.34)
    if b % 2 == 0:
        s.place(s.pos(b), reverb(vox([midi(n) for n in ch], 32, vowel='ah'),
                                 decay=2.2, wet=0.3, tone=3500), 0.15)
for b in range(64, 80, 4):                                # peak: hits + zaps join
    s.place(s.pos(b), reverb(orchhit(CHAOS[((b - 48) // 2) % 4][0] + 24),
                             decay=2.5, wet=0.4), 0.26)
    s.place_echo(s.pos(b + 2, 14), zap(2), 0.14, times=2, delay_steps=2, fb=0.45)
s.place(s.pos(64), CR, 0.7)
s.place(s.pos(64), subdrop(8, 70, 28), 0.4)
for i, st in enumerate(np.arange(8, 16, 1.0)):
    s.place(s.pos(79, st), SN1, 0.45 + 0.07 * i)

# ================= collapse (b80-87): swallowed again =================
for i, b in enumerate(range(80, 88)):
    cut = 2200 * (0.62 ** i) + 220                        # darker every bar
    s.place(s.pos(b), lp(bar_of([0, 1, 2, 1][b % 4]), cut), 0.8 * (0.87 ** i))
    s.place(s.pos(b, 0), sub(A / 2, 6), 0.22 * (0.88 ** i))
s.place(s.pos(80), impact(24), 0.5)
s.place(s.pos(82), drone(A / 2, 200), 0.30)               # the drone reclaims us
s.place(s.pos(84), vox(Am9[1:], 96, vowel='oo'), 0.10)

# ================= after (b88-111) =================
s.place(s.pos(96), drone(A / 2, 224), 0.32)
s.place(s.pos(90), wind(128), 0.3)
stardust(90, 20, density=1.6)
for i, b in enumerate(range(92, 108, 4)):
    ch = [Fx11, Am9][i % 2]
    s.place(s.pos(b), pad(ch, 64, 900), 0.09)
for b in range(92, 102):
    heartbeat(b, max(0.24 - 0.02 * (b - 92), 0.06))       # heart settles
s.place_echo(s.pos(104, 0), reverb(bell(midi(93), 4), decay=6.0, wet=0.9, tone=5000),
             0.10, times=4, delay_steps=5, fb=0.55)

# ================= peace (b112-135) =================
s.place(s.pos(110), drone(A / 2, 256), 0.30)
s.place(s.pos(118), wind(140), 0.28)
stardust(114, 16, density=0.8, gain=0.09)
s.place(s.pos(120), vox(Am9[1:], 120, vowel='oo'), 0.08)
s.place_echo(s.pos(128, 0), reverb(bell(midi(105), 4), decay=7.0, wet=0.95, tone=4500),
             0.08, times=5, delay_steps=6, fb=0.6)
s.place(s.pos(126, 0), sub(A / 4, 64), 0.14)              # 13.75 Hz-root felt, not heard

s.render('amen_cosmos_174.wav', drive=1.1)
