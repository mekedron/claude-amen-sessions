"""Liquid: pads (Am9/Fmaj9/C/G) all the way, gentle rolling break, sub follows chords."""
import numpy as np
from amenlib import *

np.random.seed(7)
s = Session(22)

CHORDS = {
    'Am9':   [midi(45), midi(52), midi(55), midi(59), midi(64)],
    'Fmaj9': [midi(41), midi(48), midi(52), midi(57), midi(64)],
    'C':     [midi(48), midi(55), midi(60), midi(64)],
    'G':     [midi(43), midi(50), midi(55), midi(62)],
}
PROG = ['Am9', 'Fmaj9', 'C', 'G']
ROOTS = [45, 41, 36, 43]   # A1 F1 C1 G1

for b in range(0, 22, 2):
    s.place(s.pos(b), pad(CHORDS[PROG[(b // 2) % 4]], 32, 1600), 0.16)

s.place(s.pos(0), lp(bar_of(0), 900), 0.6)
s.place(s.pos(1), lp(bar_of(1), 2000), 0.7)
s.place(s.pos(2), bar_of(0), 0.85)
s.place(s.pos(3), bar_of(1), 0.85)
s.place(s.pos(3, 14), SN1, 0.5); s.place(s.pos(3, 15), SN1, 0.65)

for b in range(4, 20):
    if b % 8 == 7:
        s.pat(b, [(0, K, 0.9), (2, K2, 0.85), (4, SN, 0.9), (7, G, 0.5),
                  (8, K, 0.85), (10, SN1, 0.55), (12, S2, 0.9), (14, rev(SN1), 0.6)])
    else:
        s.place(s.pos(b), bar_of([0, 1, 0, 2][b % 4]), 0.9)
    root = midi(ROOTS[(b // 2) % 4] - 12)
    s.place(s.pos(b, 0), sub(root, 3), 0.3)
    s.place(s.pos(b, 6), sub(root, 2), 0.24)
    s.place(s.pos(b, 10), sub(root * 1.5 if b % 4 == 3 else root, 4), 0.27)
s.place(s.pos(4), CR, 0.6)
s.place(s.pos(12), CR, 0.6)

s.place(s.pos(20), lp(bar_of(0), 1200), 0.7)
s.pat(21, [(0, K, 0.8), (4, SN, 0.7)])
s.place(s.pos(20, 0), sub(midi(33), 8), 0.28)
s.place(s.pos(21, 0), sub(midi(33), 12), 0.24)

s.render('amen_liquid_174.wav', drive=1.1)
